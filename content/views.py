import os

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, RedirectView

from filebrowser.decorators import path_exists, get_path
from filebrowser.sites import filebrowser_view, site as filebrowser_site

from menus.models import BigHeaderMenu, FooterMenu
from content.models import Page, Module, Talk


class HomeView(TemplateView):
	template_name = 'base.html'
	model = Page

	def get_footer_menus(self, event_slug):
		return FooterMenu.objects.filter(event__slug=event_slug).order_by('order')

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		event_slug = self.request.META['HTTP_HOST'].split('.')[0]
		try:
			page = Page.objects.get(slug='', event__slug=event_slug)
		except:
			page = Page.objects.filter(event__slug=event_slug).first()
		if not page.event.slug == event_slug:
			raise Http404("Requested page doesn't exist")
		header_menus = BigHeaderMenu.objects.filter(event__slug=event_slug).order_by('order')
		footer_menus = self.get_footer_menus(event_slug)

		modules = Module.objects.filter(modules_in_page__page=page, event__slug=event_slug).order_by('modules_in_page__order')
		context.update({
			'pages': header_menus,
			'title': page.title,
			'footer_menus': footer_menus,
			'page' : page,
			'modules' : modules
		})
		return context


class PageView(DetailView):
	template_name = "base.html"
	model = Page
	context_object_name = "page"

	def get_menus(self, event_slug):
		return BigHeaderMenu.objects.filter(event__slug=event_slug).order_by('order')

	def get_footer_menus(self, event_slug):
		return FooterMenu.objects.filter(event__slug=event_slug).order_by('order')

	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()

		slug = self.kwargs.get(self.slug_url_kwarg)

		event_slug = self.request.META['HTTP_HOST'].split('.')[0]
		obj = queryset.filter(event__slug=event_slug, slug=slug).get()
		return obj

	def get_context_data(self, **kwargs):
		context = super(PageView, self).get_context_data(**kwargs)
		event_slug = self.request.META['HTTP_HOST'].split('.')[0]
		page = kwargs['object']
		if not page.event.slug == event_slug:
			raise Http404("Requested page doesn't exist")
		header_menus = self.get_menus(event_slug)
		footer_menus = self.get_footer_menus(event_slug)
		modules = Module.objects.filter(modules_in_page__page=page, event__slug=event_slug).order_by('modules_in_page__order')
		context.update({
			'pages': header_menus,
			'footer_menus' : footer_menus,
			'title': page.title,
			'page' : page,
			'modules' : modules
		})
		return context


class TalkView(PageView):
	template_name = "talk_detail.html"
	model = Talk
	context_object_name = "talk"

	def get_context_data(self, **kwargs):
		context = super(PageView, self).get_context_data(**kwargs)
		event_slug = self.request.META['HTTP_HOST'].split('.')[0]
		talk = kwargs['object']
		if not talk.event.slug == event_slug:
			raise Http404("Requested page doesn't exist")
		header_menus = self.get_menus(event_slug)
		footer_menus = self.get_footer_menus(event_slug)

		context.update({
			'pages': header_menus,
			'footer_menus': footer_menus,
			'title': talk.title,
			'talk' : talk,
		})
		return context


class ClearCache(RedirectView): # TODO: move to admin.py?

	permanent = False
	query_string = True

	def get_redirect_url(self, *args, **kwargs):
		cache.clear()
		messages.success(self.request, 'The site cache was cleared successfully.')
		return self.request.META.get('HTTP_REFERER') or reverse('admin:index') #TOFIX: use slugs

def filebrowser_browse(request):
	slug = request.META['HTTP_HOST'].split('.')[0]
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
		slug = request.META['HTTP_HOST'].split('.')[0]
		filebrowser_site.directory = "uploads/%s/" % slug
		return path_exists(filebrowser_site, filebrowser_view(getattr(globals()['filebrowser_site'], f_name)))(request)
	return f
