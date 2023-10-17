from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Category
from .forms import PostForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect(reverse('access_denied_page'))  # Пользователь не является автором поста
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView, AuthorRequiredMixin):
    form_class = PostForm
    template_name ='blog/post_edit.html'

    def form_valid(self, form):
        feilds = form.save(commit=False)
        feilds.author = self.request.user
        feilds.published_date = timezone.now()
        feilds.save()
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')    
class PostUpdateView(UpdateView, AuthorRequiredMixin):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'text']

@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView, AuthorRequiredMixin):
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