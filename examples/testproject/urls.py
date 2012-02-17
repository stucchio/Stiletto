from django.conf.urls.defaults import *
from stiletto import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^blogpost_dynamic/(?P<id>.*)$', 'myapp.views.view_blogpost', {}, 'blogpost_dynamic'),
    (r'^admin/', include(admin.site.urls)),
)

from myapp.views import view_blogpost
from myapp.models import Blogpost

def blogpost_id_iterator():
    for bp in Blogpost.objects.all():
        yield (bp.id, )

static_urlpatterns = PreRenderedURLMapper([
    PreRenderedURL("blogpost/(?P<id>.*).html$", blogpost_id_iterator, view_blogpost, "blogpost_static")
    ], prefix="pre_rendered_files/")

urlpatterns += static_urlpatterns.urls()
