from django.http import HttpResponse
import requests
import json

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def index(request):

    if request.method == "GET":
        param = request.GET.getlist("table[]")
    if request.method == "POST":
        param = request.POST.getlist("table[]")
    
    if param is None:
        return HttpResponse("ERROR: parametro ['table'] non settato")
    
    param_string = ""

    for p in param:
        param_string += "table="+p+"&"
    param_string = param_string[:-1]
    
    tomcatAPI_request = requests.get(
        "http://localhost:8080/intermediario/importaStruttura",
        params = param_string
    )
    array_tabelle = tomcatAPI_request.json()
    result = "DB esiste<br>"

    DBesiste = checkEsistenzaDB()

    if not DBesiste:
        result = creaDB()

    for tabella in array_tabelle:
        
        nome_tabella = list(tabella.keys())[0]
        campi_tabella = tabella[nome_tabella]
        
        tabellaEsiste = checkEsistenzaTabella(nome_tabella)
        
        if not tabellaEsiste:
            result += creaTabella(nome_tabella, campi_tabella)
        else:
            result += "tabella ["+nome_tabella+"] esiste<br>"
    return HttpResponse(result)

def checkEsistenzaDB():
    # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    # USARE UNA VARIABILE DI SESSIONE PER VERIFICARE SE IL CONTROLLO CONNESSIONE E' STATO FATTO
    conn = psycopg2.connect(database="postgres",
        user='postgres',
        password='admin',
        host='localhost', port='5432')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.autocommit = True

    cursor = conn.cursor()

    query = sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s")
    
    cursor.execute(query, ["PW24_headers"])

    exists = cursor.fetchone()

    conn.close()
    cursor.close()
    
    return exists

def creaDB():
    # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    # USARE UNA VARIABILE DI SESSIONE PER VERIFICARE SE IL CONTROLLO CONNESSIONE E' STATO FATTO
    conn = psycopg2.connect(database="postgres",
        user='postgres',
        password='admin',
        host='localhost', port='5432')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.autocommit = True

    cursor = conn.cursor()

    query = sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier("PW24_headers")
        )
    cursor.execute(query)
    
    conn.close()
    cursor.close()

    return "DB creato<br>"
    
def checkEsistenzaTabella(tabella):
    conn = psycopg2.connect(database="PW24_headers",
        user='postgres',
        password='admin',
        host='localhost', port='5432')
    conn.autocommit = True

    cursor = conn.cursor()

    query = sql.SQL("SELECT 1 FROM information_schema.tables WHERE table_name = %s")
    
    cursor.execute(query, [tabella.lower()])

    result = cursor.fetchone()

    conn.close()
    cursor.close()

    return result

def creaTabella(tabella, struttura):
    msg = ""
    # # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    # # USARE UNA VARIABILE DI SESSIONE PER VERIFICARE SE IL CONTROLLO CONNESSIONE E' STATO FATTO
    # conn = psycopg2.connect(database="postgres",
    #     user='postgres',
    #     password='admin',
    #     host='localhost', port='5432')
    # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # conn.autocommit = True

    # cursor = conn.cursor()

    # query = sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s")
    
    # cursor.execute(query, ["PW24_headers"])

    # exists = cursor.fetchone()

    # if not exists:
        
    #     query = sql.SQL("CREATE DATABASE {}").format(
    #         sql.Identifier("PW24_headers")
    #     )
    #     cursor.execute(query)

    #     msg="DB creato"
    
    # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    conn = psycopg2.connect(database="PW24_headers",
        user='postgres',
        password='admin',
        host='localhost', port='5432')
    conn.autocommit = True

    cursor = conn.cursor()
    
    query_string = "CREATE TABLE IF NOT EXISTS %s (" % (tabella.lower(),)
    keys = []
    for campo in struttura:
        nome = campo['Field']
        tipo = campo['Type']
        if 'int' in tipo: tipo = 'int8'
        if 'blob' in tipo: tipo = 'bytea'
        if 'datetime' in tipo: tipo = 'timestamptz'
        if 'text' in tipo: tipo = 'text'
        if 'enum' in tipo: tipo = 'varchar'
        if(campo['Extra'] == 'auto_increment'):
            tipo = 'SERIAL'
        key = ''
        if(campo['Key'] == 'PRI'):
            keys.append(nome)
        null = ''
        if(campo['Null'] == 'NO'):
            null = 'NOT NULL'
        query_string += '%s %s %s,' % (nome, tipo, null)
    query_string += " PRIMARY KEY ("
    for key in keys:
        query_string += "%s," % (key)
    query_string = query_string.strip(',')
    query_string += '))'
    # msg += "<br>"+query_string
    query = sql.SQL(query_string)
    
    cursor.execute(query)

    result = checkEsistenzaTabella(tabella)

    if result:
        msg += "tabella ["+tabella+"] creata<br>"
    else:
        msg += "tabella ["+tabella+"] non creata<br>"

    conn.close()
    cursor.close()

    return msg