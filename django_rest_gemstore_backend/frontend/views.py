from django.shortcuts import render,redirect
from products.models import Products
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils import timezone
import paypalrestsdk

from django.conf import settings
from django.contrib.auth.models import User

from cart.models import Cart, ProductOrder

# Create your views here.
def index(request):
    return render(request, "frontend/index.html")

def add_to_cart(request, Products_id):
    if request.user.is_authenticated():
        try:
            gem = Products.objects.get(pk=Products_id)
        except ObjectDoesNotExist:
            pass
        else:
            try:
                cart = Cart.objects.get(user=request.user,active=True)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(
                    user = request.user
                )
                cart.save()

            cart.add_to_cart(Products_id)
        return redirect('cart')
    else:
        return redirect('index')

def remove_from_cart(request,Products_id):
    if request.user.is_authenticated():
        try:
            gem = Products.objects.get(pk=Products_id)
        except ObjectDoesNotExist:
            pass
        else:
            cart = Cart.objects.get(user=request.user, active=True)
            cart.remove_from_cart(Products_id)
        return redirect('cart')
    else:
        return redirect('index')

def cart(request):
    if request.user.is_authenticated():
        cart = Cart.objects.filter(user=request.user.id, active=True)
        orders = ProductOrder.objects.filter(cart=cart)
        total = 0
        count = 0
        for order in orders:
            total += (order.product.price * order.quantity)
            count += order.quantity
        context = {
            'cart': orders,
            'total':total,
            'count':count,
        }
        return render(request, 'cart.html',context)
    else:
        return redirect('index')

 #Configure PayPal payments

def checkout(request, processor):
    if request.user.is_authenticated():
        cart = Cart.objects.filter(user=request.user.id, active=True)
        orders = ProductOrder.objects.filter(cart=cart)
        if processor == 'paypal':
            redirect_url = checkout_paypal(request,cart,orders)
            return redirect(redirect_url)

def checkout_paypal(request, cart, orders):
    if request.user.is_authenticated():
        items = []
        total = 0
        for order in orders:
            total += (order.product.price * order.quantity)
            product = order.product
            item = {
                'name': product.name,
                'sku':product.id,
                'price':str(product.price),
                'currency':'USD',
                'quantity':order.quantity
            }
            items.append(item)

        paypalrestsdk.configure({
            "mode":'sandbox',
            "client_id": 'AUqAXUGcS_J6kBaW-F6tc3pYw5ZDcwixWyi8T8oF4PGRqAmbNxlRYsDCUqzrLPu_DnSOwvWXgooxi_xm',
            "client_secret":'EAusIpJikEpE_okTySexY_00um-vmSDZ-XuUOH5bU-CyO8ynsdkmR2GEqomPuTUqN5VtuvlStZu4WI6l'})
        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {
                'payment_method': 'paypal'},
            'redirect_urls':{
                'return_url':"http://localhost:8000/process/paypal",
                'cancel_url':"http://localhost:8000/"},
            'transactions':[{
                'item_list':{
                    'items':items},
                'amount':{
                    'total':str(total),
                    'currency':'USD'},
                'description': "My Gem Store Orders"}]})
        if payment.create():
            cart_instance = cart.get()
            cart_instance.payment_id = payment.id
            cart_instance.save()
            for link in payment.links:
                if link.method == 'REDIRECT':
                    redirect_url = str(link.href)
                    return redirect_url
        else:
            return reverse('order_error')
    else:
        return redirect('index')

def order_error(request):
    if request.user.is_authenticated():
        return render(request, 'store/order_error.html')
    else:
        return redirect('index')

def process_order(request, processor):
    if request.user.is_authenticated():
        if processor == 'paypal':
            payment_id = request.GET.get('paymentId')
            cart = Cart.objects.filter(payment_id=payment_id)
            orders = ProductOrder.objects.filter(cart=cart)
            total = 0
            for order in orders:
                total += (order.product.price * order.quantity)
            context = {
                'cart':orders,
                'total': total,
            }
            return render(request, 'process_order.html', context)
    else:
         return redirect('index')

def complete_order(request, processor):
    if request.user.is_authenticated():
        cart = Cart.objects.get(user=request.user.id, active=True)
        if processor == 'paypal':
            payment = paypalrestsdk.Payment.find(cart.payment_id)
            if payment.execute({'payer_id': payment.payer.payer_info.payer_id}):
                message = "Success! Your order has been completed, and is being processed. Payment ID: %s" % (payment.id)
                cart.active = False
                cart.order_date = timezone.now()
                cart.save()
            else:
                message = "There was a problem with the transaction. Error: %s" % (payment.error.message)
            context = {
                'message':message,
            }
            return render(request, 'order_complete.html', context)
    else:
        return redirect('index')