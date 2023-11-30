from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Blog, BlogCategory, BlogTag, BlogComment


class BlogListView(ListView):
    template_name = 'blog/blog_list.html'
    model = Blog
    context_object_name = 'blogs'
    paginate_by = 4

    def get_queryset(self):
        query = super(BlogListView, self).get_queryset()
        category_title = self.kwargs.get('category')
        tag_title = self.kwargs.get('tag')
        if category_title:
            query = query.filter(category__url_title__iexact=category_title).order_by('-id')
        if tag_title:
            query = query.filter(tag__url_title__iexact=tag_title).order_by('-id')
        return query.filter(is_active=True, is_delete=False).order_by('-id')


def blog_categories_component(request: HttpRequest):
    blog_categories = BlogCategory.objects.filter(is_active=True)
    context = {
        'blog_categories': blog_categories
    }
    return render(request, 'blog/blog_category.html', context)


def blog_tags_component(request: HttpRequest):
    blog_tags = BlogTag.objects.filter(is_active=True)
    context = {
        'blog_tags': blog_tags
    }
    return render(request, 'blog/blog_tag.html', context)


def last_blogs_component(request: HttpRequest):
    sorted_blogs = Blog.objects.filter(is_active=True, is_delete=False).order_by('-id')[:4]
    context = {'sorted_blogs': sorted_blogs}
    return render(request, 'blog/last_blog.html', context)


class BlogDetailView(DetailView):
    template_name = 'blog/blog_detail.html'
    model = Blog
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data()
        loaded_article = self.object
        context['related_articles'] = Blog.objects.filter(category_id=loaded_article.category_id, is_active=True,
                                                          is_delete=False).exclude(pk=loaded_article.id)[:3]
        context['comments'] = BlogComment.objects.filter(article_id=loaded_article.id, parent_id=None,
                                                         is_verify=True).prefetch_related(
            'blogcomment_set').order_by('-created_date')
        context['comments_count'] = BlogComment.objects.filter(article_id=loaded_article.id, is_verify=True).count()

        return context

    def get_queryset(self):
        query = super(BlogDetailView, self).get_queryset()
        return query.filter(is_active=True, is_delete=False)


class AddBlogComment(View):
    def post(self, request: HttpRequest):
        comment_text = request.POST.get('comment_text')
        parent_id = request.POST.get('parent_id')
        blog_id = request.POST.get('blog_id')

        if comment_text:
            comment = BlogComment(message=comment_text, parent_id=parent_id, user_id=request.user.id,
                                  article_id=blog_id)
            comment.save()

            return JsonResponse({
                'status': 'ok',
                'title': 'عملیات موفقیت آمیز...',
                'text': 'دیدگاه شما با موفقیت ارسال شد و پس از تاًیید توسط ادمین در این صفحه منتشر خواهد شد.',
                'icon': 'success',
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'title': 'خطا...',
                'text': 'در صورت خالی بودن قسمت نظر؛ امکان ارسال آن وجود ندارد!',
                'icon': 'error',
            })

        context = {
            'comments': BlogComment.objects.filter(article_id=blog_id, parent_id=None,
                                                   is_verify=True).prefetch_related(
                'blogcomment_set').order_by('-created_date'),
            'comments_count': BlogComment.objects.filter(article_id=blog_id, is_verify=True).count()
        }
        return render(request, 'blog/blog_comment.html', context)


class SearchBlogView(ListView):
    template_name = 'blog/blog_list.html'
    model = Blog
    context_object_name = 'blogs'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query is None:
            query = super(SearchBlogView, self).get_queryset()
            return query.filter(is_active=True, is_delete=False).order_by('-id')
        else:
            blogs = Blog.objects.search(query).order_by('-id')
            return blogs
