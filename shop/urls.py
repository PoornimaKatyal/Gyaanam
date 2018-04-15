from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cart import views as cart_views

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('products/', views.products, name='products'),
	path('compititive/<id>/', views.compititive, name='compititive'),
	path('bookdetail/<int:id>/', views.bookdetail, name='bookdetail'),
	path('contact_us/', views.contact_us, name='contact_us'),
	path('profile/', views.userProfile, name='profile'),
	path('add_to_cart/', cart_views.add_to_cart, name='add_to_cart'),
	path('showcart/', cart_views.show, name='show_cart'),
	path('user_account/', views.user_account, name='user_account'),


]
