# run tasks

PYTHONPATH='' luigi --module luigi-tasks GenerateSecurityIntradayCorrelationIndicators --GenerateSecurityIntradayCorrelationIndicators-security-codes ALUA.BA,YPF.D,PATY.BA,PAMP.BA

PYTHONPATH='' luigi --module luigi-tasks DownloadYahooDataSecurityHistory --DownloadYahooDataSecurityHistory-security-code ALUA.BA

PYTHONPATH='' luigi --module luigi-tasks DownloadYahooDataSecurityHistory --DownloadYahooDataSecurityHistory-security-code YPFD.BA
