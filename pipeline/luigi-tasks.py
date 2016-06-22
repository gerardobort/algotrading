from __future__ import print_function
import requests
from collections import defaultdict
from luigi import six
import luigi
import datetime

class DownloadYahooDataSecurityHistory(luigi.Task):

    security_code = luigi.Parameter()
    date = luigi.DateParameter(default=datetime.date.today())

    def run(self):
        # http://real-chart.finance.yahoo.com/table.csv?s=ALUA.BA&d=5&e=15&f=2016&g=d&a=6&b=22&c=2002&ignore=.csv
        with self.output().open('w') as outfile:
            response = requests.get('http://real-chart.finance.yahoo.com/table.csv?s=' + self.security_code + '&d=5&e=15&f=' + str(self.date.year) + '&g=d&a=6&b=22&c=1995&ignore=.csv', stream=True)
            if response.ok:
                for block in response.iter_content(1024):
                    outfile.write(block)

    def output(self):
        return luigi.LocalTarget(self.date.strftime('data/YahooSecurityHistory_' + self.security_code + '_%Y-%m-%d.csv'))



class GenerateSecurityIntradayIndicators(luigi.Task):

    security_code = luigi.Parameter()
    date = luigi.DateParameter(default=datetime.date.today())

    def requires(self):
        return DownloadYahooDataSecurityHistory(date=self.date, security_code=self.security_code)

    def run(self):
        with self.input().open('r') as infile:
            infile.readline()
            # infile: Date,Open,High,Low,Close,Volume,Adj Close
            with self.output().open('w') as outfile:
                for line in infile:
                    aline = line.rstrip().split(',')
                    info = (
                        aline[0],           # date
                        float(aline[1]),    # open
                        float(aline[2]),    # high
                        float(aline[3]),    # low
                        float(aline[4]),    # close
                        float(aline[5]),    # volumen
                        float(aline[6])     # adj close

                        # http://www.investopedia.com/articles/active-trading/101314/top-technical-indicators-options-trading.asp
                        # @TODO
                            # RSI (http://www.investopedia.com/terms/r/rsi.asp)
                            # BollingerBand (http://www.investopedia.com/terms/b/bollingerbands.asp)
                            # Intraday Momentum Index
                            # Money Flow Index (http://www.investopedia.com/terms/m/mfi.asp)
                            # Put Call Ratio Indicator (http://www.investopedia.com/terms/p/putcallratio.asp)
                            # Open Interest (http://www.investopedia.com/terms/o/openinterest.asp)
                    )
                    print(*info, file=outfile, sep='\t')

    def output(self):
        return luigi.LocalTarget(self.date.strftime('data/SecurityIntradayIndicators_' + self.security_code + '_%Y-%m-%d.tsv'))



if __name__ == "__main__":
    luigi.run()

