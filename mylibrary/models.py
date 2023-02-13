import datetime
from django.db import models
from django.utils import timezone


# Create your models here.




class Book(models.Model):

    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    pub_year = models.IntegerField()
    type = models.IntegerField()
    copies = models.IntegerField()
    summary = models.TextField(max_length=800)
    wikipedia = models.TextField(max_length=150)
    isbn = models.BigIntegerField()

    class Meta:
        app_label = 'mylibrary'


class Customer(models.Model):

    name = models.CharField(max_length=40,null=True)
    city = models.CharField(max_length=40)
    age = models.IntegerField()

    class Meta:
        app_label = 'mylibrary'

class Loan(models.Model):

    cust_id = models.IntegerField()
    book = models.CharField(max_length=50)
    loandate = models.DateField(default=datetime.date.today)
    returndate = models.DateField()

    class Meta:
        app_label = 'mylibrary'

class City(models.Model):

    city_name = models.TextField()

    class Meta:
        app_label = 'mylibrary'
    





    



