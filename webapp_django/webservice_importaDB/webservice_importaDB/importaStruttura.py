from django.http import HttpResponse
import requests
import json

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Funzione per l'importo dei dati delle tabelle richieste da altervista a postgreSQL
# Parametri necessari:
# lista di tabelle, chiave: 'table[]'
#
# Return: Pagina html con il risultato dell operazione di importo

# Nome DB in cui importare le tabelle
nomeDB_importo = "PW24_headers"


def index(request):
    # Salvo la lista di tabelle da importare
    if request.method == "GET":
        param = request.GET.getlist("table[]")
    if request.method == "POST":
        param = request.POST.getlist("table[]")

    # Se nessuna tabella da importare è stata trovata restituisco errore
    if param is None:
        return HttpResponse("ERROR: parametro ['table'] non settato")
    
    # Con la lista di tabelle creo una stringa formattata come query string (key=value) 
    param_string = ""
    for p in param:
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
    # Salvo la risposta alla chiamata
    array_tabelle = tomcatAPI_request.json()

    # Messaggio di default
    msg = "DB esiste<br>"

    # Controllo se il DB in cui importare le tabelle esiste
    DBesiste = checkEsistenzaDB(nomeDB_importo)

    # Se il DB non esiste lo creo
    if not DBesiste:
        try:
            # Creo il DB
            success = creaDB(nomeDB_importo)
            if success:
               msg = "DB creato<br>"
        # Se il DB non è stato creato termino l'esecuzione inviando l'errore all'utente
        except:
            msg = "Errore nella creazione del DB"
            return HttpResponse(msg)

    # Per ogni tabella controllo se esiste e se non esiste la creo
    for tabella in array_tabelle:

        # Salvo il nome della tabella
        nome_tabella = list(tabella.keys())[0]
        # Salvo la struttura della tabella
        campi_tabella = tabella[nome_tabella]
        
        # Controllo se la tabella esiste
        tabellaEsiste = checkEsistenzaTabella(nome_tabella)
        
        # Se la tabella non esiste la creo
        if not tabellaEsiste:
            try:
                # Creo la tabella
                success = creaTabella(nome_tabella, campi_tabella)
                if success:
                    msg += "Tabella ["+tabella+"] importata<br>"
            # Se la creazione è fallita invio l'errore all'utente
            except:
                msg += "Tabella ["+nome_tabella+"] non è stata importata<br>"
        else:
            # Aggiungo al messaggio che la tabella "nome_tabella" esiste
            msg += "Tabella ["+nome_tabella+"] esiste<br>"
    return HttpResponse(msg)

# Controllo esistenza DB "nomeDB" su postgreSQL
# 
# Parametri necessari:
# nomeDB (String): nome DB da cercare
# 
# Return: boolean risultato controllo sull'esistenza del DB
def checkEsistenzaDB(nomeDB):
    # Connessione al DB
    # DAFARE
    # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    # USARE UNA VARIABILE DI SESSIONE PER VERIFICARE SE IL CONTROLLO CONNESSIONE E' STATO FATTO
    conn = psycopg2.connect(database="postgres",
        user='postgres',
        password='admin',
        host='localhost', port='5432')
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
# nomeDB (String): nome DB da creare
# 
# Return: boolean risultato creazione
def creaDB(nomeDB):
    # Connessione al DB postgreSQL
    # DAFARE
    # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    # USARE UNA VARIABILE DI SESSIONE PER VERIFICARE SE IL CONTROLLO CONNESSIONE E' STATO FATTO
    conn = psycopg2.connect(database="postgres",
        user='postgres',
        password='admin',
        host='localhost', port='5432')
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
# tabella (String): nome DB da cercare
# 
# Return: boolean risultato controllo sull'esistenza della tabella
def checkEsistenzaTabella(tabella):
    # Connessione al DB
    conn = psycopg2.connect(database=nomeDB_importo,
        user='postgres',
        password='admin',
        host='localhost', port='5432')
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
# tabella (String): nome tabella da creare
# struttura (Dictionary): campi della tabella da creare
# 
# Return: boolean risultato creazione
def creaTabella(tabella, struttura):
    # Connessione al DB
    # DAFARE
    # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    conn = psycopg2.connect(database=nomeDB_importo,
        user='postgres',
        password='admin',
        host='localhost', port='5432')
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

    return 1