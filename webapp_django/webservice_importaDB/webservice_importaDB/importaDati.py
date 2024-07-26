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
# Return: Pagina html con il risultato dell operazione di importo

# Nome DB in cui importare le tabelle
nomeDB_importo = "PW24_headers"

def index(request):
    # Salvo la lista di tabelle da importare e il nome del DB in cui importarle
    if request.method == "GET":
        param = request.GET.getlist("table[]")
        nomeDB_importo = request.GET.get("nomeDB")
    if request.method == "POST":
        param = request.POST.getlist("table[]")
        nomeDB_importo = request.POST.get("nomeDB")

    # Nome DB in cui importare le tabelle se non scelto dall'utente
    if nomeDB_importo is None or nomeDB_importo is "":
        nomeDB_importo = "PW24_headers"

    # Se nessuna tabella da importare è stata trovata restituisco errore
    if param is None:
        return HttpResponse("ERROR: parametro ['table'] non settato")

    context = importaDati(param, nomeDB_importo)

    return render(request,"resultDati.html", context)

# Importa dati delle tabelle da altervista a postgreSQL
# 
# Parametri necessari:
# lista_tabelle (List): lista di tabelle da importare
# 
# Parametri opzionali:
# nomeDB_importo (String): nome DB in cui importare le tabelle
# 
# Return: dizionario (struttura: {'table1': x, 'table2': x, ...})
# x ha avere valori:
# 1, se i dati sono stati importati con successo
# -1, se i dati non sono stati importati 
def importaDati(lista_tabelle, nomeDB_importo="PW24_headers"):

    # Salvo la risposta alla chiamata alla servlet Tomcat
    array_tabelle = chiamaIntermediario(lista_tabelle)

    # Per poter aggiungere i dati a delle tabelle devo avere le tabelle, quindi confermo che ci siamo o le creo
    # Chiamo la funzione importaTabelle passando tutti i parametri
    result_importo_tabelle = importaStruttura.importaTabelle(lista_tabelle, nomeDB_importo)
    

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
        if(result_importo_tabelle['tables'][nome_tabella] == -1):
            result_table_list[nome_tabella] = -1
            break
        
        # Altrimenti inserisco i dati
        try:
            success = aggiungiDati(nome_tabella, rows_tabella, nomeDB_importo)

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

def aggiungiDati(tabella, dati, nomeDB):
    # Connessione al DB
    # DAFARE
    # DA AGGIUNGERE VARIABILI DI SESSIONE PER LA CONNESSIONE
    conn = psycopg2.connect(database=nomeDB,
        user='postgres',
        password='admin',
        host='localhost', port='5432')
    conn.autocommit = True

    cursor = conn.cursor()

    # Costruzione stringa dei dati da inserire nella tabella
    args_str = ""
    # Numero di colonne
    num_campi = len(dati[0].keys())
    # Stringa temporanea con %s al posto dei parametri
    filler_args = f"({','.join(["'%s'"]*num_campi)})"
    
    # Per ogni riga da aggiungere alla tabella
    # sostituisco i dati a %s della stringa temporanea
    # e la aggiungo alla stringa finale args_str
    for row in dati:
        # Creo una lista dei parametri da inserire
        row_args = []
        for campo in row.keys():
            row_args.append(row[campo])
        # String formatting con la lista dei parametri
        args_str += filler_args % tuple(row_args)
        args_str += ","
    
    # Rimuovo l'ultima virgola
    args_str = args_str[:-1]

    # Costruisco la query
    query_string = "INSERT INTO %s VALUES " % (tabella.lower(),)
    query_string += args_str
    # query_string += " ON CONFLICT DO NOTHING"

    # Eseguo la query
    cursor.execute(query_string)

    conn.close()
    cursor.close()
    
    # Se l'inserimento ha avuto successo restituisce 1
    return 1