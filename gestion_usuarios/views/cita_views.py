from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class CitasViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                citas = list(Cita.objects.filter(id=campo).values())
                if len(citas) > 0:
                    citas = citas
                    citas = {'message': "Consulta exitosa", 'citas': citas}
                else:
                    citas = {'message': "No se encontraron los datos", 'citas': []} 
                    return JsonResponse(citas)
            elif criterio == "fechaProgramada":
                citas = list(Cita.objects.filter(fechaProgramada=campo).values())
                if len(citas) > 0:
                    citas = citas
                    citas = {'message': "Consulta exitosa", 'citas': citas}
                else:
                    citas = {'message': "No se encontraron los datos", 'citas': []} 
                    return JsonResponse(citas)
        else:
            citas = list(Cita.objects.values())
            if len(citas) > 0:
                citas = {'message': "Consulta exitosa", 'citas': citas}
            else:
                citas = {'message': "No se encontraron los datos", 'citas': []} 
        return JsonResponse(citas)
#idPaciente fechaActual fechaProgramada fechaMaxima activa
#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        rsp_fechaActual = datetime.fromisoformat(jd['fechaActual'])
        rsp_fechaProgramada = datetime.fromisoformat(jd['fechaProgramada'])
        rsp_fechaMaxima = datetime.fromisoformat(jd['fechaMaxima'])

        if validar_id(jd['idPaciente']):
            citas = {'message': "El paciente no existe"}
            #fechaActual
        elif (rsp_fechaActual) is None:
            citas = {'message': "La fecha actual esta vacía"}
        elif isinstance(rsp_fechaActual, str):
            citas = {'message': "La fecha actual esta vacía"}
        elif (rsp_fechaActual.year) < 2000:
            citas = {'message': "La fecha actual debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fechaActual.year) > 2030:
            citas = {'message': "La fecha actual debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fechaActual) >= rsp_fechaProgramada:
            citas = {'message': "La fecha actual debe ser menor a la fecha programada"}
        elif (rsp_fechaActual) >= rsp_fechaMaxima:
            citas = {'message': "La fecha actual debe ser menor a la fecha maxima"}
            #validar tiempo fecha actual
        elif (rsp_fechaActual.time()) < time(5, 0, 0) or (rsp_fechaActual.time()) > time(22, 0, 0):
            citas = {'message': "La hora actual debe estar dentro del rango de 5:00AM a 10:00PM"}
        elif rsp_fechaActual.date == rsp_fechaProgramada.date and (rsp_fechaActual.time()) >= (rsp_fechaProgramada.time()):
            citas = {'message': "La hora actual debe ser menor a la hora programada"}
        elif rsp_fechaActual.date == rsp_fechaMaxima.date and (rsp_fechaActual.time()) > (rsp_fechaMaxima.time()):
            citas = {'message': "La hora actual debe ser menor a la hora maxima"}
            #fechaProgramada
        elif (rsp_fechaProgramada) is None:
            citas = {'message': "La fecha programada esta vacía"}
        elif isinstance(rsp_fechaProgramada, str):
            citas = {'message': "La fecha programada esta vacía"}
        elif (rsp_fechaProgramada.year) < 2000:
            citas = {'message': "La fecha programada debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fechaProgramada.year) > 2030:
            citas = {'message': "La fecha programada debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fechaProgramada) <= rsp_fechaActual:
            citas = {'message': "La fecha programada debe ser mayor a la fecha de registro"}
        elif (rsp_fechaProgramada) > rsp_fechaMaxima:
            citas = {'message': "La fecha programada debe ser menor o igual a la fecha maxima"}
        elif validar_fecha_programada_repetida(rsp_fechaProgramada):
            citas = {'message': "Ya hay una cita programada en la misma fecha"}
            #validar tiempo fecha programada
        elif (rsp_fechaProgramada.time()) < time(5, 0, 0) or (rsp_fechaProgramada.time()) > time(22, 0, 0):
            citas = {'message': "La hora actual debe estar dentro del rango de 5:00AM a 10:00PM"}
        elif rsp_fechaActual.date == rsp_fechaProgramada.date and (rsp_fechaActual.time()) >= (rsp_fechaProgramada.time()):
            citas = {'message': "La hora actual debe ser menor a la hora programada"}
        elif rsp_fechaActual.date == rsp_fechaMaxima.date and (rsp_fechaActual.time()) > (rsp_fechaMaxima.time()):
            citas = {'message': "La hora actual debe ser menor a la hora maxima"}
        elif (calcular_hora_fecha(rsp_fechaProgramada, rsp_fechaActual)) < 2:
            citas = {'message': "La hora programada debe tener un margen mínimo de 2 horas respecto a la hora actual"}
            #fechaMaxima
        elif (rsp_fechaMaxima) is None:
            citas = {'message': "La fecha maxima esta vacía"}
        elif isinstance(rsp_fechaMaxima, str):
            citas = {'message': "La fecha maxima esta vacía"}
        elif (rsp_fechaMaxima.year) < 2000:
            citas = {'message': "La fecha maxima debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fechaMaxima.year) > 2030:
            citas = {'message': "La fecha maxima debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fechaMaxima) < rsp_fechaActual:
            citas = {'message': "La fecha maxima debe ser mayor a la fecha de registro"}
        elif (rsp_fechaMaxima) < rsp_fechaProgramada:
            citas = {'message': "La fecha maxima debe ser mayor a la fecha programada"}
        elif validar_fecha_maxima_repetida(rsp_fechaMaxima):
            citas = {'message': "Ya hay una cita programada en la misma fecha"} 
            #validar tiempo fecha maxima
        elif (rsp_fechaMaxima.time()) < time(5, 0, 0) or (rsp_fechaMaxima.time()) > time(22, 0, 0):
            citas = {'message': "La hora actual debe estar dentro del rango de 5:00AM a 10:00PM"}
        elif (calcular_hora_fecha(rsp_fechaMaxima, rsp_fechaActual)) < 2:
            citas = {'message': "La hora maxima debe tener un margen mínimo de 2 horas respecto a la hora actual"}
        elif jd['activa'] < 0:
            citas = {'message': "Activo debe ser positivo."}
        elif jd['activa'] > 1:
            citas = {'message': "Activo unicamente puede ser 0 o 1."}         
        else:
            Cita.objects.create(idPaciente=instanciar_paciente(jd['idPaciente']), fechaActual=jd['fechaActual'], fechaProgramada=jd['fechaProgramada'], fechaMaxima=jd['fechaMaxima'], activa=jd['activa'])
            citas = {'message':"Registro Exitoso."}
        return JsonResponse(citas)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        citas = list(Cita.objects.filter(id=id).values())
        if len(citas) > 0:
            cita_actualizar = Cita.objects.get(id=id)
            if validar_id(jd['idPaciente']):
                citas = {'message': "El paciente no existe"}
                rsp_fechaActual = datetime.fromisoformat(jd['fechaActual'])
                rsp_fechaProgramada = datetime.fromisoformat(jd['fechaProgramada'])
                rsp_fechaMaxima = datetime.fromisoformat(jd['fechaMaxima'])

                if validar_id(jd['idPaciente']):
                    citas = {'message': "El paciente no existe"}
                    #fechaActual
                elif (rsp_fechaActual) is None:
                    citas = {'message': "La fecha actual esta vacía"}
                elif isinstance(rsp_fechaActual, str):
                    citas = {'message': "La fecha actual esta vacía"}
                elif (rsp_fechaActual) >= rsp_fechaProgramada:
                    citas = {'message': "La fecha actual debe ser menor a la fecha programada"}
                elif (rsp_fechaActual) >= rsp_fechaMaxima:
                    citas = {'message': "La fecha actual debe ser menor a la fecha maxima"}
                    #validar tiempo fecha actual
                elif (rsp_fechaActual.time()) < time(5, 0, 0) or (rsp_fechaActual.time()) > time(22, 0, 0):
                    citas = {'message': "La hora actual debe estar dentro del rango de 5:00AM a 10:00PM"}
                elif (rsp_fechaActual.time()) >= (rsp_fechaProgramada.time()):
                    citas = {'message': "La hora actual debe ser menor a la hora programada"}
                elif (rsp_fechaActual.time()) > (rsp_fechaMaxima.time()):
                    citas = {'message': "La hora actual debe ser menor a la hora maxima"}
                elif (rsp_fechaProgramada.time()) > (rsp_fechaMaxima.time()):
                    citas = {'message': "La hora programada debe ser menor a la hora maxima"}
                    #fechaProgramada
                elif (rsp_fechaProgramada) is None:
                    citas = {'message': "La fecha programada esta vacía"}
                elif isinstance(rsp_fechaProgramada, str):
                    citas = {'message': "La fecha programada esta vacía"}
                elif (rsp_fechaProgramada) <= rsp_fechaActual:
                    citas = {'message': "La fecha programada debe ser mayor a la fecha de registro"}
                elif (rsp_fechaProgramada) > rsp_fechaMaxima:
                    citas = {'message': "La fecha programada debe ser menor o igual a la fecha maxima"}
                    #validar tiempo fecha programada
                elif (rsp_fechaProgramada.time()) < time(5, 0, 0) or (rsp_fechaProgramada.time()) > time(22, 0, 0):
                    citas = {'message': "La hora actual debe estar dentro del rango de 5:00AM a 10:00PM"}
                elif (rsp_fechaActual.time()) >= (rsp_fechaProgramada.time()):
                    citas = {'message': "La hora actual debe ser menor a la hora programada"}
                elif (rsp_fechaActual.time()) > (rsp_fechaMaxima.time()):
                    citas = {'message': "La hora actual debe ser menor a la hora maxima"}
                elif (calcular_hora_fecha(rsp_fechaProgramada, rsp_fechaActual)) < 2:
                    citas = {'message': "La hora programada debe tener un margen mínimo de 2 horas respecto a la hora actual"}
                    #fechaMaxima
                elif (rsp_fechaMaxima) is None:
                    citas = {'message': "La fecha maxima esta vacía"}
                elif isinstance(rsp_fechaMaxima, str):
                    citas = {'message': "La fecha maxima esta vacía"}
                elif (rsp_fechaMaxima) < rsp_fechaActual:
                    citas = {'message': "La fecha maxima debe ser mayor a la fecha de registro"}
                elif (rsp_fechaMaxima) < rsp_fechaProgramada:
                    citas = {'message': "La fecha maxima debe ser mayor a la fecha programada"}
                    #validar tiempo fecha maxima
                elif (rsp_fechaMaxima.time()) < time(5, 0, 0) or (rsp_fechaMaxima.time()) > time(22, 0, 0):
                    citas = {'message': "La hora actual debe estar dentro del rango de 5:00AM a 10:00PM"}
                elif (calcular_hora_fecha(rsp_fechaMaxima, rsp_fechaActual)) < 2:
                    citas = {'message': "La hora maxima debe tener un margen mínimo de 2 horas respecto a la hora actual"}
                elif jd['activa'] < 0:
                    citas = {'message': "Activo debe ser positivo."}
                elif jd['activa'] > 1:
                    citas = {'message': "Activo unicamente puede ser 0 o 1."}   
            else:
                citas = {'message': "Registro Exitoso."}
                cita_actualizar.idPaciente = instanciar_paciente(jd['idPaciente'])
                cita_actualizar.fechaActual = jd['fechaActual']
                cita_actualizar.fechaProgramada = jd['fechaProgramada']
                cita_actualizar.fechaMaxima = jd['fechaMaxima']
                cita_actualizar.activa = jd['activa']
                cita_actualizar.save()
                citas = {'message': "La actualización fue exitosa."}
        return JsonResponse(citas)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        citas = list(Cita.objects.filter(id=id).values())
        if len(citas) > 0:
            Cita.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontró el registro", 'citas': []}
        return JsonResponse(datos)


        
def instanciar_paciente(id):
    if (id>0):
        paciente = Paciente.objects.get(id=id)
        if paciente:
            return paciente

def validar_id(id):
    if (id>0):
        registro = Paciente.objects.filter(id=id)
        if registro:
            return False
        else:
            return True
        
def validar_fecha_programada_repetida(fecha): 
    if (fecha):
        registros = Cita.objects.filter(fechaProgramada=fecha)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def validar_fecha_maxima_repetida(fecha): 
    if (fecha):
        registros = Cita.objects.filter(fechaMaxima=fecha)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def calcular_hora_fecha(fecha_max, fecha_min):
    diferencia_horas = (fecha_max - fecha_min).total_seconds() / 3600
    return diferencia_horas


def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))

    
         