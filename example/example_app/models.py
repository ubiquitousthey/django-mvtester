from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink

class Registration(models.Model):
    user = models.ForeignKey(User)
    industry = models.CharField(max_length=50)

    @permalink
    def get_absolute_url(self):
        return reverse('registration',kwargs={'slug':self.user.username})