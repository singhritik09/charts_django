from django.db import models

# Create your models here.

class Application(models.Model):
    APPLICATION_TYPE_CHOICES = [
        ('emergency', 'Emergency'),
        ('planned', 'Planned'),
        ('superfix', 'Superfix'),
    ]

    owner_name=models.CharField(max_length=255)
    date_of_register=models.DateField()
    application_type=models.CharField(max_length=10,choices=APPLICATION_TYPE_CHOICES)
    
    def __str__(self):
        return f'{self.owner_name} - {self.application_type}'