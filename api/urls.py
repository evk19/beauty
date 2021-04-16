from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, EmployeeViewSet, \
    ClientViewSet, AppointmentViewSet, PurchaseViewSet, ProductViewSet, \
    ProductTypeViewSet, ServiceGroupViewSet, ServiceViewSet

router = DefaultRouter()

router.register(r'news', NewsViewSet, basename='news')
router.register(r'employees', EmployeeViewSet, basename='employees')
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'appointments', AppointmentViewSet, basename='appointments')
router.register(r'purchases', PurchaseViewSet, basename='purchases')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'product-types', ProductTypeViewSet, basename='product-types')
router.register(r'service-groups', ServiceGroupViewSet,
                basename='service-groups')
router.register(r'services', ServiceViewSet, basename='services')

urlpatterns = [
    path("", include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path("rest-auth/", include('rest_framework.urls')),
]
