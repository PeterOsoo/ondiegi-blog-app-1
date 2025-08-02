from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import BlogPost
from .serializers import BlogPostSerializer

from django.contrib import messages  
from django.core.paginator import Paginator


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BlogPostForm

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
            serializer.save(author=request.user)  # set author here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def blog_list_view(request):
    posts = BlogPost.objects.all().order_by('-created_at')

    paginator = Paginator(posts, 6)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})



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



class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content']
    template_name = 'blog/edit_post.html'

    def form_valid(self, form):
        messages.success(self.request, "✅ Post updated successfully!")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('view-post', kwargs={'pk': self.object.pk})

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog-posts')  

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "🗑️ Post deleted successfully.")
        return super().delete(request, *args, **kwargs)
