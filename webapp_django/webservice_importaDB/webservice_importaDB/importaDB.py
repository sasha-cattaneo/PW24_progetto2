from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def index(request):

    conn = psycopg2.connect(database="postgres",
        user='postgres',
        password='admin',
        host='localhost', port='5432')
    
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()

    query = sql.SQL("SELECT 'CREATE DATABASE {}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{}')").format(
        sql.Identifier("PW24_headers-DB"),
        sql.Identifier("PW24_headers-DB")
    )
    # query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier("PW24_headers-DB"))


    cursor.execute(query)

    o1 = "<html> <body>"
    o2 = "<p>DB creato</p>"
    o2 += str(request.GET.get("table"))

    conn = psycopg2.connect(database="PW24_headers-DB",
        user='postgres',
        password='admin',
        host='localhost', port='5432')
    
    cursor = conn.cursor()


    query = sql.SQL("SELECT count(*) FROM pg_database WHERE datname = '{}'").format(
        sql.Identifier("PW24_headers-DB")
    )

    cursor.execute(query)

    results = cursor.fetchall()

    for r in results:
        o2 += "<p>"+str(r)+"</p>"

    o3 = "<p>tabella creata</p>"
    o4 = "</body> </html>"
    return HttpResponse(o1 + o2 + o3 + o4)

# def importa