from django.contrib.syndication.views import Feed
from .models import Article


class ArticleRssFeed(Feed):
    title = "xlc的博客"
    link = '/'
    description = 'xlc文章更新'

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return '[%s] %s' %(item.category, item.title)

    def item_description(self, item):
        return item.content[:54]
