from django.shortcuts import render ,get_object_or_404,redirect
from django.http import HttpResponse,Http404 ,HttpResponseRedirect ,JsonResponse 
from django.template import loader , RequestContext
from django.urls import reverse
from django.views import generic
from django.contrib import auth ,messages
from .forms import NewBookForm , NewCustomerForm ,NewLoanForm ,CustomUserCreationForm , BookSelectForm
from .models import Book,Customer,Loan,City
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout 
from datetime import date , timedelta
from django.contrib.auth.forms import UserCreationForm 
import json
from django.contrib.auth.models import User
import logging
from django.core import serializers


logger = logging.getLogger(__name__)

syslogHandler = logging.StreamHandler()
infoFileHandler = logging.FileHandler("app.log")
errorFileHandler = logging.FileHandler("error.log")

syslogHandler.setLevel(logging.INFO)
errorFileHandler.setLevel(logging.ERROR)
infoFileHandler.setLevel(logging.INFO)

sys_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
info_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

syslogHandler.setFormatter(sys_formatter)
infoFileHandler.setFormatter(info_formatter)
errorFileHandler.setFormatter(error_formatter)


logger.addHandler(syslogHandler)
logger.addHandler(infoFileHandler)
logger.addHandler(errorFileHandler)
logger.setLevel(logging.INFO)
# logging.basicConfig(level=logging.INFO , filename="app.log" , format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logger.setLevel(logging.INFO)
# logger.error("thie is info message")



# Create your views here.

@csrf_exempt
def loginPage(request):
        return redirect('mylibrary:userLogin')


@csrf_exempt    
def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'Logged in')
            return render(request,'mylibrary/main.html')
        else:
            messages.error(request, 'Login Failed ; This user is not registered/Wrong Password')
            return redirect('mylibrary:userLogin')
    else:
        return render(request,'mylibrary/login.html')


@csrf_exempt
def userLogout(request):
        
        logout(request)
        return render(request, 'mylibrary/login.html')


@csrf_exempt
def register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return render(request, 'mylibrary/login.html') 
        return render(request, 'mylibrary/signup.html', {'form':form}) 
    else:
        form = CustomUserCreationForm()
        return render(request,'mylibrary/signup.html', {'form': form})


@csrf_exempt
def main(request):
    template = loader.get_template('mylibrary/main.html')
    return HttpResponse(template.render())


def books(request):
    books = Book.objects.all()
    choices = [(book.pk, f"{book.name} - Available copies: {book.copies}") for book in books]
    if request.method == 'POST':
        form = BookSelectForm(request.POST)
        if form.is_valid():
            book_pk = form.cleaned_data['book']
            book_pk=int(book_pk)
            return redirect('mylibrary:bookdetail', pk=book_pk)
    else:
        form = BookSelectForm()
        form.fields['book'].choices = choices
    context = {
        'form': form,
    }
    return render(request, 'mylibrary/books.html', context)




def bookdetail(request, pk):

    book = get_object_or_404(Book, pk=pk)
    context = {
        'book' : book
    }
    return render(request, 'mylibrary/bookdetail.html',context)


def addbook(request):

    if request.method == 'POST':
        form = NewBookForm(request.POST)
        if form.is_valid():
            isbn = form.cleaned_data['isbn']
            name = form.cleaned_data['name']
            author = form.cleaned_data['author']
            pub_year = form.cleaned_data['pub_year']
            type = form.cleaned_data['type']
            copies = form.cleaned_data['copies']
            summary = form.cleaned_data['summary']
            wikipedia = form.cleaned_data['wikipedia']
            Book.objects.create(isbn=isbn,name=name,author=author,pub_year=pub_year,type=type,copies=copies,summary=summary,wikipedia=wikipedia)
            messages.success(request, 'Book added successfully')
            return HttpResponseRedirect(reverse('mylibrary:books'))
        else:
            return render(request, 'mylibrary/newbook.html', {'form':form}) 
    else:
        form = NewBookForm()
        context = {
            'form' : form
        }
        return render(request, 'mylibrary/newbook.html', context)


def customers(request):

    all_customers = Customer.objects.all().values()
    context = {
        'all_customers' : all_customers
    }
    return render(request, 'mylibrary/customers.html', context)


def customerdetail(request, pk):

    customer = get_object_or_404(Customer, pk=pk)
    context = {
        'customer' : customer
    }
    return render(request, 'mylibrary/customerdetail.html',context)


def addcustomer(request):

    if request.method == 'POST':
        form = NewCustomerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            age = form.cleaned_data['age']
            messages.success(request, 'Cusomer added successfully')
            Customer.objects.create(name=name,city=city,age=age)
            return HttpResponseRedirect(reverse('mylibrary:customers'))
        return render(request, 'mylibrary/newcustomer.html', {'form':form}) 
    else:    
        form = NewCustomerForm()
        context = {
            'form' : form
        }
        return render(request , 'mylibrary/newcustomer.html', context)


def loans(request):

    all_loans = Loan.objects.all().values()
    context = {
        'all_loans' : all_loans,
    }
    return render(request, 'mylibrary/loans.html', context)

   
