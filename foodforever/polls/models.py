from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ingredient(models.Model):
    owner = models.ForeignKey(User)
    ingredient_name = models.CharField(max_length=200)
    exp_date = models.DateField('expiration date')
    def __str__(self):
        return self.ingredient_name

    def expiration_soon(self):
        now = timezone.now()
        expiration_soon.admin_order_field = 'exp_date'
        expiration_soon.boolean = True
        expiration_soon.short_description = 'Expiring Soon?'

class Choice(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
