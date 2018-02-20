from django.db import models

class EventSub(models.Model):
    name = models.CharField(blank=False, max_length=50, help_text='Please enter your name')
    email = models.EmailField(blank=False, help_text='Please enter your email', unique=True)

    def __str__(self):
        return '%s - %s' % (self.name, self.email)
