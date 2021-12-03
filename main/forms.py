from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.messages.api import warning
from django.forms import widgets
from .models import *
User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['fname', 'lname','dob', 'email','password','password_2']
        widgets = {
                'fname' : forms.TextInput(attrs={'type' : "text", "class" : "form-control" 
                ,"aria-describedby" : "fname", "placeholder" : "First Name " ,"name" :"fname"}),
                'lname' : forms.TextInput(attrs={'type' : "text", "class" : "form-control" 
                ,"aria-describedby" : "lname", "placeholder" : "Last Name" ,"name" :"lname"}),
                'email' : forms.TextInput(attrs={'type' : "email", "class" : "form-control" 
                ,"aria-describedby" : "email", "placeholder" : "Enter email" ,"name" :"email"}),
                'password': forms.PasswordInput(attrs={'type' : "password", "class" : "form-control" 
                ,"aria-describedby" : "password", "placeholder" : "password" ,"name" :"password"}),
                'password_2': forms.PasswordInput(attrs={'type' : "password", "class" : "form-control" 
                ,"aria-describedby" : "password_2", "placeholder" : "password" ,"name" :"password-2"}),
                'dob' : forms.DateInput(attrs={'type' : "date", "class" : "form-control", 'required pattern' : "\d{4}-\d{2}-\d{2}" 
                ,"aria-describedby" : "dob", "placeholder" : "yyyy-mm-dd" ,"name" :"dob" ,'min':'1959-01-01'})
        }
    
    def clean_email(self):
        """
        Verify email is available
        """
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already exists")
        return email
    
    def clean(self):
        """
        Verify both passwords match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_2 = cleaned_data.get('password_2')
        if password is not None and password != password_2:
            self.add_error('password_2', "Your passwords must match")
        return cleaned_data
        