def loandetail(request, pk):

    loan = get_object_or_404(Loan, pk=pk)
    loan_book_id = loan.book
        
    books = Book.objects.all().values()
    for i in range(len(books)):
        single_book = books[i]
        a_book = []
        for detail in single_book.values():
            a_book.append(detail)
        if int(loan_book_id)==a_book[0]:
            book_name = a_book[1]


    customers = Customer.objects.all().values()
    for i in range(len(customers)):
        single_customer = customers[i]
        details_lst = []
        for detail in single_customer.values():
            details_lst.append(detail)
            continue
        if loan.cust_id == details_lst[0] :
            customer_name = details_lst[1]
            break
    
    context = {'loan' : loan, 'customer_name' : customer_name, 'book_name' : book_name}
    return render(request, 'mylibrary/loandetail.html', context)


def loanbook(request):

    if request.method == 'POST':
        form = NewLoanForm(request.POST)
        if form.is_valid():
            cust_id = form.cleaned_data['cust_id']
            book = form.cleaned_data['book']
            book = int(book)
            loandate = date.today()
            books = Book.objects.all().values()

            for i in range(len(books)):
                single_book = books[i]
                details_lst = []
                for detail in single_book.values():
                    details_lst.append(detail)

                if book == int(details_lst[0]):
                    selected_book = get_object_or_404(Book, pk=book)
                    selected_book.copies -= 1
                    selected_book.save()

                    if details_lst[4] == 1:
                        returndate = loandate + \
                        timedelta(days=10)
                        Loan.objects.create(cust_id=cust_id,book=book,loandate=loandate,returndate=returndate)
                        messages.success(request, 'Loaned successfully')
                        return HttpResponseRedirect(reverse('mylibrary:loans')) 

                    elif details_lst[4] == 2:
                        returndate = loandate+ \
                        timedelta(days=5)
                        Loan.objects.create(cust_id=cust_id,book=book,loandate=loandate,returndate=returndate)
                        messages.success(request, 'Loaned successfully')
                        return HttpResponseRedirect(reverse('mylibrary:loans'))

                    elif details_lst[4] == 3:
                        returndate = loandate + \
                        timedelta(days=2)
                        Loan.objects.create(cust_id=cust_id,book=book,loandate=loandate,returndate=returndate)
                        messages.success(request, 'Loaned successfully')
                        return HttpResponseRedirect(reverse('mylibrary:loans'))
                    
        return render(request, 'mylibrary/newloan.html', {'form':form})
    else:
        form = NewLoanForm()
        all_books = Book.objects.all().values()
        context = {
            'form' : form,
            'all_books' : all_books
        }
        return render(request, 'mylibrary/newloan.html', context)
    

def removeloan(request, pk):
    
    loan = Loan.objects.get(pk=pk)
    loan.delete()
    books = Book.objects.all().values()
    messages.success(request, 'Loan deleted successfully')
    for i in range(len(books)):
        single_book = books[i]
        details_lst = []
        for detail in single_book.values():
            details_lst.append(detail)
            continue
        if int(loan.book) == details_lst[0]:
            selected_book = get_object_or_404(Book, pk=loan.book)
            selected_book.copies += 1
            selected_book.save()
    return HttpResponseRedirect(reverse('mylibrary:loans'))


def removebook(request , pk):

    to_be_deleted = Book.objects.get(pk=pk)
    loans = Loan.objects.all().values()
    for i in range(len(loans)):
        single_loan = loans[i]
        details_lst = []
        for detail in single_loan.values():
            details_lst.append(detail)
        if to_be_deleted.pk == int(details_lst[2]):   # details_lst[2] is the book_id of the loan
            messages.error(request,'This book cannot be removed as it has an on going loan !')
            return redirect('mylibrary:bookdetail',pk=pk)
    to_be_deleted.delete()
    messages.success(request, 'Book deleted successfully')
    return HttpResponseRedirect(reverse('mylibrary:books'))


def removecustomer(request, pk):

    to_be_deleted = Customer.objects.get(pk=pk)
    loans = Loan.objects.all().values()
    for i in range(len(loans)):
        single_loan = loans[i]
        details_lst = []
        for detail in single_loan.values():
            details_lst.append(detail)
        if to_be_deleted.pk == int(details_lst[1]):
            messages.error(request,'This customer cannot be removed as it has an on going loan !')
            return redirect('mylibrary:customerdetail',pk=pk)
    to_be_deleted.delete()
    messages.success(request, 'Customer deleted successfully')
    return HttpResponseRedirect(reverse('mylibrary:customers'))


def get_city_names(request):
    term = request.GET.get('term', '')
    cities = City.objects.filter(city_name__startswith=term)
    city_names = [city.city_name for city in cities]
    return JsonResponse(city_names, safe=False)


# def book_autocomplete(request):
#     if request.is_ajax():
#         q = request.GET.get('term', '')
#         books = Book.objects.filter(name__icontains=q).values_list('name', flat=True)
#         results = list(books)
#         return JsonResponse(results, safe=False) 
