from django.urls import path
from .views import (
    PostList, PostDetail,
    PostCreate, CommentList,
    CommentDetail, CommentCreate,
    PostDetailUser, PostUpdate,
    PostDelete, CommentDelete,
    user_posts, user_comments,
    accept_comment, SearchPost
)

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', SearchPost.as_view(), name='search_post'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/comment_create/', CommentCreate.as_view(), name='comment_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/comment_delete/', CommentDelete.as_view(), name='comment_delete'),
    path('post_user/<int:pk>/', PostDetailUser.as_view(), name='post_user'),
    path('comments/', CommentList.as_view(), name='comment_list'),
    path('comment/<int:pk>/', CommentDetail.as_view(), name='comment'),
    path('user_posts/', user_posts, name='user_posts'),
    path('user_comments/', user_comments, name='user_comments'),
    path('accept_comment/<int:pk>/', accept_comment, name='accept_comment')
]
