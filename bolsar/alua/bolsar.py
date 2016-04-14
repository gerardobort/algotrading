import httplib, json
import numpy as np, scipy as sp
from pluck import pluck

def getSecurityHistory(strEspecie):
    print('security: ' + strEspecie)
    body = '{"strEspecie":"' + strEspecie + '","intVto":"4","intPeriodoId":4}'
    headers = {"Content-type": "application/json",
               "Accept": "application/json"}
    conn = httplib.HTTPSConnection("www.bolsar.com")
    conn.request("POST", "/VistasDL/PaginaIntradiarioEspecies.aspx/GetIntradiarioHistorico", body, headers)
    response = conn.getresponse()
    jsondata = json.load(response)
    conn.close()
    print response.status, response.reason
    series = jsondata['d'].pop()['EspeciesSeries']
    data = np.array([pluck(series, 'Fecha'),
            pluck(series, 'Hora'),
            pluck(series, 'PrecioUltimo'),
            pluck(series, 'PrecioOperacion'),
            pluck(series, 'PrecioApertura'),
            pluck(series, 'PrecioMaximo'),
            pluck(series, 'PrecioMinimo'),
            pluck(series, 'PrecioCierre'),
            pluck(series, 'VariacionPrecio'),
            pluck(series, 'VolumenNominal'),
            pluck(series, 'Operaciones'),
            pluck(series, 'TotalOperadoVn'),
            pluck(series, 'TotalOperadoMonto')])
    data[0] = map(dateToInt, data[0])
    data[1] = map(timeToInt, data[1])
    data[2] = map(float, data[2])
    return data

def dateToInt(strDate):
    return int(strDate.replace('/Date(','').replace('000)/',''))

def timeToInt(intTime):
    s = str(intTime) # 114553
    return int(60*60*int(s[:2]) + 60*int(s[2:4]) + int(s[4:6]))
