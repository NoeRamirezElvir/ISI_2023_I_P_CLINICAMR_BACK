from datetime import date
from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import CorrelativoSar
import json

class CorrelativoSarTests(TestCase):
    def setUp(self):
        self.url = reverse('correlativo_list')
        self.correlativo_post = CorrelativoSar.objects.create(cai=('30990398-6a82-44b5-84ca-ed13112a0ee5').strip(),
                                          rangoInicial=1,
                                          rangoFinal=100,
                                          consecutivo=1,
                                          fechaInicio = date.today(),
                                          fechaLimiteEmision='2023-06-30',
                                          )

    def test_get_correlativos_sar(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        correlativos_sar = response.json()
        self.assertEqual(len(correlativos_sar), 2)

    def test_post_correlativo_sar(self):
        data = {
            'cai': '30990398-6a82-44b5-84ca-ed13112a0ee8',
            'rangoInicial': 1000,
            'rangoFinal': 2000,
            'consecutivo':1000,
            'fechaLimiteEmision': '2023-06-30',
            'activo': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(CorrelativoSar.objects.filter(cai='30990398-6a82-44b5-84ca-ed13112a0ee8').exists())
        self.correlativo_post = CorrelativoSar.objects.filter(cai='30990398-6a82-44b5-84ca-ed13112a0ee8')

    def test_post_correlativo_sar_invalid_(self):
        data = {
            'cai': '30990398-6a82-44b5-84ca--ed13112a0ee8',
            'rangoInicial': 1,
            'rangoFinal': 200,
            'consecutivo':1,
            'fechaLimiteEmision': '2023-06-30',
            'activo': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(CorrelativoSar.objects.filter(cai='30990398-6a82-44b5-84ca-ed13112a0ee8').exists())

    def test_post_correlativo_sar_invalid_range(self):
        data = {
            'cai': '30990398-6a82-44b5-84ca-ed13112a0ee8',
            'rangoInicial': 2500,
            'rangoFinal': 2000,
            'consecutivo':1000,
            'fechaLimiteEmision': '2023-06-30',
            'activo': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(CorrelativoSar.objects.filter(cai='30990398-6a82-44b5-84ca-ed13112a0ee8').exists())

    def test_put_correlativo_sar(self):
        correlativo_sar = self.correlativo_post
        data = {
            'cai': '30990398-6a82-44b5-84ca-ed13112a0ee8',
            'rangoInicial': 1,
            'consecutivo':1,
            'rangoFinal': 300,
            'fechaLimiteEmision': '2023-07-31',
            'activo': 1
        }

        put_url = reverse('correlativo_process_id', args=[correlativo_sar.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        correlativo_sar.refresh_from_db()
        self.assertEqual(correlativo_sar.cai, '30990398-6a82-44b5-84ca-ed13112a0ee8')
        self.assertEqual(correlativo_sar.rangoInicial, 1)
        self.assertEqual(correlativo_sar.rangoFinal, 300)
        self.assertEqual(str(correlativo_sar.fechaLimiteEmision), '2023-07-31')
        self.assertEqual(str(correlativo_sar.fechaInicio), '2023-06-12')
        self.assertEqual(correlativo_sar.activo, 1)

    def test_delete_correlativo_sar(self):
            correlativo_sar = self.correlativo_post
            delete_url = reverse('correlativo_process_id', args=[correlativo_sar.pk])
            response = self.client.delete(delete_url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
            with self.assertRaises(CorrelativoSar.DoesNotExist):
                correlativo_sar.refresh_from_db()

    def test_delete_correlativo_sar_invalid(self):
            correlativo_sar = self.correlativo_post
            delete_url = reverse('correlativo_process_id', args=[100])
            response = self.client.delete(delete_url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
            with self.assertRaises(CorrelativoSar.DoesNotExist):
                correlativo_sar.refresh_from_db()
