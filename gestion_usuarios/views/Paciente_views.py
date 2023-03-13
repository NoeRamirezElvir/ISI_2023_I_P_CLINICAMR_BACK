from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class PacienteViews(View):
    #Este metodo permite realizar Els conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if(criterio=="id"):
                pacientes = list(Paciente.objects.filter(id=campo).values())
                if len(pacientes) > 0:
                    pacientes = pacientes
                    pacientes = {'message': "Consulta exitosa", 'pacientes': pacientes}
                else:
                    pacientes = {'message': "No se encontraron los datos", 'pacientes': []} 
                    return JsonResponse(pacientes)
            elif(criterio=="nombre"):
                pacientes = list(Paciente.objects.filter(nombre=campo).values())
                if len(pacientes) > 0:
                    pacientes = {'message': "Consulta exitosa", 'pacientes': pacientes}
                else:
                    pacientes = {'message': "No se encontraron los datos", 'pacientes': []} 
                    return JsonResponse(pacientes)
            elif(criterio=="documento"):
                pacientes = list(Paciente.objects.filter(documento=campo).values())
                if len(pacientes) > 0:
                    pacientes = {'message': "Consulta exitosa", 'pacientes': pacientes}
                else:
                    pacientes = {'message': "No se encontraron los datos", 'pacientes': []} 
                    return JsonResponse(pacientes)
        else:
            pacientes = list(Paciente.objects.values())
            if len(pacientes) > 0:
                pacientes = {'message': "Consulta exitosa", 'pacientes': pacientes}
            else:
                pacientes = {'message': "No se encontraron los datos", 'pacientes': []} 
        return JsonResponse(pacientes)
    
