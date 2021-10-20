import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
#from .forms import RenewBookForm
from .models import BookInstance
from django.forms import ModelForm
from .models import BookInstance
from django.core.mail import EmailMessage

class InquiryForm(forms.Form):
    name = forms.CharField(label='名前', max_length=30)
    email = forms.EmailField(label='メール')
    inquiry = forms.CharField(label='問い合わせ内容', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        inquiry = self.cleaned_data['inquiry']

        message = EmailMessage(subject=name + "からの問い合わせ",
                               body=inquiry,
                               from_email=email,
                               to=["fr8ybzthb@icloud.com"],
                               cc=[email])
        message.send()



class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']

       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))


       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))


       return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}




class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data

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

class ContactForm(forms.Form):
    contact_me = forms.EmailField(help_text="write here")

