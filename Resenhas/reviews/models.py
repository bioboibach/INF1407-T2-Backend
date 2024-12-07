from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=100)
    content = models.TextField()
    brand = models.CharField(max_length=100, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product_url = models.URLField(blank=True, null=True)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
 
class Meta:
    managed = True
    db_table = 'Reviews'
    ordering = ['id']

def __str__(self):
    return self.name