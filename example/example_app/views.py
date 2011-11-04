from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from example_app.models import Registration
from example.example_app.forms import RegistrationForm
from mvtester.decorators import has_template_experiements

@has_template_experiements
class RegisterView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'example_app/test_template.html'
    def get_success_url(self):
        return reverse('registration_thanks')

class RegistrationView(DetailView):
    model = Registration
    slug_field = 'username'
    context_object_name = 'registration'

    def get_object(self, queryset=None):
        return self.model.objects.get(user__username=self.kwargs[self.slug_field])
  