from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    """Add a product to the cart or update its quantity."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # We will get the requested quantity from the HTML form (defaulting to 1)
    # and check if the user is trying to override the exact quantity or just add to it.
    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override', False) == 'True'

    # Send the data to the brain we built earlier
    cart.add(product=product, quantity=quantity, override_quantity=override)

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Remove a product entirely from the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')


def cart_detail(request):
    """Display the contents of the cart."""
    cart = Cart(request)

    # We will pass the cart object to our HTML template soon
    return render(request, 'cart/detail.html', {'cart': cart})