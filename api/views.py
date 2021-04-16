from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, password_validation, logout, authenticate
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from .utils import get_and_authenticate_user, create_user_account
from .serializers import EmptySerializer, ServiceGroupSerializer, ServiceGroupShortSerializer, ServiceSerializer, ServiceShortSerializer, WorkPositionSerializer, WorkPositionShortSerializer, UserSerializer, UserShortSerializer, UserCreateSerializer, NewsSerializer, NewsShortSerializer, DiscountSerializer, ProductTypeSerializer, ProductTypeShortSerializer, ProductSerializer, ProductShortSerializer, EmployeeSerializer, EmployeeShortSerializer, EmployeeChangeStatusSerializer, ClientSerializer, ClientShortSerializer, AppointmentSerializer, AppointmentChangeStatusSerializer, AppointmentListSerializer, PurchaseSerializer

from .models import News, Discount, ProductType, Product, User, ServiceGroup, WorkPosition, Service, Employee, Client, Appointment, Purchase

User = get_user_model()

# ============================================
# НОВОСТИ
# ============================================


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().filter(status__in=['published', ],)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsShortSerializer
        elif self.action == 'retrieve':
            return NewsSerializer
        else:
            return EmptySerializer

    def create(self, request, pk=None):
        content = {
            'NotAllowed': 'Создание новости доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        content = {
            'NotAllowed': 'Удаление новости доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        content = {
            'NotAllowed': 'Изменение новости доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)


# ============================================
# СОТРУДНИКИ
# ============================================


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'update':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeShortSerializer
        elif self.action == 'retrieve':
            return EmployeeSerializer
        elif self.action == 'update':
            return EmployeeChangeStatusSerializer
        else:
            return EmptySerializer

    def create(self, request, pk=None):
        content = {
            'NotAllowed': 'Создание сотрудника доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        content = {
            'NotAllowed': 'Удаление сотрудника доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)


# ============================================
# КЛИЕНТЫ
# ============================================

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return ClientShortSerializer
        elif self.action == 'create':
            return ClientSerializer
        elif self.action == 'retrieve':
            return ClientSerializer
        else:
            return EmptySerializer

    # def create(self, request, pk=None):
    #     content = {
    #         'NotAllowed': 'Создание оператора доступно только в админ панели'}
    #     return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        content = {
            'NotAllowed': 'Удаление клиента доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

# ============================================
# ЗАПИСИ
# ============================================


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AppointmentListSerializer
        elif self.action == 'update':
            return AppointmentChangeStatusSerializer
        else:
            return AppointmentSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def destroy(self, request, pk=None):
        content = {
            'NotAllowed': 'Удаление записи доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)


# ============================================
# ПОКУПКИ
# ============================================


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()

    def get_serializer_class(self):
        return PurchaseSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, pk=None):
        content = {
            'NotAllowed': 'Создание покупки доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        content = {
            'NotAllowed': 'Удаление покупки доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

# ============================================
# ТОВАРЫ
# ============================================


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductShortSerializer
        if self.action == 'retrieve':
            return ProductSerializer
        else:
            return EmptySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, pk=None):
        content = {
            'NotAllowed': 'Создание товара доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        content = {
            'NotAllowed': 'Удаление товара доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

# ============================================
# ТИПЫ ТОВАРОВ
# ============================================


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductTypeShortSerializer
        if self.action == 'retrieve':
            return ProductTypeSerializer
        else:
            return EmptySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, pk=None):
        content = {
            'NotAllowed': 'Создание типа товара доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        content = {
            'NotAllowed': 'Удаление типа товара доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)


# ============================================
# ГРУППА УСЛУГ
# ============================================


class ServiceGroupViewSet(viewsets.ModelViewSet):
    queryset = ServiceGroup.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceGroupShortSerializer
        if self.action == 'retrieve':
            return ServiceGroupSerializer
        else:
            return EmptySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, pk=None):
        content = {
            'NotAllowed': 'Создание группы услуг доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        content = {
            'NotAllowed': 'Удаление группы услуг доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

# ============================================
# УСЛУГИ
# ============================================


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceShortSerializer
        if self.action == 'retrieve':
            return ServiceSerializer
        else:
            return EmptySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, pk=None):
        content = {
            'NotAllowed': 'Создание услуги доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        content = {
            'NotAllowed': 'Удаление услуги доступно только в админ панели'}
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)
