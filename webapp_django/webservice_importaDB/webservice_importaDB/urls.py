from django.urls import path

# Importo i file python contenenti le funzioni per i webservices
from . import viewsIndex
from . import importaDB
from . import importaStruttura
from . import importaDati
from . import checkConnessioneDB

# Solo per debugging
from . import myController

# Creo i pattern per collegare URL a funzione python
urlpatterns = [
    path('', viewsIndex.index),
    path("importaDB/", importaDB.index, name="importaDB"),
    path("importaStruttura/", importaStruttura.index, name="importaStruttura"),
    path("importaDati/", importaDati.index, name="importaDtai"),
    path("checkConnessioneDB/", checkConnessioneDB.index, name="checkConnessioneDB"),
    path("test/", myController.index)
]
