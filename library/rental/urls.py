from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('books/', views.books, name='all_books'),
    path('register/', views.register, name='register'),
    path('login/', views.LoginPage, name='login'),
    path('book_details/<str:pk>/', views.book_details, name="book_details"),
    path('logout/', views.LogoutPage, name='logout'),
    path('borrow/<str:pk>/', views.borrow, name='borrow'),
    path('profile/', views.profile, name='profile'),
    path('user_page/', views.user_page, name='user'),
    path('return_book/<str:pk>/', views.return_book, name='return'),
]
