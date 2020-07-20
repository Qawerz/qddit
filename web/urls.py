from django.contrib import admin
from django.urls import path, include

from web import views

urlpatterns = [
    ########################################################################################

    path('', views.PublicationsListNew.as_view(), name="home"),
    path('top', views.PublicationsListTop.as_view(), name="home/top"),
    path('page/<int:pk>', views.PublicationDetail, name="page"),
    path('update_page/<int:pk>', views.PublicationUpdateView.as_view(), name="update_page"),
    path('delete_page/<int:pk>', views.PublicationDeleteView.as_view(), name="delete_page"),
    path('submit', views.SubmitCreateView.as_view(), name="submit"),
    path('like/$', views.like_publication, name="like_publications"),
    path('dislike/$', views.dislike_publication, name="dislike_publications"),
    # path('edit_page', views.PublicationCreateView.as_view(), name="edit_page"),

    ########################################################################################

    path('community/<str:name>', views.CommunityTemplateView.as_view(), name="community"),
    path('community/join/$', views.join_community, name="join_community"),

    ########################################################################################

    path('user/<str:username>', views.ProfileTemplateViewNew.as_view(), name="user_profile_new"),
    path('user/<str:username>/top', views.ProfileTemplateViewTop.as_view(), name="user_profile_top"),
    # path('user/<str:username>/update_profile', views.ProfileUpdateTemplateView.as_view(), name="user_profile_update"),
    path('user/<str:username>/update_profile', views.ProfileUpdate, name="user_profile_update"),
    path('login', views.MyProjectLoginView.as_view(), name="login_page"),
    path('registration', views.RegisterUserView.as_view(), name="registration_page"),
    path('logout', views.MyProjectLogout.as_view(), name="logout_page"),

    ########################################################################################

    path('reddit_clone', views.reddit_clone, name="reddit_clone"),
    path('contacts', views.contacts, name="contacts"),
    path('index', views.index),

]
