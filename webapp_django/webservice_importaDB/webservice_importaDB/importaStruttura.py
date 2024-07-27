from django.http import HttpResponse
from django.shortcuts import render
import requests
import json

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Funzione per l'importo dei dati delle tabelle richieste da altervista a postgreSQL
# Parametri necessari:
# lista di tabelle, chiave: 'table[]'
# 
# Parametri opzionali:
# nomeDB_importo (String): nome DB in cui importare le tabelle
#
# Return: Pagina html con il risultato dell operazione di importo
def index(request):
    # Salvo la lista di tabelle da importare e il nome del DB in cui importarle
    if request.method == "GET":
        param = request.GET.getlist("table[]")
        nomeDB_importo = request.GET.get("nomeDB")
    if request.method == "POST":
        param = request.POST.getlist("table[]")
        nomeDB_importo = request.POST.get("nomeDB")
    
    # Nome DB in cui importare le tabelle se non scelto dall'utente
    if nomeDB_importo is None or nomeDB_importo == "":
        nomeDB_importo = "PW24_headers"

    # Se nessuna tabella da importare è stata trovata restituisco errore
    if param is None or len(param) == 0:
        return HttpResponse("ERROR: parametro ['table[]'] non settato")
    
    context = importaTabelle(request, param, nomeDB_importo)
    
    return render(request,"resultStruttura.html", context)

# Importa tabelle da altervista a postgreSQL
# 
# Parametri necessari:
# request (HttpRequest): HttpRequest utilizzata per accedere alla sessione
# lista_tabelle (List): lista di tabelle da importare
# 
# Parametri opzionali:
# nomeDB_importo (String): nome DB in cui importare le tabelle
# 
# Return: dizionario (struttura: {'DB': x, 'tables': {'table1': x, 'table2': x, ...}})
# x ha avere valori:
# 0, se la tabella/DB esiste già
# 1, se la tabella/DB è stata/o creata/o con successo
# -1, se la tabella/DB non è stata/o creata/o per un errore
def importaTabelle(request, lista_tabelle, nomeDB_importo="PW24_headers"):
    
    # Salvo la risposta alla chiamata alla servlet Tomcat
    array_tabelle = chiamaIntermediario(lista_tabelle)

    # Dizionario da restituire
    result_table_list = {}
    result = {"DB":0,"tables":result_table_list}

    # Controllo se il DB in cui importare le tabelle esiste
    DBesiste = checkEsistenzaDB(request, nomeDB_importo)

    # Se il DB non esiste lo creo
    if not DBesiste:
        try:
            # Creo il DB
            success = creaDB(request, nomeDB_importo)
            if success:
                result["DB"] = 1
        # Se il DB non è stato creato termino l'esecuzione restituendo l'errore
        except:
            result["DB"] = -1
            return result

    # Per ogni tabella controllo se esiste e se non esiste la creo
    for tabella in array_tabelle:

        # Salvo il nome della tabella
        nome_tabella = list(tabella.keys())[0]
        # Salvo la struttura della tabella
        campi_tabella = tabella[nome_tabella]
        
        # Controllo se la tabella esiste
        tabellaEsiste = checkEsistenzaTabella(request, nome_tabella, nomeDB_importo)
        
        # Se la tabella non esiste la creo
        if not tabellaEsiste:
            try:
                # Creo la tabella
                success = creaTabella(request, nome_tabella, campi_tabella, nomeDB_importo)
                if success:
                    result_table_list[nome_tabella] = 1
            # Se la creazione è fallita invio salvo l'errore 
            except:
                result_table_list[nome_tabella] = -1
        else:
            # Aggiungo al result che la tabella "nome_tabella" esiste
            result_table_list[nome_tabella] = 0
        
    return result

# Chiamata servelet Apache Tomcat per ottenere la struttura delle tabelle da altervista
# 
# Parametri necessari:
# param (List): lista di tabelle da importare
# 
# Return: risultato chiamata
def chiamaIntermediario(lista_tabelle):
    # Con la lista di tabelle creo una stringa formattata come query string (key=value) 
    param_string = ""
    for p in lista_tabelle:
        param_string += "table="+p+"&"
    param_string = param_string[:-1]

    # Chiamata HTTP POST al webservice di Apache Tomcat
    tomcatAPI_request = requests.post(
        "http://localhost:8080/intermediario/importaStruttura",
        # Per poter passare la query string in una richiesta POST imposto il Content-Type a application/x-www-form-urlencoded
        headers = {"Content-Type":"application/x-www-form-urlencoded"},
        # Imposto come parametro la lista delle tabelle formattata
        params = param_string
    )
    return tomcatAPI_request.json()

