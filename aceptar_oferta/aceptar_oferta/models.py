from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

    @staticmethod
    def generate_clientes():
        if not Cliente.objects.exists():
            Cliente.objects.create(nombre="Andrés", correo="andresserranoconti@hotmail.com", telefono="3052312342")
            Cliente.objects.create(nombre="María", correo="maria@gmail.com", telefono="1234567890")
            Cliente.objects.create(nombre="Carlos", correo="carlos@hotmail.com", telefono="9876543210")
            Cliente.objects.create(nombre="Sofía", correo="sofia@yahoo.com", telefono="1357924680")
            Cliente.objects.create(nombre="Juan", correo="juan@outlook.com", telefono="2468135790")

class Oferta(models.Model):
    ESTADO_CHOICES = [
        ('aceptado', 'Aceptado'),
        ('noAceptado', 'No Aceptado'),
    ]
    
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='noAceptado')

    def __str__(self):
        return self.nombre
    def aceptarOferta(self):
        self.estado = 'aceptado'
        self.save()
