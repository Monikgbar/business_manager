"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
    
Examples:

Function views

    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
    
Class-based views

    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    
Including another URLconf

    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    
URLs routes:

    - "path('admin/', admin.site.urls)": Display de administration page.
    - "path('', include('appointment.urls'))": Display the appointment page.
    - "path('client/', include('client.urls'))": Display the client page.
    - "path('employee/', include('employee.urls'))": Display de employee page.
    - "path('sales/', include('sales.urls'))": Display the sales page.
    - "path('service/', include('service.urls'))": Display the service page.
    - "path('stock/', include('stock.urls'))": Display the stock page.
    - "path('', lambda request: redirect('appointment:agenda'))": Redirects the root URL to the appointment agenda.
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('appointment/', include('appointment.urls', namespace='appointment')),
    path('client/', include('client.urls', namespace='client')),
    path('employee/', include('employee.urls', namespace='employee')),
    path('sales/', include('sales.urls', namespace='sales')),
    path('service/', include('service.urls', namespace='service')),
    path('stock/', include('stock.urls', namespace='stock')),
    
    # Root route redirects to the agenda
    path('', lambda request: redirect('appointment:agenda'))
] + debug_toolbar_urls()


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
