# Write your tests here
from django.test import TestCase


class TestViews(TestCase):
    
    fixtures = ['db.json', ]
    
    def setUp(self):
        pass
    
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
