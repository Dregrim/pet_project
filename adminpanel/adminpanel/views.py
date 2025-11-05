from django.shortcuts import render,redirect,get_object_or_404
from .models import Clients,Orders, Products,OrderItems, Composition,Transportations,TransportationItems,CompositionAvailability,Supply,SupplyItems
import mysqlqueries as q
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages

def clients_list(request):
    search_tel = request.GET.get("search_tel", "")
    
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        tel_number = request.POST.get("tel_number")
        email = request.POST.get("email")

        # Виклик твоєї SQL-функції
        q.create_client(first_name, last_name, tel_number, email)

        return redirect("clients_list")
    clients = Clients.objects.all()  # отримуємо всі записи з таблиці
    if search_tel:
        clients = clients.filter(tel_number__icontains=search_tel)
    return render(request, 'clients_list.html', {'clients': clients})

def delete_client_view(request, client_id):
    if request.method == "POST":
        client = Clients.objects.get(id=client_id)
        client.delete()
    return redirect("clients_list")  # повертаємося на список клієнтів

def edit_client_view(request, client_id):
    client = q.client_profile(client_id)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        tel_number = request.POST.get("tel_number")
        email = request.POST.get("email")
        q.update_client(client_id, first_name, last_name, tel_number, email)  # твоя функція для UPDATE
        return redirect("clients_list")  # назад до списку

    return render(request, "edit_client.html", {"client": client,"client_id":client_id})

def products_list(request):
    search_name = request.GET.get("search_name", "")
    
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        price = request.POST.get("price")
        Products.objects.create(
                name=name,
                category=category,
                price=price
            )
        return redirect("products")
    products = Products.objects.all()  # отримуємо всі записи з таблиці
    if search_name:
        products = products.filter(Q(name__icontains=search_name) | Q(price__icontains=search_name))
    return render(request, 'products.html', {'products': products})

def delete_product(request, product_id):
    if request.method == "POST":
        product = Products.objects.get(id=product_id)
        product.delete()
    return redirect("products_list")

def edit_product(request, product_id):
    product = Products.objects.get(id=product_id)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.category = request.POST.get("category")
        product.price = request.POST.get("price")
        product.save() 

        return redirect("products_list")  # назад до списку

    return render(request, "edit_products.html", {"product": product})

def orders_list(request):
    search_tel = request.GET.get("search_tel", "")
    
    orders = Orders.objects.select_related("client").all()  # отримуємо всі записи з таблиці
    if search_tel:
        orders = orders.filter(client__tel_number__icontains=search_tel)
    return render(request, 'orders_list.html', {'orders': orders})

def order_details(request, order_id):
    order = (
        Orders.objects.select_related("client").prefetch_related("orderitems_set","orderitems_set__product","composition").get(id=order_id)
    )
    availability = CompositionAvailability.objects.filter(composition=order.composition.id).filter(Q(status="in_stock") | Q(status="reserved", order=order))
    total_sum = sum(item.quantity * item.price for item in order.orderitems_set.all())
    statuses = ['Нове', 'Опрацювання', 'Доставка', 'Готове до видачі', 'Успішне', 'Відмінене']
    
    return render(request, 'order.html', {'order': order, 'total_sum': total_sum, 'statuses': statuses, "availability":availability})

def client_orders(request, client_id):
    orders = Orders.objects.select_related("client").all()  # отримуємо всі записи з таблиці
    orders = orders.filter(client__id__icontains=client_id)
    return render(request, 'client_orders.html', {'orders': orders, 'client_id': client_id})

def products_autocomplete(request):
    q = request.GET.get('q', '')
    products = Products.objects.filter(name__icontains=q)[:10]
    results = [{'id': p.id, 'name': p.name} for p in products]
    return JsonResponse(results, safe=False)

def delete_item(request, item_id):
    try:
        order_item = OrderItems.objects.get(id=item_id)
        try:
            availability = order_item.availability
            availability.status = "in_stock"
            availability.order = None
            availability.save()
        except OrderItems.availability.RelatedObjectDoesNotExist:
            pass

        order_id = order_item.order.id
        order_item.delete()
    except OrderItems.DoesNotExist:
        pass  # або кинути помилку
    return redirect("order", order_id=order_id)

