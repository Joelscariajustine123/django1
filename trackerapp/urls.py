from django.urls import path
from .views import index,edit,ExpenseDeleteView
from django.contrib import admin
from trackerapp import views

urlpatterns = [
    path("index/",index,name='index'),
    path("edit/<int:id>/",edit,name="edit"),
    path("delete/<int:pk>/",ExpenseDeleteView.as_view(template_name='trackerapp/expense_delete.html'),name='expense_delete'),
    path('logout/', views.custom_logout, name="logout"),
    path('admin/', admin.site.urls),
    path('' , views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.custom_logout, name="logout"),
]