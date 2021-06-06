# Vista basada en clases
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import  Producto
from .forms import ProductForm
from django.contrib.auth.models import User


class ProductoList(ListView):
    model = Producto
    form_class = ProductForm
    template_name = 'index.html'


class CrearProducto(CreateView):
    model = Producto
    form_class = ProductForm
    template_name = 'crearProducto.html'
    success_url = reverse_lazy('index')


class EditarProducto(UpdateView):
    model = Producto
    form_class = ProductForm
    template_name = 'editarProducto.html'
    success_url = reverse_lazy('index')


class EliminarProducto(DeleteView):
    model = Producto
    template_name = 'verificacion.html'
    success_url = reverse_lazy('index')
