# Stiletto

Consider the standard django setup - gunicorn serving up django pages to nginx.

Each of these steps adds latency to your queries. It's possible that in addition, you need to query a database, which can add further latency.

To speed things up, we want to remove as many of these steps as possible. Stiletto is a tool which pre-renders some of your django views and saves the result as files.
You are then free to point nginx directly at the files.

# Usage

    # urls.py
    from stiletto import *

    ...

    static_urlpatterns = PrerenderedURLMapper([
            PreRenderedURL("foo/(?P<slug>.*).html$", foo_slug_iterator, foo, "foo")
            ], prefix= "staticmodule/")

The `foo_slug_iterator` should return an iterator which yields the slugs for which the foo view should be rendered.

    # settings.py

    STATIC_VIEW_FOLDER="/var/www/nginx/staticmodule"

Now open the shell and run the command:

    $ python manage.py compile_static_views

The views will be compiled and rendered in the folder /var/www/nginx/staticmodule.

Configuring nginx to serve the static files is your responsibility.

# Comparison to Jekyll/Hyde

At Styloot, we used Hyde for a while. Hyde is a great tool, but we ultimately found ourselves using it for the wrong thing.

The ultimate goal of Hyde, near as we can tell, is to be a replacement for Django for some use cases (e.g., blogging). What
we needed was a static page renderer which integrates with django.
