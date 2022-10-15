from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import uuid
from ckeditor_uploader.fields import RichTextUploadingField
import jsonfield
# from meta.models import ModelMeta
from rest_framework.fields import JSONField


def scramble_uploaded_filename(instance, filename):
    extention = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extention)


class Category(models.Model): #ModelMeta
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='گروه بورسی')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    description = models.TextField(max_length=10000, null=True, blank=True, help_text='توضیحات')

    # _metadata = {
    #     'title': 'title',
    #     'description': 'description',
    #     'image': 'get_meta_image',
    # }

    class Meta:
        ordering = ["createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:category-detail", kwargs={'category_id': self.pk})

    # def get_meta_image(self):
    #     if self.pic:
    #         return self.pic.url


SYMBOL_TYPE_CHOICES = (
    ('0', "شاخص کل"),
    ('1', "نماد"),
    ('2', "شاخص صنعت"),
)


class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='گروه')
    symbol = models.CharField(max_length=120, null=True, blank=True, help_text='نماد')
    fullName = models.CharField(max_length=120, null=True, blank=True, help_text='نام شرکت')
    alias = models.CharField(max_length=120, null=True, blank=True, help_text='نام معادل انگلیسی')
    type = models.CharField(max_length=20, help_text='نوع نماد', choices=SYMBOL_TYPE_CHOICES, default='1')
    bourseType = models.CharField(max_length=120, null=True, blank=True, help_text='بازار بورس')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    tse = models.URLField(null=True, blank=True, help_text='لینک tse')
    site = models.URLField(null=True, blank=True, help_text='وبسایت')
    isTarget = models.BooleanField(default=False, help_text='تحت نظر')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    hit_count = models.BigIntegerField(default=0)
    description = models.TextField(max_length=10000, null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:company-detail", kwargs={'company_id': self.pk})


class StockPortfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE,
                                help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')


class RequestSymbol(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE,
                                help_text='نماد')
    isAnalyzed = models.BooleanField(default=False, help_text='آیا تحلیل برای این نماد انجام گرفته')
    analyzedAt = models.DateField(default=timezone.now, help_text='تاریخ تحلیل')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')


class News(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE,
                                 help_text='در صورت اختصاص خبر برای گروه انتخاب شود')
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE,
                                help_text='در صورت اختصاص خبر برای نماد انتخاب شود')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='گروه بورسی')
    reference = models.CharField(max_length=120, null=True, blank=True, help_text='مرجع')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    tag = models.CharField(max_length=120, null=True, blank=True, help_text='تگ ها')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    isApproved = models.BooleanField(default=False, help_text='تایید خبر')
    isImportant = models.BooleanField(default=False, help_text='خبر مهم')
    hit_count = models.BigIntegerField(default=0)
    shortDescription = models.TextField(max_length=200, null=True, blank=True, help_text='توضیحات کوتاه')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')


    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:news-detail", kwargs={'news_id': self.pk})


class Technical(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    video = models.FileField(upload_to='videos/', null=True, blank=True, help_text='فایل ویدیو')
    audio = models.FileField(upload_to='audio/', null=True, blank=True, help_text='فایل صوتی')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    hit_count = models.BigIntegerField(default=0)
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:technical-detail", kwargs={'technical_id': self.pk})


class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender_user', on_delete=models.CASCADE, null=True, blank=True,
                             help_text='فرستنده')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver_user', on_delete=models.CASCADE, null=True, blank=True,
                             help_text='گیرنده')
    createAt = models.DateTimeField(default=timezone.now, help_text='تاریخ ایجاد')
    isSeen = models.BooleanField(default=False, help_text='مشاهده شده')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return str(self.sender)

    @property
    def owner(self):
        return self.sender


class Webinar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    hit_count = models.BigIntegerField(default=0)
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:webinar-detail", kwargs={'webinar_id': self.pk})


class MapBazaar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')

    class Meta:
        ordering = ["-createAt"]

    def __unicode__(self):
        return self.createAt

    @property
    def owner(self):
        return self.user


