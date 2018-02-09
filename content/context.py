from django.urls import reverse
from django.utils.safestring import mark_safe

from content.models import Page


class UrlReverser:

    @classmethod
    def reverse_content(cls, obj):
        model = obj._meta.model_name
        return reverse('admin:content_' + model + '_change', args=(obj.id,))


class ContextManager:

    @classmethod
    def generate_pages_string(cls, instance):
        pages_str_list = list()
        pages = Page.objects.filter(modules_in_page__module=instance)
        if pages:
            for page in pages:
                rev = UrlReverser.reverse_content(page)
                page_str = mark_safe('<a href="%s">%s</a>' % (rev, page.title))
                pages_str_list.append(page_str)
        return 'Pages: ', ', '.join(pages_str_list)


    @classmethod
    def generate_context(cls, *args):
        first = True
        context_str = ''
        for title, item in args:
            if item:
                if not first:
                    context_str += ' / '
                else:
                    context_str += title + item
                first = False
        if not context_str:
            context_str = 'Not included anywhere.'
        return context_str