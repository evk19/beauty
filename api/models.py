from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date


# ============================================
# НОВОСТИ
# ============================================

class News(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = (
        (DRAFT, 'Черновик'),
        (PUBLISHED, 'Опубликована'),
    )

    title = models.CharField(
        max_length=200, verbose_name="Название новости", unique=True)
    description = models.TextField(
        verbose_name="Описание новости", blank=True)
    image = models.ImageField(
        verbose_name="Картинка новости", null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT,
                              verbose_name="Статус новости")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")

    published_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "новости"

    def __str__(self):
        return self.title


# ============================================
# СКИДКИ
# ============================================

class Discount(models.Model):
    discountAmount = models.IntegerField(default=0, validators=[MinValueValidator(
        0), MaxValueValidator(100)],  verbose_name="Скидка в %")
    promoCode = models.CharField(
        max_length=6, verbose_name="Промокод", unique=True, validators=[RegexValidator(r'^[A-Z0-9]*$', 'Можно использовать буквы A-Z и цифры 0-9')])

    class Meta:
        verbose_name = "скидка"
        verbose_name_plural = "скидки"

    def __str__(self):
        return str(self.discountAmount) + "%"


# ============================================
# ТИПЫ ТОВАРОВ
# ============================================

class ProductType(models.Model):
    title = models.CharField(
        max_length=120, verbose_name="Тип товара", unique=True)
    description = models.TextField(
        verbose_name="Описание типа", blank=True)
    image = models.ImageField(
        verbose_name="Картинка типа товаров", null=True, blank=True)

    class Meta:
        verbose_name = "тип товаров"
        verbose_name_plural = "типы товаров"

    def __str__(self):
        return self.title


# ============================================
# ТОВАРЫ
# ============================================

class Product(models.Model):

    productType = models.ForeignKey(
        ProductType, models.SET_NULL, verbose_name="Тип товара", null=True, blank=True)
    title = models.CharField(
        max_length=200, verbose_name="Название товара", unique=True)
    description = models.TextField(
        verbose_name="Описание товара", blank=True)
    photo = models.ImageField(
        verbose_name="Картинка товара", null=True, blank=True)
    countLeft = models.IntegerField(
        default=0, validators=[MinValueValidator(0)], verbose_name="Кол-во в наличии")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.title


# ============================================
# ИНДИВИДУАЛЬНАЯ МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ
# ============================================
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None,  **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have an name')
        if not surname:
            raise ValueError('Users must have an surname')

        user = self.model(
            email=self.normalize_email(email),
            surname=surname,
            name=name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('userType', 'admin')

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            surname=surname,
            name=name,
            **extra_fields
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'admin'
    CLIENT = 'user'
    EMPLOYEE = 'driver'
    USER_TYPE_CHOICES = (
        (ADMIN, 'Администратор'),
        (CLIENT, 'Клиент'),
        (EMPLOYEE, 'Сторудник'),
    )

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Зарегистрировался")
    last_login = models.DateTimeField(auto_now=True, verbose_name="Был в сети")
    is_admin = models.BooleanField(
        default=False, verbose_name="Может вносить изменения в данные")
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        default=False, verbose_name="Доступ в админ панель")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserProfileManager()

    userType = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=CLIENT,
                                verbose_name="Тип пользователя")

    name = models.CharField(max_length=100, blank=True, verbose_name="Имя")
    surname = models.CharField(
        max_length=100, blank=True, verbose_name="Фамилия")

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.name + ' ' + self.surname

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# ============================================
# ГРУППА УСЛУГ
# ============================================


class ServiceGroup(models.Model):
    title = models.CharField(
        max_length=200, verbose_name="Название группы", unique=True)
    description = models.TextField(
        verbose_name="Описание группы услуг", blank=True)
    image = models.ImageField(
        verbose_name="Картинка группы", null=True, blank=True)

    class Meta:
        verbose_name = "группа услуг"
        verbose_name_plural = "группы услуг"

    def __str__(self):
        return str(self.title)


# ============================================
# РАБОЧИЕ МЕСТА
# ============================================

class WorkPosition(models.Model):
    FIVE_TWO = 'five_two'
    SIX_ONE = 'six_one'
    TWO_TWO = 'two_two'
    THREE_THREE = 'three_three'
    WORK_SCHEDULE = (
        (FIVE_TWO, '5/2'),
        (SIX_ONE, '6/1'),
        (TWO_TWO, '2/2'),
        (THREE_THREE, '3/3'),
    )

    serviceGroup = models.ForeignKey(
        ServiceGroup, models.SET_NULL, verbose_name="Группа услуг", null=True, blank=True)
    title = models.CharField(
        max_length=200, verbose_name="Название должности", unique=True)
    description = models.TextField(
        verbose_name="Описание услуг", blank=True)
    workSchedule = models.CharField(max_length=30, choices=WORK_SCHEDULE, default=FIVE_TWO,
                                    verbose_name="График работы")

    class Meta:
        verbose_name = "рабочее место"
        verbose_name_plural = "рабочие места"

    def __str__(self):
        return str(self.title)


# ============================================
# УСЛУГИ
# ============================================

class Service(models.Model):

    serviceGroup = models.ForeignKey(
        ServiceGroup, models.SET_NULL, verbose_name="Группа услуг", null=True, blank=True)
    title = models.CharField(
        max_length=200, verbose_name="Название услуги", unique=True)
    description = models.TextField(
        verbose_name="Описание услуг", blank=True)
    image = models.ImageField(
        verbose_name="Картинка услуги", null=True, blank=True)
    price = models.IntegerField(
        default=0, verbose_name="Стоимость услуги")
    percToEmpl = models.IntegerField(
        default=0, validators=[MinValueValidator(0)], verbose_name="Процент сотруднику")

    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "услуги"

    def __str__(self):
        return str(self.title)

