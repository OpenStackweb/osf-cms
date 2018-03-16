import re
from django import template
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.template import VariableDoesNotExist, Node
from django.urls import reverse

from content.models import Post, Page, ModuleInPage
from events.models import Event

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
    
    # Adjustment for Home page
    if path == '/%2F':
        path = '/'
    
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
    
    return ''

@register.simple_tag(name='add_vertical_separator')
def add_vertical_separator(is_last, list_style):
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

    if not col_type:
        return 'col-{}'.format(str(col_size))

    
    # 1 logo = col-12
    # para col, es 6 o 12
    # para sm es 12, 6, 4 para el resto.
    return 'col-{}-{}'.format(col_type, str(col_size))

@register.simple_tag(name='set_justify')
def set_justify(justify):
    if justify == 'CENTER':
        return ' align-center '
    elif justify == 'RIGHT':
        return ' align-right '
    return ' align-left '


# @register.simple_tag(name='get_next_talk')
# def get_next_talk(talk):
#     order = talk.order
#     next = Talk.objects.filter(order=order + 1).first()
#     if next:
#         return next.get_absolute_url()
#     return False
#
#
# @register.simple_tag(name='get_prev_talk')
# def get_prev_talk(talk):
#     order = talk.order
#     prev = Talk.objects.filter(order=order - 1).first()
#     if prev:
#         return prev.get_absolute_url()
#     return False


@register.simple_tag(name='get_sites')
def get_sites():
    return Site.objects.all()

    
# @register.simple_tag(name='get_posts_for_module')
# def get_posts_for_module(module, year):
#     postsingallery = module.post.postingallery.all()
#     posts = Post.objects.filter(postingallery__in=postsingallery)
#     if year:
#         posts = posts.filter(date__year=year)
#     return posts


@register.simple_tag(name='get_current_event')
def get_current_event(request):
    slug = request.META['HTTP_HOST'].split('.')[0]
    event = get_object_or_404(Event, slug=slug)
    return event


@register.simple_tag(name='get_videos_row')
def get_videos_row(per_row, videos):
    rows = int(videos) // int(per_row)
    if int(videos) % int(per_row):
        rows += 1
    return rows


@register.simple_tag(name='parse_youtube_link')
def parse_youtube_link(link):
    video_id = re.match(r'(https:\/\/)?(www.)?(youtube.com\/watch\?v=)(\w+)', link).group(4)
    formatted_link = 'https://www.youtube.com/embed/{}?rel=0&showinfo=0'.format(video_id)
    return formatted_link


@register.simple_tag(name='get_post_back_links')
def get_post_back_links(post):
    pages = list()
    modulesinpage = ModuleInPage.objects.filter(module__in=post.categories.all())
    for moduleinpage in modulesinpage:
        pages.append('<a href="{}">{}</a>'.format(moduleinpage.page.get_absolute_url(), moduleinpage.page.title))
    return ', '.join(pages) + ' >'\
    
    
@register.simple_tag(name='get_recent_posts')
def get_recent_posts(post):
    posts = Post.objects.exclude(id=post.id).order_by('-date')[:3]
    return posts
