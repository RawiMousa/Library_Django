from django.contrib import admin
from .models import Book,Customer,Loan,City

# Register your models here.

admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Loan)
admin.site.register(City)

