from django.urls import path
from spam_detection import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('mark-spam/', views.MarkSpamView.as_view(), name='mark-spam'),
    path('search/', views.SearchView.as_view(), name='search'),
]
