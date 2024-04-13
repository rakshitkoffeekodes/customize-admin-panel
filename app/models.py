from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

