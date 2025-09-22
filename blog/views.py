# blog/views.py

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView, ListView

# Django REST Framework
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Local app
from .models import BlogPost, Category
from .serializers import BlogPostSerializer, CategorySerializer
from .forms import BlogPostForm




# ------------------ API VIEWS ------------------ #
class BlogPostListView(APIView):
    def get(self, request):
        posts = BlogPost.objects.all().order_by('-created_at')
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)


class CreateBlogPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # category_id handled automatically
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all().order_by("name")
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ------------------ HTML VIEWS ------------------ #
def blog_list_view(request):
    query = request.GET.get('q', '')  # get search query if exists
    posts = BlogPost.objects.all().order_by('-created_at')

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    paginator = Paginator(posts, 5)  # paginate
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {
        'page_obj': page_obj,
        'query': query,
    })


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, "✅ Post created successfully.")
            return redirect('blog-posts')
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/view_post.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content']
    template_name = 'blog/edit_post.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, "✅ Post updated successfully!")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse('view-post', kwargs={'slug': self.object.slug})


class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/delete_post.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('blog-posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        messages.success(self.request, "🗑️ Post deleted successfully.")
        return super().form_valid(form)



class CategoryListHTMLView(ListView):
    model = Category
    template_name = "blog/category_list.html"
    context_object_name = "categories"
    ordering = ["name"]

    def get_queryset(self):
        return Category.objects.annotate(post_count=Count("posts"))



class CategoryPostsHTMLView(ListView):
    model = BlogPost
    template_name = "blog/category_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get("slug"))
        return BlogPost.objects.filter(category=self.category).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
