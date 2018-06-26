import os

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import Http404
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, ListView

from filebrowser.decorators import path_exists, get_path
from filebrowser.sites import filebrowser_view, site as filebrowser_site

from menus.models import BigHeaderMenu, SocialMediaMenu
from content.models import Page, Module, Post


class BaseEventPageView(DetailView):
    template_name = 'index.html'
    model = Page
    paginate_by = 6

    def __init__(self):
        super(BaseEventPageView, self).__init__()
        self.page = None
        self.posts = Post.objects.none()

    def get_posts_for_module(self, module):
        posts = module.postcategory.posts.all()
        if self.kwargs.get('year'):
            posts = posts.filter(date__year=self.kwargs['year'])
        if self.kwargs.get('tag'):
            pass
        if not self.request.user.is_staff:
            posts = posts.filter(public=True)
        return (self.posts | posts).order_by('-date')

    def get_all_posts(self, modules):
        if self.request.GET.get('category'):
            try:
                modules = [Module.objects.get(title__iexact=self.request.GET.get('category')), ]
            except:
                return
        for module in modules:
            if module.type == 'POSTCATEGORY':
                self.posts = self.get_posts_for_module(module)

    def get_context_data(self, **kwargs):
        context = super(BaseEventPageView, self).get_context_data(**kwargs)
        header_menus = BigHeaderMenu.objects.filter().order_by('order')
        social_menus = SocialMediaMenu.objects.all().order_by('order')
        modules = Module.objects.filter(modules_in_page__page=self.page).order_by('modules_in_page__order')
        self.get_all_posts(modules)
        paginator = Paginator(self.posts, self.paginate_by)
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)
        context.update({
            'header_menus': header_menus,
            'title': self.page.title,
            'social_menus': social_menus,
            'page': self.page,
            'modules': modules,
            'year': None,
            'posts': posts,
            'base_template': 'base.html'
        })

        return context


class HomeView(BaseEventPageView):

    def get_object(self, queryset=None):
        try:
            self.page = Page.objects.get(slug='')
        except:
            self.page = Page.objects.all().first()
        return self.page


class PageView(BaseEventPageView):
    context_object_name = "page"

    def get_object(self, queryset=None):
        page = super(PageView, self).get_object(queryset)
        if page.public or self.request.user.is_staff:
            return page
        raise Http404

    def get_context_data(self, **kwargs):
        self.page = kwargs['object']

        return super(PageView, self).get_context_data(**kwargs)


class PostView(ListView):
    template_name = "post_detail.html"
    model = Post
    context_object_name = "post"

    def __init__(self):
        super(PostView, self).__init__()
        self.page = None

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs['post_slug']

        obj = queryset.filter(slug=slug).get()
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('post_slug')
        self.post = context['post'].get(slug = slug)
        if not self.post.public and not self.request.user.is_staff:
            raise Http404
        header_menus = BigHeaderMenu.objects.filter().order_by('order')
        social_menus = SocialMediaMenu.objects.all().order_by('order')
        context.update({
            'header_menus': header_menus,
            'social_menus': social_menus,
            'title': self.post.title,
            'post': self.post,
            # 'back_url' : back_url
        })
        return context


class ClearCache(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        cache.clear()
        messages.success(self.request, 'The site cache was cleared successfully.')
        return self.request.META.get('HTTP_REFERER') or reverse('admin:index')

def filebrowser_browse(request):
    slug = 'katacontainers'
    filebrowser_site.directory = "uploads/%s/" % slug
    if get_path('', site=filebrowser_site) is None and \
            not os.path.exists(settings.MEDIA_ROOT + '/' + filebrowser_site.directory):
        dir = settings.MEDIA_ROOT + '/' + filebrowser_site.directory
        os.makedirs(dir)

    # Check and create folders named as modelname/fieldname
    url_dir = request.GET.get('dir', '')
    dir = settings.MEDIA_ROOT + '/' + filebrowser_site.directory + url_dir
    if get_path(url_dir, site=filebrowser_site) is None and not os.path.exists(dir):
        os.makedirs(dir)

    return path_exists(filebrowser_site, filebrowser_view(filebrowser_site.browse))(request)


def filebrowser_base(f_name):
    def f(request):
        slug = 'katacontainers'
        filebrowser_site.directory = "uploads/%s/" % slug
        return path_exists(filebrowser_site, filebrowser_view(getattr(globals()['filebrowser_site'], f_name)))(request)
    return f
