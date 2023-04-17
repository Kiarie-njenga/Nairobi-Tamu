











from django.contrib.sitemaps import Sitemap

from .models import Post
from profiles.models import Profile

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.updated_on


class ProfileSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Profile.objects.all()

    def lastmod(self, obj):
        return obj.created_on

    # def location(self, item):
    #     return reverse(item)
