from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import News, Discount, ProductType, Product, User, ServiceGroup, WorkPosition, Service, Employee, Client, Appointment, Purchase
import datetime
from django.urls import reverse
from django.utils.html import escape, mark_safe
from django_reverse_admin import ReverseModelAdmin

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget


class NewsResource(resources.ModelResource):

    class Meta:
        model = News


class NewsAdmin(ImportExportActionModelAdmin):
    resource_class = NewsResource
    list_filter = ('status',)
    list_display = ('title', 'description', 'status',
                    'created_at', 'published_at')
    actions = ImportExportActionModelAdmin.actions + ["make_news_published", ]
    search_fields = ('title', 'description')
    fieldsets = ((None, {
        'fields': (
            'title',
            'image',
            'description',
        )
    }),)
    filter_horizontal = ()

    def make_news_published(self, request, queryset):
        rows_updated = queryset.update(
            status='published', published_at=datetime.datetime.now())
        message_bit = ""
        if rows_updated == 1:
            message_bit = "1 новости"
        else:
            message_bit = "%s новостей" % rows_updated
        self.message_user(
            request, "успешная публикация %s." % message_bit)

    make_news_published.short_description = "Опубликовать выбранные новости"


class ProductTypeResource(resources.ModelResource):

    class Meta:
        model = ProductType


class ProductTypeAdmin(ImportExportActionModelAdmin):
    resource_class = ProductTypeResource
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    fieldsets = ((None, {
        'fields': (
            'title',
            'description',
            'image',
        )
    }),)
    filter_horizontal = ()


class ProductResource(resources.ModelResource):
    productType = fields.Field(column_name="productType", attribute="productType",
                               widget=ForeignKeyWidget(ProductType, 'productType'))

    class Meta:
        model = Product


class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource

    def productType_link(self, obj: Product):
        if obj.productType == None:
            return 'Нет типа'
        link = reverse("admin:api_producttype_change",
                       args=[obj.productType.id])
        return mark_safe(f'<a href="{link}">{escape(obj.productType.__str__())}</a>')

    productType_link.short_description = 'Тип продукта'
    productType_link.admin_order_field = 'тип продукта'

    list_display = ('title', 'productType_link',
                    'description', 'countLeft')
    search_fields = ('title', 'description',)
    list_filter = ('productType',)
    fieldsets = ((None, {
        'fields': (
            'productType',
            'title',
            'description',
            'countLeft',
            'photo',
        )
    }),)
    filter_horizontal = ()


class ServiceGroupResource(resources.ModelResource):

    class Meta:
        model = ServiceGroup


class ServiceGroupAdmin(ImportExportActionModelAdmin):
    resource_class = ServiceGroupResource
    list_display = ('title', 'description',)
    search_fields = ('title', 'description')
    fieldsets = ((None, {
        'fields': (
            'title',
            'description',
            'image',
        )
    }),)
    filter_horizontal = ()


class WorkPositionResource(resources.ModelResource):
    serviceGroup = fields.Field(column_name="serviceGroup", attribute="serviceGroup",
                                widget=ForeignKeyWidget(ServiceGroup, 'serviceGroup'))

    class Meta:
        model = WorkPosition


class WorkPositionAdmin(ImportExportActionModelAdmin):
    resource_class = WorkPositionResource

    def serviceGroup_link(self, obj: Product):
        if obj.serviceGroup == None:
            return 'Нет типа'
        link = reverse("admin:api_servicegroup_change",
                       args=[obj.serviceGroup.id])
        return mark_safe(f'<a href="{link}">{escape(obj.serviceGroup.__str__())}</a>')

    serviceGroup_link.short_description = 'Группа услуг'
    serviceGroup_link.admin_order_field = 'группа услуг'

    list_display = ('title', 'description',
                    'serviceGroup_link', 'workSchedule')
    list_filter = ('serviceGroup', 'workSchedule')
    search_fields = ('title', )
    fieldsets = ((None, {
        'fields': (
            'title',
            'description',
            'serviceGroup',
            'workSchedule',
        )
    }),)
    filter_horizontal = ()


