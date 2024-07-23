from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# def index(request):
#     o = "esiste"
#     conn = psycopg2.connect(database="postgres",
#         user='postgrs',
#         password='admin',
#         host='localhost', port='5432')

#     cursor = conn.cursor()

#     query = sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s")
    
#     cursor.execute(query, ["PW24_headers"])
    
#     exists = cursor.fetchone()

#     if not exists:
#         conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#         query = sql.SQL("CREATE DATABASE {}").format(
#             sql.Identifier("PW24_headers")
#         )
#         cursor.execute(query)
#         # o = cursor.query
#         o="CREATO"

#     # query = sql.SQL("SELECT 'CREATE DATABASE {}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{}')").format(
#     #     sql.Identifier("PW24_headers"),
#     #     sql.Identifier("PW24_headers")
#     # )
#     # query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier("PW24_headers"))


#     # cursor.execute(query)

    
#     return HttpResponse(o)


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
#     if request.method == "GET":
#         param = request.GET.getlist("table[]")
#     if request.method == "POST":
#         param = request.POST.getlist("table[]")
    
#     if param is None:
#         return HttpResponse("ERROR: parametro ['table'] non settato")
    
    
#     return HttpResponse(str(param))