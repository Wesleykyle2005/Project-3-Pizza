from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from . import models


@login_required
def index(request):
    cats = models.Category.objects.all()
    data = []
    for cat in cats:
        products = list(models.Product.objects.filter(category=cat))
        has_size = any(
            item.size
            for p in products
            for item in p.menu_items.all()
        )
        data.append((cat, products, has_size))
    return render(request, "orders/index.html", {"data": data})


@login_required
def item(request, item_id):
    try:
        item = models.MenuItem.objects.get(id=item_id)
    except models.MenuItem.DoesNotExist:
        return HttpResponseBadRequest()

    context = {}
    context["item"] = item

    if item.product.extras_category:
        context["extras_category_kind"] = item.product.extras_category.kind
        context["extras_category_name"] = item.product.extras_category.name
        context["extras"] = models.MenuItem.objects.filter(product__category=item.product.extras_category)
        if item.product.extras_amount is not None:
            context["extras_amount"] = range(item.product.extras_amount)
    return render(request, "orders/item.html", context)


@login_required
def cart(request):
    if request.method == "POST":
        order_status = request.POST["order_status"]
        if order_status == "confirm":
            selections = models.Selection.objects.filter(user=request.user, ordered=False)
            order = models.Order()
            order.save()
            for selection in selections:
                selection.ordered = True
                selection.save()
                order.selections.add(selection)
            return HttpResponseRedirect(reverse("index"))
        elif order_status == "cancel":
            selections = models.Selection.objects.filter(user=request.user, ordered=False)
            for selection in selections:
                selection.delete()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseBadRequest
    else:
        selections = models.Selection.objects.filter(user=request.user, ordered=False)
        total_sum = sum(s.total_sum() for s in selections)
    return render(request, "orders/cart.html", {"selections": selections, "total_sum": total_sum})


@login_required
def add_to_cart(request):
    try:
        items = []
        item_id = int(request.POST["item_id"])
        items += [models.MenuItem.objects.get(id=item_id)]
        for extra in request.POST.getlist("extras"):
            items += [models.MenuItem.objects.get(id=int(extra))]
    except (KeyError, ValueError, models.MenuItem.DoesNotExist):
        return HttpResponseBadRequest()

    selection = models.Selection(user=request.user)
    selection.save()
    for item in items:
        selected_item = models.SelectedItem(selection=selection, item=item)
        selected_item.save()

    return HttpResponseRedirect(reverse("cart"))
