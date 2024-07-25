from django.http import HttpResponse
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
        "http://localhost:8080/intermediario/importaDati",
        # Per poter passare la query string in una richiesta POST imposto il Content-Type a application/x-www-form-urlencoded
        headers = {"Content-Type":"application/x-www-form-urlencoded"},
        # Imposto come parametro la lista delle tabelle formattata
        params = param_string
    )
    # Salvo la risposta alla chiamata
    array_tabelle = tomcatAPI_request.json()

    pag_con_param = HttpResponse(content_type="application/x-www-form-urlencoded", params = param_string)

    importaStruttura.index(pag_con_param)

    # # Messaggio di default
    # result = "DB esiste<br>"

    # Controllo se il DB in cui importare le tabelle esiste
    # DBesiste = importaStruttura.checkEsistenzaDB(nomeDB_importo)

    # # Se il DB non esiste lo creo e creo anche ogni tabella
    # if not DBesiste:
    #     # Creo il DB
    #     success = importaStruttura.creaDB(nomeDB_importo)
    #     if success:
    #         result = "DB creato<br>"
        
    #     # Creo ogni tabella
    #     for tabella in array_tabelle:
    #         # Salvo il nome della tabella
    #         nome_tabella = list(tabella.keys())[0]
    #         # Salvo la struttura della tabella
    #         campi_tabella = tabella[nome_tabella]

    #         try:
    #             # Creo la tabella
    #             success = importaStruttura.creaTabella(nome_tabella, campi_tabella)
    #             if success:
    #                 result += "Tabella ["+tabella+"] importata<br>"
    #         # Se la creazione è fallita invio l'errore all'utente
    #         except:
    #             result += "Tabella ["+nome_tabella+"] non è stata importata<br>"

    # # Se il DB esiste
    # else:
    #     success = False
    #     # Per ogni tabella controllo se esiste e se non esiste la creo
    #     for tabella in array_tabelle:
    #         # Salvo il nome della tabella
    #         nome_tabella = list(tabella.keys())[0]
    #         # Salvo la struttura della tabella
    #         campi_tabella = tabella[nome_tabella]

    #         # Controllo se la tabella esiste
    #         tabellaEsiste = importaStruttura.checkEsistenzaTabella(nome_tabella)

    #         # Se la tabella non esiste la creo
    #         if not tabellaEsiste:
    #             try:
    #                 # Creo la tabella
    #                 success = importaStruttura.creaTabella(nome_tabella, campi_tabella)
    #                 if success:
    #                     result += "Tabella ["+tabella+"] importata<br>"
    #             # Se la creazione è fallita invio l'errore all'utente
    #             except:
    #                 result += "Tabella ["+nome_tabella+"] non è stata importata<br>"
    #         else:
    #             # Aggiungo al messaggio che la tabella "nome_tabella" esiste
    #             result += "Tabella ["+nome_tabella+"] esiste<br>"

    #         # Se la tabella è stata creata, importo i suoi dati
    #         if success:
    #             success = aggiungiDati(nome_tabella,dati)

    
    return HttpResponse(result)