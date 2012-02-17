# Stiletto

Consider the standard django setup - gunicorn serving up django pages to nginx.

Each of these steps adds latency to your queries. Querying a database will can add further latency.

To speed things up, we want to remove as many of these steps as possible. Stiletto is a tool which pre-renders some of your django views and saves the result as files.
You are then free to point nginx directly at the files.

# Installation

Standard installation:

    $ python setup.py install

# Usage

## Django Setup

Your Stiletto configuration lives in urls.py:

    # urls.py
    from stiletto import *

    ...

    static_urlpatterns = PrerenderedURLMapper([
            PreRenderedURL("foo/(?P<slug>.*).html$", foo_slug_iterator, foo, "foo")
            ], prefix="pre_rendered_files/")

    urlpatterns += static_urlpatterns.urls()

The `foo_slug_iterator` should return an iterator which yields the slugs for which the foo view should be rendered.

The line `urlpatterns += static_urlpatterns.urls()` is necessary so that the `{% url "foo" %}` tag works properly, in both static and dynamic pages.
The result of `{% url "foo" "slug" %}` will be `/"pre_rendered_files/foo/slug`.

    # settings.py

    STATIC_VIEW_FOLDER="/var/www/nginx/staticmodule"

Now open the shell and run the command:

    $ python manage.py compile_static_views

The views will then be compiled and rendered in the folder /var/www/nginx/staticmodule.

## App URL modules

If you want to include the URL's from a module (as is done in normal python url routing with the `include` directive), you need
to use the include method:

    # urls.py
    static_urlpatterns = PrerenderedURLMapper(...)

    static_urlpatterns.include("appname", appname.urls.static_urlpatterns)

## Webserver configuration

Configuring nginx to serve the static files is your responsibility - obviously a django module has no ability to control this.
In Nginx, for example, you might do something like this:

    # nginx.conf
    location ^~ /pre_rendered_files/ {
        expires       15m;
	add_header Cache-Control public;
	alias /var/www/nginx/staticmodule/pre_rendered_files;
    }

In production you probably want to use [gzip](http://wiki.nginx.org/HttpGzipModule) or [gzip_static](http://wiki.nginx.org/HttpGzipStaticModule).


# FAQ

## What does "Stiletto" refer to?

At styloot, most of our projects are named after fashion items. This project is named after [Stiletto Heels](http://en.wikipedia.org/wiki/Stiletto_heel).

Note that we *strongly discourage* the use of high heeled shoes since they are harmful to the body.

## How does Stiletto compare to Hyde/Jekyll

At Styloot, we used Hyde for a while. Hyde is a great tool, but we ultimately found ourselves using it for purposes it was not meant for.

The ultimate goal of Hyde, near as we can tell, is to be a *replacement* for Django for some use cases (e.g., blogging). What
we needed was a static page renderer which *integrates* with django. Using Hyde involved too much duplication - one set of templates
for static pages, another for django.

For this reason, we build Stiletto for pthe purposes of integration.

