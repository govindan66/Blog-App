from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name = 'Blog Title')
    description = models.TextField(verbose_name='Blog Description')
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user', default=1,null=True, blank=True)
    pub_date = models.DateTimeField(verbose_name='Published Date',default=timezone.now)
    image = models.ImageField(verbose_name='Upload Picture', blank=True, upload_to='media/')
    featured = models.BooleanField(verbose_name='Is Featured', blank=False, default=False)

    def __str__(self):
        return self.title

    def short_des(self):
        return self.description[:100]

    def isFeatured(self):
        self.featured = True

    class Meta:
        ordering = ['title']
