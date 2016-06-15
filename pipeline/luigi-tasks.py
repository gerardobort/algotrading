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

if __name__ == "__main__":
    luigi.run()

