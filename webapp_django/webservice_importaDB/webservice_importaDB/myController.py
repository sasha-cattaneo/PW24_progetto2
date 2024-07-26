from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import requests
import json
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from . import importaStruttura
from . import importaDati

# File utilizzato per il debugging di piccole aggiunte o modifiche ai webservice di importo (importaData, importaStruttura, importaDB)
# prima di implementarle nei webservice

def index(request):
    if request.method == "GET":
        params = request.GET.getlist("table[]")
    if request.method == "POST":
        params = request.POST.getlist("table[]")
    
    if params is None:
        return HttpResponse("ERROR: parametro ['table'] non settato")
    
    param_string = ""

    for p in params:
        param_string += "table="+p+"&"
    param_string = param_string[:-1]
    
    tomcatAPI_request = requests.get(
        "http://localhost:8080/intermediario/importaStruttura",
        params = param_string
    )
    struttura = tomcatAPI_request.json()

    return HttpResponse(json.dumps(struttura), content_type="application/json")

# def index(request):
#     o = "esiste"
#     conn = psycopg2.connect(database="postgres",
#         user='postgres',
#         password='admin',
#         host='localhost', port='5432')

#     cursor = conn.cursor()

#     # query = sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s")
    
#     # cursor.execute(query, ["=test"])
    
#     # exists = cursor.fetchone()

#     # if not exists:
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     query = sql.SQL("CREATE DATABASE {}").format(
#         sql.Identifier("=test")
#     )
#     cursor.execute(query)
#     # o = cursor.query
#     o="CREATO"

#     # query = sql.SQL("SELECT 'CREATE DATABASE {}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{}')").format(
#     #     sql.Identifier("PW24_headers"),
#     #     sql.Identifier("PW24_headers")
#     # )
#     # query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier("PW24_headers"))


#     # cursor.execute(query)

    
#     return HttpResponse(o)


# def index(request):
#     if request.method == "GET":
#         param = request.GET.getlist("table[]")
#     if request.method == "POST":
#         param = request.POST.getlist("table[]")
    
#     if param is None:
#         return HttpResponse("ERROR: parametro ['table'] non settato")
    
    
#     return HttpResponse(str(param))

# def index(request):
#     # Mi connetto al DB
#     conn = psycopg2.connect(database='PW24_headers',
#         user='postgres',
#         password='admin',
#         host='localhost', port='5432')
#     conn.autocommit = True

#     cursor = conn.cursor()
#     # Query per verificare se la tabella "tabella" esiste
#     query = sql.SQL('CREATE TABLE IF NOT EXISTS "%s"' % ("tipologiaTariffa",))
#     # try:
#     #     cursor.execute(query)
#     #     # Salvo il risultato della query
#     #     result = cursor.fetchone()
#     # except:
#     #     result = "fail"
#     cursor.execute(query)
#         # Salvo il risultato della query
#     result = cursor.fetchone()

#     conn.close()
#     cursor.close()

#     # Restituisco il risultato della query, cioè se la tabella esiste o no
#     return HttpResponse(result)

# def index(request):
#     if request.method == "GET":
#         param = request.GET.getlist("table[]")
#     if request.method == "POST":
#         param = request.POST.getlist("table[]")

#     # Se nessuna tabella da importare è stata trovata restituisco errore
#     if param is None:
#         return HttpResponse("ERROR: parametro ['table'] non settato")
    
#     # # Con la lista di tabelle creo una stringa formattata come query string (key=value) 
#     # param_string = ""
#     # for p in param:
#     #     param_string += "table="+p+"&"
#     # param_string = param_string[:-1]

#     # pag_con_param = HttpRequest()
#     # pag_con_param.method = "POST"
#     # # pag_con_param.POST.setlist("table[]",param)
#     # pag_con_param.POST.update({"tipo":"test"})
#     # pag_con_param.POST.update({"msg":"aaaa"})

#     # context = {
#     #     'tipo':"test",
#     #     'msg':"aaaa",
#     # }
#     result_importo_tabelle = importaStruttura.importaTabelle(param)
#     r = ""
#     # return HttpResponse(str(result_importo_tabelle))
#     # for key, value in result_importo_tabelle["tables"].items():
#     #     r+=str(value)+","
#     r = result_importo_tabelle['tables']['ombrellone']
#     return HttpResponse(r)

# def index(request):
#     # Salvo la lista di tabelle da importare e il nome del DB in cui importarle
#     if request.method == "GET":
#         param = request.GET.getlist("table[]")
#         nomeDB_importo = request.GET.get("nomeDB")
#     if request.method == "POST":
#         param = request.POST.getlist("table[]")
#         nomeDB_importo = request.POST.get("nomeDB")

#     # Nome DB in cui importare le tabelle se non scelto dall'utente
#     if nomeDB_importo is None or nomeDB_importo is "":
#         nomeDB_importo = "PW24_headers"

#     # Se nessuna tabella da importare è stata trovata restituisco errore
#     if param is None:
#         return HttpResponse("ERROR: parametro ['table'] non settato")
    
#     conn = psycopg2.connect(database="PW24_headers",
#         user='postgres',
#         password='admin',
#         host='localhost', port='5432')
#     conn.autocommit = True

#     cursor = conn.cursor()

#     array_tabelle = importaDati.chiamaIntermediario(param)
#     t= ""
#     for tabella in array_tabelle:
#         # Salvo il nome della tabella
#         nome_tabella = list(tabella.keys())[0]
#         # Salvo i dati della tabella
#         # 
#         # 
#         # 
        
#         # 
#         # 
#         struttura = tabella[nome_tabella]
#         t += nome_tabella + "<br>"
#         # args_str = ','.join(cur.mogrify(f"({','.join(['%s']*len(fields))})", [d[field] for field in fields]) for d in data)

#         # rows_list = list(rows_tabella.items())
#         # Costruzione query per la creazione della tabella
#         num_campi = len(struttura[0].keys())
#         filler_args = f"({','.join(["'%s'"]*num_campi)})"
#         # args_str = ",".join(str(cursor.mogrify(f"({','.join(['%s']*len(x.keys()))})", [x[campo] for campo in x.keys()])) for x in rows_tabella)
#         # args_str = ",".join((filler_args % [row[campo] for campo in row.keys()]) for row in rows_tabella)

#         args_str = ""

#         for row in struttura:
#             row_args = []
#             for campo in row.keys():
#                 row_args.append(row[campo])

#             args_str += filler_args % tuple(row_args)
#             args_str += ","
        
#         args_str = args_str[:-1]
            
#         # args_str = ",".join("(%s,%s,%s,%s,%s)" % ([row[campo] for campo in row.keys()]) for row in rows_tabella)
#         query_string = "INSERT INTO %s VALUES " % (nome_tabella.lower(),)
#         query_string += args_str
        
#         # Eseguo la query
#         cursor.execute(sql.SQL(query_string))

#         t += "aggiunti dati<br>"
    
#     conn.close()
#     cursor.close()
        
#     return HttpResponse(t)