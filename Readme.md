# Django todo App + React Front API RESTFULL
## Create et access project folder
~$  mkdir project_name
~$  cd project_name

## Create Python virtual env 
~$  python3 -m venv venv

## Activate virtual env
~$  source venv/bin/activate

## If you want to deactivate virtual env
~$  deactivate

## Install django (~= same as 3.1.*)
~$  pip install django~=3.1.0 

## New django project (from project_name folder)
~$  django-admin startproject config .

## Create app (from project_name folder)
    ~$  python manage.py startapp app_name
## Make Migrations
    ~$  python manage.py makemigrations 
    ~$  python manage.py migrate

## Create Admin unser
    ~$  python manage.py createsuperuser

## Run server
    ~$  python manage.py runserver 

## Create a requirements file that contain all your projet dependencies
    ~$  pip freeze > requirements.txt

## Install your project requirements (if a requirements file exist) 
    ~$  pip install -r requirements.txt

## Django shell (Run projet code direclty)
    ~$ python manage.py shell

## example of code to run in the shell:
 >>> from app_name.models import User
 >>> user1 = User.objects.first()

## Prepare static folders for production
    $ python manage.py collectstatic

## Take all data from app blog and export in json
    python manage.py dumpdata blog >myapp.json

## Take all data in json file and import in app data table
    python manage.py loaddata myapp.json

## Add app to settings.py
    INSTALLED_APPS = [ … , 'app_name' ]

## App templates folder
    create folder appfolder/templates/appname

## Project templates folder: 
    create folder projectname/templates

