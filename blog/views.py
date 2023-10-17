from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Category
from .forms import PostForm, LoginForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.generic.edit import FormView

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required(view)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return self.form_invalid(form)

class PostCreateView(CreateView, LoginRequiredMixin):
    template_name ='blog/post_edit.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        feilds = form.save(commit=False)
        feilds.author = self.request.user
        feilds.published_date = timezone.now()
        feilds.save()
        return super().form_valid(form)
    
class PostUpdateView(UpdateView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'text']

class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')

#def post_list(request):
#    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#    return render(request, 'blog/post_list.html', {'posts': posts})
#def post_detail(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    return render(request, 'blog/post_detail.html', {'post': post})
#def post_new(request):
#    if request.method == "POST":
#        form = PostForm(request.POST)
#        if form.is_valid():
#            post = form.save(commit=False)
#            post.author = request.user
#            post.published_date = timezone.now()
#            post.save()
#            return redirect('post_detail', pk=post.pk)
#    else:
#        form = PostForm()
#    return render(request, 'blog/post_edit.html', {'form': form})
#def post_edit(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    if request.method == "POST":
#        form = PostForm(request.POST, instance=post)
#        if form.is_valid():
#            post = form.save(commit=False)
#            post.author = request.user
#            post.published_date = timezone.now()
#            post.save()
#            return redirect('post_detail', pk=post.pk)
#    else:
#        form = PostForm(instance=post)
#    return render(request, 'blog/post_edit.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/cat_list.html', {'Categories': categories})