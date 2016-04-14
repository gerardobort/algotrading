curl -XPOST\
     -H'Content-Type:application/json; charset=UTF-8'\
     -H'Host:www.bolsar.com'\
     -H'Origin:https://www.bolsar.com'\
     -d'{"objEstadoIntradiarioEspecie":{"FiltroEspecie":"ALUA","FiltroVto":"4","MensajeNro":0}}'\
     https://www.bolsar.com/VistasDL/PaginaIntradiarioEspecies.aspx/GetDataPack > GetDataPack.json

curl -XPOST\
     -H'Content-Type:application/json; charset=UTF-8'\
     -H'Host:www.bolsar.com'\
     -H'Origin:https://www.bolsar.com'\
     -d'{"strEspecie":"ALUA","intVto":"4","intPeriodoId":4}'\
     https://www.bolsar.com/VistasDL/PaginaIntradiarioEspecies.aspx/GetIntradiarioHistorico > GetIntradiarioHistorico.json

     #-H'Content-Length:666'\
     #-d'{"aEstadoTabla":[{"TablaNombre":"tbMontos","FiltroVto":"","FiltroEspecies":"","PagActualNro":"1","Orden":"","EsOrdenAsc":true,"FilasxPagina":-1,"MensajeNro":0,"HashCode":0},{"TablaNombre":"tbAlzasBajasSinCambio","FiltroVto":"","FiltroEspecies":"","PagActualNro":"1","Orden":"","EsOrdenAsc":true,"FilasxPagina":-1,"MensajeNro":0,"HashCode":0},{"TablaNombre":"GraficoIM","FiltroVto":"","FiltroEspecies":"","PagActualNro":"1","FilasxPagina":-1,"MensajeNro":0,"HashCode":0,"Orden":"Simbolo","EsOrdenAsc":true},{"TablaNombre":"TK","FiltroVto":"72","FiltroEspecies":"","PagActualNro":"1","FilasxPagina":-1,"MensajeNro":0,"HashCode":0,"Orden":"Simbolo","EsOrdenAsc":true}]}' \
     #https://www.bolsar.com/VistasDL/PaginaPrincipal.aspx/GetDataPack > GetDataPack.json
