from django.db import models
from django.conf import settings


class Category(models.Model):
    KIND_CHOICES = (("primary", "Primary"), ("components", "Components"), ("additions", "Additions"))
    name = models.CharField(max_length=25)
    kind = models.CharField(max_length=15, choices=KIND_CHOICES, default="primary")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="products")
    extras_category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="supplemented_products", null=True)
    extras_amount = models.IntegerField(null=True)  # null means unlimited when extras_category is specified, otherwise meaningless

    def __str__(self):
        return f"{self.name}"


class MenuItem(models.Model):
    SIZE_CHOICES = (("small", "Small"), ("large", "Large"))
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="menu_items")
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        if self.product.category.kind == "primary":
            cat = self.product.category.name + " - "
        else:
            cat = ""
        if self.size:
            size = "[{}]".format(self.size[0].upper())
        else:
            size = ""
        return f"{cat}{self.product.name} {size}"




# CARTS
class Selection(models.Model):
    # an instance might consist of just a MenuItem or of a MenuItem and supplementary/component MenuItems
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField("MenuItem", through="SelectedItem")
    ordered = models.BooleanField(default=False)

    def __str__(self):
        items = self.items.all()
        main = str(items[0])
        extras = "(" + ", ".join(str(x) for x in items[1:]) + ")" if items[1:] else ""
        return main + extras

    def total_sum(self):
        return sum(filter(None, [item.price for item in self.items.all()]))


class SelectedItem(models.Model):
    item = models.ForeignKey("MenuItem", on_delete=models.CASCADE)
    selection = models.ForeignKey("Selection", on_delete=models.CASCADE)


class Order(models.Model):
    selections = models.ManyToManyField(Selection)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    finished = models.BooleanField(default=False)
