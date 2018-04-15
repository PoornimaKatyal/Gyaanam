from django.db import models
from django.forms import ModelForm
from shop.models import Books
from django.contrib.auth.models import User
from django.utils import timezone
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save


TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

ORDER_STATUS = (
    ('PEND', 'Pending'),
    ('DISP', 'Dispatched'),
    ('DELI', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
    ('REFUNDED', 'Refunded'),
)

class Order_Details(models.Model):
	order_No = models.CharField(max_length=120, blank=True)
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=3, choices=TITLE_CHOICES, default='MR')
	first_Name = models.CharField(max_length=50)
	last_Name = models.CharField(max_length=50)
	address1 = models.CharField(max_length=150)
	address2 = models.CharField(max_length=150)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	pincode = models.IntegerField(blank=True, null=True)
	order_datetime = models.DateTimeField(default=timezone.now)
	order_status = models.CharField(max_length=4, choices=ORDER_STATUS, default='PEND')
	order_amount = models.FloatField(blank=True, null=True)
	mode_of_Payment = models.CharField(max_length=50)

	

	def __str__(self):
		return 'Order_No: {}, User: {}'.format(self.order_No, self.username)

	
	def pre_save_create_order_id(sender, instance, *args, **kwargs):
		if not instance.order_No:
			instance.order_No= unique_order_id_generator(instance)

pre_save.connect(Order_Details.pre_save_create_order_id, sender=Order_Details)






class Order_Item_Detail(models.Model):
	order_No = models.ForeignKey(Order_Details, on_delete=models.CASCADE)
	book_Id = models.ForeignKey(Books, on_delete=models.CASCADE)
	quantity = models.IntegerField(blank=True, null=True)
	item_Amount = models.FloatField(blank=True, null=True)



