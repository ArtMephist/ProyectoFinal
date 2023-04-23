from django.urls import path
from prueba import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static



app_name = 'prueba'

urlpatterns = [
    path("browse/", views.browse),
    path("index/", views.index),
    path("profile/<user>", views.profile,name = "Profile"),
    path("Details/", views.details),
    path("streams/", views.streams),
    path("login/", LoginView.as_view(template_name='Login_Final_Proyect.html'), name= "Login"),
    path("home/", views.Home, name= "home"), 
    path("register/",views.Register_Final, name="Registro"),
    path("about/", views.about),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('post/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path("detail/<int:post_id>", views.post_detail, name='detail'),
    path("edit/", views.profile_edit, name="edit"),
    path("inbox/", views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('compose/', views.compose, name='compose_with_recipient'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('avatar/', views.avatar_change, name='avatar'),
    path('postlist/', views.post_list, name='post_list'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)