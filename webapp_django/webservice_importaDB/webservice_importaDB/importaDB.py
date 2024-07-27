from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from . import importaStruttura
from . import importaDati


# Funzione per l'importo di tutte le tabelle, con o senza dati, da altervista a postgreSQL
# Parametri opzionali:
# operazione (String): withData o noData per indicare se scaricare i dati o no
# nomeDB_importo (String): nome DB in cui importare le tabelle
#
# Return: Pagina html con il risultato dell operazione di importo
def index(request):
    # Lista delle tabelle
    param_list = ['cliente', 'ombrellone', 'ombrelloneVenduto', 'tipologiaTariffa', 'tipologia', 'giornoDisponibilita', 'tariffa', 'contratto']

    # Operazione di default: importare tutto, compresi i dati
    operation = "withData"
    # Salvo l'operazione da svolgere e il nome del DB in cui importare le tabelle
    if request.method == "GET":
        operation = request.GET.get("operazione")
        nomeDB_importo = request.GET.get("nomeDB")
    if request.method == "POST":
        operation = request.POST.get("operazione")
        nomeDB_importo = request.POST.get("nomeDB")

     # Nome DB in cui importare le tabelle se non scelto dall'utente
    if nomeDB_importo is None or nomeDB_importo == "":
        nomeDB_importo = "PW24_headers"

    # Altrimenti importo solo le strutture o tutto in base alla scelta
    if operation == "noData":
        context = importaStruttura.importaTabelle(request, param_list, nomeDB_importo)
        return render(request,"resultStruttura.html", context) 
    elif operation == "withData":
        context = importaDati.importaDati(request, param_list, nomeDB_importo)
        return render(request,"resultDati.html", context)
    else:
        return HttpResponse("ERRORE: Operazione non riconosciuta")