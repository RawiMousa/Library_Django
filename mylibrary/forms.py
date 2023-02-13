from django import forms
from django.utils import timezone
import datetime
from django.core import validators
from django.contrib.auth.models import User
from .models import Book ,Customer , Loan , City
from django.forms import ValidationError 
from django.contrib.auth.forms import UserCreationForm
import re
from datetime import date , timedelta
from django.shortcuts import get_object_or_404
from dal import autocomplete


class BookSelectForm(forms.Form):

    book = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        super(BookSelectForm, self).__init__(*args, **kwargs)
        self.fields['book'].choices = [(book.pk, f"{book.name} (Available copies: {book.copies})") for book in Book.objects.all()]
        

# class BookSelectForm(forms.Form):

#     book = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control searchable-field'}))
#     book_hidden = forms.CharField(widget=forms.HiddenInput(), required=False)

#     def __init__(self, *args, **kwargs):
#         super(BookSelectForm, self).__init__(*args, **kwargs)
#         self.fields['book'].widget.attrs['id'] = 'id_book'
#         self.fields['book_hidden'].widget.attrs['id'] = 'id_book_hidden'




class CustomUserCreationForm(UserCreationForm): 

    username = forms.CharField(label='username', min_length=5, max_length=30,widget=forms.TextInput({'placeholder':"""Username"""}), help_text="""Username should contain 8-30 Characters, 
    English letters and Numbers only """)

    email = forms.CharField(label='email',widget=forms.TextInput({'placeholder':"""Email"""}), help_text="""Make sure the e-mail is valid.""") 

    password1 = forms.CharField(label='password1', widget=forms.PasswordInput({'placeholder':"""Password"""}), 
help_text="""*Password cannot be too similar to your other personal information.
*Password must contain at least 8 characters.
*Password cannot be a commonly used password.
*Password cannot be entirely numeric.""") 
     
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput({'placeholder':"""Confirm password"""}), help_text='Type your password again') 

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') 
  
    def clean(self):

        super(CustomUserCreationForm, self).clean()

        username = self.cleaned_data.get('username')
        username = str(username)

        new = User.objects.filter(username=username) 

        pat = re.compile(r"[A-Za-z-0-9- ]+") # the name pattern (To make sure it is valid)

        if new.count():  
            self._errors['username'] = self.error_class([
                'username already exists'])
        elif not re.fullmatch(pat, username):
            self._errors['username'] = self.error_class([
                'username should contain 5-30 english letters and numbers ONLY'])
        elif  len(username) < 8 or len(username) > 30:
            self._errors['username'] = self.error_class([
                'Name should contain 5-30 english letters and numbers ONLY']) 
  
        email = self.cleaned_data.get('email') 
        # print(email)
        email = str(email) 
        new = User.objects.filter(email = email) 

        pat = re.compile(r"[A-Za-z-0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$") 

        if not re.fullmatch(pat,email):
            self._errors['email'] = self.error_class([
                'Invalid email'])            
        elif new.count():  
            self._errors['email'] = self.error_class([
                'email already exists'])

        password1 = self.cleaned_data.get('password1')  
        password2 = self.cleaned_data.get('password2')

        password1 = str(password1)
        password2 = str(password2)

        pat = re.compile(r"[a-zA-Z0-9]+$") 

        if not re.fullmatch(pat, password1):
            self._errors['password1'] = self.error_class([
                'password should contain 8-30 english letters and numbers ONLY'])
        elif  len(password1) < 8 or len(password1) > 30:
            self._errors['password1'] = self.error_class([
                'password should contain 8-30 english letters and numbers ONLY']) 
        elif re.search(username, password1, re.IGNORECASE) or re.search(email, password1, re.IGNORECASE):
            self._errors['password1'] = self.error_class([
                'Password cannot be similar to your personal information (email,username)'])   
        elif password2 != password1: 
                print(False) 
                self._errors['password2'] = self.error_class([
                'Passowrd confirmation does not match the given passsword'])
        return
  

