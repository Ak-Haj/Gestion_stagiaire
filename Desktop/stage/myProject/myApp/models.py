from django.db import models
from django.utils import timezone

class Stagiaire(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    universite = models.CharField(max_length=150)
    projet = models.CharField(max_length=200)
    type_stage = models.CharField(max_length=50)
    date_debut = models.DateField()
    date_fin = models.DateField()
    archive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Reunion(models.Model):
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE, related_name='reunions')
    titre = models.CharField(max_length=200)
    date = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.titre} - {self.date.strftime('%d/%m/%Y %H:%M')}"
    
    
