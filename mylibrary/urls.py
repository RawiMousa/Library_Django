from django.urls import path 
from .import views
# from .views import QuestionViewSet

app_name = "mylibrary"


urlpatterns = [
    path('', views.userLogin , name='userLogin'),
    path('main/', views.main, name='main'),
    path('userLogout/', views.userLogout, name='userLogout'),
    path('register/', views.register, name='register'),
    path('books/', views.books, name='books'),
    path('customers/', views.customers, name='customers'),
    path('loans/', views.loans, name='loans'),
    path('bookdetail/<int:pk>', views.bookdetail, name='bookdetail'),
    path('customerdetail/<int:pk>', views.customerdetail, name='customerdetail'),
    path('loandetail/<int:pk>', views.loandetail, name='loandetail'),
    path('removeloan/<int:pk>', views.removeloan, name='removeloan'),
    path('removebook/<int:pk>', views.removebook, name='removebook'),
    path('removecustomer/<int:pk>', views.removecustomer, name='removecustomer'),
    path('addbook/', views.addbook, name='addbook'),
    path('addcustomer', views.addcustomer, name='addcustomer'),
    path('loanbook/', views.loanbook, name='loanbook'),
    path('get_city_names/', views.get_city_names, name='get_city_names'), 
]