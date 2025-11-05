# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Clients(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    tel_number = models.CharField(unique=True, max_length=10)
    email = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'


class ClientsOld(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    tel_number = models.CharField(max_length=10)
    email = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients_old'
        db_table_comment = 'clients data sets'


class Composition(models.Model):
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'composition'





class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.IntegerField()
    imei = models.CharField(max_length=45, blank=True, null=True)
    availability = models.ForeignKey('CompositionAvailability', models.DO_NOTHING, related_name='availability')
    
    class Status(models.TextChoices):
        NO_STATUS = "no_status", "Статус"
        RESERVED = "reserved", "Зарезервовано"
        TO_ORDER = "to_order", "Замовити"
        TO_SEND = "to_send", "Відправити"
        ORDERED = "ordered", "Замовлено"
        SENT = "sent", "Відправлено"
    status = models.CharField(max_length=16, choices=Status.choices,default=Status.NO_STATUS)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "availability"], name="unique_availability_per_order"
            )
        ]
        managed = False
        db_table = 'order_items'


class Orders(models.Model):
    class Status(models.TextChoices):
        NEW = "Нове", "Нове"
        PROCESSING = "Опрацювання", "Опрацювання"
        DELIVERY = "Доставка", "Доставка"
        READY = "Готове до видачі", "Готове до видачі"
        SUCCESS = "Успішне", "Успішне"
        CANCELED = "Відмінене", "Відмінене"
    date = models.DateTimeField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)
    client = models.ForeignKey(Clients, models.DO_NOTHING)
    composition = models.ForeignKey(Composition, models.DO_NOTHING)
    city = models.CharField(max_length=45)
    address = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'orders'


class Products(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=45)
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'products'


class ReceiptItems(models.Model):
    receipt = models.ForeignKey('Receipts', models.DO_NOTHING)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    imei = models.CharField(max_length=45, blank=True, null=True)
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'receipt_items'


class Receipts(models.Model):
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    client = models.ForeignKey(Clients, models.DO_NOTHING)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'receipts'


class Supplier(models.Model):
    name = models.CharField(max_length=45)
    city = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier'


class Supply(models.Model):
    class Status(models.TextChoices):
        ORDERED = "ordered", "Замовлено"
        RECEIVED = "received", "Прийнято"
        DELETED = "deleted", "Видалено"
    id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, models.DO_NOTHING, default=1)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ORDERED)
    composition = models.ForeignKey(Composition,models.DO_NOTHING, default=1)
    class Meta:
        managed = False
        db_table = 'supply'


class SupplyItems(models.Model):
    supply = models.ForeignKey(Supply, models.DO_NOTHING)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    imei = models.CharField(max_length=45, blank=True, null=True)
    price = models.IntegerField(default=0)
    order_item = models.ForeignKey(OrderItems, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supply_items'


class Transportations(models.Model):
    class Status(models.TextChoices):
        SENT= "sent", "Відправлено"
        RECEIVED = "received", "Отримано"
        DELETED = "deleted", "Видалено"
    date = models.DateTimeField(auto_now_add=True)
    order_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.SENT)
    update_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Composition, models.DO_NOTHING, related_name='sender')
    receiver = models.ForeignKey(Composition, models.DO_NOTHING,related_name='receiver')

    class Meta:
        managed = False
        db_table = 'transportations'

class CompositionAvailability(models.Model):
    class Status(models.TextChoices):
        IN_STOCK= "in_stock", "В наявності"
        RESERVED = "reserved", "Зарезервовано"
        TRANSPORTATION = "transportation","Транспортується"
        SOLD = "sold", "Продано"
    id = models.AutoField(primary_key=True)
    composition = models.ForeignKey(Composition, models.DO_NOTHING,related_name="availabilities")
    product = models.ForeignKey(Products, models.DO_NOTHING,related_name="products")
    quantity = models.IntegerField()
    imei = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.IN_STOCK)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'composition_availability'

class TransportationItems(models.Model):
    id = models.AutoField(primary_key=True)
    transportation = models.ForeignKey(Transportations, models.DO_NOTHING)
    product = models.ForeignKey(CompositionAvailability, models.DO_NOTHING, related_name='products')
    imei = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transportation_items'