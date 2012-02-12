from django.core.urlresolvers import reverse, resolve
from django.conf.urls.defaults import patterns, url, include

import os
import imp
import uuid
import copy

import logging
log = logging.getLogger(__name__)

class StilettoURLPrerenderedException(Exception):
    pass

def __null_view__(request, *args, **kwargs):
    raise StilettoURLPrerenderedException("The page " + request.path + " was rendered by Django, rather than served by the static webserver. This should never occur.")

class PreRenderedURL(object):
    def __init__(self, pattern, param_iterator, view, name):
        self.pattern = pattern
        self.param_iterator = param_iterator
        self.view = view
        self.name = name

    def url(self):
        return url(self.pattern, self.view, name=self.name)

    def __call_view__(self, reversed, urlconf):
        url_resolution = resolve(reversed, urlconf)
        return url_resolution.func(None, *url_resolution.args, **url_resolution.kwargs)

    def render(self, urlconf, output_path = ""):
        log.info('Rendering urls mapped by "' + self.pattern + '"')
        rendered_paths = []
        for p in self.param_iterator():
            path = reverse(self.name, urlconf, args=p)
            output_file_path = os.path.join(output_path, path[1:])

            #Ensure outputdir exists
            dirname = os.path.split(output_file_path)[0]
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            #Write results
            with open(output_file_path, 'w') as outfile:
                outfile.write(self.__call_view__(path, urlconf).content)
            log.info("Rendered view " + self.name + " with args " + str(p) + " to path " + output_file_path)
            rendered_paths.append(path)
            #Do actual rendering here
        return rendered_paths

class PreRenderedURLMapper(object):
    def __init__(self, mapping, prefix):
        self.mapping = mapping
        self.prefix = prefix

    def urls(self):
        return [m.url() for m in self.mapping]

    def include(self, prefix, other):
        for m in other.mapping:
            mcp = copy.deepcopy(m)
            mcp.pattern = os.path.join(prefix, mcp.pattern)
            self.mapping.append(mcp)

    def __urlconf__(self):
        module = imp.new_module("stiletto_url_" + str(uuid.uuid4()).replace("-","_"))
        inner_module = imp.new_module("stiletto_url_" + str(uuid.uuid4()).replace("-","_"))
        inner_module.urlpatterns = patterns( '', *self.urls() )
        module.urlpatterns = patterns('', (self.prefix, include(inner_module)))
        return module

    def render(self, output_path):
        urlconf = self.__urlconf__()
        for m in self.mapping:
            m.render(urlconf, output_path)


if __name__ == "__main__":
    from django.http import HttpResponse
    def foo(request, slug):
        return slug
        #return HttpResponse(str(foo), content_type="application/xhtml+xml")

    def buz(request, slug):
        return slug + " -> " + slug

    mapper = PrerenderedURLMapper([ PreRenderedURL("foo/(?P<slug>.*).html$", lambda: ( (x,) for x in range(25)), foo, "foo") ], prefix= "staticmodule/")
    mapper2 = PrerenderedURLMapper([ PreRenderedURL("buz/(?P<slug>.*).html$", lambda: ( (x,) for x in range(12)), buz, "buz") ], prefix= "staticmodule/")
    mapper.include("prefix", mapper2)
    mapper.render("/tmp/stiletto")