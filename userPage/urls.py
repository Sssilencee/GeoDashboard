from django.urls import path
from . import views


urlpatterns = [

    path('', views.Home.as_view()),

    path('login', views.Login.as_view()),
    path('logout', views.Logout.as_view()),

    path('api', views.Api.as_view()),
    # ^ Old versions wrong url address. "licenseKey" - is correct. ^
    path('invite', views.Invite.as_view()),

    path('unbind', views.Unbind.as_view()),
    path('unbindDiscord', views.UnbindDiscord.as_view())

]
