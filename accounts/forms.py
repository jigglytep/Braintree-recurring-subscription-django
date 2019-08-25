from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegistrationForm(UserCreationForm):
    #email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = (
        'username'
        ,'email'
        ,)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            print(user.email)
            user.save()

        return user

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email'
            ,'first_name'
            ,'last_name'
            ,'password')
        exclude = ()
