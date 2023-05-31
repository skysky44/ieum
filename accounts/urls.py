from django.urls import path
from accounts import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("update/", views.update, name="update"),
    path("password/", views.change_password, name="change_password"),
    path("profile/<username>/", views.profile, name="profile"),
    path('follow/<int:user_pk>/', views.follow, name='follow'),
    path('search/', views.search_spotify, name='search_spotify'),
    path('set_profile_music/<str:track_id>/', views.set_profile_music, name='set_profile_music'),
    path('save_track/', views.save_track, name='save_track'),
    path('delete_track/<int:track_pk>/',views.delete_track, name='delete_track'),
]
