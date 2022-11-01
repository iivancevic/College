from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Uloge(models.Model):
    ADMIN = 'ADMIN'
    STUDENT = 'STUDENT'
    PROFESOR = 'PROFESOR'
    ULOGE = [
        (ADMIN, 'Admin'),
        (STUDENT, 'Student'),
        (PROFESOR, 'Profesor'),
    ]

    uloga = models.CharField(
        max_length=8,
        choices=ULOGE,
        default=STUDENT,
    )

    def __str__(self):
        return self.uloga

class Korisnik(AbstractUser):
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    uloga = models.ForeignKey(Uloge, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return f"/students/{self.id}/"

class Predmet(models.Model):
    IZBORNI = (('Da', 'da'), ('Ne', 'ne'))
    ime = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    nositelj = models.ForeignKey(Korisnik, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.ime

    def get_absolute_url(self):
        return f"/subjects/{self.id}/"

class Upisi(models.Model):
    student = models.ForeignKey(Korisnik, on_delete=models.SET_NULL, null=True)
    predmet = models.ForeignKey(Predmet, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=64)