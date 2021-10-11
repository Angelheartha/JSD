from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

def index(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    template_name = "catalog/book_list.html"
    queryset = Book.objects.filter(language__name__icontains='Hebrew')

class BookDetailView(generic.ListView):
    model = Book


class BokListView(generic.ListView):
    model = Book
    template_name = "catalog/bok_list.html"
    queryset = Book.objects.filter(language__name__icontains='Japanese')


class BokDetailView(generic.ListView):
    model = Book
    def get_queryset(self):
        self.book.summary = get_object_or_404(Book, summary=self.kwargs['summary'])
        return Book.objects.filter(book=self.book.summary)




class BkListView(generic.ListView):
    model = Book
    template_name = "catalog/bk_list.html"
    queryset = Book.objects.filter(language__name__icontains='English')

class BkDetailView(generic.ListView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.ListView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')