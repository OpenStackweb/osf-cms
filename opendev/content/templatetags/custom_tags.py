from django import template
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
		path = reverse(name)

	if request.path == path:
		return ' active '

	return ''


@register.simple_tag(name='set_background_img')
def add_active(request, bg_image):
	""" Return the string 'active' current request.path is same as name

	Keyword aruguments:
	request  -- Django request object
	name     -- name of the url or the actual path
	by_path  -- True if name contains a url instead of url name
	"""
	if bg_image:
		style = "background: url('{}') 90% center no-repeat;".format(bg_image.url)
		return style

	return ''
