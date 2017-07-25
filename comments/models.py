from django.db import models

# Create your models here.


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('blog.Article')
    text = models.TextField()

    def __str__(self):
        return self.text[:20]
