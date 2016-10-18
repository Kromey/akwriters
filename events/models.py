from django.db import models

# Create your models here.
class Calendar(models.Model):
    name = models.CharField(max_length=30, unique=True)
    remote_id = models.CharField(max_length=60)
    css_class = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]

