import datetime
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class resultadosViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto resultado todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                resultados = Resultados.objects.filter(id=campo).select_related('idTratamiento')
                if resultados is not None:
                    resultados_values = []
                    for resultado in resultados:
                        tratamiento = resultado.idTratamiento
                        resultado_dict = {
                            'id': resultado.id,
                            'idTratamiento': resultado.idTratamiento.id,
                            'fecha': resultado.fecha,
                            'observacion': resultado.observacion,
                            

                            'idTratamiento': {
                                'id': tratamiento.id,
                                'fecha': tratamiento.fecha
                            }
                        }
                        resultados_values.append(resultado_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'resultados': resultados_values
                        }
                        return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'resultados': []
                    }
                    return JsonResponse(context)
            elif criterio == "fecha":
                idTratamiento = Tratamiento.objects.filter(fecha=campo)
                if idTratamiento is not None:
                    for tratamiento in idTratamiento:
                        reg = Resultados.objects.filter(idTratamiento=tratamiento.id).select_related('idTratamiento')
                        if reg is not None:
                            resultados_values = []
                            for resultado in reg:
                                tratamiento = resultado.idTratamiento
                                resultado_dict = {
                                    'id': resultado.id,
                                    'idTipo': resultado.idTipo.id,
                                    'fecha': resultado.fecha,
                                    'observacion': resultado.observacion,
                                    'idTratamiento': {
                                        'id': tratamiento.id,
                                        'fecha': tratamiento.fecha
                                    }
                                }
                                resultados_values.append(resultado_dict)
                            context = {
                                'message': "Consulta exitosa",
                                'resultados': resultados_values
                            }
                            return JsonResponse(context)
                        else:
                            context = {
                                'message': "No se encontraron los datos",
                                'resultados': []
                            }
                            return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'resultados': []
                    }
                    return JsonResponse(context)
            context = {
                    'message': "No se encontraron los datos",
                    'resultados': []
                }
            return JsonResponse(context)
        else:
            reg = Resultados.objects.select_related('idTratamiento')
            if reg is not None:
                resultados_values = []
                for resultado in reg:
                    tratamiento = resultado.idTratamiento
                    resultado_dict = {
                        'id': resultado.id,
                        'idTratamiento': resultado.idTratamiento.id,
                        'observacion': resultado.observacion,
                        'fecha': resultado.fecha,
                        'idTratamiento': {
                            'id': tratamiento.id,
                            
                            'fecha': tratamiento.fecha
                        }
                    }
                    resultados_values.append(resultado_dict)
                context = {
                    'message': "Consulta exitosa",
                    'resultados': resultados_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'resultados': []
                }
                return JsonResponse(context)

#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)
        rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
        if validar_id_tratamiento(jd['idTratamiento']):    
            resultados= {'message': "El resultado no existe"}
        if validar_id_tipo(jd['idtipo']):    
            resultados= {'message': "El resultado no existe"}
        elif len(jd['observacion']) <= 0:
            resultados = {'message': "La observación esta vacía."}
        elif len(jd['observacion']) < 5:
            resultados = {'message': "La observación debe tener más de 5 caracteres."}
        elif len(jd['observacion']) > 100:
            resultados = {'message': "La observación debe tener menos de 100 caracteres."}
        elif not validar_cadena_espacios(jd['observacion']):
            resultados = {'message': "No se permiten mas de un espacio consecutivo.[observacion]"}
        elif validar_cadena_repeticion(jd['observacion']):
            resultados = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[observacion]"}
        elif (rsp_fecha) is None:
            resultados= {'message': "La fecha esta vacía"}
        elif isinstance(rsp_fecha, str):
            resultados= {'message': "La fecha esta vacía"}
        elif (rsp_fecha.year) < 2000:
            resultados= {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fecha.year) > 2030:
            resultados= {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        else:
            resultados= {'message': "Registro Exitoso."}
            Resultados.objects.create(idTratamiento=instanciar_tratamiento(jd['idTratamiento']),idtipo=instanciar_tipo(jd['idtipo']), fecha=jd['fecha'],observacion=jd['observacion'])
            resultados= {'message':"Registro Exitoso."}
        return JsonResponse(resultados)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        resultados= list(Resultados.objects.filter(id=id).values())
        if len(resultados) > 0:
            rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
            resultado=Resultados.objects.get(id=id)
            if validar_id_tratamiento(jd['idTratamiento']):    
                resultados= {'message': "El tratamiento no existe"}
            if validar_id_tipo(jd['idtipo']):    
                resultados= {'message': "El resultado no existe"}
            elif len(jd['observacion']) <= 0:
                resultados = {'message': "La observación esta vacía."}
            elif len(jd['observacion']) < 5:
                resultados = {'message': "La observación debe tener más de 5 caracteres."}
            elif len(jd['observacion']) > 100:
                resultados = {'message': "La observación debe tener menos de 100 caracteres."}
            elif not validar_cadena_espacios(jd['observacion']):
                resultados = {'message': "No se permiten mas de un espacio consecutivo.[observacion]"}
            elif validar_cadena_repeticion(jd['observacion']):
                resultados = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[observacion]"}
            elif (rsp_fecha) is None:
                resultados= {'message': "La fecha esta vacía"}
            elif isinstance(rsp_fecha, str):
                resultados= {'message': "La fecha esta vacía"}
            elif (rsp_fecha.year) < 2000:
                resultados= {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            elif (rsp_fecha.year) > 2030:
                resultados= {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            else:
                resultado.idTratamiento = instanciar_tratamiento(jd['idTratamiento'])
                resultado.idtipo = instanciar_tipo(jd['idtipo'])
                resultado.observacion = jd['observacion']
                resultado.fecha = jd['fecha']
                resultado.save()
                resultados= {'message': "La actualización fue exitosa."}
        return JsonResponse(resultados)
        
        
#Eliminar un registro de tipo
    def delete(self, request,id):
        resultado = list(Resultados.objects.filter(id=id).values())
        if len(resultado) > 0:
            Resultados.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'resultado': []}
        return JsonResponse(datos)
    
def instanciar_tratamiento(id):
    if (id>0):
        tratamiento = Tratamiento.objects.get(id=id)
        if tratamiento:
            return tratamiento   

def validar_id_tratamiento(id):
    if (id>0):
        registro = Tratamiento.objects.filter(id=id)
        if registro:
            return False
        else:
            return True    

def instanciar_tipo(id):
    if (id>0):
        tratamiento = Tipo.objects.get(id=id)
        if tratamiento:
            return tratamiento   

def validar_id_tipo(id):
    if (id>0):
        registro = Tipo.objects.filter(id=id)
        if registro:
            return False
        else:
            return True  

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

