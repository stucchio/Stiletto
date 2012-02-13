# Stiletto

Consider the standard django setup - gunicorn serving up django pages to nginx.

Each of these steps adds latency to your queries. Querying a database will can add further latency.

To speed things up, we want to remove as many of these steps as possible. Stiletto is a tool which pre-renders some of your django views and saves the result as files.
You are then free to point nginx directly at the files.

# Usage

    # urls.py
    from stiletto import *

    ...

    static_urlpatterns = PrerenderedURLMapper([
            PreRenderedURL("foo/(?P<slug>.*).html$", foo_slug_iterator, foo, "foo")
            ], prefix="staticmodule/")

    urlpatterns += static_urlpatterns.urls()

The `foo_slug_iterator` should return an iterator which yields the slugs for which the foo view should be rendered.

The line `urlpatterns += static_urlpatterns.urls()` is necessary so that the `{% url "foo" %} tag works properly, in both static and dynamic pages.
The result of `{% url "foo" "slug" %}` will be `/staticmodule/foo/slug`.

    # settings.py

    STATIC_VIEW_FOLDER="/var/www/nginx/staticmodule"

Now open the shell and run the command:

    $ python manage.py compile_static_views

The views will then be compiled and rendered in the folder /var/www/nginx/staticmodule.

Configuring nginx to serve the static files is your responsibility.

## App URL modules

If you want to include the URL's from a module (as is done in normal python url routing with the `include` directive), you need
to use the include method:

    # urls.py
    static_urlpatterns = PrerenderedURLMapper(...)

    static_urlpatterns.include("appname", appname.urls.static_urlpatterns)



# Comparison to Jekyll/Hyde

At Styloot, we used Hyde for a while. Hyde is a great tool, but we ultimately found ourselves using it for the wrong thing.

The ultimate goal of Hyde, near as we can tell, is to be a replacement for Django for some use cases (e.g., blogging). What
we needed was a static page renderer which integrates with django. Using Hyde involved too much duplication - one set of templates
for static pages, another for django.

In contrast, the goal of Stiletto is to *integrate* with Django. All content is shared.
