from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Paciente, TipoDocumentos
from gestion_usuarios.views.Paciente_views import PacienteViews
from datetime import date
import json

class PacienteTests(TestCase):
    def setUp(self):
        self.url = reverse('paciente_list')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        TipoDocumentos.objects.create(id=1, nombre='DNI',longitud=13)

    def test_post_paciente(self):
        data = {
            'nombre': 'Nuevo Paciente',
            'apellido': 'Apellido',
            'fechaNacimiento': '1995-01-01',
            'idTipoDocumento': 1,
            'telefono': '98890033',
            'documento': '0801200200482',
            'correo': 'nuevo_paciente@example.com',
            'direccion': '123 col calpules'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})

        self.assertTrue(Paciente.objects.filter(nombre='Nuevo Paciente').exists())

        paciente = Paciente.objects.get(nombre='Nuevo Paciente')
        self.assertEqual(paciente.apellido, 'Apellido')
        self.assertEqual(paciente.fechaNacimiento, date(1995, 1, 1))
        self.assertEqual(paciente.idTipoDocumento, TipoDocumentos.objects.get(id=1))  
        self.assertEqual(paciente.telefono, '98890033')
        self.assertEqual(paciente.documento, '0801200200482')
        self.assertEqual(paciente.correo, 'nuevo_paciente@example.com')
        self.assertEqual(paciente.direccion, '123 col calpules')

    def test_get_pacientes(self):
            Paciente.objects.create(nombre='Paciente 1', apellido='Apellido 1', fechaNacimiento=date(1990, 1, 1),
                                    idTipoDocumento=TipoDocumentos.objects.get(id=1),
                                    telefono='98890033', documento='0801200200482', correo='correo1@example.com',
                                    direccion='123 col calpules 1')
            Paciente.objects.create(nombre='Paciente 2', apellido='Apellido 2', fechaNacimiento=date(1995, 1, 1),
                                    idTipoDocumento=TipoDocumentos.objects.get(id=1),
                                    telefono='987654321', documento='0801200200482', correo='correo2@example.com',
                                    direccion='123 col calpules 2')

            response = self.client.get(self.url)

            self.assertEqual(response.status_code, 200)
            pacientes = response.json()
            self.assertEqual(len(pacientes), 2)  

    def test_put_paciente(self):
        paciente = Paciente.objects.create(nombre='Paciente 1', apellido='Apellido 1', fechaNacimiento=date(1990, 1, 1),
                                            idTipoDocumento=TipoDocumentos.objects.get(id=1),
                                            telefono='98890033', documento='0801200200482', correo='correo1@example.com',
                                            direccion='123 col calpules 1')

        data = {
            'nombre': 'Paciente actualizado',
            'apellido': 'Apellido actualizado',
            'fechaNacimiento': '2000-01-01',
            'idTipoDocumento': paciente.idTipoDocumento.pk,
            'telefono': '987654321',
            'documento': '0801200200482',
            'correo': 'correo2@example.com',
            'direccion': '123 col calpules 2'
        }


        put_url = reverse('paciente_process_id', args=[paciente.pk])  
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'El actualización fue exitosa.'})


        paciente.refresh_from_db()
        self.assertEqual(paciente.nombre, 'Paciente actualizado')
        self.assertEqual(paciente.apellido, 'Apellido actualizado')
        self.assertEqual(paciente.fechaNacimiento, date(2000, 1, 1))
        self.assertEqual(paciente.telefono, '987654321')
        self.assertEqual(paciente.documento, '0801200200482')
        self.assertEqual(paciente.correo, 'correo2@example.com')
        self.assertEqual(paciente.direccion, '123 col calpules 2')

    def test_delete_paciente(self):
        paciente = Paciente.objects.create(nombre='Paciente 1', apellido='Apellido 1', fechaNacimiento=date(1990, 1, 1),
                                idTipoDocumento=TipoDocumentos.objects.get(id=1),
                                telefono='98890033', documento='0801200200482', correo='correo1@example.com',
                                direccion='123 col calpules 1')

        delete_url = reverse('paciente_process_id', args=[paciente.pk]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Paciente.DoesNotExist):
            paciente.refresh_from_db()

    def test_delete_paciente_invalid(self):
        paciente = Paciente.objects.create(nombre='Paciente 1', apellido='Apellido 1', fechaNacimiento=date(1990, 1, 1),
                                idTipoDocumento=TipoDocumentos.objects.get(id=1),
                                telefono='98890033', documento='0801200200482', correo='correo1@example.com',
                                direccion='123 col calpules 1')

        delete_url = reverse('paciente_process_id', args=[100]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Paciente.DoesNotExist):
            paciente.refresh_from_db()