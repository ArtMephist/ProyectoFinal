from django.http import HttpResponse
import datetime
from django.template import Template, Context

def css_file(request):
    with open('C:/Users/Alan/Desktop/PythonProyecto1/proyecto1/static/admin/css/style/style.css') as f:
        css = f.read()
    response = HttpResponse(css, content_type='text/css')
    return response


def saludo(request):
    return HttpResponse("Hola Django - Coder")

def today(request):
    day = datetime.datetime.now()

    textdocument = f"el tiempo ahora es: {day}"

    return HttpResponse(textdocument)

def probandoTemplate(self):

    name = "Alan"
    surname = "Amante"

    dictionary = {"name": name, "surname": surname}

    miHtml = open("C:/Users/Alan/Desktop/PythonProyecto1/proyecto1/proyecto1/templates/template1.html")

    plantilla = Template(miHtml.read())

    miHtml.close()

    micontexto = Context(dictionary)

    documento = plantilla.render(micontexto)

    return HttpResponse(documento)

def testTemplate(self):

    miHtml = open("C:/Users/Alan/Desktop/PythonProyecto1/proyecto1/proyecto1/templates/index.html")

    plantilla = Template(miHtml.read())

    miHtml.close()

    micontexto = Context()

    documento = plantilla.render(micontexto)

    return HttpResponse(documento)