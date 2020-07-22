from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class Question(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    asked_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    posted_on=models.DateTimeField(null=True,blank=True)
    tags = TaggableManager()

    def __str__(self):
        return f"Question:{self.title}"

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})

class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,null=True,blank=True)
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    content=models.TextField()
    upvotes=models.IntegerField(default=0)
    downvotes=models.IntegerField(default=0)
    posted_on=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"Answer to {self.question.title}"
    
    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.question.pk})

class Upvote(models.Model):
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    by=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"Upvote of {self.answer} by {self.by}"
    
    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.answer.question.pk})

class Downvote(models.Model):
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    by=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"Downvote of {self.answer} by {self.by}"
    
    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.answer.question.pk})


