import os

from django.apps import apps
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import DetailView, TemplateView

from filebrowser.decorators import path_exists, get_path
from filebrowser.sites import filebrowser_view, site as filebrowser_site

from menus.models import BigHeaderMenu
from content.models import Page, Module, Talk


class HomeView(TemplateView):
	template_name = 'base.html'
	model = Page

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		try:
			page = Page.objects.get(slug='')
		except:
			page = Page.objects.all().first()
		header_menus = BigHeaderMenu.objects.all().order_by('order')
		modules = Module.objects.filter(modules_in_page__page=page).order_by('modules_in_page__order')
		context.update({
			'pages': header_menus,
			'title': page.title,
			'page' : page,
			'modules' : modules
		})
		return context


class PageView(DetailView):
	template_name = "base.html"
	model = Page
	context_object_name = "page"

	def get_menus(self):
		return BigHeaderMenu.objects.all().order_by('order')

	def get_context_data(self, **kwargs):
		context = super(PageView, self).get_context_data(**kwargs)
		page = kwargs['object']
		header_menus = self.get_menus()
		modules = Module.objects.filter(modules_in_page__page=page).order_by('modules_in_page__order')
		context.update({
			'pages': header_menus,
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
		talk = kwargs['object']
		header_menus = self.get_menus()
		context.update({
			'pages': header_menus,
			'title': talk.title,
			'talk' : talk,
		})
		return context


def filebrowser_browse(request):
	slug = request.META['HTTP_HOST'].split('.')[0]
	filebrowser_site.directory = "uploads/%s/" % slug
	# Check and create folder named as the hotel id number
	asd = get_path('', site=filebrowser_site)
	dsa = os.path.exists(settings.MEDIA_ROOT + '/' + filebrowser_site.directory)
	if asd is None and \
			not dsa:
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
