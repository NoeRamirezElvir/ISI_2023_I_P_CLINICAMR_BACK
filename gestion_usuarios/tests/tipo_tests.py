from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Tipo, Subtipo, Impuesto
import json

class TipoTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Subtipo.objects.create(nombre='medicamento', activo=1)
        Subtipo.objects.create(nombre='tratamiento', activo=1)
        Subtipo.objects.create(nombre='examen', activo=1)
        Subtipo.objects.create(nombre='consulta', activo=1)
        Subtipo.objects.create(nombre='otros', activo=1)
        Impuesto.objects.create(nombre='ISV15%', valor=0.15)

    def setUp(self):
        self.url = reverse('tipo_list')

    def test_get_tipos(self):
        tipo1 = Tipo.objects.create(idsubtipo=Subtipo.objects.get(id=5), nombre='Tipo 1', descripcion='Descripción 1')
        tipo2 = Tipo.objects.create(idsubtipo=Subtipo.objects.get(id=5), nombre='Tipo 2', descripcion='Descripción 2')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        tipos = response.json()
        self.assertEqual(len(tipos), 2) 

    def test_post_tipo_valid_data(self):
        subtipo = Subtipo.objects.get(id=5)

        data = {
            'idsubtipo': subtipo.pk,
            'nombre': 'Tipo de prueba',
            'descripcion': 'Descripción de prueba',
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Tipo.objects.filter(nombre=data['nombre']).exists())

    def test_post_tipo_invalid_data(self):
        subtipo = Subtipo.objects.get(id=5)

        data = {
            'idsubtipo': subtipo.pk,
            'nombre': 'Tipo con descripción demasiado larga, más de 40 caracteres',
            'descripcion': 'Descripción de prueba',
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertFalse(Tipo.objects.filter(nombre=data['nombre']).exists())

    def test_put_tipo(self):
        tipo = Tipo.objects.create(idsubtipo=Subtipo.objects.get(id=5), nombre='Tipo 1', descripcion='Descripción 1')
        
        data = {
            'idsubtipo': tipo.idsubtipo.pk,
            'nombre': 'Tipo actualizado',
            'descripcion': 'Descripción actualizada',
            'idImpuesto': 0,
            'precio':0
        }

        put_url = reverse('tipo_process_id', args=[tipo.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        tipo.refresh_from_db()