# ============================================
# СОТРУДНИКИ
# ============================================


class Employee(models.Model):
    ON_APPOINTMENT = 'on_appointment'
    WAITING_APPOINTMENT = 'waiting_appointment'
    ON_SICK_LEAVE = 'on_sick_leave'
    ON_VACATION = 'on_vacation'
    NONWORKING_TIME = 'nonworking_time'
    FIRED = 'fired'
    DRIVER_STATUS_CHOICES = (
        (ON_APPOINTMENT, 'Принимает клиента'),
        (WAITING_APPOINTMENT, 'В ожидании клиента'),
        (ON_SICK_LEAVE, 'На больничном'),
        (ON_VACATION, 'В отпуске'),
        (NONWORKING_TIME, 'Нерабочее время'),
        (FIRED, 'Уволен'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name="ФИО"
    )
    workPosition = models.ForeignKey(
        WorkPosition, models.SET_NULL, verbose_name="Рабочее место", null=True, blank=True, )
    photo = models.ImageField(
        verbose_name="Фото сотрудника", blank=True, null=True)
    birthdate = models.DateField(
        verbose_name="Дата рождения",)
    phone = PhoneNumberField(
        unique=True, verbose_name="Телефон")
    address = models.CharField(
        max_length=200, verbose_name="Адрес проживания")
    employeeStatus = models.CharField(max_length=30, choices=DRIVER_STATUS_CHOICES, default=NONWORKING_TIME,
                                      verbose_name="Статус сотрудника")

    class Meta:
        verbose_name = "сотрудник"
        verbose_name_plural = "сотрудники"

    def __str__(self):
        return str(self.user)


# ============================================
# КЛИЕНТЫ
# ============================================

class Client(models.Model):
    SERVE_CLIENT = 'serve_client'
    WAITING = 'waiting'
    ON_SICK_LEAVE = 'on_sick_leave'
    ON_VACATION = 'on_vacation'
    NONWORKING_TIME = 'nonworking_time'
    FIRED = 'fired'
    OPERATOR_STATUS_CHOICES = (
        (SERVE_CLIENT, 'Обслуживает клиента'),
        (WAITING, 'В ожидании'),
        (ON_SICK_LEAVE, 'На больничном'),
        (ON_VACATION, 'В отпуске'),
        (NONWORKING_TIME, 'Нерабочее время'),
        (FIRED, 'Уволен'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name="ФИО"
    )
    birthdate = models.DateField(
        verbose_name="Дата рождения", null=True, blank=True,)
    phone = PhoneNumberField(
        unique=True, verbose_name="Телефон")
    address = models.CharField(
        max_length=200, verbose_name="Адрес проживания")

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return str(self.user)


# ============================================
# ЗАПИСИ
# ============================================

class Appointment(models.Model):
    EMPLOYEE_WAITING = 'driver_waiting'
    CLIENT_CANCELED = 'client_canceled'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    APPOINTMENT_STATUS_CHOICES = (
        (EMPLOYEE_WAITING, 'сотрудник ожидает клиента'),
        (CLIENT_CANCELED, 'клиент отменил запись'),
        (IN_PROGRESS, 'клиента обслуживают'),
        (COMPLETED, 'выполнено'),
    )
    services = models.ManyToManyField(Service)
    client = models.ForeignKey(
        Client, models.SET_NULL, verbose_name="Клиент", null=True, blank=True, )
    employee = models.ForeignKey(
        Employee, models.SET_NULL, verbose_name="Сотрудник", null=True, blank=True, )
    discount = models.ForeignKey(
        Discount, models.SET_NULL, verbose_name="Скидка", null=True, blank=True, )
    fullPrice = models.IntegerField(
        default=0, verbose_name="Общая стоимость услуги")
    unauthorizedUser = models.CharField(
        null=True, blank=True, max_length=100, verbose_name="Неавторизованный клиент")
    unauthorizedPhone = PhoneNumberField(
        unique=True, verbose_name="Телефон неавторизованного клиента", null=True, blank=True,)
    appointmentStatus = models.CharField(max_length=30, choices=APPOINTMENT_STATUS_CHOICES, default=EMPLOYEE_WAITING,
                                         verbose_name="Статус записи")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время оформления")
    scheduledTime = models.DateTimeField(
        verbose_name="Назначенное время", null=True, blank=True,)

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"

    def __str__(self):
        return str(self.id)


# ============================================
# ПОКУПКИ
# ============================================

class Purchase(models.Model):
    CLIENT_CANCELED = 'client_canceled'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    PURCHASE_STATUS_CHOICES = (
        (CLIENT_CANCELED, 'клиент отменил покупку'),
        (IN_PROGRESS, 'обработка'),
        (COMPLETED, 'выполнена'),
    )
    products = models.ManyToManyField(Product)
    client = models.ForeignKey(
        Client, models.SET_NULL, verbose_name="Клиент", null=True, blank=True, )
    discount = models.ForeignKey(
        Discount, models.SET_NULL, verbose_name="Скидка", null=True, blank=True, )
    fullPrice = models.IntegerField(
        default=0, verbose_name="Общая стоимость услуги")
    unauthorizedUser = models.CharField(
        null=True, blank=True, max_length=100, verbose_name="Неавторизованный клиент")
    purchaseStatus = models.CharField(max_length=30, choices=PURCHASE_STATUS_CHOICES, default=IN_PROGRESS,
                                      verbose_name="Статус покупки")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время оформления")

    class Meta:
        verbose_name = "покупка"
        verbose_name_plural = "покупки"

    def __str__(self):
        return str(self.id)
