from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.conf import settings
from django.contrib.auth import  get_user_model
from crispy_forms.helper import FormHelper,Layout
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.contrib.auth import authenticate,login
from bootstrap_datepicker_plus import DatePickerInput


User =get_user_model()

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Create password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder':'Repeat password'}))

    class Meta:
        model = User
        fields = ('email', 'username')

        widgets = {
            'email':forms.EmailInput(attrs={'placeholder':'Email address'}),
            'username':forms.TextInput(attrs={'placeholder':'Full name'}),  #  i removed 'class':'form-control' as the crispy automatically add it

        }


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



DOY = ('1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987',
       '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
       '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
       '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
       '2012', '2013', '2014', '2015')


class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False,help_text='The image should be cool.',label='profile picture')
    date_of_birth = forms.DateField(
                widget=forms.SelectDateWidget(years=DOY, empty_label=("Choose Year", "Choose Month", "Choose Day"))
            )
    class Meta:
        model = User
        exclude = [
            'is_active',
            'is_admin',
            'password',
            'last_login'
        ]
        widgets= {
            'firstname':forms.TextInput(attrs={'placeholder':'First Name'}),
            'lastname': forms.TextInput(attrs={'placeholder':'Last Name'}),
        }


    # def save(self, commit=True):
    #     user=super().save(commit=False)
    #
    #     return user



    # def __init__(self,*args,**kwargs):
    #     # self.request= kwargs.pop('request')
    #     form = super().__init__(*args,**kwargs)
    #     form.fields['firstname']['placeholder']='First Name'
    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #
    #     user = authenticate(username=username,password=password)
    #     if user is not None:
    #         login(self.request,user)
    #     else:
    #         raise forms.ValidationError("The credentials is Invalid,please verify the Username or/and password")

