import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Author(models.Model):
    author_name =models.CharField(max_length=48)
    author_bio = models.TextField(max_length=300)
    def __str__(self):
        return self.author_name

class Post(models.Model):
    post_title=models.CharField(max_length=48)
    post_desc=models.TextField(max_length=200)
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    pub_date=models.DateTimeField('date published')
    def __str__(self):
        return self.post_title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)