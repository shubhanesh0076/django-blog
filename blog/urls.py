from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from .  import views 
from django.contrib.auth import views as auth_views




urlpatterns = [
    path("", views.landing, name='landing'),
    
    path('signin/', views.signIn, name='signIn'),
    path('signup/', views.signUp, name='signUp'),
    path('logout', views.signOut, name='logout'),
    path('error_404', views.error_404, name='error_404'),
    path('about/', views.about, name='about'),
    path('blog', views.blog, name='blog'),
    path('contactus', views.contactus, name='contactus'),
    path('post_blog', views.Post_blog, name='post_blog'),
    path('search/', views.search, name='search'),
    path('postComment', views.postComment, name="postComment"),
    path('userprofile/', views.userprofile, name="userprofile"),
    path('profileinfoform', views.profileinfoform, name='profileinfoform'),
    path('like/', views.like_post, name='like_post'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('<slug:slug>/', views.Detail_view, name='detail_view'),
    path('<slug:slug_cat>/', views.filter_post, name="post" ),
    path('edit_blog/<int:id>/', views.Edit_bl, name='edit_blog'),
    path('delete/<int:id>/', views.Delete_blog, name='delete'),
    path('publicuserprofile/<int:id>/', views.publicuserprofile, name='publicuserprofile'),
    path('review/<int:id>/', views.review, name='review'), 
    

    # path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    # path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    # path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]

