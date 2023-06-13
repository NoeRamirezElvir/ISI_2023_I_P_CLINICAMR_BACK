from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import EspecialidadMedico
import json

class EspecialidadMedicoTests(TestCase):
    def setUp(self):
        self.url = reverse('especialidad_list')
        self.especialidad_post = EspecialidadMedico.objects.create(nombre='Especialidad 1', descripcion='Descripción 1')

    def test_get_especialidades(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        especialidades = response.json()
        self.assertEqual(len(especialidades), 2)

    def test_post_especialidad(self):
        data = {
            'nombre': 'Especialidad 2',
            'descripcion': 'Descripción 2'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(EspecialidadMedico.objects.filter(nombre='Especialidad 2').exists())
        self.especialidad_post = EspecialidadMedico.objects.filter(nombre='Especialidad 2').first()

    def test_post_especialidad_invalid_name(self):
        data = {
            'nombre': 'Especialidaaaad',
            'descripcion': 'Descripción 2'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(EspecialidadMedico.objects.filter(nombre='Especialidad 2').exists())
        self.especialidad_post = EspecialidadMedico.objects.filter(nombre='Especialidad 2').first()

    def test_post_especialidad_invalid_description(self):
        data = {
            'nombre': 'Especialidad',
            'descripcion': 'Descripcion de mas de cincuenta caracteres, para probar la validacion de longitud'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(EspecialidadMedico.objects.filter(nombre='Especialidad 2').exists())
        self.especialidad_post = EspecialidadMedico.objects.filter(nombre='Especialidad 2').first()

    def test_put_especialidad(self):
        especialidad = self.especialidad_post
        data = {
            'nombre': 'Especialidad Actualizada',
            'descripcion': 'Descripción Actualizada'
        }

        put_url = reverse('especialidad_process_id', args=[especialidad.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        especialidad.refresh_from_db()
        self.assertEqual(especialidad.nombre, 'Especialidad Actualizada')
        self.assertEqual(especialidad.descripcion, 'Descripción Actualizada')

    def test_delete_especialidad(self):
        especialidad = self.especialidad_post
        delete_url = reverse('especialidad_process_id', args=[especialidad.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(EspecialidadMedico.DoesNotExist):
            especialidad.refresh_from_db()

    def test_delete_especialidad_invalid(self):
        especialidad = self.especialidad_post
        delete_url = reverse('especialidad_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(EspecialidadMedico.DoesNotExist):
            especialidad.refresh_from_db()
