import httplib, json
import numpy as np, scipy as sp
import os
from pluck import pluck
import datetime

def getSecurityHistory(strEspecie):
    print('fetching security data...')
    strEspecie = strEspecie.upper()
    strFilename = 'data/SecurityHistory/' + strEspecie + '.json'
    if (os.path.exists(strFilename)):
        print('from file: ' + strFilename)
        with open(strFilename) as jsonFile:
            jsondata = json.load(jsonFile)
    else:
        print('from bolsar.com: ' + strEspecie)
        body = '{"strEspecie":"' + strEspecie + '","intVto":"4","intPeriodoId":4}'
        headers = {"Content-type": "application/json",
                   "Accept": "application/json"}
        conn = httplib.HTTPSConnection("www.bolsar.com")
        conn.request("POST", "/VistasDL/PaginaIntradiarioEspecies.aspx/GetIntradiarioHistorico", body, headers)
        response = conn.getresponse()
        print response.status, response.reason
        jsondata = json.load(response)
        conn.close()
        with open(strFilename, 'w') as outfile:
            json.dump(jsondata, outfile)
            outfile.close()
    series = jsondata['d'].pop()['EspeciesSeries']

    # all dates represented here are at GMT-3 (Buenos Aires)
    intDates = map(dateToInt, pluck(series, 'Fecha'))
    intTimes = map(timeToInt, pluck(series, 'Hora'))
    intTimestamps = np.sum([np.array(intDates).astype(np.float), np.array(intTimes).astype(np.float)], axis=0)
    datetimeDates = map(timestampToDatetime, intTimestamps)
    strDates = map(timestampToStr, intTimestamps)

    data = np.array([
            intTimestamps,
            pluck(series, 'VolumenNominal'),
            pluck(series, 'PrecioUltimo'),
            pluck(series, 'PrecioCierre'),
            pluck(series, 'PrecioOperacion'),
            pluck(series, 'PrecioApertura'),
            pluck(series, 'PrecioMaximo'),
            pluck(series, 'PrecioMinimo'),
            pluck(series, 'VariacionPrecio'),
            pluck(series, 'Operaciones'),
            pluck(series, 'TotalOperadoVn'),
            pluck(series, 'TotalOperadoMonto')

            #datetimeDates,
            #strDates,
            ])
    data = data.transpose()
    data = data[data[:,0].argsort()] # sort data by column 0 (timepstamps)
    return data


def dateToInt(strDate):
    return int(strDate.replace('/Date(','').replace('000)/',''))

def timeToInt(intTime):
    s = str(intTime) # 114553
    return int(60*60*int(s[:2]) + 60*int(s[2:4]) + int(s[4:6]))

def timestampToStr(intTimestamp):
    return datetime.datetime.fromtimestamp(float(intTimestamp)).strftime('%Y-%m-%d %H:%M:%S')

def timestampToDatetime(intTimestamp):
    return datetime.datetime.fromtimestamp(float(intTimestamp))
