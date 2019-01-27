from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/',views.post, name='post'),
    path('<int:post_id>/new',views.new, name='new'),
    path('<int:post_id>/edit',views.edit, name='edit'),
    path('<int:author_id>/',views.author, name='author'),
    path('<int:post_id>/publish',views.publish,name='publish'),
]