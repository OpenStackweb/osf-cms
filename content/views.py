from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import DetailView, TemplateView

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
