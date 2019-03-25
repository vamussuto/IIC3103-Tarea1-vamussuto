from django.urls import path, include, re_path

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("home_t1/", hello.views.home_t1, name="home_t1"),
    #path("busqueda?search_box=<texto>", hello.views.busqueda, name="busqueda"),
    path("pelicula/<url>/", hello.views.pelicula, name="pelicula"),
    path("personaje/<url>/", hello.views.personaje, name="personaje"),
    path("nave/<url>/", hello.views.nave, name="nave"),
    path("planeta/<url>/", hello.views.planeta, name="planeta"),
    path("busqueda/$", hello.views.busqueda, name="busqueda"),
    #re_path(r'^busqueda/(?P<url>\w{1,50})/$', hello.views.busqueda, name="busqueda"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
]

