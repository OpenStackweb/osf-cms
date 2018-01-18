from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from menus.models import BigHeaderMenu
from content.models import Page, Module


def about(request):
	template = loader.get_template('base.html')
	page = Page.objects.get(title='About')
	header_menus = BigHeaderMenu.objects.all().order_by('order')
	modules = Module.objects.filter(modules_in_page__page=page).order_by('modules_in_page__order')
	context = {
		'pages': header_menus,
		'title': page.title,
		'page' : page,
		'modules': modules,
	}
	return HttpResponse(template.render(context, request))


def sponsors(request):
	template = loader.get_template('base.html')
	page = Page.objects.get(title='Sponsors')
	header_menus = BigHeaderMenu.objects.all().order_by('order')
	modules = Module.objects.filter(modules_in_page__page=page).order_by('modules_in_page__order')

	context = {
		'pages': header_menus,
		'title': page.title,
		'page' : page,
		'modules': modules,
	}
	return HttpResponse(template.render(context, request))


def schedule(request):
	template = loader.get_template('base.html')
	page = Page.objects.get(title='Schedule')
	header_menus = BigHeaderMenu.objects.all().order_by('order')
	modules = Module.objects.filter(modules_in_page__page=page).order_by('modules_in_page__order')
	context = {
		'pages': header_menus,
		'title': page.title,
		'page' : page,
		'modules' : modules,
	}
	return HttpResponse(template.render(context, request))


def videos(request):
	template = loader.get_template('base.html')
	page = Page.objects.get(title='Videos')
	header_menus = BigHeaderMenu.objects.all().order_by('order')
	context = {
		'pages': header_menus,
		'title': page.title,
		'page' : page,
	}
	return HttpResponse(template.render(context, request))


def faq (request):
	template = loader.get_template('base.html')
	page = Page.objects.get(title='FAQ')
	header_menus = BigHeaderMenu.objects.all().order_by('order')
	context = {
		'pages': header_menus,
		'title': page.title,
		'page' : page,
	}
	return HttpResponse(template.render(context, request))
