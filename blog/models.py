from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.html import strip_tags
import markdown
# Create your models here.


class Article(models.Model):
    title = models.CharField("标题", max_length=50)
    author = models.CharField("作者", max_length=50)
    created_date = models.DateTimeField("创建日期", auto_now_add=True)
    modify_date = models.DateTimeField("修改日期", auto_now=True)
    excerpt = models.CharField(max_length=200, blank=True)
    content = models.TextField("内容")
    is_show = models.BooleanField()
    category = models.ForeignKey('Category', verbose_name='分类',
                                 null=True,
                                 on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签', blank=True)
    views = models.IntegerField(default=0)

    class Meta:
        db_table = "article"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])

            self.excerpt = strip_tags(md.convert(self.content))[:54]
        super(Article, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name


class MyUser(AbstractUser):
    point = models.IntegerField('积分', default=0)

    class Meta:
        db_table = 'MyUser'

    def __str__(self):
        return self.username


class Contact(models.Model):
    name = models.CharField('姓名', max_length=30)
    subject = models.CharField('标题', max_length=30)
    email = models.EmailField('邮箱', max_length=255)
    message = models.TextField('内容')

    def __str__(self):
        return self.subject