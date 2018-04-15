from django.forms import ModelForm
from cart.models import Order_Details, Order_Item_Detail

class OrderDetailForm(ModelForm):
    class Meta:
        model = Order_Details
        fields = ['title', 'first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'pincode', 'mode_of_payment', 'order_amount', 'order_status', 'order_datetime' ]