from django.urls import path


from . import views
urlpatterns = [
    # path('', views.HomeView.as_view()),
    path('', views.UserRegistrationView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('logindd/', views.show),
    path('parse/', views.ParseFile.as_view()),
    path('upload/', views.FileUploadView.as_view()),
    path('fetch/<int:id>', views.PreviousBatchFetch.as_view())
]
