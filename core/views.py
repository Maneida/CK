from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Post, Category, Tag
from typing import Dict

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import DatabaseError
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.db.models import Count
import uuid


# Create your views here.
def index(request):
    return render(request, 'core/base.html')

def blog(request):
    try:
        # Retrieve all posts
        posts_list = Post.objects.all()
        
        if not posts_list:
            return HttpResponse("No posts found.", status=404)

        # Create a Paginator object
        paginator = Paginator(posts_list, 10)  # Show 10 posts per page
        
        # Get the desired page number from the request
        page_number = request.GET.get('page', 1)
        
        try:
            # Get the page object for the current page number
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            return HttpResponseNotFound("The page number is out of range.")
        except PageNotAnInteger:
            return HttpResponseBadRequest("The page number is not an integer.")
        
        # Render the posts to a template
        return render(request, 'core/blog.html', {'page_obj': page_obj})

    except DatabaseError as e:
        # Log the error if needed
        print(f"Database error occurred: {e}")
        return HttpResponse("A database error occurred. Please try again later.", status=500)

    except Exception as e:
        # Log the error if needed
        print(f"An unexpected error occurred: {e}")
        return HttpResponse("An unexpected error occurred. Please try again later.", status=500)




def post(request, post_id_or_slug) -> Dict[str, str]:
    try:
        # First, try to get the post by UUID
        post_id = uuid.UUID(post_id_or_slug)
        post = get_object_or_404(Post, id=post_id)
    except ValueError:
        # If it's not a valid UUID, try to get the post by slug
        post = get_object_or_404(Post, slug=post_id_or_slug)
    category = post.category_name
    post = post.to_dict()
    post["category_name"] = category
    return render(request, 'core/post.html', {'post': post})

def blog2(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    
    blog_posts = Post.objects.all().order_by('-created_at')
    
    if query:
        blog_posts = blog_posts.filter(title__icontains=query)
    if category_slug:
        blog_posts = blog_posts.filter(category__slug=category_slug)
    if tag_slug:
        blog_posts = blog_posts.filter(tags__slug=tag_slug)
        
    categories = Category.objects.annotate(post_count=Count('posts'))
    tags = Tag.objects.annotate(post_count=Count('posts'))
    
    paginator = Paginator(blog_posts, 4)  # Show 4 blog posts per page
    
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Calculate the range of pages to display
    max_pages = 5
    current_page = posts.number
    page_range = list(range(max(1, current_page - 2), min(paginator.num_pages + 1, current_page + 3)))
    
    # Add first and last page if they're not already in the range
    if 1 not in page_range:
        page_range.insert(0, 1)
        if 2 not in page_range:
            page_range.insert(1, '...')
    if paginator.num_pages not in page_range:
        if paginator.num_pages - 1 not in page_range:
            page_range.append('...')
        page_range.append(paginator.num_pages)
        
    context = {
        'posts': posts,
        'total_post_count': blog_posts.count(),
        'page_range': page_range,
        'category_count': {category.name: category for category in categories},
        'categories': categories,
        'tags': tags,
        'tag_count': {tag: tag.post_count for tag in tags},
        'current_category': category_slug,
        'current_tag': tag_slug,
        'query': query,
    }
    return render(request, 'core/blog2.html', context)
