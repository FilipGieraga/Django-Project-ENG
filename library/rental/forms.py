from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Person, Borrowed


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['user']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ['email']


class BorrowForm(forms.ModelForm):
    # book = Book.objects.get(id=pk)

    class Meta:
        model = Borrowed
        fields= ['book','return_date']
        widgets = {
            'return_date': forms.DateInput(attrs={'readonly': 'readonly'}),
            # 'book': forms.Select(attrs={'disabled':'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].disabled = True