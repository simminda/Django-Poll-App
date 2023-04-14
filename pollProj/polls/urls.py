from django.views.generic import ListView, DetailView
from django.urls import path
from .models import Post
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('polls/', views.poll, name='poll'),
    path('polls/<int:question_id>', views.detail, name='detail'),
    path('polls/<int:question_id>/results/', views.results, name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('search_polls', views.search_polls, name='search_polls'),
    # Authentication
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    # Legacy
    path('blog/', 
        ListView.as_view(
            queryset=
            Post.objects.all().order_by("-date")[:25],
            template_name="polls/blog.html"
            ), name="blog"
        ),
    path('blog/<int:pk>/',
        DetailView.as_view(
            model = Post,
            template_name="polls/post.html"
            ), name="post"
        ), 
]