def add_item(request, order_id):
    if request.method == "POST":
        product_id = int(request.POST.get("product"))
        quantity = int(request.POST.get("quantity", 1))
        order = get_object_or_404(Orders, id=order_id)
        product = get_object_or_404(Products, id=product_id)
        OrderItems.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price = product.price,
                status = None
            )
    return redirect("order", order_id=order_id)

def create_order(request, client_id):
    client = get_object_or_404(Clients, id=client_id)
    order = Orders.objects.create(
                date=timezone.now(),   # автоматично ставимо поточну дату/час
                status="Нове",          # або інший статус за замовчуванням
                client=client 
            )
    return redirect("order", order_id=order.id)

def change_status(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    new_status = request.GET.get("status")
    
    if new_status:
        order.status = new_status
        order.save()
    return redirect("order", order_id=order_id)

def change_composition(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    composition_id = int(request.POST.get("composition"))
    new_composition = get_object_or_404(Composition, id=composition_id)
    items = OrderItems.objects.filter(order=order)
    for i in items:
        if i.availability_id:
            i.availability.status = 'in_stock'
            i.availability.order = None 
            i.availability.save()
        i.availability = None
        i.status = i.Status.NO_STATUS
        i.imei = None
        
        i.save()
    order.composition = new_composition
    order.save()
    return redirect("order", order_id=order_id)

def change_price(request, order_id, item_id):
    item = get_object_or_404(OrderItems, id=item_id)
    new_price = int(request.POST.get("item_price"))
    item.price = new_price
    item.save()
    return redirect("order", order_id=order_id)

def compositions_autocomplete(request):
    q = request.GET.get('q', '')
    compositions = Composition.objects.filter(name__icontains=q)[:10]
    results = [{'id': c.id, 'name': c.name} for c in compositions]
    return JsonResponse(results, safe=False)

def compositions_list(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        
        Composition.objects.create(
                name = name,
                address = address
            )

        return redirect("composition_list")
    compositions = Composition.objects.all()
    return render(request, 'composition_list.html', {'compositions': compositions})

def products_availability(request, composition_id):
    products = (
        Composition.objects.prefetch_related("availabilities__product").get(id=composition_id)
    )
    return render(request, 'products_availability.html', {'products': products,"composition_id": composition_id})

def transportations(request):
    transportations = Transportations.objects.all()
    if request.method == "POST":
        sender_value = int(request.POST.get("sender"))
        receiver_value = int(request.POST.get("receiver"))
        transportation = Transportations.objects.create(
                 sender_id=sender_value,
                 receiver_id=receiver_value,
             )
        return redirect("transportation", transportation_id=transportation.id)
    return render(request, 'transportations.html', {'transportations': transportations})

def transportation(request, transportation_id):
    transportation = Transportations.objects.prefetch_related('transportationitems_set__product__product').get(id=transportation_id)
    
    return render(request, 'transportation.html', {'transportation': transportation})

def create_transportation(request):
    sender_id =  int(request.POST.get("sender"))
    receiver_id = int(request.POST.get("receiver")) 
    order_id = request.POST.get("order")

    print(sender_id,receiver_id)
    transportation = Transportations.objects.create(
        sender_id = sender_id,
        receiver_id = receiver_id,
        order_id = order_id,
    )
    return redirect("transportation", transportation_id=transportation.id)    
    

def add_transportation_item(request, transportation_id,):
    if request.method == "POST":
        product_data = request.POST.get("product")
        product_id, imei = product_data.split("|")
        print(product_id, imei)
        transportation = get_object_or_404(Transportations, id=transportation_id)
        product = get_object_or_404(CompositionAvailability, id=product_id,imei=imei)
        TransportationItems.objects.create(
        transportation_id = transportation.id,
        product_id = product_id,
        imei = product.imei
    )
    return redirect("transportation", transportation_id=transportation_id)   

def delete_transportation_item(request, transportation_id, item_id): 
    item = TransportationItems.objects.get(id=item_id)
    transportation_id = item.transportation.id
    item.delete()
    return redirect("transportation", transportation_id=transportation_id) 

def composition_autocomplete(request):
    q = request.GET.get('q', '')
    compositions = Composition.objects.filter(name__icontains=q)[:10]
    results = [{'id': p.id, 'name': p.name} for p in compositions]
    return JsonResponse(results, safe=False)

def availability_autocomplete(request):
    q = request.GET.get("q", "")
    sender_id = request.GET.get("sender_id")
    composition = get_object_or_404(Composition, id=sender_id)
    products = (
        CompositionAvailability.objects
        .filter(product__name__icontains=q)
        .select_related("product")
    )
    if sender_id:
        products = products.filter(composition_id=sender_id)
    products = products[:10]
    results = [
        {"id": f"{p.id}|{p.imei}", "text": f"{p.product.name} {p.imei}"}
        for p in products
    ]
    return JsonResponse(results, safe=False)

def change_transportation_composition(request, transportation_id):
    transportation = get_object_or_404(Transportations, id=transportation_id)
    sender_id = int(request.POST.get("sender"))
    new_sender = get_object_or_404(Composition, id=sender_id)
    receiver_id = int(request.POST.get("receiver"))
    new_receiver = get_object_or_404(Composition, id=receiver_id)
    
    if new_receiver:
        transportation.receiver = new_receiver
        transportation.save()

    if new_sender:
        transportation.sender = new_sender
        transportation.save()
    return redirect("transportation", transportation_id=transportation_id)   

def change_item_imei(request, order_id, item_id):
    order = Orders.objects.get(id=order_id)
    item = OrderItems.objects.get(id=item_id)

    if item.availability_id is not None:
        composition_availability = CompositionAvailability.objects.get(id=item.availability_id)
        composition_availability.status = composition_availability.Status.IN_STOCK
        composition_availability.order = None
        composition_availability.save()

    if request.method == "POST":
        imei = request.POST.get("imei")

        try:
            availability = CompositionAvailability.objects.get(imei=imei)

            # Перевірка на дубль
            if OrderItems.objects.filter(order=order, availability=availability).exclude(id=item.id).exists():
                messages.error(request, "❌ Цей товар вже доданий у замовлення.")
                return redirect("order", order_id=order_id)

            # оновлення
            availability.order = order
            availability.status = availability.Status.RESERVED
            item.availability = availability
            item.status = item.Status.RESERVED
            item.imei = imei
            item.save()
            availability.save()

            messages.success(request, "✅ Товар успішно змінено.")
        except CompositionAvailability.DoesNotExist:
            item.availability = None
            item.status = item.Status.NO_STATUS
            item.save()

        return redirect("order", order_id=order_id)

def change_item_status(request, item_id):
    item = OrderItems.objects.get(id=item_id)
    if request.method == "POST":
        status = request.POST.get("item_status")
        if status == 'to_order' or status == 'no_status':
            item.imei=None
            item.availability = None
        item.status = status
        item.save()
        return redirect("order", order_id=item.order.id)

def to_order(request):
    items = OrderItems.objects.filter(status='to_order')
    return render(request, 'to_order.html', {'items': items})

def supplies(request):
    supplies = Supply.objects.all()
    return render(request, 'supplies.html', {'supplies': supplies})

def supply(request, supply_id):
    supply = Supply.objects.get(id=supply_id)
    items = SupplyItems.objects.filter(supply_id=supply_id)
    return render(request, 'supply.html', {'supply': supply, 'items':items})

def create_supply(request, item_id):
    item = OrderItems.objects.get(id=item_id)
    supply = Supply.objects.create()
    add_supply_item(request, supply_id=supply.id, item_id=item.id)
    return redirect("supply", supply_id=supply.id)

def add_supply_item(request, supply_id, item_id):
    supply = Supply.objects.get(id=supply_id)
    item = OrderItems.objects.get(id=item_id)
    SupplyItems.objects.create(supply=supply,product=item.product)

    return redirect("supply", supply_id=supply.id)