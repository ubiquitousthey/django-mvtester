from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields, forms
from example_app.models import Registration
import models

class RegistrationForm(UserCreationForm):
    email = fields.EmailField(label='Email')
    first_name = fields.CharField(label='First Name')
    last_name = fields.CharField(label='Last Name')
    user_type = fields.ChoiceField(choices=models.USER_TYPES)
    app_interest_area = fields.ChoiceField(choices=models.APP_INTEREST_AREAS,required=False)

    def save(self, commit=True):
        user = super(RegistrationForm,self).save(commit)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        reg = Registration.objects.create(
            user = user,
            user_type = self.cleaned_data['user_type'],
            app_interest_area = self.cleaned_data['app_interest_area']
        )
        return reg

    def clean_email(self):
        """Prevent account hijacking by disallowing duplicate emails."""
        email = self.cleaned_data.get('email', None)
        if email and User.objects.filter(email__iexact=email).count() > 0:
            raise forms.ValidationError("That email address is already in use.")
        return email




