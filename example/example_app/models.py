from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink

USER_TYPES = (
    ('xdev','Experienced Developer'),
    ('apprentice','Apprentice'),
    ('ideaman','Idea Man'),
)

APP_INTEREST_AREAS = (
    ('games','Games'),
    ('entertainment','Entertainment'),
    ('productivity','Productivity'),
    ('branded','Branded'),
    ('other','Other'),
)

class Registration(models.Model):
    user = models.ForeignKey(User)
    user_type = models.CharField(max_length=50,choices=USER_TYPES)
    app_interest_area = models.CharField(max_length=50,choices=APP_INTEREST_AREAS,null=True,blank=True)

    @permalink
    def get_absolute_url(self):
        return reverse('registration',kwargs={'slug':self.user.username})