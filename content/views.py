from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import DetailView

from menus.models import BigHeaderMenu
from content.models import Page, Module


class PageView(DetailView):
	template_name = "base.html"
	model = Page
	context_object_name = "page"

	def get_context_data(self, **kwargs):
		context = super(PageView, self).get_context_data(**kwargs)
		page = kwargs['object']
		header_menus = BigHeaderMenu.objects.all().order_by('order')
		modules = Module.objects.filter(modules_in_page__page=page).order_by('modules_in_page__order')
		context.update({
			'pages': header_menus,
			'title': page.title,
			'page' : page,
			'modules' : modules
		})
		return context
