from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(max_length=240)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
