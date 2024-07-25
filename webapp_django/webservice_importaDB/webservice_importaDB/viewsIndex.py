from django.shortcuts import render

# Come pagina index della webapp carico la template index.html
def index(request):
    return render(request, "index.html")