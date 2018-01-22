from django import template
from django.template import VariableDoesNotExist, Node
from django.urls import reverse

register = template.Library()


@register.simple_tag(name='add_active')
def add_active(request, name, by_path=False):
	""" Return the string 'active' current request.path is same as name

	Keyword aruguments:
	request  -- Django request object
	name     -- name of the url or the actual path
	by_path  -- True if name contains a url instead of url name
	"""
	if by_path:
		path = name
	else:
		path = reverse('page', kwargs={'slug': name})

	if request.path == path:
		return ' active '

	return ''

@register.simple_tag(name='add_horizontal_separator')
def add_horizontal_separator(list_style):
	""" Return the string 'active' current request.path is same as name

	Keyword aruguments:
	request  -- Django request object
	name     -- name of the url or the actual path
	by_path  -- True if name contains a url instead of url name
	"""
	if list_style == 'HORIZONTALSEP' or list_style == 'VERTICALHORIZONTAL':
		return ' top-side '

	return ''\


@register.simple_tag(name='add_vertical_separator')
def add_vertical_separator(is_last ,list_style):
	""" Return the string 'active' current request.path is same as name

	Keyword aruguments:
	request  -- Django request object
	name     -- name of the url or the actual path
	by_path  -- True if name contains a url instead of url name
	"""
	if (list_style == 'VERTICALSEP' or list_style == 'VERTICALHORIZONTAL') and not is_last:
		return ' left-side '

	return ''


@register.simple_tag(name='set_col_size')
def set_col_size(item_count, col_type):
	if item_count == 5:
		col_size = '5ths'
	else:
		col_size = int(12 / int(item_count))

	return 'col-{}-{}'.format(col_type, str(col_size))\


@register.simple_tag(name='set_justify')
def set_justify(justify):
	if justify == 'CENTER':
		return ' align-center '
	elif justify == 'RIGHT':
		return ' align-right '
	return ' align-left '
