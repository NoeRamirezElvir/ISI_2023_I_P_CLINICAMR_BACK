from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import *
import json

class TratamientoTests(TestCase):
    def setUp(self):
        self.url = reverse('tratamientos_list')
        self.subtipo = Subtipo.objects.create(nombre='tratamiento', activo=1)
        self.impuesto = Impuesto.objects.create(nombre='ISV15%',valor=0.15)
        self.tipo = Tipo.objects.create(idsubtipo=self.subtipo, nombre='tratamiento general', descripcion='Descripcion',precio=100,idImpuesto=self.impuesto)

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
        
        self.tipo = TipoMuestra.objects.create(nombre='Tipo Muestra 1',
                                               metodoConservacion='Conservación 1'
                                            )
        
    def test_get_tratamiento(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        tratamiento = response.json()
        self.assertEqual(len(tratamiento), 2)

    def test_post_tratamiento(self):
        data = {
            'idTipo': self.tipo.pk, 
            'idPaciente': self.paciente.pk,
            'fecha': '2023-06-13',
            'diasTratamiento': 16,
            'estado': 'Sin estado', 
            'pagado': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Tratamiento.objects.filter(idPaciente__documento='8901220004753').exists())

    def test_post_tratamiento_invalid(self):
        data = {
            'idTipo': self.tipo.pk, 
            'idPaciente': self.paciente.pk,
            'fecha': '2023-06-13',
            'diasTratamiento': 1,
            'estado': 'aaaa', 
            'pagado': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Tratamiento.objects.filter(idPaciente__documento='8901220004753').exists())

    def test_post_tratamiento_invalid_estado(self):
        data = {
            'idTipo': self.tipo.pk, 
            'idPaciente': self.paciente.pk,
            'fecha': '2023-06-13',
            'diasTratamiento': 1,
            'estado': 'aa  aa', 
            'pagado': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Tratamiento.objects.filter(idPaciente__documento='8901220004753').exists())

    def test_delete_tratamiento(self):
        data = {
            'idTipo': self.tipo.pk, 
            'idPaciente': self.paciente.pk,
            'fecha': '2023-06-13',
            'diasTratamiento': 16,
            'estado': 'Sin estado', 
            'pagado': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        tratamiento = Tratamiento.objects.filter(idPaciente__documento='8901220004753').last()

        delete_url = reverse('tratamientos_process_id', args=[tratamiento.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(tratamiento.DoesNotExist):
            tratamiento.refresh_from_db()

    def test_delete_tratamiento_invalid(self):
        data = {
            'idTipo': self.tipo.pk, 
            'idPaciente': self.paciente.pk,
            'fecha': '2023-06-13',
            'diasTratamiento': 16,
            'estado': 'Sin estado', 
            'pagado': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        tratamiento = Tratamiento.objects.filter(idPaciente__documento='8901220004753').last()

        delete_url = reverse('tratamientos_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(tratamiento.DoesNotExist):
            tratamiento.refresh_from_db()