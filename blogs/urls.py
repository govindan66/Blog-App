from django.urls import path
from . import views
# To view static files and images
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

app_name = 'blogs'
urlpatterns = [
       path('', views.index, name = 'Home'),
       path('about/', views.about, name='About'),
       path('contact/', views.contact, name='Contact'),
       path('signup/', views.signup_view, name = 'Signup'),
       path('login/', views.login_view, name='Login'),
       path('logout/', views.logout_view, name='Logout'),
       path('change_password/', views.change_password, name='ChangePassword'),
       path('profile/', views.profile, name = 'Profile'),
       path('addBlogs/', views.addBlogs, name='AddBlogs'),
       path('updateBlogs/<int:id>', views.updateBlogs, name='UpdateBlogs'),
       path('deleteBlogs/<int:id>', views.deleteBlogs, name='DeleteBlogs'),
       path('viewBlog/<int:id>', views.viewBlogs, name = 'ViewBlog'),
       path('blogs/', views.allBlogs, name='AllBlogs'),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
