from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *

# Create your views here.
#OBTENER los registros de cargos
class DocumentoViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                documentos = list(TipoDocumentos.objects.filter(id=campo).values())
                if len(documentos) > 0:
                    documentos = documentos[0]
                    documentos = {'message': "Consulta exitosa", 'documentos': documentos}
                else:
                    documentos = {'message': "No se encontraron los datos"} 
                    return JsonResponse(documentos)
            elif criterio == "nombre":
                documentos = list(TipoDocumentos.objects.filter(nombre=campo).values())
                if len(documentos) > 0:
                    documentos = documentos[0]
                    documentos = {'message': "Consulta exitosa", 'documentos': documentos}
                else:
                    documentos = {'message': "No se encontraron los datos"} 
                    return JsonResponse(documentos)
        else:
            documentos = list(TipoDocumentos.objects.values())
            if len(documentos) > 0:
                documentos = {'message': "Consulta exitosa", 'documentos': documentos}
            else:
                documentos = {'message': "No se encontraron los datos"} 
        return JsonResponse(documentos)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            documentos = {'message': "El nombre esta vacío."}
        elif (validar_documento_repetido(jd['nombre'])):
            documentos = {'message': "El cargo ya existe."}
        elif len(jd['nombre']) < 2:
            documentos = {'message': "El nombre debe tener mas de 2 caracteres."}
        elif len(jd['nombre']) > 50:
            documentos = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif (jd['longitud']) <= 0:
            documentos = {'message': "La longitud debe ser mayor a 0."}
        elif (jd['longitud']) < 5:
                documentos = {'message': "La longitud debe ser mayor a 5."}
        else:
            documentos = {'message': "Registro Exitoso."}
            TipoDocumentos.objects.create(nombre=jd['nombre'], longitud=jd['longitud'])
            documentos = {'message':"Registro Exitoso."}
        return JsonResponse(documentos)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        documentos = list(TipoDocumentos.objects.filter(id=id).values())
        if len(documentos) > 0:
            documento=TipoDocumentos.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                documentos = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 2:
                documentos = {'message': "El nombre debe tener mas de 2 caracteres."}
            elif len(jd['nombre']) > 50:
                documentos = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif (jd['longitud']) <= 0:
                documentos = {'message': "La longitud debe ser mayor a 0."}
            elif (jd['longitud']) < 5:
                documentos = {'message': "La longitud debe ser mayor a 5."}
            else:
                documentos = {'message': "Registro Exitoso."}
                documento.nombre = jd['nombre']
                documento.longitud = jd['longitud']
                documento.save()
                documentos = {'message': "La actualización fue exitosa."}
        return JsonResponse(documentos)
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        documentos = list(TipoDocumentos.objects.filter(id=id).values())
        if len(documentos) > 0:
            TipoDocumentos.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro"}
        return JsonResponse(datos)

def validar_documento_repetido(nombre): 
    if (nombre):
        registros = TipoDocumentos.objects.filter(nombre=nombre)
        if len(registros) > 0:
            return True
        else:
            return False
    return False