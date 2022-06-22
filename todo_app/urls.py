#from django.contrib import admin
from django.urls import path

from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage
# logout view does not required post method
from django.contrib.auth.views import LogoutView

# our url resolver cant use a class inside of it so we are gonna use this method as_viewfunction--
# ->going to trigger a function inside of that view function depending on the method type  so if it
# is post or get request now it knows what to do
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', TaskList.as_view(), name='tasks'),
    # view by default looks for the primary key i.e. pk value
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
]
