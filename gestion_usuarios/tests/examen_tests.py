from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import *
import json

class ExamenTests(TestCase):
    def setUp(self):
        self.url = reverse('examen_list')
        self.impuesto = Impuesto.objects.create(nombre='ISV15%',valor=0.15)

        self.subtipo = Subtipo.objects.create(nombre='examen', activo=1)
        self.tipo = Tipo.objects.create(idsubtipo=self.subtipo, nombre='examen de sangre', descripcion='Descripcion',precio=100,idImpuesto=self.impuesto)

        self.tipoDocumento = TipoDocumentos.objects.create(id=1, nombre='DNI',longitud=13)
        self.paciente = Paciente.objects.create(nombre='paciente',
                                                apellido='prueba',
                                                fechaNacimiento='2000-11-11',
                                                correo='correo@tipo.com',
                                                telefono='99886677',
                                                direccion='123 col prueba',
                                                idTipoDocumento=self.tipoDocumento,
                                                documento='8901220004753')
        
        self.tipo_muestra = TipoMuestra.objects.create(nombre='sangre',
                                                       metodoConservacion='Conservación 1'
                                                    )
        
        self.muestra = Muestra.objects.create(idPaciente=self.paciente, 
                                              idTipoMuestra=self.tipo_muestra,
                                              fecha='2023-06-13'
                                              )
        
        self.laboratorio =Laboratorios.objects.create(nombre='Laboratorio 1', 
                                                      direccion='Dirección 1', 
                                                      telefono='99887755', 
                                                      disponibilidad=1
                                                      )
        
    def test_get_examen(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        examen = response.json()
        self.assertEqual(len(examen), 2)

    def test_post_examen(self):
        data = {'idMuestra':self.muestra.pk,
                'idTipo':self.tipo.pk,
                'idLaboratorio':self.laboratorio.pk,
                'fechaProgramada':'2023-06-15',
                'observacion':'Presentó problemas con el procedimiento'
                }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})

    def test_post_examen_invalid_observacion(self):
        data = {'idMuestra':self.muestra.pk,
                'idTipo':self.tipo.pk,
                'idLaboratorio':self.laboratorio.pk,
                'fechaProgramada':'2023-06-15',
                'observacion':'Present  abc'
                }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})

    def test_put_examen(self):
        data = {'idMuestra':self.muestra.pk,
                'idTipo':self.tipo.pk,
                'idLaboratorio':self.laboratorio.pk,
                'fechaProgramada':'2023-06-15',
                'observacion':'Presentó problemas con el procedimiento'
                }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        examen = Examen.objects.filter(idMuestra__idPaciente__documento='8901220004753').last()
        data = {
            'idMuestra':self.muestra.pk,
            'idTipo':self.tipo.pk,
            'idLaboratorio':self.laboratorio.pk,
            'fechaProgramada':'2023-06-15',
            'observacion':'observacion actualizada'
        }

        put_url = reverse('examen_process_id', args=[examen.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        examen.refresh_from_db()
        self.assertEqual(examen.observacion, 'observacion actualizada')

    def test_delete_examen(self):
        data = {'idMuestra':self.muestra.pk,
                'idTipo':self.tipo.pk,
                'idLaboratorio':self.laboratorio.pk,
                'fechaProgramada':'2023-06-15',
                'observacion':'Presentó problemas con el procedimiento'
                }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        examen = Examen.objects.filter(idMuestra__idPaciente__documento='8901220004753').last()

        delete_url = reverse('examen_process_id', args=[examen.pk]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Examen.DoesNotExist):
            examen.refresh_from_db()

    def test_delete_examen_invalid(self):
        data = {'idMuestra':self.muestra.pk,
                'idTipo':self.tipo.pk,
                'idLaboratorio':self.laboratorio.pk,
                'fechaProgramada':'2023-06-15',
                'observacion':'Presentó problemas con el procedimiento'
                }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        examen = Examen.objects.filter(idMuestra__idPaciente__documento='8901220004753').last()

        delete_url = reverse('examen_process_id', args=[100]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Examen.DoesNotExist):
            examen.refresh_from_db()
