"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import conf, path, include
from aplicaciones.principal.views import inicio, loginPage, logoutUser, registerPage
from aplicaciones.principal.class_view import ProductoList, CrearProducto, EditarProducto, EliminarProducto
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('aplicaciones.principal.urls')),
    #path('', login_required(ProductoList.as_view(), login_url='login'), name='index'),
    path('crearProducto', login_required(CrearProducto.as_view(),
                                         login_url='login'), name='crear_producto'),
    path('editarProducto/<int:pk>/',
         login_required(EditarProducto.as_view(),
                        login_url='login'), name='editar_producto'),
    path('eliminarProducto/<int:pk>/',
         login_required(EliminarProducto.as_view(), login_url='login'), name='eliminar_producto'),
    path('register', registerPage, name='register'),
    path('login', loginPage, name='login'),
    path('logout', logoutUser, name='logout'),

    path('test/',include('aplicaciones.tests.urls', namespace='tests'))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