class NewBookForm(forms.ModelForm):

    name = forms.CharField(max_length=50,widget= forms.TextInput
                           (attrs={'placeholder':"""Book's name""", 'class':'custom-class'}),help_text='Name should contain 5-30 english letters and numbers ONLY')
    author = forms.CharField(max_length=50,widget= forms.TextInput
                           (attrs={'placeholder':"""Author's name"""}), help_text='Author should contain 5-30 english letters ONLY')
    pub_year = forms.IntegerField(widget= forms.NumberInput
                           ({'placeholder':"""Published year"""}),help_text='Year should be 1800-Current year')
    type = forms.IntegerField(widget= forms.NumberInput
                           ({'placeholder':"""Type 1/2/3"""}),help_text='Book type should 1,2 or 3 ONLY')
    copies = forms.IntegerField(widget= forms.NumberInput
                           ({'placeholder':"""Total copies"""}),help_text='Copies should be between 1-100')
    summary = forms.CharField(widget=forms.Textarea(attrs={'rows' : 10 , 'cols':40}),help_text='Summary should be in English ONLY, and a minimum of 100 Characters')

    wikipedia = forms.CharField(widget=forms.Textarea(attrs={'rows' : 1 , 'cols':65}),help_text='Provide a correct Wikipedia link for further information about the book')

    isbn = forms.CharField(max_length=50,widget= forms.NumberInput
                           (attrs={'placeholder':"""ISBN Number"""}), help_text='The International Standard Book Number')


    class Meta:
        model = Book
        fields = '__all__'
        # fields = ['name','author','pub_year','type','copies','summary','wikipedia']

    def clean(self):
 
        super(NewBookForm, self).clean()

        isbn = self.cleaned_data.get('isbn')
        isbn = str(isbn)

        new = Book.objects.filter(isbn=isbn)

        if new.count():  
            self._errors['isbn'] = self.error_class([
                'Book is already registered'])
         
        name = self.cleaned_data.get('name')  #Validating the name
        name = str(name)

        pat = re.compile(r"[A-Za-z-0-9- ]+") # the name pattern (To make sure it is valid)
        if not re.fullmatch(pat, name):
            self._errors['name'] = self.error_class([
                'Name should contain 5-30 english letters and numbers ONLY'])
        elif  len(name) < 4 or len(name) > 30:
            self._errors['name'] = self.error_class([
                'Name should contain 5-30 english letters and numbers ONLY'])

        author = self.cleaned_data.get('author')  #Validating the author 
        author = str(author)


        pat = re.compile(r"[A-Za-z- ]+") # the name pattern (To make sure it is valid)
        if not re.fullmatch(pat, author):
            self._errors['author'] = self.error_class([
                'Author should contain 5-30 english letters ONLY'])
        elif  len(author) < 4 or len(author) > 30:
            self._errors['author'] = self.error_class([
                'Author should contain 5-30 english letters ONLY'])   


        pub_year = self.cleaned_data.get('pub_year')  #Validating the year
        
        current_year = date.today()   # Using the class date to keep up with the current year
        current_year = current_year.year

        if  pub_year < 1800 or pub_year > current_year:
            self._errors['pub_year'] = self.error_class([
                'Year should be 1800-Current year'])   

        type = self.cleaned_data.get('type')  #Validating the type 

        if type != 1 and type !=2 and type !=3:
            self._errors['type'] = self.error_class([
                'Book type should 1,2 or 3 ONLY'])

        copies = self.cleaned_data.get('copies') #Validating the copies

        if not 0 < copies < 101 :
            self._errors['copies'] = self.error_class([
                'Copies should be between 1-100'])
 
        summary = self.cleaned_data.get('summary') #Validating the summary
        summary = str(summary)
        
        if len(summary) < 100 :
            self._errors['summary'] = self.error_class([
                'Summary is too short, length should be at least 100 characters'])

        wikipedia = self.cleaned_data.get('wikipedia')
        wikipedia = str(wikipedia)

        if len(wikipedia) < 30 : 
            self._errors['wikipedia'] = self.error_class([
                'Invalid wikipedia link'
            ])
     

