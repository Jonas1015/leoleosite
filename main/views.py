from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, JsonResponse
import os
from django.conf import settings
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F, Q
import mimetypes
from .models import *


# Create your views here.
def home(request):
    latest_books  = Book.objects.all().order_by('-id')[:10]
    popular_books  = Book.objects.filter(is_popular = True)[:10]
    categories  = Category.objects.all()[:10]
    context = {
        'popular_books': popular_books,
        'latest_books': latest_books,
        'categories': categories,
    }
    template_name = 'main/home.html'
    return render(request, template_name, context)


def books(request):
    books_list = Book.objects.all().order_by('-id')

    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        books_list = Book.objects.filter(Q(name__icontains = search_term)|Q(author__icontains = search_term)).order_by('-id')
        if not books_list:
            books_list = Book.objects.all().order_by('-id')
            messages.warning(request, f'Book Not Found')

    page = request.GET.get('page', 1)

    paginator = Paginator(books_list, 8)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books,
    }
    template_name = 'main/books.html'
    return render(request, template_name, context)

def categories(request):
    categories_list = Category.objects.all().order_by('-id')

    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        categories_list = Category.objects.filter(Q(name__icontains = search_term)).order_by('-id')
        if not categories_list:
            categories_list = Category.objects.all().order_by('-id')
            messages.warning(request, f'Category Not Found')

    page = request.GET.get('page', 1)

    paginator = Paginator(categories_list, 8)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
    }
    template_name = 'main/categories.html'
    return render(request, template_name, context)

def category_books(request, id):
    category = get_object_or_404(Category, id=id)
    books_list = Book.objects.filter(category = category)

    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        books_list = Book.objects.filter(Q(name__icontains = search_term)|Q(author__icontains = search_term), category = category).order_by('-id')
        if not books_list:
            books_list = Book.objects.filter(category = category).order_by('-id')
            messages.warning(request, f'Book Not Found')

    page = request.GET.get('page', 1)

    paginator = Paginator(books_list, 8)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books,
        'category': category,
    }
    template_name = 'main/category_books.html'
    return render(request, template_name, context)



def book(request, id):
    book = ""
    similar_books = ""
    try:
        book = Book.objects.get(id=id)
        similar_books = Book.objects.filter(category = book.category)
    except:
        pass


    context = {
        'book': book,
        'similar_books': similar_books,
    }
    template_name = 'main/book.html'
    return render(request, template_name, context)

def download_book(request, id):
    book = Book.objects.get(id=id)
    book_path = book.file.path
    file_path = os.path.join(settings.MEDIA_ROOT, book_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = f"attachment; filename={book.name}"
            return response
    raise Http404


def about(request):
    context = {}
    template_name = 'main/about.html'
    return render(request, template_name, context)


def contact(request):
    context = {}
    template_name = 'main/contact.html'
    return render(request, template_name, context)

# ============================== BOOKS ADMIN ======================================================

@login_required
def allBooks(request):
    books_list = Book.objects.all().order_by('-id')
    categories = Category.objects.all()
    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        books_list = Book.objects.filter(Q(name__icontains = search_term)|Q(author__icontains = search_term)).order_by('-id')
        if not books_list:
            books_list = Book.objects.all().order_by('-id')
            messages.warning(request, f'Query Not Found')

    page = request.GET.get('page', 1)

    paginator = Paginator(books_list, 10)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books,
        'categories': categories,
    }
    template_name = 'main/allBooks.html'
    return render(request, template_name, context)

@login_required
def add_book(request):
    if request.method == "POST" and request.FILES:
        name = request.POST.get('name')
        category = request.POST.get('category')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        year = int(request.POST.get('year'))
        isbn = request.POST.get('isbn')
        description = request.POST.get('description')
        to_be_sold = request.POST.get('to_be_sold')
        is_popular = request.POST.get('is_popular')
        image = request.FILES['image']
        book_file = request.FILES['book_file']

        if to_be_sold == "on":
            to_be_sold = True
        else:
            to_be_sold = False

        if is_popular == "on":
            is_popular = True
        else:
            is_popular = False

        category_instance = get_object_or_404(Category, name = category)

        book = Book.objects.create(
            name = name,
            category = category_instance,
            author = author,
            publisher = publisher,
            year = year,
            isbn = isbn,
            description = description,
            to_be_sold = to_be_sold,
            is_popular = is_popular,
            image = image,
            file = book_file,
        )
        messages.success(request, f'Book Added Successfully!')
        return redirect('allBooks')
    messages.error(request, f'Error occured while saving your data!', extra_tags = "alert alert-danger")
    return redirect('allBooks')

@login_required
def update_book(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        year = int(request.POST.get('year'))
        isbn = request.POST.get('isbn')
        description = request.POST.get('description')
        to_be_sold = request.POST.get('to_be_sold')
        is_popular = request.POST.get('is_popular')


        if to_be_sold == "on":
            to_be_sold = True
        else:
            to_be_sold = False

        if is_popular == "on":
            is_popular = True
        else:
            is_popular = False

        book = get_object_or_404(Book, id=id)
        book.name = name
        book.author = author
        book.publisher = publisher
        book.year = year
        book.isbn = isbn
        book.description = description
        book.to_be_sold = to_be_sold
        book.is_popular = is_popular
        try:
            image = request.FILES['image']
            book.image = image
        except:
            pass
        try:
            book_file = request.FILES['book_file']
            book.file = book_file
        except:
            pass
        book.save()
        messages.success(request, f'Book Updated Successfully!')
        return redirect('allBooks')
    messages.error(request, f'Error Occured while updating your data!', extra_tags = "alert alert-danger")
    return redirect('allBooks')

@login_required
def delete_book(request, id):
    book = get_object_or_404(Book, id = id)
    book.delete()
    messages.success(request, f'Book Deleted Successfully!')
    return redirect('allBooks')


# ==================== CATEGORY ADMIN =========================================================
@login_required
def allCategories(request):
    categories_list = Category.objects.all().order_by('-id')

    if request.GET.get('search_term'):
        search_term = request.GET.get('search_term')
        categories_list = Category.objects.filter(Q(name__icontains = search_term)).order_by('-id')
        if not books_list:
            categories_list = Category.objects.all().order_by('-id')
            messages.warning(request, f'Query Not Found')

    page = request.GET.get('page', 1)

    paginator = Paginator(categories_list, 10)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)
    context = {
        'categories': categories,
    }
    template_name = 'main/allCategories.html'
    return render(request, template_name, context)

@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get('name')
        image = request.FILES['image']

        category = Category (
            name = name,
            image = image,
        )
        category.save()
        messages.success(request, f'Category Added Successfully!')
        return redirect('allCategories')
    messages.error(request, f'Error occured while saving your data!', extra_tags = "alert alert-danger")
    return redirect('allCategories')

@login_required
def update_category(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        category = get_object_or_404(Category, id=id)
        try:
            image = request.FILES['image']
            category.image = image
        except:
            pass
        category.name = name
        category.save()
        messages.success(request, f'Category Updated Successfully!')
        return redirect('allCategories')
    messages.error(request, f'Error Occured while updating your data!', extra_tags = "alert alert-danger")
    return redirect('allCategories')

@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id = id)
    category.delete()
    messages.success(request, f'Category Deleted Successfully!')
    return redirect('allCategories')
