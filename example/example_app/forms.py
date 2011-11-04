from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields, forms
from example_app.models import Registration

class RegistrationForm(UserCreationForm):
    first_name = fields.CharField(label='First Name')
    last_name = fields.CharField(label='Last Name')
    email = fields.EmailField(label='Email')

    def save(self, commit=True):
        user = super(RegistrationForm,self).save(commit)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        reg = Registration.objects.create(
            user = user,
            industry = self.cleaned_data['industry']
        )
        return reg

    def clean_email(self):
        """Prevent account hijacking by disallowing duplicate emails."""
        email = self.cleaned_data.get('email', None)
        if email and User.objects.filter(email__iexact=email).count() > 0:
            raise forms.ValidationError("That email address is already in use.")
        return email




