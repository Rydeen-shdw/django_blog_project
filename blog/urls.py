from django.urls import path

from blog import views

app_name = 'blog'


urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('post/<slug:post_slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/comment/', views.post_comment_view, name='post_comment'),
    path('post/<int:post_id>/like/', views.post_like_view, name='post_like'),
    path('post/<int:post_id>/dislike/', views.post_dislike_view, name='post_dislike'),
    path('post/comment/<int:comment_id>/like/', views.comment_like_view, name='comment_like'),
    path('post/comment/<int:comment_id>/dislike/', views.comment_dislike_view, name='comment_dislike'),
    path('post/comment/disabling/<int:comment_id>/', views.comment_disable_view, name='comment_disabling'),
    path('post/comment/delete/<int:comment_id>', views.comment_delete_view, name='comment_delete'),

]
