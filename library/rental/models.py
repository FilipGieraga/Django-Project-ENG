from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)
    average_rating = models.FloatField()
    num_pages = models.IntegerField()
    publication_date = models.CharField(max_length=12)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Person(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Borrowed(models.Model):
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, null=True, editable=True, on_delete=models.SET_NULL)
    taken_date= models.DateField(auto_now_add=True)
    return_date= models.DateField(default=datetime.today()+timedelta(days=90))

    def __str__(self):
        return f"{self.person} borrowed {self.book}"