class ServiceResource(resources.ModelResource):
    serviceGroup = fields.Field(column_name="serviceGroup", attribute="serviceGroup",
                                widget=ForeignKeyWidget(ServiceGroup, 'serviceGroup'))

    class Meta:
        model = Service


class ServiceAdmin(ImportExportActionModelAdmin):
    resource_class = ServiceResource

    def serviceGroup_link(self, obj: Service):
        if obj.serviceGroup == None:
            return 'Нет в группе'
        link = reverse("admin:api_servicegroup_change",
                       args=[obj.serviceGroup.id])
        return mark_safe(f'<a href="{link}">{escape(obj.serviceGroup.__str__())}</a>')

    serviceGroup_link.short_description = 'Группа услуг'
    serviceGroup_link.admin_order_field = 'группа услуг'

    list_display = ('title', 'description',
                    'serviceGroup_link', 'price', 'percToEmpl')
    list_filter = ('serviceGroup',)
    search_fields = ('title', 'description',)
    fieldsets = ((None, {
        'fields': (
            'title',
            'description',
            'serviceGroup',
            'image',
            'price',
            'percToEmpl'
        )
    }),)
    filter_horizontal = ()


class DiscountResource(resources.ModelResource):

    class Meta:
        model = Discount


class DiscountAdmin(ImportExportActionModelAdmin):
    resource_class = DiscountResource
    list_display = ('id', 'discountAmount', 'promoCode')
    search_fields = ('promoCode',)
    fieldsets = ((None, {
        'fields': (
            'discountAmount',
            'promoCode',
        )
    }),)
    filter_horizontal = ()


class UserProfileAdmin(UserAdmin):
    ordering = ('email',)
    list_filter = ('userType',)
    list_display = ('email', 'name', 'surname',
                    'date_joined', 'last_login', 'userType')
    search_fields = ('name', 'surname', "email")
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('name', 'surname', "email",
                           "last_login", "date_joined", 'password')}),
    )
    add_fieldsets = (
        (None, {'fields': ("email", 'name', 'surname', 'password1', 'password2')}),
    )

    filter_horizontal = ()


class UserEmployeeInline(admin.TabularInline):
    model = User
    fieldsets = (
        (None, {'fields': ('name', 'surname', "email", 'password', 'userType', 'is_staff', 'is_admin',
                           "last_login", "date_joined")}),
    )
    readonly_fields = ('date_joined', 'last_login')

    def has_delete_permission(self, request, obj=None):
        return False


class UserClientInline(admin.TabularInline):
    model = User
    fieldsets = (
        (None, {'fields': ('name', 'surname', "email", 'password', 'userType',
                           "last_login", "date_joined")}),
    )
    readonly_fields = ('date_joined', 'last_login')

    def has_delete_permission(self, request, obj=None):
        return False


class EmployeeAdmin(ReverseModelAdmin):

    def workPosition_link(self, obj: Service):
        if obj.workPosition == None:
            return 'Нет должности'
        link = reverse("admin:api_workposition_change",
                       args=[obj.workPosition.id])
        return mark_safe(f'<a href="{link}">{escape(obj.workPosition.__str__())}</a>')

    workPosition_link.short_description = 'Должность'
    workPosition_link.admin_order_field = 'должность'

    inline_type = 'stacked'
    inline_reverse = [
        {
            'field_name': 'user',
            'admin_class': UserEmployeeInline
        },

    ]

    list_filter = ('employeeStatus', 'workPosition')
    list_display = ('user', 'workPosition_link', 'phone',
                    'address', 'employeeStatus')
    search_fields = ('user__name',
                     'user__surname', 'phone')


class ClientAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = [
        {
            'field_name': 'user',
            'admin_class': UserClientInline
        },
    ]
    list_display = ('user', 'phone', 'birthdate', 'address')
    search_fields = ('user__name', 'user__surname', 'phone',)