class Fundamental(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    hit_count = models.BigIntegerField(default=0)
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:fundamental-detail", kwargs={'fundamental_id': self.pk})


class Bazaar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    hit_count = models.BigIntegerField(default=0)
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:bazaar-detail", kwargs={'bazaar_id': self.pk})


TIME_FRAME_CHOICES = (
    ('M1', "1 دقیقه"),
    ('M5', "5 دقیقه"),
    ('M15', "15 دقیقه"),
    ('M30', "30 دقیقه"),
    ('H1', "۱ ساعت"),
    ('H4', "4 ساعت"),
    ('D1', "1 روز"),
    ('W1', "1 هفته"),
    ('MN1', "1 ماه"),
)
class Chart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    lastCandleDate = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    timeFrame = models.CharField(max_length=20, help_text='تایم فریم', choices=TIME_FRAME_CHOICES, default='D1')
    data = models.FileField('uploaded chart file', upload_to='charts/', null=True, blank=True, help_text='فایل csv,  prn, txt چارت نماد')

    class Meta:
        ordering = ["-lastCandleDate"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user


class TechnicalUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateTimeField(default=timezone.now, help_text='تاریخ ایجاد')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='نام فایل')
    isShare = models.BooleanField(default=False, help_text='اجازه اشتراک گذاریا')
    # data = models.TextField(null=True, blank=True, help_text='فایل متنی شده json')
    data = jsonfield.JSONField(help_text='فایل متنی شده json')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user


class Candle(models.Model):
    # dateTime = models.DateTimeField(unique=True, help_text='تاریخ و زمان')
    dateTime = models.DateTimeField(unique=True, help_text='تاریخ و زمان')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    timeFrame = models.CharField(max_length=20, help_text='تایم فریم', choices=TIME_FRAME_CHOICES, default='7')
    open = models.IntegerField(default=0, null=True, blank=True, help_text='قیمت باز شدن')
    close = models.IntegerField(default=0, null=True, blank=True, help_text='قیمت بسته شدن')
    high = models.IntegerField(default=0, null=True, blank=True, help_text='بالاترین قیمت')
    low = models.IntegerField(default=0, null=True, blank=True, help_text='پایین ترین قیمت')
    volume = models.IntegerField(default=0, null=True, blank=True, help_text='حجم')

    class Meta:
        ordering = ["-dateTime"]

    def __str__(self):
        return self.company.symbol


class CandleJson(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    lastCandleDate = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    timeFrame = models.CharField(max_length=20, help_text='تایم فریم', choices=TIME_FRAME_CHOICES, default='D1')
    candleData = models.TextField(blank=True, help_text='فایل متنی شده json')

    class Meta:
        ordering = ["-lastCandleDate"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user


class TutorialCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user


CATEGORY_LEVEL_CHOICES = (
    ('0', "مقدماتی"),
    ('1', "پیشرفته"),
)
class TutorialSubCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    category = models.ForeignKey(TutorialCategory, on_delete=models.CASCADE, null=True, blank=True, help_text='دسته بندی')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    categoryLevel = models.CharField(max_length=20, help_text='سطح آموزش', choices=CATEGORY_LEVEL_CHOICES,
                                default='0')
    pic = models.ImageField('uploaded image', null=True, blank=True, help_text='تصویر')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user


class Tutorial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    file = models.FileField('uploaded file', null=True, blank=True, help_text='فایل')
    title = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان')
    # category = models.CharField(max_length=120, null=True, blank=True, help_text='دسته آموزش', choices=CATEGORY_CHOICES,
    #                             default='تحلیل بازار')
    subCategory = models.ForeignKey(TutorialSubCategory, on_delete=models.CASCADE, null=True, blank=True, help_text='زیر دسته بندی')
    externalLink = models.URLField(null=True, blank=True, help_text='لینک آموزش')
    aparatEmbedCode = models.CharField(max_length=1000, null=True, blank=True, help_text='کد امبد آپارات')
    hit_count = models.BigIntegerField(default=0)
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    description = RichTextUploadingField(null=True, blank=True, help_text='توضیحات')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self, request=None):
        return reverse("bourseapp:tutorial-detail", kwargs={'tutorial_id': self.pk})


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    isShow = models.BooleanField(default=False, help_text='نمایش برای کاربران')
    title = models.TextField(max_length=3000, null=True, blank=True, help_text='پیام')

    class Meta:
        ordering = ["-createAt"]

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user


class CompanyFinancial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, help_text='نماد')
    createAt = models.DateField(default=timezone.now, help_text='تاریخ ایجاد')
    file = models.FileField(upload_to='CompanyFinancial/', null=True, blank=True, help_text='فایل')
    isSuperUserPermition = models.BooleanField(default=False, help_text='دسترسی سطح بالا')
    previousFinancialPeriodProfitability = models.IntegerField(default=0, help_text='سودآوری-دوره مالی قبل')
    previousFinancialPeriodSell = models.IntegerField(default=0, help_text='فروش-دوره مالی قبل')
    previousFinancialPeriodProduction = models.IntegerField(default=0, help_text='تولی-دوره مالی قبلد')
    previousFinancialPeriodAccumulatedProfits = models.IntegerField(default=0, help_text='سود انباشته-دوره مالی قبل')
    previousFinancialPeriodSymbolPrice = models.IntegerField(default=0, help_text='قیمت سهم-دوره مالی قبل')
    newFinancialPeriodProfitability = models.IntegerField(default=0, help_text='سودآوری-دوره مالی جدید')
    newFinancialPeriodSell = models.IntegerField(default=0, help_text='فروش-دوره مالی جدید')
    newFinancialPeriodProduction = models.IntegerField(default=0, help_text='تولید-دوره مالی جدید')
    newFinancialPeriodAccumulatedProfits = models.IntegerField(default=0, help_text='سود انباشته-دوره مالی جدید')
    newFinancialPeriodSymbolPrice = models.IntegerField(default=0, help_text='قیمت سهم-دوره مالی جدید')
    forecastProfitability = models.IntegerField(default=0, help_text='سودآوری-پیشبینی')
    forecastSell = models.IntegerField(default=0, help_text='فروش-پیشبینی')
    forecastProduction = models.IntegerField(default=0, help_text='تولید-پیشبینی')
    forecastAccumulatedProfits = models.IntegerField(default=0, help_text='سود انباشته-پیشبینی')
    forecastSymbolPrice = models.IntegerField(default=0, help_text='قیمت سهم-پیشبینی')

    class Meta:
        ordering = ["-isSuperUserPermition", "-createAt"]

    def __str__(self):
        return self.company.symbol

    @property
    def owner(self):
        return self.user


class FileRepository(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             help_text='کاربر')
    file = models.FileField('uploaded file', upload_to='files/', null=True, blank=True)
    createAt = models.DateTimeField(default=timezone.now)
    fileTag = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ["-createAt"]

    @property
    def owner(self):
        return self.user