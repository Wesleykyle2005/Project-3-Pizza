import os
import django
import sys

# Configura el entorno de Django si se ejecuta directamente
if __name__ == "__main__":
    # Ajusta la ruta al directorio del proyecto si es necesario
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza.settings")
    django.setup()

from orders import models

SIZES = ("small", "large")

CATEGORIES = [
    ("Regular Pizza", "primary"),
    ("Sicilian Pizza", "primary"),
    ("Toppings", "components"),
    ("Subs", "primary"),
    ("Sub Extras", "additions"),
    ("Pasta", "primary"),
    ("Salads", "primary"),
    ("Dinner Platters", "primary"),
]
for r in CATEGORIES:
    item = models.Category(name=r[0], kind=r[1])
    item.save()

# PIZZA
REGULAR_PIZZAS = [
    ("Cheese", 14.25, 19.75, 0),
    ("1 topping", 16.25, 21.75, 1),
    ("2 toppings", 18.25, 23.75, 2),
    ("3 toppings", 20.25, 25.75, 3),
    ("Special", 22.25, 27.75, 0),
]

SICILIAN_PIZZAS = [
    ("Cheese", 26.25, 41.50, 0),
    ("1 item", 28.75, 44.50, 1),
    ("2 items", 31.25, 47.50, 2),
    ("3 items", 33.75, 50.50, 3),
    ("Special", 36.25, 53.50, 0),
]

for data, cat_name in [
    (REGULAR_PIZZAS, "Regular Pizza"),
    (SICILIAN_PIZZAS, "Sicilian Pizza"),
]:
    cat = models.Category.objects.get(name=cat_name)
    extras_category = models.Category.objects.get(name="Toppings")
    for r in data:
        product = models.Product(
            name=r[0], category=cat, extras_category=extras_category, extras_amount=r[3]
        )
        product.save()
        for size, price in zip(SIZES, (r[1], r[2])):
            item = models.MenuItem(product=product, size=size, price=price)
            item.save()

TOPPINGS = [
    "Pepperoni",
    "Sausage",
    "Mushrooms",
    "Onions",
    "Ham",
    "Canadian Bacon",
    "Pineapple",
    "Eggplant",
    "Tomato & Basil",
    "Green Peppers",
    "Hamburger",
    "Spinach",
    "Artichoke",
    "Buffalo Chicken",
    "Barbecue Chicken",
    "Anchovies",
    "Black Olives",
    "Jalapenos",
    "Fresh Garlic",
    "Zucchini"
]
cat = models.Category.objects.get(name="Toppings")
for r in TOPPINGS:
    product = models.Product(name=r, category=cat)
    product.save()
    item = models.MenuItem(product=product)
    item.save()

SUBS = [
    ("Cheese", 9.85, 11.95),
    ("Italian", 9.85, 11.95),
    ("Ham + Cheese", 9.85, 11.95),
    ("Meatball", 9.85, 11.95),
    ("Tuna", 9.85, 11.95),
    ("Turkey", 10.45, 12.45),
    ("Chicken Parmigiana", 10.95, 12.95),
    ("Eggplant Parmigiana", 9.85, 11.95),
    ("Steak", 9.95, 11.95),
    ("Steak + Cheese", 10.95, 12.95),
    ("Sausage, Peppers & Onions", None, 12.95),
    ("Hamburger", 9.45, 11.45),
    ("Cheeseburger", 10.45, 12.45),
    ("Fried Chicken", 10.95, 12.95),
    ("Veggie", 10.95, 12.95),
]
cat = models.Category.objects.get(name="Subs")
extras_category = models.Category.objects.get(name="Sub Extras")
for r in SUBS:
    product = models.Product(name=r[0], category=cat, extras_category=extras_category)
    product.save()
    for size, price in zip(SIZES, (r[1], r[2])):
        if price is not None:
            item = models.MenuItem(product=product, size=size, price=price)
            item.save()

SUB_EXTRAS = [
    ("+ Mushrooms", 1.00),
    ("+ Green Peppers", 1.00),
    ("+ Onions", 1.00),
    ("Extra Cheese on any sub", 1.00),
]
cat = models.Category.objects.get(name="Sub Extras")
for r in SUB_EXTRAS:
    product = models.Product(name=r[0], category=cat)
    product.save()
    item = models.MenuItem(product=product, price=r[1])
    item.save()

PASTAS = [
    ("Baked Ziti w/Mozzarella", 11.25),
    ("Baked Ziti w/Meatballs", 13.75),
    ("Baked Ziti w/Chicken", 14.75),
]
cat = models.Category.objects.get(name="Pasta")
for r in PASTAS:
    product = models.Product(name=r[0], category=cat)
    product.save()
    item = models.MenuItem(product=product, price=r[1])
    item.save()

SALADS = [
    ("Garden Salad", 9.95),
    ("Greek Salad", 11.45),
    ("Antipasto or Tuna", 13.25),
    ("Salad w/Chicken (breaded)", 14.75),
]
cat = models.Category.objects.get(name="Salads")
for r in SALADS:
    product = models.Product(name=r[0], category=cat)
    product.save()
    item = models.MenuItem(product=product, price=r[1])
    item.save()

DINNERPLATTERS = [
    ("Garden Salad", 40.00, 65.00),
    ("Greek Salad", 50.00, 75.00),
    ("Antipasto", 50.00, 75.00),
    ("Baked Ziti", 40.00, 65.00),
    ("Meatball Parm", 50.00, 75.00),
    ("Chicken Parm", 55.00, 85.00),
]
cat = models.Category.objects.get(name="Dinner Platters")
for r in DINNERPLATTERS:
    product = models.Product(name=r[0], category=cat)
    product.save()
    for size, price in zip(SIZES, (r[1], r[2])):
        if price is not None:
            item = models.MenuItem(product=product, size=size, price=price)
            item.save()
