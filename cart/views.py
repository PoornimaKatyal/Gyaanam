from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.conf import settings
from shop.models import Books
from cart.models import Order_Details, Order_Item_Detail
from django.contrib.auth.models import User
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template import loader




def add_to_cart(request):
	print("in the cart views")
	print(request)
	print(request.session['username'])
	cart = Cart(request.session)
	book = get_object_or_404(Books, id=request.GET.get('id'))
	quantity = request.GET.get('quantity')
	discount = request.GET.get('discount', 0)
	
	price = book.price - float(discount)

	print(book.price);
	print(quantity);
	print(discount);
	print(request.session['cart_item_count'])
	
	print("before adding in cart:-")
	print(cart.count)

	cart.add(book, price, quantity)
	print("after adding in cart:-")
	print(cart.count)
	#cart_item_count = cart.count
	request.session['cart_item_count'] = cart.count
	print("after adding in session")
	print(request.session['cart_item_count'])
	data = {'is_added' : "TRUE"}
	return JsonResponse(data)



	

@login_required
def show(request):
	cart = Cart(request.session)
	if not request.user.is_authenticated:
		request.session['username']='Guest'
	else:
		request.session['username'] = request.user.username
	response = ''
	print("unique count - %s" %cart.unique_count)
	for item in cart.items:
		response += '%(quantity)s %(item)s for $%(price)s\n' % {
			'quantity': item.quantity,
			'item': item.book.title,
			'price': item.subtotal,
			
		}
		print("book id")
		print(item.book.id)
		response += 'items count: %s\n' % cart.count
		print("count - %s" %cart.count)
		response += 'unique count: %s\n' % cart.unique_count
	context = {'response' : response, 'cart' : cart}
	print("show the cart")
	print(response)
	return render(request, 'cart/show_cart.html', context)
    #return HttpResponse(response)


@login_required
def placeOrder(request):

	return render(request, 'cart/place_order.html')


@login_required
def set_quantity(request):
	print("setting the quantity")
	cart = Cart(request.session)
	book = get_object_or_404(Books, id=request.POST.get('product_id'))
	quantity = request.POST.get('quantity')
	print("set quantity of %s" %book.title)
	print(quantity)
	cart.set_quantity(book, quantity)
	return HttpResponse()

@login_required
def final_order(request):
	print("Final order")
	cart = Cart(request.session)
	if request.method == 'POST':
		firstname = request.POST.get("firstName")
		lastName = request.POST.get("lastName")
		address1 = request.POST.get("address1")
		address2 = request.POST.get("address2")
		city = request.POST.get("city")
		state = request.POST.get("state")
		pinCode = request.POST.get("zip")
		modeofpayment = request.POST.get("modeofpayment")
		totalAmount = cart.total
		userName = get_object_or_404(User, username=request.user.username)
		

		
		print(modeofpayment)
		print(firstname)
		print(lastName)
		print(address1)
		print(address2)
		print(city)
		print(state)
		print(pinCode)
		print(cart.total)
		if cart.total==0:
			return HttpResponseRedirect('/')

		order = Order_Details(username=userName, first_Name=firstname, last_Name=lastName, address1=address1, address2=address2, city=city, state=state, pincode=pinCode, mode_of_Payment=modeofpayment, order_datetime=timezone.now(), order_status='PEND', order_amount=totalAmount )
		order.save()
		print(order.order_No)
		for item in cart.items:
			book = item.book
			quantity = item.quantity
			subtotal = item.subtotal
			order_item_detail = Order_Item_Detail(order_No=order, book_Id=book, quantity=quantity, item_Amount=subtotal)
			order_item_detail.save()

		cart.clear()
		print("after clearing")
		print(cart.total)
		template = loader.get_template("cart/Thanks.html")
		context = {'order_no' : order.order_No, 'username' : userName}
		#return render(request, 'cart/Thanks.html', context)
		return HttpResponse(template.render(context, request))
	return HttpResponseRedirect('/')



