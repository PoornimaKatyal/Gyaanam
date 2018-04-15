from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from cart import views

urlpatterns = [
	path('', views.add_to_cart, name='add_to_cart'),
	path('showcart/', views.show, name='show_cart'),
	path('order/', views.placeOrder, name='place_order'),
	path('set_quantity/', views.set_quantity, name='set_quantity'),
	path('final_order/', views.final_order, name='final_order'),
	
]
