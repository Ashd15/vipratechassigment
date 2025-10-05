from decimal import Decimal
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import uuid

from .models import Product, Order
from .forms import QuantityForm

# -------------------
# Mock Stripe Setup
# -------------------
class MockStripeSession:
    def __init__(self, id, url):
        self.id = id
        self.url = url
        self.payment_status = 'paid'  # Always paid for mock

class MockStripe:
    @staticmethod
    def create(**kwargs):
        # Generate a unique session id for every checkout
        session_id = str(uuid.uuid4())
        return MockStripeSession(
            id=session_id,
            url=f"{kwargs.get('success_url')}?session_id={session_id}"  # append session_id
        )

stripe = MockStripe()  # Use this mock instead of real Stripe

# -------------------
# Views
# -------------------
def index(request):
    products = Product.objects.all()
    paid_orders = Order.objects.filter(paid=True).order_by('-created_at')
    form = QuantityForm()
    return render(request, 'shop/index.html', {
        'products': products,
        'orders': paid_orders,
        'form': form,
        'stripe_publishable_key': 'pk_test_mock',  # mock key
    })

@require_POST
def create_checkout_session(request):
    form = QuantityForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest('Invalid input')

    product_id = form.cleaned_data['product_id']
    quantity = form.cleaned_data['quantity']

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return HttpResponseBadRequest('Product not found')

    total_amount = product.price * quantity

    # Use mocked Stripe session with unique session_id
    success_url = request.build_absolute_uri(reverse('shop:success'))
    session = stripe.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {'name': product.name},
                'unit_amount': int((product.price * Decimal('100')).to_integral_value()),
            },
            'quantity': quantity,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=request.build_absolute_uri(reverse('shop:index')),
    )

    # Create new order for each checkout session
    order = Order.objects.create(
        checkout_session_id=session.id,
        product=product,
        quantity=quantity,
        total_amount=total_amount,
        paid=True,  # always paid in mock
    )

    return redirect(session.url)

def success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('shop:index')

    try:
        order = Order.objects.get(checkout_session_id=session_id)
    except Order.DoesNotExist:
        order = None

    return render(request, 'shop/success.html', {'order': order})

@csrf_exempt
def stripe_webhook(request):
    # Skip real webhook handling in mock
    return HttpResponse(status=200)
