from django.urls import path

from . import views


app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_list, name='group_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('create/', views.recipe_create, name='recipe_create'),
    path('recipes/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipes/<int:pecipe_id>/comment/', views.add_comment, name='add_comment'),
    path('follow/', views.follow_index, name='follow_index'),
    path('profile/<str:username>/follow/', views.profile_follow, name='profile_follow'),
    path('profile/<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow'),
]
