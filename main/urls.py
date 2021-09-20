from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('books/', books, name = 'books'),
    path('categories/', categories, name = 'categories'),
    path('book/<int:id>/', book, name = 'book'),
    path('download-book/<int:id>/', download_book, name = 'download-book'),
    path('category-books/<int:id>/', category_books, name = 'category-books'),
    path('about/', about, name = 'about'),
    path('contact/', contact, name = 'contact'),

    # BOOKS
    path('all-books/', allBooks, name = 'allBooks'),
    path('add-book/', add_book, name = 'add-book'),
    path('update-book/<int:id>/', update_book, name = 'update-book'),
    path('delete-book/<int:id>/', delete_book, name = 'delete-book'),

    # CATEGORIES
    path('all-categories/', allCategories, name = 'allCategories'),
    path('add-category/', add_category, name = 'add-category'),
    path('update-category/<int:id>/', update_category, name = 'update-category'),
    path('delete-category/<int:id>/', delete_category, name = 'delete-category'),
]
