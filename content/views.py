import os
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
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
    paginate_by = 2

    def __init__(self):
        super(BaseEventPageView, self).__init__()
        self.page = None
        self.posts = Post.objects.none()

    def get_posts_for_module(self, module):
        posts = module.postcategory.posts.filter(site=self.request.site)
        if self.kwargs.get('year'):
            posts = posts.filter(site=self.request.site,
                                 date__year=self.kwargs['year'])
        return (self.posts | posts).order_by('-date')

    def get_all_posts(self, modules):
        if self.request.GET.get('category'):
            try:
                modules = [Module.objects.get(site=self.request.site,
                                              title__iexact=self.request.GET.get('category')), ]
            except Module.DoesNotExist:
                return
        for module in modules:
            if module.type == 'POSTCATEGORY':
                self.posts = self.get_posts_for_module(module)

    def get_context_data(self, **kwargs):
        context = super(BaseEventPageView, self).get_context_data(**kwargs)

        if (not self.page.site.id == self.request.site.id) \
                or (not self.page.public and not self.request.user.is_staff):
            raise Http404("Requested page doesn't exist")

        # Gathering menus
        header_menus = BigHeaderMenu.objects.filter(site=self.request.site).order_by('order')
        social_menus = SocialMediaMenu.objects\
            .filter(site=self.request.site).order_by('order')

        # Gather modules and all its posts if available
        modules = Module.objects.filter(modules_in_page__page=self.page, site=self.request.site)\
            .order_by('modules_in_page__order')

        self.get_all_posts(modules)
        paginator = Paginator(self.posts, 2)
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)
        context.update({
            'header_menus': header_menus,
            'title': self.page.title,
            'social_menus': social_menus,
            'page': self.page,
            'modules': modules,
            'year': None,
            'posts': posts
        })

        return context


class HomeView(BaseEventPageView):

    def get_object(self, queryset=None):
        try:
            self.page = Page.objects.get(slug='', site=self.request.site)
        except Page.DoesNotExist:
            self.page = Page.objects.filter(site=self.request.site).first()
        return self.page


class PageView(BaseEventPageView):
    context_object_name = "page"

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
        self.post = None

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs['post_slug']

        obj = queryset.filter(slug=slug, site=self.request.site).get()
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('post_slug')
        self.post = context['post'].get(slug=slug, site=self.request.site)
        # if not self.post.event.slug == self.event_slug:
        #     raise Http404("Requested page doesn't exist")
        header_menus = BigHeaderMenu.objects\
            .filter(site=self.request.site).order_by('order')
        # footer_menus = self.get_footer_menus(self.event_slug)
        social_menus = SocialMediaMenu.objects\
            .filter(site=self.request.site).order_by('order')
        # back_url = Page.objects.get(title='Schedule').get_absolute_url()
        context.update({
            'header_menus': header_menus,
            'social_menus': social_menus,
            'title': self.post.title,
            # 'footer_menus': footer_menus,
            'post': self.post,
            # 'back_url' : back_url
        })
        return context


class ClearCache(RedirectView):
    # TODO: move to admin.py?

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        Site.objects.clear_cache()
        cache.clear()
        messages.success(self.request, 'The site cache was cleared successfully.')
        return self.request.META.get('HTTP_REFERER') or reverse('admin:index')
        # TOFIX: use slugs


def filebrowser_browse(request):
    slug = request.site.domain
    filebrowser_site.directory = "uploads/%s/" % slug
    # Check and create folder named as the site domain

    if get_path('', site=filebrowser_site) is None and \
            not os.path.exists(settings.MEDIA_ROOT + '/' + filebrowser_site.directory):
        new_dir = settings.MEDIA_ROOT + '/' + filebrowser_site.directory
        os.makedirs(new_dir)

    # Check and create folders named as modelname/fieldname
    url_dir = request.GET.get('dir', '')
    new_dir = settings.MEDIA_ROOT + '/' + filebrowser_site.directory + url_dir
    if get_path(url_dir, site=filebrowser_site) is None and not os.path.exists(dir):
        os.makedirs(new_dir)

    return path_exists(filebrowser_site, filebrowser_view(filebrowser_site.browse))(request)


def filebrowser_base(f_name):
    def f(request):
        # slug = request.META['HTTP_HOST'].split('.')[0]
        # Temporary slug
        slug = request.site.domain
        filebrowser_site.directory = "uploads/%s/" % slug
        return path_exists(filebrowser_site, filebrowser_view(getattr(globals()['filebrowser_site'], f_name)))(request)
    return f
