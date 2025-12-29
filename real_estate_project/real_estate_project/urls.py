"""
real_estate_project URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # URLs for the 'listings' app (homepage, property details, etc.)
    # The empty path '' means this will be the root of your site
    path('', include('listings.urls')),

    # URLs for the 'users' app (login, register, logout)
    # These are grouped under the 'accounts/' path
    path('accounts/', include('users.urls')),
]

# This is a helper for serving media files (like property images) during development.
# This is not suitable for a production environment.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