#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            pacientes = {'message': "El nombre esta vacío."}
        elif len(jd['nombre']) < 3:
            pacientes = {'message': "El nombre debe tener más de 3 caracteres."}
        elif len(jd['nombre']) > 50:
            pacientes = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif not jd['apellidos'].isalpha():
            pacientes = {'message': "El apellido solo puede contener letras."}
        elif len(jd['apellidos']) <= 0:
            pacientes = {'message': "El apellido esta vacío."}
        elif len(jd['apellidos']) < 3:
            pacientes = {'message': "El apellido debe tener más de 3 caracteres."}
        elif len(jd['apellidos']) > 50:
            pacientes = {'message': "El apellido debe tener menos de 50 caracteres."}
        elif len(jd['email']) <= 0:
            pacientes = {'message': "El email esta vacío."}
        elif len(jd['email']) < 5:
            pacientes = {'message': "El email debe tener más de 5 caracteres."}
        elif len(jd['email']) > 30:
            pacientes = {'message': "El email debe tener menos de 30 caracteres."}
        elif validar_email(jd['email']):
            pacientes = {'message': "El email debe tener un formato válido."}
        elif len(str(jd['fechaNacimiento'])) <= 0:
            pacientes = {'message': "La fecha de nacimiento esta vacía."}
        elif len(str(jd['fechaNacimiento'])) > 10:
            pacientes = {'message': "La fecha de nacimiento debe tener menos de 10 caracteres."}
        elif str(jd['telefono']).isalpha():
            pacientes = {'message': "El teléfono solo puede contener numeros."}
        elif len(str(jd['telefono'])) <= 0:
            pacientes = {'message': "El teléfono esta vacío."}
        elif len(str(jd['telefono'])) < 8:
            pacientes = {'message': "El teléfono debe tener más de 8 caracteres."}
        elif len(str(jd['telefono'])) > 15:
            pacientes = {'message': "El teléfono debe tener menos de 15 caracteres."}
        elif (str(jd['telefono']))[0] == '1':
            pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
        elif (str(jd['telefono']))[0] == '4':
            pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
        elif (str(jd['telefono']))[0] == '5':
            pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
        elif (str(jd['telefono']))[0] == '6':
            pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
        elif (str(jd['telefono']))[0] == '7':
            pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
        elif (str(jd['telefono']))[0] == '0':
            pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
        elif len(jd['direccion']) <= 0:
            pacientes = {'message': "La dirección esta vacía."}
        elif len(jd['direccion']) < 5:
            pacientes = {'message': "La dirección debe tener más de 5 caracteres."}
        elif len(jd['direccion']) > 50:
            pacientes = {'message': "La dirección debe tener menos de 50 caracteres."}
        elif (jd['idTipoDocumentos']) <= 0:
            pacientes = {'message': "El tipo de documento esta vacío."}
        elif validar_id_documento(jd['idTipoDocumentos']):
            pacientes = {'message': "El id de documento no existe."}
        elif len(jd['documento']) <= 0:
            pacientes = {'message': "El documento esta vacío."}
        elif (validar_documento_repetido(jd['documento'])):
            pacientes = {'message': "El documento esta en uso."}
        elif len(jd['documento']) < 7:
            pacientes = {'message': "El documento debe tener más de 7 caracteres."}
        elif len(jd['documento']) > 50:
            pacientes = {'message': "El documento debe tener menos de 50 caracteres."}
        elif len(jd['documento']) < (validar_documento(jd['idTipoDocumentos'])):
            pacientes = {'message': "El documento debe cumplir la longitud asignada."}
        
        else:
            pacientes = {'message': "Registro Exitoso."}
            Paciente.objects.create(nombre=jd['nombre'], apellidos=jd['apellidos'],fechaNacimiento=datetime.strptime(str(jd['fechaNacimiento']), "%Y-%m-%d").strftime("%Y-%m-%d"),email=jd['email'],telefono=str(jd['telefono']),direccion=jd['direccion'],idTipoDocumentos=(instanciar_documento(jd['idTipoDocumentos'])),documento=jd['documento'])
            pacientes = {'message':"Registro Exitoso."}
        return JsonResponse(pacientes)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        pacientes = list(Paciente.objects.filter(id=id).values())
        if len(pacientes) > 0:
            paciente=Paciente.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                pacientes = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 3:
                pacientes = {'message': "El nombre debe tener más de 3 caracteres."}
            elif len(jd['nombre']) > 50:
                pacientes = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif not jd['apellidos'].isalpha():
                pacientes = {'message': "El apellido solo puede contener letras."}
            elif len(jd['apellidos']) <= 0:
                pacientes = {'message': "El apellido esta vacío."}
            elif len(jd['apellidos']) < 3:
                pacientes = {'message': "El apellido debe tener más de 3 caracteres."}
            elif len(jd['apellidos']) > 50:
                pacientes = {'message': "El apellido debe tener menos de 50 caracteres."}
            elif len(jd['email']) <= 0:
                pacientes = {'message': "El email esta vacío."}
            elif len(jd['email']) < 5:
                pacientes = {'message': "El email debe tener más de 5 caracteres."}
            elif len(jd['email']) > 30:
                pacientes = {'message': "El email debe tener menos de 30 caracteres."}
            elif validar_email(jd['email']):
                pacientes = {'message': "El email debe tener un formato válido."}
            elif len(str(jd['fechaNacimiento'])) <= 0:
                pacientes = {'message': "La fecha de nacimiento esta vacía."}
            elif len(str(jd['fechaNacimiento'])) > 10:
                pacientes = {'message': "La fecha de nacimiento debe tener menos de 10 caracteres."}
            elif str(jd['telefono']).isalpha():
                pacientes = {'message': "El teléfono solo puede contener numeros."}
            elif len(str(jd['telefono'])) <= 0:
                pacientes = {'message': "El teléfono esta vacío."}
            elif len(str(jd['telefono'])) < 8:
                pacientes= {'message': "El teléfono debe tener más de 8 caracteres."}
            elif len(str(jd['telefono'])) > 15:
                pacientes = {'message': "El teléfono debe tener menos de 15 caracteres."}
            elif (str(jd['telefono']))[0] == '1':
                pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
            elif (str(jd['telefono']))[0] == '4':
                pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
            elif (str(jd['telefono']))[0] == '5':
                pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
            elif (str(jd['telefono']))[0] == '6':
                pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
            elif (str(jd['telefono']))[0] == '7':
                pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
            elif (str(jd['telefono']))[0] == '0':
                pacientes = {'message': "El teléfono debe comenzar con 2, 3, 8, 9."}
            elif len(jd['direccion']) <= 0:
                pacientes = {'message': "La dirección esta vacía."}
            elif len(jd['direccion']) < 5:
                pacientes = {'message': "La dirección debe tener más de 5 caracteres."}
            elif len(jd['direccion']) > 50:
                pacientes = {'message': "La dirección debe tener menos de 50 caracteres."}
            elif (jd['idTipoDocumentos']) <= 0:
                pacientes = {'message': "El tipo de documento esta vacío."}
            elif validar_id_documento(jd['idTipoDocumentos']):
                pacientes = {'message': "El id de documento no existe."}
            elif len(jd['documento']) <= 0:
                pacientes = {'message': "El documento esta vacío."}
            elif len(jd['documento']) < 7:
                pacientes = {'message': "El documento debe tener más de 7 caracteres."}
            elif len(jd['documento']) > 50:
                pacientes = {'message': "El documento debe tener menos de 50 caracteres."}
            elif len(jd['documento']) < (validar_documento(jd['idTipoDocumentos'])):
                pacientes = {'message': "El documento debe cumplir la longitud asignada."}
            
            else:
                pacientes = {'message': "Registro Exitoso."}
                paciente.nombre = jd['nombre']
                paciente.apellidos = jd['apellidos']
                paciente.email = jd['email']
                paciente.telefono = str(jd['telefono'])
                paciente.direccion = jd['direccion']
                paciente.fechaNacimiento = datetime.strptime(str(jd['fechaNacimiento']), "%Y-%m-%d").strftime("%Y-%m-%d")
                paciente.idTipoDocumentos = instanciar_documento(jd['idTipoDocumentos'])
                paciente.documento = jd['documento']
                
                print(paciente)
                paciente.save()
                pacientes = {'message': "El actualización fue exitosa."}
        return JsonResponse(pacientes)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        pacientes = list(Paciente.objects.filter(id=id).values())
        if len(pacientes) > 0:
            Paciente.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'pacientes': []}
        return JsonResponse(datos)
    

#validaciones metodos
def validar_email(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is None

def validar_documento(id):
    if (id>0):
        documento = TipoDocumentos.objects.get(id=id)
        return documento.longitud
    return False

def validar_documento_repetido(documento):
    if (documento):
        documentos = Paciente.objects.filter(documento=documento)
        if len(documentos) > 0:
            return True
        else:
            return False
    return False


        
def instanciar_documento(id):
    if (id>0):
        documentos = TipoDocumentos.objects.get(id=id)
        if documentos:
            return documentos

def validar_id_documento(id):
    if (id>0):
        documento = TipoDocumentos.objects.filter(id=id)
        if documento:
            return False
        else:
            return True
        
def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))