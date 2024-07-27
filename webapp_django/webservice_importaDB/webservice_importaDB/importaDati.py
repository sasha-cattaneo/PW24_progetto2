from django.http import HttpResponse
from django.shortcuts import render
import requests
import json

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from . import importaStruttura 

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

    context = importaDati(request, param, nomeDB_importo)
    
    return render(request,"resultDati.html", context)

# Importa dati delle tabelle da altervista a postgreSQL
# 
# Parametri necessari:
# request (HttpRequest): HttpRequest utilizzata per accedere alla sessione
# lista_tabelle (List): lista di tabelle da importare
# 
# Parametri opzionali:
# nomeDB_importo (String): nome DB in cui importare le tabelle
# 
# Return: dizionario (struttura: {'table1': x, 'table2': x, ...})
# x ha avere valori:
# 1, se i dati sono stati importati con successo
# 0, se non ci sono dati da importare
# -1, se i dati non sono stati importati 
def importaDati(request, lista_tabelle, nomeDB_importo="PW24_headers"):

    # Salvo la risposta alla chiamata alla servlet Tomcat
    array_tabelle = chiamaIntermediario(lista_tabelle)

    # Per poter aggiungere i dati a delle tabelle devo avere le tabelle, quindi confermo che ci siamo o le creo
    # Chiamo la funzione importaTabelle passando tutti i parametri
    result_importo_tabelle = importaStruttura.importaTabelle(request, lista_tabelle, nomeDB_importo)
    

    # Dizionario da restituire
    result_table_list = {}
    result = {"create":result_importo_tabelle,"tables":result_table_list}

    # Se il DB non è stato creato termino l'esecuzione restituendo l'errore
    if result_importo_tabelle['DB'] == -1:
        return result

    for tabella in array_tabelle:
        # Salvo il nome della tabella
        nome_tabella = list(tabella.keys())[0]
        # Salvo i dati della tabella
        rows_tabella = tabella[nome_tabella]

        # Se la tabella non è stata creata con successo non posso inserire i suoi dati
        if result_importo_tabelle['tables'][nome_tabella] == -1:
            result_table_list[nome_tabella] = -1
            break
        # Se non ci sono dati da importare
        if len(rows_tabella) == 0:
            result_table_list[nome_tabella] = 0
        # Altrimenti inserisco i dati
        else:
            try:
                success = aggiungiDati(request, nome_tabella, rows_tabella, nomeDB_importo)

                if success:
                    result_table_list[nome_tabella] = 1
            except:
                result_table_list[nome_tabella] = -1

    return result

# Chiamata servelet Apache Tomcat per ottenere la struttura delle tabelle da altervista
# 
# Parametri necessari:
# param (List): lista di tabelle da importare
# 
# Return: boolean risultato chiamata
def chiamaIntermediario(lista_tabelle):
    # Con la lista di tabelle creo una stringa formattata come query string (key=value) 
    param_string = ""
    for p in lista_tabelle:
        param_string += "table="+p+"&"
    param_string = param_string[:-1]
    
    # Chiamata HTTP POST al webservice di Apache Tomcat
    tomcatAPI_request = requests.post(
        "http://localhost:8080/intermediario/importaDati",
        # Per poter passare la query string in una richiesta POST imposto il Content-Type a application/x-www-form-urlencoded
        headers = {"Content-Type":"application/x-www-form-urlencoded"},
        # Imposto come parametro la lista delle tabelle formattata
        params = param_string
    )
    return tomcatAPI_request.json()


# Aggiunge dati alla tabella "tabella"
# 
# Parametri necessari:
# request (HttpRequest): HttpRequest utilizzata per accedere alla sessione
# tabella (String): nome tabella da creare
# dati (Dictionary): dati da importare
# nomeDB (String): nome DB in cui importare i dati
# 
# Return: boolean risultato creazione
def aggiungiDati(request, tabella, dati, nomeDB):
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
    conn = psycopg2.connect(database=nomeDB,
        user='postgres',
        password='admin',
        host='localhost', port='5432')
    conn.autocommit = True

    cursor = conn.cursor()

    # Stringa temporanea con %s al posto dei parametri
    filler_args_str = "("
    
    # Per ogni riga da aggiungere alla tabella
    # aggiungo un %s alla stringa filler_args_str
    # e aggiungo il dato a una lista, che alla fine avrà tutti i dati
    args = []
    for row in dati:
        for campo in row.keys():
            filler_args_str += "%s,"

            args.append(row[campo])

        filler_args_str = filler_args_str[:-1]
        filler_args_str += "),("
    filler_args_str = filler_args_str[:-2]

    # Costruisco la query
    query_string = "INSERT INTO %s VALUES " % (tabella.lower(),)
    query_string += filler_args_str
    # query_string += " ON CONFLICT DO NOTHING"

    # Eseguo la query
    cursor.execute(sql.SQL(query_string), args)

    conn.close()
    cursor.close()
    
    # Se l'inserimento ha avuto successo restituisce 1
    return 1