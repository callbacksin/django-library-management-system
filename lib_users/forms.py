from crispy_forms import helper
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from dal import autocomplete
from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from core.models import Item
from demo import settings
from .models import Group, Profile


class AssignBookInstanceForm(forms.Form):
    inventory_number = forms.ModelChoiceField(
        label='Inventory Number',
        queryset=Item.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='item_autocomplete',
            attrs={
                'data-minimum-input-length': 0,
                'data-max-results': 10,
                'style': 'width:100%',
                'data-html': True,
            }
        ),
        help_text='Start typing the inventory number for autocomplete',
        required=False,
    )
    inventory = forms.CharField(
        label='Inventory Number',
        required=False,
    )
    due_back = forms.DateField(
        label='Return Date',
        help_text='Format: DD.MM.YYYY.\n Return date is optional',
        input_formats=settings.DATE_INPUT_FORMATS,
        required=False,
    )


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'] = forms.CharField(
            label='',
            widget=forms.TextInput(attrs={'placeholder': 'Enter login'}))
        self.fields['password'] = forms.CharField(
            label='',
            widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
        self.fields['remember'].label = 'Remember me'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('group_name',)


class UserForm(UserCreationForm):
    username = forms.CharField(
        label='User Code',
        help_text='''Used for login.
                     May consist of the group number and student number. 
                     For example, "SP841-14". 
                     Keep in mind that usernames must be unique.'''
    )
    first_name = forms.CharField(
        label='First Name',
    )
    last_name = forms.CharField(
        label='Last Name',
    )
    patronymic = forms.CharField(
        label='Patronymic',
    )
    email = forms.EmailField(
        label='E-mail Address',
        required=False,
    )
    password1 = forms.CharField(
        label='Password',
        help_text='''It is recommended to use the user\'s phone number 
                     as the password. 
                     In any case, it is advisable to recommend changing the password.''',
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput)
    academy_group = forms.ModelChoiceField(
        empty_label='---Select from the list---',
        label='Group',
        queryset=Group.objects.all())
    birth_date = forms.DateField(
        label='Date of Birth',
        help_text='Format: DD.MM.YYYY',
        input_formats=settings.DATE_INPUT_FORMATS
    )
    is_superuser = forms.BooleanField(
        label='Is a Librarian?',
        required=False,
        help_text='''BE CAREFUL: it is not recommended to grant these 
                     privileges to third parties'''
    )

    class Meta:
        model = User
        fields = ('username', 'academy_group', 'last_name', 'first_name',
                  'patronymic', 'birth_date', 'email', 'password1', 'password2',
                  'is_superuser',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserFormWithoutPassword(forms.ModelForm):
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    username = forms.CharField(
        label='User Code',
        help_text='''May consist of the group number and student number. 
                     For example, "SP841-14".
                     Keep in mind that usernames must be unique.''',
        error_messages={
            'unique': 'A user with this user code already exists'
        }
    )
    first_name = forms.CharField(
        label='First Name',
    )
    last_name = forms.CharField(
        label='Last Name',
    )
    email = forms.EmailField(
        label='E-mail Address',
        required=False,
        error_messages={'invalid': 'Invalid e-mail format'}
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'email')


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=settings.DATE_INPUT_FORMATS,
        help_text='Date format: dd.mm.yyyy',
        error_messages={'invalid': 'Invalid date format'}
    )

    class Meta:
        model = Profile
        fields = ('academy_group', 'patronymic', 'birth_date')


class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': "Passwords do not match",
    }
    new_password1 = forms.CharField(label="New Password",
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password",
                                    widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2', )