class NewCustomerForm(forms.ModelForm):

    # all_cities = City.objects.all().values()
    # cities = []
    # for i in range(len(all_cities)):
    #     city = all_cities[i]
    #     details_lst = []
    #     key_value = ()
    #     for detail in city.values():
    #         details_lst.append(detail)
    #         continue
    #     key_value = (details_lst[0],details_lst[1])
    #     cities.append(key_value)

    name = forms.CharField(max_length=40,widget=forms.TextInput({'placeholder':"""Name"""}),help_text='Name should be in English ONLY (spaces can be used),5-30 characters')
    # city = forms.ChoiceField()
    city = forms.CharField(max_length=100,widget=forms.TextInput({'placeholder':"""City""" , 'id': 'id_city'}),help_text='City should be in English ONLY')

    age = forms.IntegerField(widget=forms.TextInput({'placeholder':"""Age"""}),help_text='Age should be between 12-120')

    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cities = City.objects.values_list('city_name', flat=True)
        self.fields['city'].choices = [(city, city) for city in cities]

    def clean(self):

        super(NewCustomerForm, self).clean()

        name = self.cleaned_data.get('name')  #Validating the author 
        name = str(name)

        pat = re.compile(r"[A-Za-z- ]+") # the name pattern (To make sure it is valid)

        if not re.fullmatch(pat, name):
            self._errors['name'] = self.error_class([
                'Name should contain 5-30 english letters ONLY'])
        elif  len(name) < 6 or len(name) > 30:
            self._errors['name'] = self.error_class([
                'Name should contain 5-15 english letters ONLY'])

        city = self.cleaned_data.get('city')
        city = str(city)

        if not City.objects.filter(city_name__iexact=city).exists():
            self._errors['city'] = self.error_class([
                'City does not exist'])

        elif  len(city) < 5 or len(city) > 30:
            self._errors['city'] = self.error_class([
                'City should contain 5-15 english letters ONLY'])

        age = self.cleaned_data.get('age')  #Validating the age

        if age < 12 or age >120 :
            self._errors['age'] = self.error_class([
                'Age should be between 12-120'])


class NewLoanForm(forms.ModelForm):

    all_books = Book.objects.all().values()
    books = []
    for i in range(len(all_books)):
        single_book = all_books[i]
        details_lst = []
        key_value = ()
        for detail in single_book.values():
            details_lst.append(detail)
        key_value = (details_lst[0],details_lst[1])
        books.append(key_value)        

    book = forms.ChoiceField(choices=books)

    cust_id = forms.ChoiceField(widget=forms.Select(attrs={}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customers = Customer.objects.all()
        choices = [(c.pk, f"{c.pk} - {c.name}") for c in customers]
        self.fields['cust_id'].choices = choices

 
    class Meta:

        model = Loan
        fields = ['cust_id']
        
    def clean(self):

        super(NewLoanForm, self).clean()

        """ 1- Making sure the ID exits in the DB """
        cust_id = self.cleaned_data.get('cust_id')  # Validating  Customer ID
        cust_id = int(cust_id)

        """ 2- Making sure the Customer requesting a loan, does not have any late loans. """
        all_loans = Loan.objects.all().values()

        for i in range(len(all_loans)):
            single_loan = all_loans[i]
            value_lst = []
            for value in single_loan.values():
                value_lst.append(value)
            print(value_lst[1])
            if cust_id == value_lst[1]:
                if value_lst[4] < date.today():
                    self._errors['cust_id'] = self.error_class([
                'This client has an on going late loan thus cannot loan a book until late loan is deleted'])
                    break
        
        """ 4- Making sure there are available copies """
        books = Book.objects.all().values()

        book = self.cleaned_data.get('book')
        book = int(book)

        for i in range(len(books)):
            single_book = books[i]
            details_lst = []
            for detail in single_book.values():
                details_lst.append(detail)
                continue

            if book == int(details_lst[0]):
                if details_lst[5] == 0:
                    self._errors['book'] = self.error_class([
                'Unfortunately there are no available copies of the selected book '])
                    
                """ 5- Modifing the return date according to the book type. """
        
                if int(details_lst[4]) == 1:
                    returndate = date.today() + \
                    timedelta(days=10)
                    
                elif int(details_lst[4]) == 2:
                    returndate = date.today() + \
                    timedelta(days=5)
                    
                elif int(details_lst[4]) == 3:
                    returndate = date.today() + \
                    timedelta(days=2)








        


        
        




