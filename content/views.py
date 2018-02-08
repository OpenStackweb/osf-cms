import os

import re
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, RedirectView

from filebrowser.decorators import path_exists, get_path
from filebrowser.sites import filebrowser_view, site as filebrowser_site

from events.models import Event
from menus.models import BigHeaderMenu, FooterMenu
from content.models import Page, Module, Talk


class BaseEventView(DetailView):
	template_name = 'base.html'
	model = Page

	def __init__(self):
		super(BaseEventView, self).__init__()
		self.page = None

	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()

		slug = self.kwargs.get(self.slug_url_kwarg)

		event_slug = self.request.META['HTTP_HOST'].split('.')[0]
		obj = queryset.filter(event__slug=event_slug, slug=slug).get()
		return obj

	def get_menus(self, event_slug):
		return BigHeaderMenu.objects.filter(event__slug=event_slug).order_by('order')

	def get_footer_menus(self, event_slug):
		return FooterMenu.objects.filter(event__slug=event_slug).order_by('order')

	def dispatch(self, request, *args, **kwargs):
		self.event_slug = re.match(r'(www.)?(\w+)\.(' + re.escape(settings.SITE_HOST) + ')', self.request.META['HTTP_HOST']).group(2)
		if not self.event_slug:
			last_event_slug = Event.objects.all().last().slug
			return redirect('http://{}.{}'.format(last_event_slug, settings.SITE_HOST))

		return super(BaseEventView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(BaseEventView, self).get_context_data(**kwargs)
		if not self.page.event.slug == self.event_slug:
			raise Http404("Requested page doesn't exist")
		header_menus = BigHeaderMenu.objects.filter(event__slug=self.event_slug).order_by('order')
		footer_menus = self.get_footer_menus(self.event_slug)

		modules = Module.objects.filter(modules_in_page__page=self.page, event__slug=self.event_slug).order_by('modules_in_page__order')
		context.update({
			'header_menus': header_menus,
			'title': self.page.title,
			'footer_menus': footer_menus,
			'page' : self.page,
			'modules' : modules
		})
		return context


class HomeView(BaseEventView):

	def get_object(self, queryset=None):
		try:
			self.page = Page.objects.get(slug='', event__slug=self.event_slug)
		except:
			self.page = Page.objects.filter(event__slug=self.event_slug).first()
		return self.page


class PageView(BaseEventView):

	context_object_name = "page"

	def get_context_data(self, **kwargs):
		self.page = kwargs['object']

		return super(PageView, self).get_context_data(**kwargs)


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
