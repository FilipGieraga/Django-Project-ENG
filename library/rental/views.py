from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, ProfileForm, UserUpdateForm, BorrowForm
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage


def home(request):
    counter = Book.objects.all().count()
    borrowed = Borrowed.objects.all().count()
    stored_books = Book.objects.aggregate(Sum('quantity'))
    context = {'counter': counter, 'stored_books': stored_books, 'borrowed': borrowed}
    return render(request, 'rental/home_page.html', context)


def books(request):
    list = []
    if request.user.is_authenticated:
        borrowed = request.user.person.borrowed_set.all()
        for b in borrowed:
            list.append(b.book)
    books = Book.objects.all().order_by('title')

    p = Paginator(books, 30)
    page_num = request.GET.get('page', 1)
    try:
        page=p.page(page_num)
    except EmptyPage:
        page=p.page(1)

    context = {'books': page, 'list': list, 'page_title': 'Books'}
    return render(request, 'rental/all_books.html', context)


def book_details(request, pk):
    book = Book.objects.get(id=pk)
    context = {'book': book, 'page_title': 'Book details'}
    return render(request, 'rental/book_details.html', context)


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You've successfully logged in!")
            return redirect('user')
        else:
            messages.info(request, "Username or password is incorrect")

    context = {}
    return render(request, 'rental/login.html', context)


def LogoutPage(request):
    logout(request)
    messages.success(request, "You've successfully logged out!")
    return redirect('homepage')


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account Created')
            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'rental/register.html', context)


@login_required(login_url='login')
def profile(request):
    person = request.user.person
    dt = request.user.person.date_created
    u_form = UserUpdateForm(instance=request.user)
    form = ProfileForm(instance=person)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        form = ProfileForm(request.POST, instance=person)
        if form.is_valid() and u_form.is_valid():
            form.save()
            u_form.save()
            messages.success(request, 'Account Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        form = ProfileForm(instance=request.user.person)

    context = {'form': form, 'dt': dt, 'u_form': u_form, 'page_title': 'Profile'}

    return render(request, 'rental/profile.html', context)


@login_required(login_url='login')
def borrow(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        form = BorrowForm(request.POST, initial={'book': book.id})
        if form.is_valid() and book.quantity >= 1:
            form = form.save(commit=False)
            form.person = request.user.person
            form.save()
            book.quantity -= 1
            book.save()
            return redirect('all_books')
        else:
            return HttpResponse('<h2>This book is not in library at the moment.</h2>')
    else:
        form = BorrowForm(initial={'book': book.id})
    context = {'form': form, 'book': book, 'page_title': 'Borrow book'}
    return render(request, 'rental/borrow.html', context)

@login_required(login_url='login')
def user_page(request):
    borrowed = request.user.person.borrowed_set.all()
    counter = borrowed.count()
    context = {'borrowed': borrowed, 'counter': counter, 'page_title': 'My books'}
    return render(request, 'rental/user_page.html', context)

@login_required(login_url='login')
def return_book(request, pk):
    borrowed = Borrowed.objects.get(id=pk)
    book = borrowed.book
    if request.method == 'POST':
        book.quantity += 1
        book.save()
        borrowed.delete()
        messages.success(request, "Book returned!")
        return redirect('user')
    context = {'borrowed': borrowed, 'book': book}
    return render(request, 'rental/return.html', context)
