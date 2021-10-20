from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from . import forms


class ContactView(generic.FormView):
   template_name = "catalog/contact.html"
   form_class = forms.InquiryForm
   success_url = reverse_lazy('contact')

   def form_valid(self, form):
       form.send_email()
       return super().form_valid(form)



class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    model = BookInstance
    fields = ['id','book','imprint','due_back','borrower']
    permission_required= 'catalog.can_mark_returned'


class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
    model = BookInstance
    fields = ['id','book','imprint','due_back','borrower']
    permission_required = 'catalog.can_mark_returned'


class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('bookinstances')
    permission_required = 'catalog.can_mark_returned'



class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'



class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)


    if request.method == 'POST':


        form = RenewBookForm(request.POST)


        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))


    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)







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



class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstace_see.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
