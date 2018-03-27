# Write your tests here
from django.contrib.sites.models import Site
from django.test import TestCase, RequestFactory

from content.models import Page
from content.views import HomeView
from domains.models import SiteSettings


class TestViews(TestCase):
    
    fixtures = ['db.json', ]
    
    def setUp(self):
        self.factory = RequestFactory()

    
    def testSiteDomain(self):
        response = self.client.get('/', HTTP_HOST='katatest.io:8000', SERVER_PORT='8000')
        self.assertEqual(response.status_code, 200)
    
    def testSiteRedirectMiddleware(self):
        response_www = self.client.get('/', HTTP_HOST='www.katatest.io:8000', SERVER_PORT='8000')
        response_com = self.client.get('/', HTTP_HOST='katatest.com:8000', SERVER_PORT='8000')
        response_www_com = self.client.get('/', HTTP_HOST='www.katatest.com:8000', SERVER_PORT='8000')
        self.assertEqual(response_www.status_code, 200)
        self.assertEqual(response_com.status_code, 200)
        self.assertEqual(response_www_com.status_code, 200)

    def testSitePostSave(self):
        new_site = Site.objects.create(domain='example.com', name='Example')
        self.assertTrue(isinstance(new_site.settings, SiteSettings))

    def testSiteHomePage(self):
        new_site = Site.objects.create(domain='example.com', name='Example')
        self.assertTrue(new_site.settings.home_page is None)
        home_page = Page.objects.create(title='Home', slug='home', site_id=new_site.id)
        settings = new_site.settings
        settings.home_page = home_page
        settings.save()
        response = self.client.get('/', HTTP_HOST='example.com:8000', SERVER_PORT='8000')
        request = response.wsgi_request
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.site.settings.home_page, home_page)
