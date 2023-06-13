from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import *
from datetime import datetime
import json

class ConsultaTests(TestCase):
    def setUp(self):
        self.url = reverse('consultas_list')
        self.sintoma=Sintoma.objects.create(nombre='sintoma 1', descripcion='sintoma 1')
        self.enfermedad=Enfermedad.objects.create(nombre='enfermedad 1')
        EnfermedadDetalle.objects.create(idEnfermedad = self.enfermedad, idSintoma = self.sintoma)
        self.diagnostico = Diagnostico.objects.create(descripcion='diagnostico 1')
        DiagnosticoDetalle.objects.create(idDiagnostico = self.diagnostico, idEnfermedad = self.enfermedad)

        self.impuesto = Impuesto.objects.create(nombre='ISV10%', valor=0.10)
        self.subtipo = Subtipo.objects.create(nombre='consulta', activo=1)
        self.tipo = Tipo.objects.create(nombre='Consulta general',
                                        descripcion='Sin descripcion',
                                        precio = 100,
                                        idsubtipo = self.subtipo,
                                        idImpuesto = self.impuesto
                                        )
        self.documento = TipoDocumentos.objects.create(nombre='DNI',longitud='13')
        self.paciente = Paciente.objects.create(
                                                nombre='paciente',
                                                apellido='prueba',
                                                fechaNacimiento='2001-11-15',
                                                correo='paciente.prueba@correo.com',
                                                telefono=88990077,
                                                direccion='123 col prueba',
                                                idTipoDocumento=self.documento,
                                                documento='0801200200577'
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

    def test_get_consultas(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        consultas = response.json()
        self.assertEqual(len(consultas), 2)

    def test_post_consulta(self):
        data = {
            'idCita': self.cita.id,
            'idTipo': self.tipo.id,
            'recomendaciones': 'Recomendaciones',
            'informacionAdicional': 'Información adicional',
            'pagado': 0,
            'idDiagnostico':[{
                "id":self.diagnostico.pk
            }]
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Consulta.objects.filter(recomendaciones='Recomendaciones').exists())

    def test_post_consulta_invalid_recomendaciones(self):
        data = {
            'idCita': self.cita.id,
            'idTipo': self.tipo.id,
            'recomendaciones': 'aaaaaaaaaa',
            'informacionAdicional': 'Información adicional',
            'pagado': 0,
            'idDiagnostico':[{
                "id":self.diagnostico.pk
            }]
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})

    def test_post_consulta_invalid_informacion(self):
        data = {
            'idCita': self.cita.id,
            'idTipo': self.tipo.id,
            'recomendaciones': 'abc  abc',
            'informacionAdicional': 'Informacioon adicional',
            'pagado': 0,
            'idDiagnostico':[{
                "id":self.diagnostico.pk
            }]
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})

    def test_put_consulta(self):
        consulta = Consulta.objects.create(idCita=self.cita, idTipo=self.tipo, recomendaciones='Recomendaciones',
                                           informacionAdicional='Información adicional', pagado=0)
        data = {
            'idCita': self.cita.id,
            'idTipo': self.tipo.id,
            'recomendaciones': 'Recomendaciones actualizadas',
            'informacionAdicional': 'Información adicional actualizada',
            'pagado': 0,
            'idDiagnostico':[{
                "id":self.diagnostico.pk
            }]
        }

        put_url = reverse('consultas_process_id', args=[consulta.id])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        consulta.refresh_from_db()
        self.assertEqual(consulta.recomendaciones, 'Recomendaciones actualizadas')
        self.assertEqual(consulta.informacionAdicional, 'Información adicional actualizada')
        self.assertEqual(consulta.pagado, 0)

    def test_delete_consulta(self):
        consulta = self.consulta
        
        delete_url = reverse('consultas_process_id', args=[consulta.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Consulta.DoesNotExist):
            consulta.refresh_from_db()

    def test_delete_consulta(self):
   
        delete_url = reverse('consultas_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})

