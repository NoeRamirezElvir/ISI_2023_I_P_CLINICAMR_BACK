from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods
from decimal import Decimal

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class TiposView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                tipo = list(Tipo.objects.filter(id=campo).values())
                if len(tipo) > 0:
                    tipo = tipo
                    tipo = {'message': "Consulta exitosa", 'tipo': tipo}
                else:
                    tipo = {'message': "No se encontraron los datos", 'tipo': []} 
                    return JsonResponse(tipo)
                
            elif criterio == "nombre":
                tipo = list(Tipo.objects.filter(nombre=campo).values())
                if len(tipo) > 0:
                    tipo = tipo
                    tipo = {'message': "Consulta exitosa", 'tipo': tipo}
                else:
                    tipo = {'message': "No se encontraron los datos", 'tipo': []} 
                    return JsonResponse(tipo)
            elif criterio == "subtipo":
                idSubtipo = Subtipo.objects.filter(nombre=campo).last()
                if idSubtipo is not None:
                    tipos = list(Tipo.objects.filter(idsubtipo=idSubtipo.id).values())
                    context = {
                        'message': "Consulta Exitosa",
                        'tipos': tipos
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'historicos': []
                    }
                    return JsonResponse(context)
            else:
                context = {
                        'message': "No se encontraron los datos",
                        'historicos': []
                    }
                return JsonResponse(context)
        else:
            tipo = list(Tipo.objects.values())
            if len(tipo) > 0:
                tipo = {'message': "Consulta exitosa", 'tipo': tipo}
            else:
                tipo = {'message': "No se encontraron los datos", 'tipo': []} 
        return JsonResponse(tipo)

#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)

        if len(jd['nombre']) <= 0:
            tipo = {'message': "El nombre esta vacío."}
        elif (validar_tipo_repetido(jd['nombre'])):
            tipo = {'message': "El tipo ya existe."}
        elif len(jd['nombre']) < 4:
            tipo = {'message': "El nombre debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            tipo = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            tipo = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['nombre']) > 50:
            tipo = {'message': "El nombre debe tener menos de 50 caracteres."}
        
        elif len(jd['descripcion']) <= 0:
            tipo = {'message': "La descripción esta vacía."}
        elif len(jd['descripcion']) < 4:
            tipo = {'message': "La descripción debe tener mas de 4 caracteres."}
        elif len(jd['descripcion']) > 50:
            tipo = {'message': "La descripción debe tener menos de 50 caracteres."}
        elif (jd['idsubtipo']) <= 0:
            tipo = {'message': "El tipo esta vacío."}
        elif validar_id_subtipo(jd['idsubtipo']):
            tipo = {'message': "El id de subtipo no existe."}
        elif Decimal(jd['precio']) <= 0:
                tipo = {'message': "El precio debe ser mayor a 0."}
        elif len(str(jd['precio'])) > 11:
            tipo = {'message': "El precio debe tener menos de 10 digitos."}
        elif round(Decimal(jd['precio'])) > 99999999.99:
            tipo = {'message': "El precio es muy alto."}
        elif round(Decimal(jd['precio']), 2) > round(Decimal(jd['precio']), 2):
            tipo = {'message': "El precio debe ser mayo al costo de compra."}
        
        
        else:
            precios= Decimal(jd['precio'])
            
            Tipo.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'],idsubtipo=instanciar_subtipo(jd['idsubtipo'],precio=precios))
            tipo = {'message':"Registro Exitoso."}
        return JsonResponse(tipo)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        tipo = list(Tipo.objects.filter(id=id).values())
        if len(tipo) > 0:
            tipos=Tipo.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                tipo = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                tipo = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                tipo = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                tipo = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
            elif len(jd['nombre']) > 50:
                tipo = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif len(jd['descripcion']) <= 0:
                tipo = {'message': "La descripción esta vacía."}
            elif len(jd['descripcion']) < 4:
                tipo = {'message': "La descripción debe tener mas de 4 caracteres."}
            elif len(jd['descripcion']) > 50:
                tipo = {'message': "La descripción debe tener menos de 50 caracteres."}
            elif Decimal(jd['precio']) <= 0:
                tipo = {'message': "El precio debe ser mayor a 0."}
            elif len(str(jd['precio'])) > 11:
                tipo = {'message': "El precio debe tener menos de 10 digitos."}
            elif round(Decimal(jd['precio'])) > 99999999.99:
                tipo = {'message': "El precio es muy alto."}
            elif round(Decimal(jd['precio']), 2) > round(Decimal(jd['precio']), 2):
                tipo = {'message': "El precio debe ser mayo al costo de compra."}
            
            
            else:
                tipo = {'message': "Registro Exitoso."}
                tipos.idsubtipo = instanciar_subtipo(jd['idsubtipo'])
                tipos.nombre = jd['nombre']
                tipos.descripcion = jd['descripcion']
                tipos.precio = Decimal(jd['precio'])    
                tipos.save()
                tipo = {'message': "La actualización fue exitosa."}
        return JsonResponse(tipo)
        
        
#Eliminar un registro de tipo
    def delete(self, request,id):
        tipo = list(Tipo.objects.filter(id=id).values())
        if len(tipo) > 0:
            Tipo.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'tipo': []}
        return JsonResponse(datos)
    
def validar_tipo_repetido(nombre): 
    if (nombre):
        registros = Tipo.objects.filter(nombre=nombre)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def validar_tipo_repedio_subtipo(nombre, idsubtipo):
    if (nombre and nombre):
        tipos = Tipo.objects.filter(nombre=nombre)
        x = 0
        for i in tipos:
            if i.idsubtipo == idsubtipo and i.nombre == nombre:
                    x = x + 1
                    if x > 1:
                        return True
                    else:
                        return False

def instanciar_subtipo(id):
    if (id>0):
        subtipo = Subtipo.objects.get(id=id)
        if subtipo:
            return subtipo
        

def validar_id_subtipo(id):
    if (id>0):
        subtipo = Subtipo.objects.filter(id=id)
        if subtipo:
            return False
        else:
            return True

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))