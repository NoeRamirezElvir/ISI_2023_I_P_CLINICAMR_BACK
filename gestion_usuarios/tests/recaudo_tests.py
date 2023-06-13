from datetime import date
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import *
import json

class RecaudoTests(TestCase):
    def setUp(self):
        self.url = reverse('recaudo_list')
        #Impuesto y subtipo
        self.impuesto = Impuesto.objects.create(nombre='ISV10%', valor=0.10)
        self.subtipo = Subtipo.objects.create(nombre='medicamento', activo=1)
        self.subtipo = Subtipo.objects.create(nombre='tratamiento', activo=1)
        self.subtipo = Subtipo.objects.create(nombre='examen', activo=1)
        self.subtipo = Subtipo.objects.create(nombre='consulta', activo=1)
        self.subtipo = Subtipo.objects.create(nombre='otros', activo=1)
        #Correlativo
        self.correlativo = CorrelativoSar.objects.create(cai=('30990398-6a82-44b5-84ca-ed13112a0ee5').strip(),
                                          rangoInicial=1,
                                          rangoFinal=100,
                                          consecutivo=1,
                                          fechaInicio = date.today(),
                                          fechaLimiteEmision='2023-06-30',
                                          )
        #Paciente
        self.tipoDocumento = TipoDocumentos.objects.create(id=1, nombre='DNI',longitud=13)
        self.paciente = Paciente.objects.create(nombre='paciente',
                                                apellido='prueba',
                                                fechaNacimiento='2000-11-11',
                                                correo='correo@tipo.com',
                                                telefono='99886677',
                                                direccion='123 col prueba',
                                                idTipoDocumento=self.tipoDocumento,
                                                documento='8901220004753'
                                                )
        #Empleado
        self.cargo = CargoEmpleado.objects.create(nombre='Cargo 1', descripcion='Descripción 1', activo=1)
        self.especialidad = EspecialidadMedico.objects.create(nombre='Medico general', descripcion='Descripción 1')
        self.empleado = Empleado.objects.create(nombre='empleado', apellidos='prueba',
                                                fechaNacimiento='2000-11-11',
                                                email='empleado@example.com',
                                                telefono='99887700',
                                                direccion='123 col prueba',
                                                idTipoDocumentos=self.tipoDocumento,
                                                documento='0801200200482',
                                                idEspecialidadMedico=self.especialidad,
                                                idCargoEmpleado=self.cargo,
                                                activo=1)
        #Metodo Pago
        self.metodo_pago1 = MetodoDePago.objects.create(nombre='tarjeta', descripcion='Descripción 1')
        self.metodo_pago2 = MetodoDePago.objects.create(nombre='efectivo', descripcion='Descripción 1')
        self.metodo_pago3 = MetodoDePago.objects.create(nombre='mixto', descripcion='Descripción 1')
        #Consulta
        self.sintoma=Sintoma.objects.create(nombre='sintoma 1', descripcion='sintoma 1')
        self.enfermedad=Enfermedad.objects.create(nombre='enfermedad 1')
        EnfermedadDetalle.objects.create(idEnfermedad = self.enfermedad, idSintoma = self.sintoma)
        self.diagnostico = Diagnostico.objects.create(descripcion='diagnostico 1')
        DiagnosticoDetalle.objects.create(idDiagnostico = self.diagnostico, idEnfermedad = self.enfermedad)


        self.tipo = Tipo.objects.create(nombre='Consulta general',
                                        descripcion='Sin descripcion',
                                        precio = 100,
                                        idsubtipo = self.subtipo,
                                        idImpuesto = self.impuesto
                                        )
        self.cita = Cita.objects.create(
                                        idPaciente=self.paciente,
                                        fechaActual=datetime(2023, 6, 12, 10, 0),
                                        fechaProgramada=datetime(2023, 6, 15, 10, 0),
                                        fechaMaxima=datetime(2023, 6, 15, 11, 0),
                                        activa=1
                                    )
        
        self.consulta = Consulta.objects.create(idCita=self.cita,
                                    idTipo=self.tipo,
                                    fecha=datetime(2023, 6, 12, 10, 0),
                                    recomendaciones='No cuenta con recomendaciones',
                                    informacionAdicional='Sin informacion adicional'
                                    )
        self.consulta_detalle = ConsultaDetalle.objects.create(idConsulta=self.consulta,
                                                               idDiagnostico=self.diagnostico)
        #descuentos
        self.descuento = Descuento.objects.create(nombre='Descuento 10%', valor=0.10)
        #parametros generales
        ParametrosGenerales.objects.create(nombre='nombre', descripcion='Descripción 1', valor='Medical Rescue Clínica General')
        ParametrosGenerales.objects.create(nombre='direccion', descripcion='Descripción 1', valor='Colonia Humuya, Calle Poseidón, Tegucigalpa')
        ParametrosGenerales.objects.create(nombre='correo', descripcion='Descripción 1', valor='medical.rescue23@gmail.com')
        ParametrosGenerales.objects.create(nombre='telefono', descripcion='Descripción 1', valor='97863003')
        ParametrosGenerales.objects.create(nombre='rtn', descripcion='Descripción 1', valor='23456798784567')
    def test_get_recaudo(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        recaudo = response.json()
        self.assertEqual(len(recaudo), 2)

    def test_post_recaudo(self):
        data = {
                'correlativo' : self.correlativo.pk,
                'idPaciente' : self.paciente.pk,
                'fechaActual' : '2023-06-13',
                'fechaEntrega' : '2023-06-13',
                'idEmpleado' : self.empleado.pk,
                'idMetodo' : self.metodo_pago2.pk,
                'idConsulta' : self.consulta.pk,
                'montoEfectivo' : 100,
                'numeroTarjeta' : None,
                'estado' : 'Pagada',
                'activa' : 1,
                'total' : 99,
                'subtotal' : 110,
                'descuento' : 11,
                'imp' : 10,
                'idDescuento' : self.descuento.pk,
                'cambio' : 1,
                'medicamentos':[],
                'tratamientos':[],
                'examenes':[]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        rsp = response.json()
        message = rsp['message']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Registro Exitoso.')
        self.assertTrue(Recaudo.objects.filter(idPaciente__documento='8901220004753').exists())

    def test_post_recaudo_invalid_detalles(self):
        data = {
                'correlativo' : self.correlativo.pk,
                'idPaciente' : self.paciente.pk,
                'fechaActual' : '2023-06-13',
                'fechaEntrega' : '2023-06-13',
                'idEmpleado' : self.empleado.pk,
                'idMetodo' : self.metodo_pago2.pk,
                'idConsulta' : 0,
                'montoEfectivo' : 100,
                'numeroTarjeta' : None,
                'estado' : 'Pagada',
                'activa' : 1,
                'total' : 99,
                'subtotal' : 110,
                'descuento' : 11,
                'imp' : 10,
                'idDescuento' : self.descuento.pk,
                'cambio' : 1,
                'medicamentos':[],
                'tratamientos':[],
                'examenes':[]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        rsp = response.json()
        message = rsp['message']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Registro Exitoso.')
        self.assertTrue(Recaudo.objects.filter(idPaciente__documento='8901220004753').exists())

    def test_post_recaudo_invalid_estado(self):
        data = {
                'correlativo' : self.correlativo.pk,
                'idPaciente' : self.paciente.pk,
                'fechaActual' : '2023-06-13',
                'fechaEntrega' : '2023-06-13',
                'idEmpleado' : self.empleado.pk,
                'idMetodo' : self.metodo_pago2.pk,
                'idConsulta' : self.consulta.pk,
                'montoEfectivo' : 100,
                'numeroTarjeta' : None,
                'estado' : None,
                'activa' : 1,
                'total' : 99,
                'subtotal' : 110,
                'descuento' : 11,
                'imp' : 10,
                'idDescuento' : self.descuento.pk,
                'cambio' : 1,
                'medicamentos':[],
                'tratamientos':[],
                'examenes':[]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        rsp = response.json()
        message = rsp['message']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Registro Exitoso.')
        self.assertTrue(Recaudo.objects.filter(idPaciente__documento='8901220004753').exists())

    def test_post_recaudo_invalid_correlativo(self):
        data = {
                'correlativo' : 0,
                'idPaciente' : self.paciente.pk,
                'fechaActual' : '2023-06-13',
                'fechaEntrega' : '2023-06-13',
                'idEmpleado' : self.empleado.pk,
                'idMetodo' : self.metodo_pago2.pk,
                'idConsulta' : self.consulta.pk,
                'montoEfectivo' : 100,
                'numeroTarjeta' : None,
                'estado' : 'Pagada',
                'activa' : 1,
                'total' : 99,
                'subtotal' : 110,
                'descuento' : 11,
                'imp' : 10,
                'idDescuento' : self.descuento.pk,
                'cambio' : 1,
                'medicamentos':[],
                'tratamientos':[],
                'examenes':[]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        rsp = response.json()
        message = rsp['message']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Registro Exitoso.')
        self.assertTrue(Recaudo.objects.filter(idPaciente__documento='8901220004753').exists())


    def test_delete_recaudo(self):
        data = {
                'correlativo' : self.correlativo.pk,
                'idPaciente' : self.paciente.pk,
                'fechaActual' : '2023-06-13',
                'fechaEntrega' : '2023-06-13',
                'idEmpleado' : self.empleado.pk,
                'idMetodo' : self.metodo_pago2.pk,
                'idConsulta' : self.consulta.pk,
                'montoEfectivo' : 100,
                'numeroTarjeta' : None,
                'estado' : 'Pagada',
                'activa' : 1,
                'total' : 99,
                'subtotal' : 110,
                'descuento' : 11,
                'imp' : 10,
                'idDescuento' : self.descuento.pk,
                'cambio' : 1,
                'medicamentos':[],
                'tratamientos':[],
                'examenes':[]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        recaudo = Recaudo.objects.filter(idPaciente__documento='8901220004753').last()

        delete_url = reverse('recaudo_process_id', args=[recaudo.id])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(recaudo.DoesNotExist):
            recaudo.refresh_from_db()

    def test_delete_recaudo_invalid(self):
        data = {
                'correlativo' : self.correlativo.pk,
                'idPaciente' : self.paciente.pk,
                'fechaActual' : '2023-06-13',
                'fechaEntrega' : '2023-06-13',
                'idEmpleado' : self.empleado.pk,
                'idMetodo' : self.metodo_pago2.pk,
                'idConsulta' : self.consulta.pk,
                'montoEfectivo' : 100,
                'numeroTarjeta' : None,
                'estado' : 'Pagada',
                'activa' : 1,
                'total' : 99,
                'subtotal' : 110,
                'descuento' : 11,
                'imp' : 10,
                'idDescuento' : self.descuento.pk,
                'cambio' : 1,
                'medicamentos':[],
                'tratamientos':[],
                'examenes':[]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        recaudo = Recaudo.objects.filter(idPaciente__documento='8901220004753').last()

        delete_url = reverse('recaudo_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(recaudo.DoesNotExist):
            recaudo.refresh_from_db()