from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from . import models
from . import models


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['news-list']

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):

    def items(self):
        return models.Category.objects.all()


class CompanySitemap(Sitemap):

    def items(self):
        return models.Company.objects.all()


class NewsSitemap(Sitemap):

    def items(self):
        return models.News.objects.all()