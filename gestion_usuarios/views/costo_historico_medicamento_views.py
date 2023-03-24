from datetime import datetime, timedelta
from decimal import Decimal
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class CostoHistoricoMedicamentosViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                costoHistoricos = CostoHistoricoMedicamento.objects.filter(id=campo).select_related('idmedicamento')
                if costoHistoricos is not None:
                    historicos_values = []
                    for historico in costoHistoricos:
                        medicamento = historico.idmedicamento
                        historico_dict = {
                            'id': historico.id,
                            'fechaInicio': historico.fechaInicio,
                            'fechaFinal': historico.fechaFinal,
                            'activo':historico.activo,
                            'costo': historico.costo,
                            'idmedicamento': {
                                'id': medicamento.id,
                                'nombre': medicamento.nombre
                            }
                        }
                        historicos_values.append(historico_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'historicos': historicos_values
                        }
                        return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'historicos': []
                    }
                    return JsonResponse(context)
            elif criterio == "nombre":
                idmedicamento = Medicamento.objects.filter(nombre=campo)
                if idmedicamento is not None:
                    for medicamento in idmedicamento:
                        costoHistoricos = CostoHistoricoMedicamento.objects.filter(idmedicamento=medicamento.id).select_related('idmedicamento')
                        if costoHistoricos is not None:
                            historicos_values = []
                            for historico in costoHistoricos:
                                med = historico.idmedicamento
                                historico_dict = {
                                    'id': historico.id,
                                    'fechaInicio': historico.fechaInicio,
                                    'fechaFinal': historico.fechaFinal,
                                    'activo':historico.activo,
                                    'costo': historico.costo,
                                    'idmedicamento': {
                                        'id': med.id,
                                        'nombre': med.nombre
                                    }
                                }
                                historicos_values.append(historico_dict)
                            context = {
                                'message': "Consulta exitosa",
                                'historicos': historicos_values
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
            context = {
                    'message': "No se encontraron los datos",
                    'historicos': []
                }
            return JsonResponse(context)
        else:
            costoHistoricos = CostoHistoricoMedicamento.objects.select_related('idmedicamento')
            if costoHistoricos is not None:
                historicos_values = []
                for historico in costoHistoricos:
                    medicamento = historico.idmedicamento
                    historico_dict = {
                        'id': historico.id,
                        'fechaInicio': historico.fechaInicio,
                        'fechaFinal': historico.fechaFinal,
                        'activo':historico.activo,
                        'costo': historico.costo,
                        'idmedicamento': {
                            'id': medicamento.id,
                            'nombre': medicamento.nombre
                        }
                    }
                    historicos_values.append(historico_dict)
                context = {
                    'message': "Consulta exitosa",
                    'historicos': historicos_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'historicos': []
                }
                return JsonResponse(context)

#Agregar un registro de cargos
#nombre, idTipo,fechaRegistro,stockActual,stockMinimo,stockMaximo,idProveedor,idImpuesto,costoCompra,precioVenta
    def post(self, request):
        jd=json.loads(request.body)
        #VALIDACIONES
        if Decimal(jd['costo']) <= 0:
            mensaje_post = {'message': "El costo debe ser mayor a 0."}
        elif len(str(jd['costo'])) > 11:
            mensaje_post = {'message': "El costo debe tener menos de 10 digitos."}
        elif round(Decimal(jd['costo'])) > 99999999.99:
            mensaje_post = {'message': "El costo es muy alto."}
        elif round(Decimal(jd['costo']), 2) > round(Decimal(jd['precioVenta']), 2):
            mensaje_post = {'message': "El costo debe ser menor al precio de venta."}
        #FIN VALIDACIONES
        else:
            CostoHistoricoMedicamento.objects.create(idmedicamento=instanciar_medicamento['idMedicamento'],
                                                     fechaInicio=datetime.now(),
                                                     activo=1,
                                                     costo=jd['costoCompra'])
            mensaje_post = {'message':"Registro Exitoso."}
        return JsonResponse(mensaje_post)

#Actualizar un registro de cargos
#nombre, idTipo,fechaRegistro,activo,stockActual,stockMinimo,stockMaximo,idProveedor,idImpuesto,costoCompra,precioVenta
    def put(self, request,id):
        jd=json.loads(request.body)
        costoHistorico = list(CostoHistoricoMedicamento.objects.filter(id=id).values())
        if len(costoHistorico) > 0:
            costo_historico_actualizar=CostoHistoricoMedicamento.objects.get(id=id)
            #VALIDACIONES
            if Decimal(jd['costo']) <= 0:
                mensaje_put = {'message': "El costo debe ser mayor a 0."}
            elif len(str(jd['costo'])) > 11:
                mensaje_put = {'message': "El costo debe tener menos de 10 digitos."}
            elif round(Decimal(jd['costo'])) > 99999999.99:
                mensaje_put = {'message': "El costo es muy alto."}
            elif round(Decimal(jd['costo']), 2) > round(Decimal(jd['precioVenta']), 2):
                mensaje_put = {'message': "El costo debe ser menor al precio de venta."}
            #FIN VALIDACIONES
            else:
                costo_historico_actualizar.idmedicamento = instanciar_medicamento(jd['idMedicamento'])
                costo_historico_actualizar.fechaInicio = datetime.now()
                costo_historico_actualizar.costo = jd['costo']
                historico_anterior = CostoHistoricoMedicamento.objects.filter(nombre=jd['nombre']).last()
                if historico_anterior is not None:
                    historico_anterior.fechaFinal = fecha_final()
                else:
                    CostoHistoricoMedicamento.objects.create(idmedicamento=instanciar_medicamento['idMedicamento'],
                                                     fechaInicio=datetime.now(),
                                                     activo=1,
                                                     costo=jd['costoCompra'])
                costo_historico_actualizar.save()
                mensaje_put = {'message': "La actualización fue exitosa."}
        return JsonResponse(mensaje_put)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        costoHistorico = list(CostoHistoricoMedicamento.objects.filter(id=id).values())
        if len(costoHistorico) > 0:
            CostoHistoricoMedicamento.objects.filter(id=id).delete()
            costoHistorico = {'message':"Registro Eliminado"}
        else:
            costoHistorico = {'message':"No se encontró el registro", 'costoHistorico': []}
        return JsonResponse(costoHistorico)

        
def instanciar_medicamento(id):
    if (id>0):
        registro = CostoHistoricoMedicamento.objects.get(id=id)
        if registro:
            return registro

def fecha_final():
    fecha_menos_un_dia=datetime.today()+timedelta(days=-1)
    return fecha_menos_un_dia
      
def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))
