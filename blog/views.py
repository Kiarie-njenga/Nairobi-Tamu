









from django.db.models.signals import pre_save
from django.urls import reverse_lazy, reverse
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views  import View
from .forms import CommentForm, PostForm
from .models import Post, Category
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.base import TemplateView
from profiles.models import Profile, Contact
from profiles.forms import ContactForm

def post_list(request):
    posts = Post.objects.select_related('author').exclude(status='0')
    categories=Category.objects.all()
    profiles=Profile.objects.filter(is_paid=True)
    new_contact = None
    # Comment posted
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():

            # Create Comment object but don't save to database yet
            new_contact = form.save()
            # Assign the current post to the comment
           
            # Save the comment to the database
            new_contact.save()
    else:
        form = ContactForm()
    context = {'posts':posts[:49], 'categories':categories, 'profiles':profiles,'new_contact':new_contact, 'form':form}
    return render(request, 'index.html', context)


def cat_detail(request,  pk):
    category = get_object_or_404(Category, pk=pk)
    post = category.post.all()
    context = {'posts': posts, 'category': category}
    return render(request, 'category_detail.html', context)


def cat_tag_search(request, title):
    
    posts=Post.objects.select_related('author').filter(category__name=title)
    profiles=Profile.objects.select_related('user').filter(about__icontains=title)
    context={
        'posts':posts,
        'profiles':profiles,
    }
    return render(request, 'categories.html', context)
def post_detail(request, slug):
    template_name = "post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )

class BlogCreateView(CreateView):
    form_class=PostForm
    template_name='create.html'
    success_url=reverse_lazy('home')

    
    
    def form_valid(self, form):
        form.instance.author=self.request.user
        form.instance.slug=slugify(form.instance.title)
        return super().form_valid(form)

class BlogEditView(UpdateView):
    
    model=Post
    template_name='edit_blog.html'
    success_url=reverse_lazy('home')
    fields=['category','title', 'thumbnail', 'content','status']
    
        
    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class BlogDeleteView(DeleteView):
    model=Post
    
    template_name='delete_blog.html'
    success_url=reverse_lazy('home')
    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class BlogSearch(View):
    def get(self,  request, *args, **kwargs):
        query=self.request.GET.get('q')
        blogs=Blog.objects.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(created_on__icontains=query)
        )
        profiles=Profile.objects.filter(
            Q(locations__icontains=query)
        )
        context={
            'posts':posts,
            'profiles':profiles,
        }
        return render(request, 'index.html', context)


class About(TemplateView):
    template_name='about.html'

class Service(TemplateView):
    template_name='service.html'