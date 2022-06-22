from .models import Task
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.generic.list import ListView
# detailview--> that returns back information about simple item
from django.views.generic.detail import DetailView
# creating a view
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# now we want to restrict a user if he didnt logged in we want to redirect a user to that login page,
# this can be done with simple decorators we can also write middleware fpr this but here i will iuse mixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# for rendering db data

# request here is listview, inheriting from list view means we have all the functionality listivew has
# this listview supposed to returned back a template with a queryset of data


class CustomLoginView(LoginView):
    template_name = 'todo_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'todo_app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

# this view is restricted if our user is not logged in it just redirect automatically so, we want to
# change that route, override into settings.py above static


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
 # i have to customized my list view and make sure that only user can only see his data
# THERE IS METHOD CALLED get context data----> we usually create a dictionary into that we throw a data by setting a key value pair
# it returns all of the data we are passing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo_app/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    # by default it will gonna look template task_form.html and also by defalut task view or create view uses model forms
    model = Task
    # list out each field that we want to show in our field
    fields = ['title', 'description', 'complete']
    # whenevr this form is submitted we want to redirect our user sucessfully to differnt page so
    # we also need to add this to our create view so for that i am going to import reverse lazy
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


# we have to go to urls of app and bcz it is a class so we have to import it differently
