from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view()),
    path('login', views.Login.as_view()),
    path('logout', views.Logout.as_view()),
    path('delete', views.Delete.as_view()),
    path('deleteInvite', views.DeleteInvite.as_view()),
    path('deleteDiscord', views.DeleteDiscord.as_view())
]
