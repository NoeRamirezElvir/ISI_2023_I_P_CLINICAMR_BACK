from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import *
import json

class MedicamentoTests(TestCase):
    def setUp(self):
        self.url = reverse('medicamentos_list')

        self.impuesto = Impuesto.objects.create(nombre='ISV15%',valor=0.15)

        self.subtipo = Subtipo.objects.create(nombre='medicamento', activo=1)
        self.tipo = Tipo.objects.create(idsubtipo=self.subtipo, nombre='examen de sangre', descripcion='Descripcion')

        self.proveedor = Proveedor.objects.create(nombre='Carlos',
                                                telefono='22465577',
                                                correo='correo@gmail.com',
                                                direccion='123 col proveedor')
        
    def test_get_medicamento(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        medicamento = response.json()
        self.assertEqual(len(medicamento), 2)

    def test_post_medicamento(self):
        data = {
            'nombre':'acetaminofen', 
            'idTipo':self.tipo.pk, 
            'fechaRegistro':'2023-06-13',
            'activo':1,
            'stockActual':50,
            'stockMinimo':5,
            'stockMaximo':100,
            'idProveedor':self.proveedor.pk,
            'idImpuesto':self.impuesto.pk,
            'costoCompra': 25.00,
            'precioVenta': 30.00
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Medicamento.objects.filter(nombre='acetaminofen').exists())

    def test_post_medicamento_invalid_name(self):
        data = {
            'nombre':'acetami nofen', 
            'idTipo':self.tipo.pk, 
            'fechaRegistro':'2023-06-13',
            'activo':1,
            'stockActual':50,
            'stockMinimo':5,
            'stockMaximo':100,
            'idProveedor':self.proveedor.pk,
            'idImpuesto':self.impuesto.pk,
            'costoCompra': 25.00,
            'precioVenta': 30.00
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Medicamento.objects.filter(nombre='acetaminofen').exists())

    def test_post_medicamento_invalid_stock(self):
        data = {
            'nombre':'acetaminofen', 
            'idTipo':self.tipo.pk, 
            'fechaRegistro':'2023-06-13',
            'activo':1,
            'stockActual':50,
            'stockMinimo':51,
            'stockMaximo':100,
            'idProveedor':self.proveedor.pk,
            'idImpuesto':self.impuesto.pk,
            'costoCompra': 25.00,
            'precioVenta': 30.00
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Medicamento.objects.filter(nombre='acetaminofen').exists())

    def test_post_medicamento_invalid_precio(self):
        data = {
            'nombre':'acetaminofen', 
            'idTipo':self.tipo.pk, 
            'fechaRegistro':'2023-06-13',
            'activo':1,
            'stockActual':50,
            'stockMinimo':5,
            'stockMaximo':100,
            'idProveedor':self.proveedor.pk,
            'idImpuesto':self.impuesto.pk,
            'costoCompra': 45.00,
            'precioVenta': 30.00
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Medicamento.objects.filter(nombre='acetaminofen').exists())

    def test_put_medicamento(self):
        data = {
            'nombre':'acetaminofen', 
            'idTipo':self.tipo.pk, 
            'fechaRegistro':'2023-06-13',
            'activo':1,
            'stockActual':50,
            'stockMinimo':5,
            'stockMaximo':100,
            'idProveedor':self.proveedor.pk,
            'idImpuesto':self.impuesto.pk,
            'costoCompra': 25.00,
            'precioVenta': 30.00
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        medicamento = Medicamento.objects.get(nombre='acetaminofen')

        data = {
            'nombre':'acetaminofen actualizado', 
            'idTipo':self.tipo.pk, 
            'fechaRegistro':'2023-06-13',
            'activo':1,
            'stockActual':50,
            'stockMinimo':5,
            'stockMaximo':100,
            'idProveedor':self.proveedor.pk,
            'idImpuesto':self.impuesto.pk,
            'costoCompra': 25.00,
            'precioVenta': 30.00
        }

        put_url = reverse('medicamentos_process_id', args=[medicamento.id])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        medicamento.refresh_from_db()
        self.assertEqual(medicamento.nombre, 'acetaminofen actualizado')

    def test_delete_medicamento_invalid(self):
        data = {
            'nombre':'acetaminofen', 
            'idTipo':self.tipo.pk, 
            'fechaRegistro':'2023-06-13',
            'activo':1,
            'stockActual':50,
            'stockMinimo':5,
            'stockMaximo':100,
            'idProveedor':self.proveedor.pk,
            'idImpuesto':self.impuesto.pk,
            'costoCompra': 25.00,
            'precioVenta': 30.00
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        medicamento = Medicamento.objects.get(nombre='acetaminofen')

        delete_url = reverse('medicamentos_process_id', args=[medicamento.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(medicamento.DoesNotExist):
            medicamento.refresh_from_db()