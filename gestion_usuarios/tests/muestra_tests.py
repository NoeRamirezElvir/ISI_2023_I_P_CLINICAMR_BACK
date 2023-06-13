from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import *
import json

class MuestraTests(TestCase):
    def setUp(self):
        self.url = reverse('muestra_list')
        self.url_paciente = reverse('paciente_list')
        self.documento = TipoDocumentos.objects.create(id=1, nombre='DNI',longitud=13)
        self.tipo = TipoMuestra.objects.create(nombre='Tipo Muestra 1', 
                                                            metodoConservacion='Conservación 1'
                                                            )
        
    def test_get_muestra(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        muestra = response.json()
        self.assertEqual(len(muestra), 2)

    def test_post_paciente(self):
        data_paciente = {
            'nombre': 'nombre',
            'apellido': 'Apellido',
            'fechaNacimiento': '1995-01-01',
            'idTipoDocumento': self.documento.pk,
            'telefono': '98890033',
            'documento': '0801200200482',
            'correo': 'nuevo_paciente@example.com',
            'direccion': '123 col calpules'
        }
        self.client.post(self.url_paciente, json.dumps(data_paciente), content_type='application/json')
        paciente = Paciente.objects.get(documento='0801200200482')

        data_muestra = {
                        'idPaciente': paciente.pk, 
                        'idTipoMuestra': self.tipo.pk,
                        'fecha': '2023-06-13'
                     }
        response = self.client.post(self.url, json.dumps(data_muestra), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})

    def test_delete_muestra(self):
        data_paciente = {
            'nombre': 'nombre',
            'apellido': 'Apellido',
            'fechaNacimiento': '1995-01-01',
            'idTipoDocumento': self.documento.pk,
            'telefono': '98890033',
            'documento': '0801200200482',
            'correo': 'nuevo_paciente@example.com',
            'direccion': '123 col calpules'
        }
        self.client.post(self.url_paciente, json.dumps(data_paciente), content_type='application/json')
        paciente = Paciente.objects.get(documento='0801200200482')

        data_muestra = {
                        'idPaciente': paciente.pk, 
                        'idTipoMuestra': self.tipo.pk,
                        'fecha': '2023-06-13'
                     }
        response = self.client.post(self.url, json.dumps(data_muestra), content_type='application/json')
        muestra = Muestra.objects.latest('id')
        delete_url = reverse('muestra_process_id', args=[muestra.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Muestra.DoesNotExist):
            muestra.refresh_from_db()

    def test_delete_muestra_invalid(self):
        data_paciente = {
            'nombre': 'nombre',
            'apellido': 'Apellido',
            'fechaNacimiento': '1995-01-01',
            'idTipoDocumento': self.documento.pk,
            'telefono': '98890033',
            'documento': '0801200200482',
            'correo': 'nuevo_paciente@example.com',
            'direccion': '123 col calpules'
        }
        self.client.post(self.url_paciente, json.dumps(data_paciente), content_type='application/json')
        paciente = Paciente.objects.get(documento='0801200200482')

        data_muestra = {
                        'idPaciente': paciente.pk, 
                        'idTipoMuestra': self.tipo.pk,
                        'fecha': '2023-06-13'
                     }
        response = self.client.post(self.url, json.dumps(data_muestra), content_type='application/json')
        muestra = Muestra.objects.latest('id')
        delete_url = reverse('muestra_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Muestra.DoesNotExist):
            muestra.refresh_from_db()