# Controllo esistenza DB "nomeDB" su postgreSQL
# 
# Parametri necessari:
# request (HttpRequest): HttpRequest utilizzata per accedere alla sessione
# nomeDB (String): nome DB da cercare
# 
# Return: boolean risultato controllo sull'esistenza del DB
def checkEsistenzaDB(request, nomeDB):
    database = 'postgres'
    user = 'PW24_headers_user'
    password = 'PW24_headers_user'
    host = 'localhost'
    port = '5432'
    if 'database' in request.session:
        database = request.session['database']
    if 'user' in request.session:
        user = request.session['user']
    if 'password' in request.session:
        password = request.session['password']
    if 'host' in request.session:
        host = request.session['host']
    if 'port' in request.session:
        port = request.session['port']
    # Connessione al DB
    # DAFARE
    # USARE UNA VARIABILE DI SESSIONE PER VERIFICARE SE IL CONTROLLO CONNESSIONE E' STATO FATTO
    conn = psycopg2.connect(database = database,
        user = user,
        password = password,
        host = host,
        port = port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.autocommit = True

    cursor = conn.cursor()

    # Query per verificare se il DB "nomeDB" esiste
    query = sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s")
    
    cursor.execute(query, [nomeDB])

    # Salvo il risultato della query
    exists = cursor.fetchone()

    conn.close()
    cursor.close()
    
    # Restituisco il risultato della query, cioè se il DB esiste o no
    return exists

# Crea il DB "nomeDB" in postgreSQL
# 
# Parametri necessari:
# request (HttpRequest): HttpRequest utilizzata per accedere alla sessione
# nomeDB (String): nome DB da creare
# 
# Return: boolean risultato creazione
def creaDB(request, nomeDB):
    database = 'postgres'
    user = 'PW24_headers_user'
    password = 'PW24_headers_user'
    host = 'localhost'
    port = '5432'
    if 'database' in request.session:
        database = request.session['database']
    if 'user' in request.session:
        user = request.session['user']
    if 'password' in request.session:
        password = request.session['password']
    if 'host' in request.session:
        host = request.session['host']
    if 'port' in request.session:
        port = request.session['port']
    # Connessione al DB postgreSQL
    # DAFARE
    # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    # USARE UNA VARIABILE DI SESSIONE PER VERIFICARE SE IL CONTROLLO CONNESSIONE E' STATO FATTO
    conn = psycopg2.connect(database = database,
        user = user,
        password = password,
        host = host,
        port = port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.autocommit = True

    cursor = conn.cursor()

    # Query per la creazione del DB "nomeDB"
    query = sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(nomeDB)
        )
    cursor.execute(query)
    
    conn.close()
    cursor.close()

    return 1

# Controllo l'esistenza della tabella "tabella" nel DB
# 
# Parametri necessari:
# request (HttpRequest): HttpRequest utilizzata per accedere alla sessione
# tabella (String): nome tabella da cercare
# nomeDB (String): nome DB in cui cercare la tabella
# 
# Return: boolean risultato controllo sull'esistenza della tabella
def checkEsistenzaTabella(request, tabella, nomeDB):
    user = 'PW24_headers_user'
    password = 'PW24_headers_user'
    host = 'localhost'
    port = '5432'
    if 'user' in request.session:
        user = request.session['user']
    if 'password' in request.session:
        password = request.session['password']
    if 'host' in request.session:
        host = request.session['host']
    if 'port' in request.session:
        port = request.session['port']
    # Connessione al DB
    conn = psycopg2.connect(database = nomeDB,
        user=user,
        password=password,
        host=host,
        port=port)
    conn.autocommit = True

    cursor = conn.cursor()
    # Query per verificare se la tabella "tabella" esiste
    query = sql.SQL("SELECT 1 FROM information_schema.tables WHERE table_name = %s")
    
    # String.lower() perché la creazione di tabelle in postgreSQL non è case sensitive 
    cursor.execute(query, [tabella.lower()])
    # Salvo il risultato della query
    msg = cursor.fetchone()

    conn.close()
    cursor.close()

    # Restituisco il risultato della query, cioè se la tabella esiste o no
    return msg

# Crea la tabella "tabella" con struttura "struttura"
# 
# Parametri necessari:
# request (HttpRequest): HttpRequest utilizzata per accedere alla sessione
# tabella (String): nome tabella da creare
# struttura (Dictionary): campi della tabella da creare
# nomeDB (String): nome DB in cui creare la tabella
# 
# Return: boolean risultato creazione
def creaTabella(request, tabella, struttura, nomeDB):
    user = 'PW24_headers_user'
    password = 'PW24_headers_user'
    host = 'localhost'
    port = '5432'
    if 'user' in request.session:
        user = request.session['user']
    if 'password' in request.session:
        password = request.session['password']
    if 'host' in request.session:
        host = request.session['host']
    if 'port' in request.session:
        port = request.session['port']
    # Connessione al DB
    # DAFARE
    # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    conn = psycopg2.connect(database = nomeDB,
        user = user,
        password = password,
        host = host,
        port = port)
    conn.autocommit = True

    cursor = conn.cursor()
    
    # Costruzione query per la creazione della tabella
    query_string = "CREATE TABLE IF NOT EXISTS %s (" % (tabella.lower(),)

    # Inizializzazione varaibile per le colonne che fanno da PRIMARY KEY
    keys = []

    # Per ogni compo della tabella aggiungo alla query il nome, il tipo (corretto da MySQL a PostgreSQL), se è PRIMARY KEY e se è NOT NULL
    for campo in struttura:
        # Salvo nome e tipo
        nome = campo['Field']
        tipo = campo['Type']
        # Correggo il tipo
        if 'int' in tipo: tipo = 'int8'
        if 'blob' in tipo: tipo = 'bytea'
        if 'datetime' in tipo: tipo = 'timestamptz'
        if 'text' in tipo: tipo = 'text'
        if 'enum' in tipo: tipo = 'varchar'
        if(campo['Extra'] == 'auto_increment'):
            tipo = 'SERIAL'
        # Salvo se PRIMARY KEY
        key = ''
        if(campo['Key'] == 'PRI'):
            keys.append(nome)
        # Salvo se NOT NULL
        null = ''
        if(campo['Null'] == 'NO'):
            null = 'NOT NULL'
        # Aggiungo le informazioni alla query
        query_string += '%s %s %s,' % (nome, tipo, null)
    # Aggiunta della PRIMARY KEY
    query_string += " PRIMARY KEY ("
    for key in keys:
        query_string += "%s," % (key)
    query_string = query_string.strip(',')
    query_string += '))'
    query = sql.SQL(query_string)
    
    # Eseguo la query
    cursor.execute(query)

    conn.close()
    cursor.close()

    # Se la creazione ha avuto successo restituisce 1
    return 1