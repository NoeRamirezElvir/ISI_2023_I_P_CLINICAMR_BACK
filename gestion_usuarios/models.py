from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
#Las llaves foraneas deben ser NULL y agregar on_delete=models.CASCADE
#Cargos de Empleados
class CargoEmpleado(models.Model):
        nombre = models.CharField(max_length=50)
        descripcion = models.CharField(max_length=50)
        activo = models.PositiveSmallIntegerField()
     
#Tipo de Documentos
class TipoDocumentos(models.Model):
        nombre = models.CharField(max_length=50)
        longitud = models.PositiveSmallIntegerField()

#Especialidades de Medicos
class EspecialidadMedico(models.Model):
        nombre = models.CharField(max_length=50)
        descripcion = models.CharField(max_length=50)

#Empleados
class Empleado(models.Model):
        nombre = models.CharField(max_length=40)
        apellidos = models.CharField(max_length=40)
        email = models.EmailField(max_length=40)
        fechaNacimiento = models.DateField()
        telefono = models.CharField(max_length=15)
        direccion = models.CharField(max_length=50)
        idTipoDocumentos = models.ForeignKey(TipoDocumentos, on_delete=models.CASCADE, null=True,blank=True)
        documento = models.CharField(max_length=20)
        idEspecialidadMedico = models.ForeignKey(EspecialidadMedico, on_delete=models.CASCADE, null=True,blank=True)
        idCargoEmpleado = models.ForeignKey(CargoEmpleado, on_delete=models.CASCADE, null=True,blank=True)
        activo = models.PositiveSmallIntegerField()

#Usuarios
class Usuario(models.Model):
        idEmpleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True,blank=True)
        nombreUsuario = models.CharField(max_length=40)
        password = models.CharField(max_length=100)
        activo = models.PositiveSmallIntegerField()
        bloqueado = models.PositiveSmallIntegerField()
        fechaCreacion = models.DateTimeField(auto_now_add=True)
        fechaModificacion = models.DateTimeField(auto_now=True)