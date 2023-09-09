from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,DeleteView,DetailView,CreateView,UpdateView,FormView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm #already create form ,as soon as form submitted it will create a User for us 
from django.contrib.auth import login
from django.shortcuts import redirect

# we will use class based views 

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields='__all__'
    redirect_authenticated_user=True
    def get_success_url(self): # will return them to home page i mean task list view here
        return reverse_lazy('tasks')

#no need to create the logout view explicitly,in urls.py it can be automatically added if we call LogoutView  

class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        # Save the user object but do not log in automatically
        user = form.save(commit=False)

        # Set the user's password (you need to do this because it's not included in `commit=False`)
        user.set_password(form.cleaned_data['password1'])
        user.save()

        # Log in the user
        login(self.request, user)

        return redirect('tasks')

class TaskList(LoginRequiredMixin,ListView):
    model = Task 
    context_object_name='tasks'

    def get_queryset(self):
        # Only retrieve tasks for the currently logged-in user
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self,**kwargs):
        #we are trying to update default provided context dict by adding count 
        context=super().get_context_data(**kwargs)#here we are calling get_context_data method of parent class
        context['count']=context['tasks'].filter(complete=False).count()
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__icontains=search_input)
        context['search_input']=search_input #to throw search input value in template0    
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=fields=['title','description','complete'] # create view will automatically create a form for us based on our Task model
    #this below code ensures that the user field of the task is set to the currently logged-in user before saving it.
    def form_valid(self, form): 
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

    success_url=reverse_lazy('tasks') #automatically redirect to Tasklist page 

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')
