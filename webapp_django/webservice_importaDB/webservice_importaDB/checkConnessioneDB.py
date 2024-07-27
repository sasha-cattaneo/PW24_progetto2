from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
from psycopg2 import sql

import json

# Funzione per il controllo della connessione al DB postgreSQL
# Parametri necessari:
# nome_DB (String): nome del DB
# nome_utente (String): nome di un utente con accesso al DB e con permesso di creare altri DB
# password (String): password dell'utente
# host (String): host di postgreSQL
# porta (String/int): porta utilizzata da postgreSQL

def index(request):
    # msg di default
    result = "Errore di connessione"
    # Ottengo i parametri per la connessione
    if request.method == "GET":
        nome_DB = request.GET.get("nome_DB")
        nome_utente = request.GET.get("nome_utente")
        password = request.GET.get("password")
        host = request.GET.get("host")
        porta = request.GET.get("porta")

    if request.method == "POST":
        nome_DB = request.POST.get("nome_DB")
        nome_utente = request.POST.get("nome_utente")
        password = request.POST.get("password")
        host = request.POST.get("host")
        porta = request.POST.get("porta")

    # Provo a connettermi
    try:
        conn = psycopg2.connect(database=nome_DB,
            user=nome_utente,
            password=password,
            host=host, port=porta,
            connect_timeout = 1)

        cursor = conn.cursor()
        # Se la connessione ha successo
        # Controllo che l'utente abbia il permesso di creare DB
        query = sql.SQL("SELECT rolcreatedb FROM pg_roles where rolname = %s")
        cursor.execute(query,[nome_utente])

        # Se l'utente ha il permesso imposto result e status 200 in response
        if (cursor.fetchone()[0] == True):
            request.session['database'] = nome_DB
            request.session['user'] = nome_utente
            request.session['password'] = password
            request.session['host'] = host
            request.session['port'] = porta

            result = "Accesso al DB eseguito e utente può creare DB<br>"
            result += "Sessione iniziata e variabili di sessione impostare"
            response = HttpResponse(result, status=200)

        # Se l'utente ha il permesso imposto result e status 500 in response
        else:
            result = "Utente non può creare DB"
            response = HttpResponse(result, status=500)
        conn.close()
        cursor.close()
    # Se la connessione fallisce imposto result e status 500 in response
    except:
        response = HttpResponse(result, status=500)
    # Restituisco response
    return response