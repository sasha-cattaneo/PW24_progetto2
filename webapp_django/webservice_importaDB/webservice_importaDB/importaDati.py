from django.http import HttpResponse
import requests
import json

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def index(request):
    
    if request.method == "GET":
        param = request.GET.get("table")
    if request.method == "POST":
        param = request.POST.get("table")
    
    if param is None:
        return HttpResponse("ERROR: parametro ['table'] non settato")
    tomcatAPI_request = requests.post(
        "http://localhost:8080/intermediario/importaDati",
        data = { "table": param } 
    )
    dati = tomcatAPI_request.json()

    # INSERISCI IN POSTGRESQL
    
    return HttpResponse(json.dumps(dati, indent=4), content_type="application/json")


def inserisciDatiInTabella(tabella, dati):
    # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    conn = psycopg2.connect(database="postgres",
        user='postgres',
        password='admin',
        host='localhost', port='5432')
    
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()

    query = sql.SQL("SELECT 'CREATE DATABASE {}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{}')").format(
        sql.Identifier("PW24_headers-DB"),
        sql.Identifier("PW24_headers-DB")
    )

    cursor.execute(query)

    query = sql.SQL("")

    return 0