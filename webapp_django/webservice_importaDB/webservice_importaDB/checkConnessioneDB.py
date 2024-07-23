from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
from psycopg2 import sql

import json

def index(request):
    result = "Errore di connessione"
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
        host = request.GET.get("host")
        porta = request.GET.get("porta")
    try:
        conn = psycopg2.connect(database=nome_DB,
            user=nome_utente,
            password=password,
            host=host, port=porta,
            connect_timeout = 1)

        cursor = conn.cursor()

        query = sql.SQL("SELECT rolcreatedb FROM pg_roles where rolname = %s")

        cursor.execute(query,[nome_utente])
        # result = cursor.query
        if (cursor.fetchone()[0] == True):
            result = "Accesso al DB eseguito e utente può creare DB"
            response = HttpResponse(result, status=200)
        else:
            result = "Utente non può creare DB"
            response = HttpResponse(result, status=500)
        conn.close()

    except:
        response = HttpResponse(result, status=500)
    
    return response