import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class ShowInformations(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    info = models.TextField()
    date_posted = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('informations-detail', kwargs={'pk': self.pk})
