from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import *
import json

class UsuariosTests(TestCase):
    def setUp(self):
        self.url = reverse('usuario_list')
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

    def test_get_usuario(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        usuario = response.json()
        self.assertEqual(len(usuario), 2)

    def test_post_usuario(self):
        data = {
            'idEmpleado': self.empleado.pk, 
            'nombreUsuario': 'usuario.prueba',
            'password': 'Contra1!',
            'passwordc': 'Contra1!',
            'activo': 1, 
            'bloqueado': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Usuario.objects.filter(nombreUsuario='usuario.prueba').exists())
    
    def test_post_usuario_invalid_user(self):
        data = {
            'idEmpleado': self.empleado.pk, 
            'nombreUsuario': 'usuario  prueba',
            'password': 'Contra1!',
            'passwordc': 'Contra2!',
            'activo': 1, 
            'bloqueado': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Usuario.objects.filter(nombreUsuario='usuario.prueba').exists())


    def test_post_usuario_invalid_password(self):
        data = {
            'idEmpleado': self.empleado.pk, 
            'nombreUsuario': 'usuario.prueba',
            'password': 'Contra1!',
            'passwordc': 'Contra2!',
            'activo': 1, 
            'bloqueado': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Usuario.objects.filter(nombreUsuario='usuario.prueba').exists())


    def test_put_usuario(self):
        data = {
            'idEmpleado': self.empleado.pk, 
            'nombreUsuario': 'usuario.prueba',
            'password': 'Contra1!',
            'passwordc': 'Contra1!',
            'activo': 1, 
            'bloqueado': 0
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        usuario = Usuario.objects.get(nombreUsuario='usuario.prueba')

        data = {
            'idEmpleado': self.empleado.pk, 
            'nombreUsuario': 'usuario.actualizado',
            'password': 'Contra1!',
            'passwordc': 'Contra1!',
            'activo': 1, 
            'bloqueado': 0
        }

        put_url = reverse('usuario_process_id', args=[usuario.id])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        usuario.refresh_from_db()
        self.assertEqual(usuario.nombreUsuario, 'usuario.actualizado')

    def test_delete_usuario(self):
        data = {
            'idEmpleado': self.empleado.pk, 
            'nombreUsuario': 'usuario.prueba',
            'password': 'Contra1!',
            'passwordc': 'Contra1!',
            'activo': 1, 
            'bloqueado': 0
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        usuario = Usuario.objects.get(nombreUsuario='usuario.prueba')

        delete_url = reverse('usuario_process_id', args=[usuario.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(usuario.DoesNotExist):
            usuario.refresh_from_db()

    def test_delete_usuario_invalid(self):
        data = {
            'idEmpleado': self.empleado.pk, 
            'nombreUsuario': 'usuario.prueba',
            'password': 'Contra1!',
            'passwordc': 'Contra1!',
            'activo': 1, 
            'bloqueado': 0
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        usuario = Usuario.objects.get(nombreUsuario='usuario.prueba')

        delete_url = reverse('usuario_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(usuario.DoesNotExist):
            usuario.refresh_from_db()