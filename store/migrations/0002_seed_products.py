from django.db import migrations

PRODUCTS = [
("Wireless Headphones","Comfortable wireless Bluetooth headphones with clear sound and long battery life.",2499,25),
("Smart Watch","Fitness tracking smart watch with heart rate monitoring and notifications.",3499,18),
("Bluetooth Speaker","Portable wireless speaker with powerful sound and compact design.",1999,30),
("Laptop Backpack","Water-resistant backpack with padded laptop compartment and multiple pockets.",1499,20),
("Mechanical Keyboard","RGB mechanical keyboard designed for comfortable typing and gaming.",2999,15),
("Wireless Mouse","Ergonomic wireless mouse with adjustable DPI and long battery life.",899,40),
("USB-C Hub","Multi-port USB-C hub with HDMI, USB and card reader connectivity.",1799,22),
("Power Bank","10000 mAh fast-charging portable power bank.",1299,35),
]

def seed_products(apps, schema_editor):
    Product = apps.get_model('store','Product')
    for name, description, price, stock in PRODUCTS:
        Product.objects.get_or_create(name=name, defaults={'description':description,'price':price,'stock':stock})

def remove_products(apps, schema_editor):
    Product = apps.get_model('store','Product')
    Product.objects.filter(name__in=[p[0] for p in PRODUCTS]).delete()

class Migration(migrations.Migration):
    dependencies=[('store','0001_initial')]
    operations=[migrations.RunPython(seed_products, remove_products)]
