from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Blog(models.Model):
    title=models.CharField(max_length=100,default="TITLE")
    content=RichTextField(default="CONTENT",blank=True,null=True)
    #content=models.TextField(default="CONTENT")
    posted_on=models.DateTimeField(null=True,blank=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    #image=models.ImageField(blank=True)
    tags = TaggableManager()

    def __str__(self):
        return f"Blog:{self.title}"
    
    # This method spicifies where to redirect after the save method is called for this model
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})

