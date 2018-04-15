from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import Books, Author, Publisher, Genre
from cart.models import Order_Item_Detail
from django.db.models import Count
from .forms import CommentForm
from django.core.mail import send_mail
from django.conf import settings
from cart.cart import Cart



def index(request):
	print(request.session)
	if not request.user.is_authenticated:
		request.session['username']='Guest'
	else:
		request.session['username'] = request.user.username
	cart = Cart(request.session)

	request.session['cart_item_count'] = cart.count
	print(request.session['cart_item_count'])
	cart_item_count = request.session['cart_item_count']
	best_selling_books = Genre.objects.all()
	books = Order_Item_Detail.objects.values('book_Id').annotate(quantity_count=Count('quantity')).order_by('-quantity_count')[:4]
	print("top 4 bestselling books")
	print(books)
	
	context = {'cart_item_count' : cart_item_count, 'books': books}
	return render(request, 'shop/index.html', context)

def products(request):
	books = Books.objects.all()[1].language
	# books = Books.objects.order_by('-date_added')
	cart_item_count = request.session['cart_item_count']

	context = {'books' : books, 'cart_item_count' : cart_item_count}

	return render(request, 'shop/products.html', context)

def compititive(request, id):
	
	print(id)
	#print(instance)
	books = Books.objects.order_by('-date_added')
	authors = Author.objects.all()
	publishers = Publisher.objects.all()
	genres = Genre.objects.all()
	print("In compititive")
	print(request.session['cart_item_count'])
	cart_item_count = request.session['cart_item_count']

	context = {'books' : books, 'cart_item_count' : cart_item_count, 'authors' : authors, 'publishers' : publishers, 'genres' : genres}

	
	return render(request, 'shop/compititive.html', context)

def bookdetail(request, id):
	instance= get_object_or_404(Books, id=id)
	cart_item_count = request.session['cart_item_count']
	context = {'book' : instance, 'cart_item_count' : cart_item_count}	
	return render(request, 'shop/bookdetail.html', context)

def contact_us(request):
	commentform = CommentForm(request.POST or None)
	title = "Comment/Feedback Form"
	context = {'title' : title, 'commentform' : commentform}

	if commentform.is_valid():

		name = commentform.cleaned_data['name']
		comment = commentform.cleaned_data['comment']
		subject = 'Message from TurtleBasket.com'
		message = '%s %s' %(comment, name)

		emailFrom = commentform.cleaned_data['email']
		print (emailFrom)
		emailTo = [settings.EMAIL_HOST_USER] 
		send_mail(subject, message, emailFrom, emailTo, fail_silently=False)
		title = "Thanks!"
		confirm_message = "Thanks for the message. We will get right back to you."
		context = {'title' : title, 'confirm_message' : confirm_message}
	
	template = 'shop/contact_us.html'
	return render(request, template, context)


@login_required
def userProfile(request):
	user = request.user
	context = {'user' : user}
	template = 'shop/profile.html'
	return render(request, template, context)


@login_required
def user_account(request):
	user = request.user
	context = {'user' : user}
	template = 'shop/profile.html'
	return render(request, template, context)





	