## settings.py template config
    Project templates settings.py: 
        TEMPLATES = [
            { …
                    'DIRS': [BASE_DIR / 'templates', ],
            … }

## Create Static folder: 
project_name\static\

## Static folder (settings.py): 
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [ BASE_DIR / 'static' ] 
    STATIC_ROOT = 'static_root'

## To use PostgresSQL
    pip install psycopg2
## settings.py
    DATABASE = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'blog',
            'USER': 'admin',
            'PASSWORD': '123456',
            'HOST': 'localhost',
            'PORT': '5432'


## models.py === The id fields is automaticly created by Django for each model that why it's not show below

    from django.db import models

    class Customer(models.Model)
        name = models.Charfield('Customer', max_length=120)
        age = models.IntegerField()
        note = models.TextField(blank=True, null = True)
        email = models.EmailField(max_length=255, blank=True, null=True)
        credit = models.FloatField(blank=True)
        is_active = models.BooleanField(default=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        # Select Field (return value, display value)
        TYPE_CHOICES = (
            ('Customer', 'Customer'),
            ('Supplier', 'Supplier'),
            ('Student', 'Student'),
        )
    
        type = models.CharField(choices=TYPE_CHOICES)

    class Customer(models.Model):
        name = models.Charfield('Customer', max_length=120)
        age = models.IntegerField()

    def __str__(self): 
        return self.name

## One-to-Many: (use double quotes if the entity is not yet declare) ex. "Supplier"
supplier = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.CASCADE)

## on_delete can be set to models.CASCADE, models.ST_DEFAULT or models.SET_NULL

## Many-to-Many: 
    tags = models.ManyToManyField(Tag, blank=True)

## One to One 
    User = models.OneToOneField(User, on_delete=models.CASCADE)

## Overwrite save method
    def save(self, (*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

    super().save(*args, **kwargs)

## Models
    from .models import Blog
    admin.site.register(Blog)


## Custom model Admin (admin.py): 
    class BlogAdmin(admin.ModelAdmin)
        fields = ("title", "description") # Fields to use for add/edit/show page
        list_display = ("title", "description") # fields to display in search page
        list_display_links = ("title") # fields that will be a link in search page
        ordering("date_created",) # Ordering allowed in the search page
        search_fields("title", "description") # Search fields allowed in the search page

## Register app
    admin.site.register(Blog, BlogAdmin)

## Custom model Admin (admin.py): 
    class BlogAdmin(admin.ModelAdmin)
        fields = ("title", "description") # Fields to use for add/edit/show page
        list_display = ("title", "description") # fields to display in search page
        list_display_links = ("title") # fields that will be a link in search page
        ordering("date_created",) # Ordering allowed in the search page
        search_fields("title", "description") # Search fields allowed in the search page

## Register app
    admin.site.register(Blog, BlogAdmin)

## project_folder/urls.py
    from django.contrib import admin
    from django.urls import path, include
    
    urlpatterns = [
        path('admin/', admin.site.urls), # pre-created admin urls routes
        path('', include('app_name.urls')) # include your app urls
    ]

## app_name/urls.py
    from django.urls import path
    from . import views
    
    url patterns = [ 
        path('posts', views.index, name='posts.index'),
        path('posts/create/', views.create, name='posts.create',
        path('posts/<int:id>/', views.show, name='posts.show'),
        path('posts/<int:id>/edit/', views.edit, name='posts.edit'),
        path('posts/<int:id>/delete/', views.delete, name='posts.delete'),
    ] 

## Static Route
    from django.conf import settings
    from django.conf.urls.static import static
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # views.py
    from django.shortcuts import render, redirect
    from .models import Post
    from .forms import PostForm
    
    def index(request):
        # Get all Posts
        posts = Post.objects.all()
    
        # Render app template with context
        return render(request, 'appfolder/index.html', {'posts': posts})
    
    def show(request, id):
        post = Post.objects.get(id=id)
        return render(request, 'appfolder/show.html', {'post': post})
    
    def create(request):
        form = PostForm(request.POST or None)
        if form.is_valid():
            # optionally we can access form data with form.cleaned_data['first_name']
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('/posts')
    
        return render(request, 'appfolder/create.html', {'form': form)
    
    def edit(request, id):
        post = Post.objects.get(id=id)
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/posts')
    
        return render(request, 'appfolder/edit.html', {'form': form)
    
    def delete(request, id):
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('/posts')

## Class based Views
    from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

    class LandingPageView(TemplateView):
        template_name = 'landing.html'
    
        # Optional: Change context data dict
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Landing Page'
            return context
    
    class PostsListView(ListView):
        queryset = Post.objects.all()

## Optional
    # context_object_name = "posts" (default: post_list)
    # template_name = 'posts.html' (default: posts/post_list.html) 

class PostsDetailView(DetailView):
    model = Post # object var in template

## Optional
    # template_name = 'post.html' (default: posts/post_detail.html)


    class PostsCreateView(CreateView):
        form_class = PostForm

    template_name = 'posts/post_create.html' # no default value

    def get_success_url(self):
        return reverse('posts-list')

    # Optional: Overwrite form data (before save)
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            from.instance.author = self.request.user

        return super().form_valid(form)

    class PostsUpdateView(UpdateView):
        model = Post
        form_class = PostForm
        template_name = 'posts/post_update.html'
    
        def get_success_url(self):
            return reverse('post-list')
    
        # Optional: Change context data dict
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['submit_text'] = 'Update'
            return context
    

    class PostsDeleteView(DeleteView):
        model = Post
        template_name = 'posts/post_delete.html'
        success_url = reverse_lazy('posts-list')
    
    # Urls.py route declaration
    path('<int:pk>/update/', PostsUpdateView.as_view(), name='post-update')

## app_folder/templates/app_name/*.html
    {% extends 'base.html' %}
    {% block content %}     
    {% endblock %} 
    
    {% include 'header.html' %} 
    
    {% if user.username = 'Mike' %}
        <p>Hello Admin</p>   
    {% else %}   
        <p>Hello User</p>
    {% endif %} 
    
    {% for product in products %}   
      <p>The product name is {{ product }}<p>
    {% endfor %} 
    
    {{ var_name }}
    
    Template variables formating
    {{ title | lower }} 
    {{ blog.post | truncatwords:50 }}
    {{ order.date | date:"D M Y" }}
    {{ list_items | slice:":3" }}
    {{ total | default:"nil" }}
    
    Current path (ex. posts/1/show)
    {{ request.path }}   
    
    URL by name with param
    {% url 'posts.delete' id=post.id %}
    
    Use static in template: 
    {% load static %}
    {% static 'css/main.css' %} 