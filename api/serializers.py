from django.contrib.auth import get_user_model, password_validation
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager
from rest_framework import serializers
from .models import News, Discount, ProductType, Product, User, ServiceGroup, WorkPosition, Service, Employee, Client, Appointment, Purchase


User = get_user_model()


class EmptySerializer(serializers.Serializer):
    pass

# ============================================
# ПОЛЬЗОВАТЕЛИ
# ============================================


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "surname",
                  "date_joined", "email", "userType"]


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "surname"]


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'surname', 'password', 'userType')

# ============================================
# ГРУППА УСЛУГ
# ============================================


class ServiceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceGroup
        fields = ["id", "title", "description", "image"]


class ServiceGroupShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceGroup
        fields = ["id", "title"]

# ============================================
# УСЛУГИ
# ============================================


class ServiceSerializer(serializers.ModelSerializer):
    serviceGroup_details = UserShortSerializer(source="serviceGroup")

    class Meta:
        model = Service
        fields = ["id", "serviceGroup_details", "title",
                  "description", "image", "price", "percToEmpl"]


class ServiceShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title", "description", "price"]

# ============================================
# РАБОЧИЕ МЕСТА
# ============================================


class WorkPositionSerializer(serializers.ModelSerializer):
    serviceGroup_details = UserShortSerializer(source="serviceGroup")

    class Meta:
        model = WorkPosition
        fields = ["id", "serviceGroup_details",
                  "title", "description", "workSchedule"]


class WorkPositionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPosition
        fields = ["id", "title", "workSchedule"]


# ============================================
# НОВОСТИ
# ============================================


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "image", "description", "created_at"]


class NewsShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "created_at"]


# ============================================
# СКИДКИ
# ============================================
class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ["id", "discountAmount", "promoCode"]


# ============================================
# ТИПЫ ТОВАРОВ
# ============================================
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["id", "title", "description", "image"]


class ProductTypeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["id", "title", "image"]


# ============================================
# ТОВАРЫ
# ============================================
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "productType", "title",
                  "description", "photo", "countLeft"]


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "photo", "countLeft"]


# ============================================
# СОТРУДНИКИ
# ============================================
class EmployeeSerializer(serializers.ModelSerializer):

    user_details = UserShortSerializer(source="user")

    class Meta:
        model = Employee
        fields = ["id", "user_details", "workPosition", "photo",
                  "phone", "birthdate", "address", "employeeStatus"]


class EmployeeShortSerializer(serializers.ModelSerializer):

    user_details = UserShortSerializer(source="user")

    class Meta:
        model = Employee
        fields = ["id", "user_details", "employeeStatus"]


class EmployeeChangeStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ["employeeStatus", ]


# ============================================
# КЛИЕНТЫ
# ============================================
class ClientSerializer(serializers.ModelSerializer):

    user_details = UserCreateSerializer(source="user")

    class Meta:
        model = Client
        fields = ["id", "user_details", "birthdate",
                  "phone", "address"]


class ClientShortSerializer(serializers.ModelSerializer):

    user_details = UserShortSerializer(source="user")

    class Meta:
        model = Client
        fields = ["id", "user_details", "phone"]

# ============================================
# ЗАПИСИ
# ============================================


class AppointmentSerializer(serializers.ModelSerializer):

    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault())

    class Meta:
        model = Appointment
        fields = ["id", "client", "discount", "employee", "fullPrice",
                  "unauthorizedUser", "unauthorizedPhone", "created_at", "scheduledTime"]


class AppointmentChangeStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ["appointmentStatus", ]


class AppointmentListSerializer(serializers.ModelSerializer):

    client_details = ClientShortSerializer(source="client", read_only=True)
    employee_details = EmployeeShortSerializer(
        source="employee", read_only=True)
    discount_details = DiscountSerializer(source="discount", read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "client_details", "employee_details", "discount_details",
                  "fullPrice", "unauthorizedUser", "appointmentStatus", "created_at", "scheduledTime"]


# ============================================
# ПОКУПКИ
# ============================================
class PurchaseSerializer(serializers.ModelSerializer):

    client_details = ClientShortSerializer(source="client", read_only=True)
    product_details = ProductShortSerializer(
        source="products", read_only=True, many=True)
    # checkboxes = serializers.ListField(child=serializers.CharField(write_only=True), write_only=True)
    discount_details = DiscountSerializer(source="discount", read_only=True)

    class Meta:
        model = Purchase
        fields = ["id", "client_details", "product_details", "discount_details",
                  "unauthorizedUser", "purchaseStatus", "fullPrice", "created_at"]