class AppointmentResource(resources.ModelResource):
    client = fields.Field(column_name="client", attribute="client",
                          widget=ForeignKeyWidget(Client, 'user'))
    employee = fields.Field(column_name="employee", attribute="employee",
                            widget=ForeignKeyWidget(Employee, "employee"))
    discount = fields.Field(column_name="discount", attribute="discount",
                            widget=ForeignKeyWidget(Discount, 'discountAmount'))

    class Meta:
        model = Appointment


class AppointmentAdmin(ImportExportActionModelAdmin):
    resource_class = AppointmentResource

    def client_link(self, obj: Appointment):
        if obj.client == None:
            return 'Нет в приложении'
        link = reverse("admin:api_client_change", args=[obj.client.id])
        return mark_safe(f'<a href="{link}">{escape(obj.client.__str__())}</a>')

    client_link.short_description = 'Клиент'
    client_link.admin_order_field = 'клиент'

    def employee_link(self, obj: Appointment):
        if obj.employee == None:
            return 'Нет сотрудника'
        link = reverse("admin:api_employee_change", args=[obj.employee.id])
        return mark_safe(f'<a href="{link}">{escape(obj.employee.__str__())}</a>')

    employee_link.short_description = 'Сотрудник'
    employee_link.admin_order_field = 'сотрудник'

    def discount_link(self, obj: Appointment):
        if obj.discount == None:
            return 'Без скидки'
        link = reverse("admin:api_discount_change", args=[obj.discount.id])
        return mark_safe(f'<a href="{link}">{escape(obj.discount.__str__())}</a>')

    discount_link.short_description = 'Скидка'
    discount_link.admin_order_field = 'скидка'

    def unauthorized(self, obj: Appointment):
        if obj.client == None:
            return obj.unauthorizedUser
        return 'Есть в приложении'

    unauthorized.short_description = 'Неавторизованный клиент'
    unauthorized.admin_order_field = 'неавторизованный клиент'

    list_filter = ('appointmentStatus',)
    list_display = ("id", 'client_link', 'unauthorized', 'employee_link', 'discount_link', 'fullPrice',
                    "appointmentStatus", "scheduledTime",)
    search_fields = ('client__user__name', 'client__user__surname',
                     'employee__user__name', 'employee__user__surname', 'unauthorizedUser')
    filter_horizontal = ()


class PurchaseResource(resources.ModelResource):
    client = fields.Field(column_name="client", attribute="client",
                          widget=ForeignKeyWidget(Client, 'user'))
    discount = fields.Field(column_name="discount", attribute="discount",
                            widget=ForeignKeyWidget(Discount, 'discountAmount'))

    class Meta:
        model = Purchase


class PurchaseAdmin(ImportExportActionModelAdmin):
    resource_class = PurchaseResource

    def client_link(self, obj: Appointment):
        if obj.client == None:
            return 'Нет в приложении'
        link = reverse("admin:api_client_change", args=[obj.client.id])
        return mark_safe(f'<a href="{link}">{escape(obj.client.__str__())}</a>')

    client_link.short_description = 'Клиент'
    client_link.admin_order_field = 'клиент'

    def discount_link(self, obj: Appointment):
        if obj.discount == None:
            return 'Без скидки'
        link = reverse("admin:api_discount_change", args=[obj.discount.id])
        return mark_safe(f'<a href="{link}">{escape(obj.discount.__str__())}</a>')

    discount_link.short_description = 'Скидка'
    discount_link.admin_order_field = 'скидка'

    def unauthorized(self, obj: Appointment):
        if obj.client == None:
            return obj.unauthorizedUser
        return 'Есть в приложении'

    unauthorized.short_description = 'Неавторизованный клиент'
    unauthorized.admin_order_field = 'неавторизованный клиент'

    list_filter = ('purchaseStatus',)
    list_display = ("id", 'client_link', 'unauthorized', 'discount_link',
                    "purchaseStatus", "fullPrice", "created_at")
    search_fields = ('client__user__name',
                     'client__user__surname', 'unauthorizedUser')
    filter_horizontal = ()


admin.site.register(News, NewsAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ServiceGroup, ServiceGroupAdmin)
admin.site.register(WorkPosition, WorkPositionAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(User, UserProfileAdmin)
