














from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField
STATUS = ((0, "Draft"), (1, "Publish"))
from django.urls import reverse





User=get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=200, default='', blank=True)
    

    class Meta:
        
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Post(models.Model):
    category = models.ForeignKey(Category,null=True, blank=True, related_name='products',
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    thumbnail=models.ImageField(upload_to='blogs/', default='stories/default.png', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        

        return reverse("post_detail", kwargs={"slug": str(self.slug)})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)
