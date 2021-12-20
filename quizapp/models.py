from uuid import uuid4
from django.db import models


# Create your models here.

class Quiz(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.text


class Choice(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    text = models.CharField(max_length=150)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
