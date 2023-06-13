from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import *
import json

class EmpleadoTests(TestCase):
    def setUp(self):
        self.url = reverse('empleado_list')
        self.cargo = CargoEmpleado.objects.create(nombre='Cargo 1', descripcion='Descripción 1', activo=1)
        self.tipo_documento = TipoDocumentos.objects.create(nombre='DNI', longitud=13)
        self.especialidad = EspecialidadMedico.objects.create(nombre='Medico general', descripcion='Descripción 1')
        self.empleado = Empleado.objects.create(nombre='empleado', apellidos='prueba',
                                                fechaNacimiento='2000-11-11',
                                                email='empleado@example.com',
                                                telefono='99887700',
                                                direccion='123 col prueba',
                                                idTipoDocumentos=self.tipo_documento,
                                                documento='0801200200482',
                                                idEspecialidadMedico=self.especialidad,
                                                idCargoEmpleado=self.cargo,
                                                activo=1)
        
    def test_get_empleado(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        empleados = response.json()
        self.assertEqual(len(empleados), 2)

    def test_post_empleado(self):
        data = {
            'nombre':'Empleado', 
            'apellidos':'Prueba',
            'fechaNacimiento':'2000-11-11',
            'email':'empleado@example.com',
            'telefono':'99887700',
            'direccion':'123 col prueba',
            'idTipoDocumentos':self.tipo_documento.pk,
            'documento':'0801200200582',
            'idEspecialidadMedico':self.especialidad.pk,
            'idCargoEmpleado':self.cargo.pk,
            'activo':1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Empleado.objects.filter(nombre='empleado').exists())
        self.assertTrue(Empleado.objects.filter(apellidos='prueba').exists())

    def test_post_empleado_invalid_name(self):
        data = {
            'nombre':'Empleadooo', 
            'apellidos':'Prueba',
            'fechaNacimiento':'2000-11-11',
            'email':'empleado@example.com',
            'telefono':'99887700',
            'direccion':'123 col prueba',
            'idTipoDocumentos':self.tipo_documento.pk,
            'documento':'0801200200582',
            'idEspecialidadMedico':self.especialidad.pk,
            'idCargoEmpleado':self.cargo.pk,
            'activo':1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Empleado.objects.filter(nombre='empleado').exists())
        self.assertTrue(Empleado.objects.filter(apellidos='prueba').exists())

    def test_post_empleado_invalid_documento(self):
        data = {
            'nombre':'Empleado', 
            'apellidos':'Prueba',
            'fechaNacimiento':'2000-11-11',
            'email':'empleado@example.com',
            'telefono':'99887700',
            'direccion':'123 col prueba',
            'idTipoDocumentos':self.tipo_documento.pk,
            'documento':'0801200200482',
            'idEspecialidadMedico':self.especialidad.pk,
            'idCargoEmpleado':self.cargo.pk,
            'activo':1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Empleado.objects.filter(nombre='empleado').exists())
        self.assertTrue(Empleado.objects.filter(apellidos='prueba').exists())

    def test_put_empleado(self):
        empleado = Empleado.objects.create(nombre='empleado actualizar', apellidos='prueba actualizar',
                                                fechaNacimiento='2000-11-11',
                                                email='empleado@example.com',
                                                telefono='99887700',
                                                direccion='123 col prueba',
                                                idTipoDocumentos=self.tipo_documento,
                                                documento='0801200200482',
                                                idEspecialidadMedico=self.especialidad,
                                                idCargoEmpleado=self.cargo,
                                                activo=1)
        data = {
            'nombre':'empleado actualizar', 
            'apellidos':'prueba actualizar',
            'fechaNacimiento':'2000-11-11',
            'email':'empleado@example.com',
            'telefono':'33445677',
            'direccion':'123 col prueba actualizada',
            'idTipoDocumentos':self.tipo_documento.pk,
            'documento':'0801200200482',
            'idEspecialidadMedico':self.especialidad.pk,
            'idCargoEmpleado':self.cargo.pk,
            'activo':1
        }

        put_url = reverse('empleado_process_id', args=[empleado.id])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'El actualización fue exitosa.'})

        empleado.refresh_from_db()
        self.assertEqual(empleado.telefono, '33445677')

    def test_delete_empleado(self):
        empleado = self.empleado
        delete_url = reverse('empleado_process_id', args=[empleado.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(empleado.DoesNotExist):
            empleado.refresh_from_db()

    def test_delete_empleado_invalid(self):
        empleado = self.empleado
        delete_url = reverse('empleado_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(empleado.DoesNotExist):
            empleado.refresh_from_db()