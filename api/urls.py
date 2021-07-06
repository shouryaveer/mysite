from django.conf.urls import url
from .users import views as user_views
from .posts import views as post_views

urlpatterns = [
    url(r'^signup', user_views.UserRegistrationView.as_view(), name="signup-api"),
    url(r'^login', user_views.UserLoginView.as_view(), name="login-api"),
    url(r'^users', user_views.UserListView.as_view(), name="users-list-api"),
    url(r'^search', user_views.SearchView.as_view(), name="search-api"),
    url(r'^user/profile', user_views.UserProfileView.as_view(), name="user-profile-api"),
    url(r'^profile/update', user_views.UserProfileUpdateView.as_view(), name="profile-update-api"),
    url(r'^post/create', post_views.PostCreateView.as_view(), name="post-create-api"),
    url(r'^posts/list', post_views.PostsListView.as_view(), name="posts-list-api"),
    url(r'^post/(?P<pk>[^/]+)/update$', post_views.PostUpdateView.as_view(), name="post-update-api"),
    url(r'^post/(?P<post_id>[^/]+)/delete$', post_views.PostDeleteView.as_view(), name="post-delete-api"),
    url(r'^posts$', post_views.PostFeedView.as_view(), name="post-feed-api"),
    url(r'^user/(?P<user_id>[^/]+)/follow$', user_views.FollowView.as_view(), name="user-follow-api"),
    url(r'^user/(?P<user_id>[^/]+)/unfollow$', user_views.UnFollowView.as_view(), name="user-unfollow-api"),
    url(r'^post/(?P<post_id>[^/]+)/like$', post_views.PostLikeView.as_view({'post': 'create','get':'list','delete':'unlike'}), name="post-like-api"),
]