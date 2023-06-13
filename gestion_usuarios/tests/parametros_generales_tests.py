from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import ParametrosGenerales
import json

class ParametrosGeneralesTests(TestCase):
    def setUp(self):
        self.url = reverse('parametrosgenerales_list')
        self.parametro_post = ParametrosGenerales.objects.create(nombre='Parametro 1', descripcion='Descripción 1', valor='Valor 1')

    def test_get_parametros_generales(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        parametros_generales = response.json()
        self.assertEqual(len(parametros_generales), 2)

    def test_post_parametro_general(self):
        data = {
            'nombre': 'Parametro 2',
            'descripcion': 'Descripción 2',
            'valor': 'Valor 2'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(ParametrosGenerales.objects.filter(nombre='Parametro 2').exists())
        self.parametro_post = ParametrosGenerales.objects.filter(nombre='Parametro 2').first()

    def test_post_parametro_general_invalid_name(self):
        data = {
            'nombre': 'Parametro  2',
            'descripcion': 'Descripción 2',
            'valor': 'Valor 2'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(ParametrosGenerales.objects.filter(nombre='Parametro 2').exists())
        self.parametro_post = ParametrosGenerales.objects.filter(nombre='Parametro 2').first()

    def test_post_parametro_general_invalid_value(self):
        data = {
            'nombre': 'Parametro 2',
            'descripcion': 'Descripción 2',
            'valor': 'Valooooor'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(ParametrosGenerales.objects.filter(nombre='Parametro 2').exists())
        self.parametro_post = ParametrosGenerales.objects.filter(nombre='Parametro 2').first()

    def test_put_parametro_general(self):
        parametro = self.parametro_post
        data = {
            'nombre': 'nombre',
            'descripcion': 'Descripción Actualizada',
            'valor': 'Valor Actualizado'
        }

        put_url = reverse('parametrosgenerales_process_id', args=[parametro.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        parametro.refresh_from_db()
        self.assertEqual(parametro.nombre, 'nombre')
        self.assertEqual(parametro.descripcion, 'Descripción Actualizada')
        self.assertEqual(parametro.valor, 'Valor Actualizado')

    def test_delete_parametro_general(self):
        parametro = self.parametro_post
        delete_url = reverse('parametrosgenerales_process_id', args=[parametro.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(ParametrosGenerales.DoesNotExist):
            parametro.refresh_from_db()

    def test_delete_parametro_general_invalid(self):
        parametro = self.parametro_post
        delete_url = reverse('parametrosgenerales_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(ParametrosGenerales.DoesNotExist):
            parametro.refresh_from_db()
