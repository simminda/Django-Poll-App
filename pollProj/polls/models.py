from django.db import models

# Creating Models
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

def __str__(self):
    return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

def __str__(self):
    return self.choice_text


# Legacy models
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=140)
    body = models.TextField()
    date = models.DateTimeField()

def __str__(self):
    return self.title
