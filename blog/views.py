from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login as auth_login, logout
from blog.forms import SignupForm
from django.contrib.auth import get_user_model
from blog.models import Article, Category, Tag
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import markdown
from comments.forms import CommentForm
from django.utils.html import strip_tags
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.db.models import Q
# Create your views here.

# def home(request):
#     article_list = Article.objects.all().order_by('-created_date')
#
#     return render(request, 'blog/index.html', locals())


class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = 4

    # def get_queryset(self):
    #     article_list = Article.objects.filter(is_show=True)
    #     for article in article_list:
    #         article.content = strip_tags(markdown.markdown(article.content,))[:54]
    #     return article_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = []
        right_has_more = []
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages -1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number -3 > 0) else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number -3 > 0) else 0:page_number - 1]
            right = page_range[page_number:page_range + 2]

            if right[-1] < total_pages -1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


'''
def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.increase_views()
    article.content = markdown.markdown(article.content,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
    form = CommentForm()
    comment_list = article.comment_set.all()
    context = {
        'article': article,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)
'''


class PostDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        article = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(configs=[('slugify', slugify)]),
        ])
        article.content = md.convert(article.content)
        article.toc = md.toc

        return article

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({'form': form, 'comment_list': comment_list})
        return context


'''
def archives(request, year, month):
    article_list = Article.objects.filter(created_date__year=year,
                                       created_date__month=month
                                       ).order_by('-created_date')
    return render(request, 'blog/index.html', locals())
'''


class ArchivesView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_date__year=year,
                                                               created_date__month=month).order_by('-created_date')

'''
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    article_list = Article.objects.filter(category=cate).order_by('-created_date')
    return render(request, 'blog/index.html', {'article_list': article_list})
'''


class CategoryView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    article_list = Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg, 'article_list': article_list})


def about(request):
    return render(request, 'blog/about.html', locals())


# def full_width(request):
#     return render(request, 'blog/full-width.html', locals())


def contact(request):
    return render(request, 'blog/contact.html', locals())


def signup(request):
    path = request.get_full_path()
    if request.method == 'POST':
        form = SignupForm(data=request.POST, auto_id="%s")
        if form.is_valid():
            UserModel = get_user_model()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = UserModel.objects.create_user(username=username, email=email, password=password)
            user.save()
            auth_user = authenticate(username=username, password=password)
            auth_login(request, auth_user)
            return redirect("home")
    else:
        form = SignupForm(auto_id="%s")
    return render(request, 'blog/signup.html', locals())


def logout_view(request):
    logout(request)
    return redirect('home')


class FullView(IndexView):
    model = Article
    template_name = 'blog/full-width.html'
    context_object_name = 'article_list'
    paginate_by = 5

    def get_queryset(self):
        article_list = Article.objects.filter(is_show=True)
        for article in article_list:
            article.content = strip_tags(markdown.markdown(article.content,))[:54]
        return article_list
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     paginator = context.get('paginator')
    #     page = context.get('page_obj')
    #     is_paginated = context.get('is_paginated')
    #
    #     pagination_data = self.pagination_data(paginator, page, is_paginated)
    #     context.update(pagination_data)
    #
    #     return context
    #
    # def pagination_data(self, paginator, page, is_paginated):
    #     if not is_paginated:
    #         return {}
    #     left = []
    #     right = []
    #     left_has_more = []
    #     right_has_more = []
    #     first = False
    #     last = False
    #     page_number = page.number
    #     total_pages = paginator.num_pages
    #     page_range = paginator.page_range
    #
    #     if page_number == 1:
    #         right = page_range[page_number:page_number + 2]
    #
    #         if right[-1] < total_pages -1:
    #             right_has_more = True
    #         if right[-1] < total_pages:
    #             last = True
    #
    #     elif page_number == total_pages:
    #         left = page_range[(page_number - 3) if (page_number -3 > 0) else 0:page_number - 1]
    #
    #         if left[0] > 2:
    #             left_has_more = True
    #
    #         if left[0] > 1:
    #             first = True
    #     else:
    #         left = page_range[(page_number - 3) if (page_number -3 > 0) else 0:page_number - 1]
    #         right = page_range[page_number:page_range + 2]
    #
    #         if right[-1] < total_pages -1:
    #             right_has_more = True
    #         if right[-1] < total_pages:
    #             last = True
    #
    #         if left[0] > 2:
    #             left_has_more = True
    #
    #         if left[0] > 1:
    #             first = True
    #
    #     data = {
    #         'left': left,
    #         'right': right,
    #         'left_has_more': left_has_more,
    #         'right_has_more': right_has_more,
    #         'first': first,
    #         'last': last,
    #     }
    #
    #     return data


