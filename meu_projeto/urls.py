from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calculos/', include('calculos.urls')),
    path('', lambda request: HttpResponseRedirect('/calculos/')),  # Redireciona a raiz para /calculos/
]