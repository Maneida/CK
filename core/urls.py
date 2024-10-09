from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path("", views.index, name="index"),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path("blog/", views.blog, name="blog"),
    path("blog2/", views.blog2, name="blog2"),
    # path("blog/post/<uuid:id>/", views.post, name="post"),
    path("blog/post/<str:post_id_or_slug>/", views.post, name="post"),
]