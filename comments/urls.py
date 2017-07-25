from django.conf.urls import url
from . import views


app_name = 'comments'
urlpatterns = [
    url(r'^comment/article/(?P<article_pk>[0-9]+)/$', views.article_comment, name='article_comment'),
]
