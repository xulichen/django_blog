from blog import views
from django.conf.urls import url
from django.views.decorators.cache import cache_page


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/', views.about),
    url(r'^signup/', views.signup),
    url(r'^logout/', views.logout_view),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^full-width/', views.FullView.as_view(), name='blog'),
    # url(r'^article/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^article/(?P<pk>[0-9]+)/$', cache_page(60 * 15)(views.PostDetailView.as_view()), name='detail'),
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
]