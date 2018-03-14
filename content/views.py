import os

import re
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, RedirectView, ListView

from filebrowser.decorators import path_exists, get_path
from filebrowser.sites import filebrowser_view, site as filebrowser_site

from events.models import Event
from menus.models import BigHeaderMenu, FooterMenu, SocialMediaMenu
from content.models import Page, Module, Post


class BaseEventPageView(DetailView):
    template_name = 'index.html'
    model = Page
    paginate_by = 2

    def __init__(self):
        super(BaseEventPageView, self).__init__()
        self.page = None
        self.posts = Post.objects.none()

    # def get_object(self, queryset=None):
    #     if queryset is None:
    #         queryset = self.get_queryset()
    #
    #     slug = self.kwargs.get(self.slug_url_kwarg)
    #
    #     # obj = queryset.filter(event__slug=self.event_slug, slug=slug).get()
    #     obj = queryset.filter(slug=slug).get()
    #     return obj
    #
    # def get_menus(self, event_slug):
    #     return BigHeaderMenu.objects.filter(event__slug=event_slug).order_by('order')
    #
    # def get_footer_menus(self, event_slug):
    #     return FooterMenu.objects.filter(event__slug=event_slug).order_by('order')
    #
    def dispatch(self, request, *args, **kwargs):
        # regex_slug = re.match(r'(www.)?(\w+)?\.?(' + re.escape(settings.SITE_HOST) + ')', self.request.META['HTTP_HOST'])
        domain_name = self.request.META['HTTP_HOST'].replace(settings.SITE_PORT, '')
        try:
            site = Site.objects.get(domain=domain_name)
        except:
            pass
        # if regex_slug:
        #     self.event_slug = regex_slug.group(2)
        # if not self.event_slug:
        #     last_event_slug = Event.objects.all().last().slug
        #     return redirect('http://{}.{}'.format(last_event_slug, settings.SITE_HOST))

        return super(BaseEventPageView, self).dispatch(request, *args, **kwargs)

    def get_posts_for_module(self, module):
        posts = module.postcategory.posts.filter(site=self.request.site)
        if self.kwargs.get('year'):
            posts = posts.filter(site=self.request.site, date__year=self.kwargs['year'])
        return (self.posts | posts).order_by('-date')

    def get_all_posts(self, modules):
        if self.request.GET.get('category'):
            try:
                modules = [Module.objects.get(site=self.request.site, title__iexact=self.request.GET.get('category')), ]
            except:
                return
        for module in modules:
            if module.type == 'POSTCATEGORY':
                self.posts = self.get_posts_for_module(module)
    
            

    def get_context_data(self, **kwargs):
        context = super(BaseEventPageView, self).get_context_data(**kwargs)

        #Checking slugs and if page is public. If it's not, user has to be staff to see it.
        if (not self.page.site.id == self.request.site.id) \
                or (not self.page.public and not self.request.user.is_staff):
            raise Http404("Requested page doesn't exist")
        header_menus = BigHeaderMenu.objects.filter(site=self.request.site).order_by('order')
        # footer_menus = self.get_footer_menus(self.event_slug)
        social_menus = SocialMediaMenu.objects.filter(site=self.request.site).order_by('order')
        # modules = Module.objects.filter(modules_in_page__page=self.page, event__slug=self.event_slug).order_by('modules_in_page__order')
        modules = Module.objects.filter(modules_in_page__page=self.page, site=self.request.site).order_by('modules_in_page__order')
        self.get_all_posts(modules)
        paginator = Paginator(self.posts, 2 )
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)
        context.update({
            'header_menus': header_menus,
            'title': self.page.title,
            # 'footer_menus': footer_menus,
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
        except:
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

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs['post_slug']

        obj = queryset.filter(slug=slug, site=self.request.site).get()
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('post_slug')
        self.post = context['post'].get(slug = slug, site=self.request.site)
        # if not self.post.event.slug == self.event_slug:
        #     raise Http404("Requested page doesn't exist")
        header_menus = BigHeaderMenu.objects.filter(site=self.request.site).order_by('order')
        # footer_menus = self.get_footer_menus(self.event_slug)
        social_menus = SocialMediaMenu.objects.filter(site=self.request.site).order_by('order')
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


class ClearCache(RedirectView): # TODO: move to admin.py?

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        Site.objects.clear_cache()
        cache.clear()
        messages.success(self.request, 'The site cache was cleared successfully.')
        return self.request.META.get('HTTP_REFERER') or reverse('admin:index') #TOFIX: use slugs

def filebrowser_browse(request):
    # slug = request.META['HTTP_HOST'].split('.')[0]
    #Temporary slug
    slug = request.site.domain
    filebrowser_site.directory = "uploads/%s/" % slug
    # Check and create folder named as the hotel id number

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
        # slug = request.META['HTTP_HOST'].split('.')[0]
        # Temporary slug
        slug = request.site.domain
        filebrowser_site.directory = "uploads/%s/" % slug
        return path_exists(filebrowser_site, filebrowser_view(getattr(globals()['filebrowser_site'], f_name)))(request)
    return f
