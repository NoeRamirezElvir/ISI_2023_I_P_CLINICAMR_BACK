from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Enfermedad, Sintoma, EnfermedadDetalle
import json

class EnfermedadTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Sintoma.objects.create(nombre='Sintoma 1', descripcion='Descripcion 1')
        Sintoma.objects.create(nombre='Sintoma 2', descripcion='Descripcion 2')

    def setUp(self):
        self.url = reverse('enfermedades_list')  # Ajusta esto según la URL de tu vista

    def test_get_enfermedades(self):
        enfermedad1 = Enfermedad.objects.create(nombre='Enfermedad 1')
        enfermedad2 = Enfermedad.objects.create(nombre='Enfermedad 2')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        enfermedades = response.json()
        self.assertEqual(len(enfermedades), 2) 

    def test_post_enfermedad_valid_data(self):
        data = {
            'nombre': 'Enfermedad de prueba',
            'idSintomas':[{
                "id":1
            },{
                "id":2
            }
            ]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Enfermedad.objects.filter(nombre=data['nombre']).exists())

    def test_post_enfermedad_invalid_data(self):
        data = {
            'nombre': 'Enfermedad  ',
            'idSintomas':[{
                "id":1
            },
            ]
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Enfermedad.objects.filter(nombre=data['nombre']).exists())


    def test_put_enfermedad(self):

        enfermedad = Enfermedad.objects.create(nombre='Enfermedad 1')
        EnfermedadDetalle.objects.create(idEnfermedad = enfermedad,idSintoma=Sintoma.objects.get(id=1))

        data = {
            'nombre': 'Enfermedad actualizada',
            'idSintomas':[{
                "id":2
            },
            ]
        }

        put_url = reverse('enfermedades_process_id', args=[enfermedad.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        enfermedad.refresh_from_db()
        self.assertEqual(enfermedad.nombre, 'Enfermedad actualizada')

    def test_delete_enfermedad(self):
        enfermedad = Enfermedad.objects.create(nombre='Enfermedad a eliminar')

        delete_url = reverse('enfermedades_process_id', args=[enfermedad.pk]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Enfermedad.DoesNotExist):
            enfermedad.refresh_from_db()

    def test_delete_enfermedad_invalid(self):
        enfermedad = Enfermedad.objects.create(nombre='Enfermedad a eliminar')

        delete_url = reverse('enfermedades_process_id', args=[100]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Enfermedad.DoesNotExist):
            enfermedad.refresh_from_db()