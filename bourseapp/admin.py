from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from django.shortcuts import redirect

from . import models


@admin.register(models.Category)
class CategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:company-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:company-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:company-list')


@admin.register(models.Company)
class CompanyAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("symbol", "category", "alias", "isTarget")
    list_filter = ("category", "alias", "isTarget" )

    def get_fields(self, request, obj=None):
        fields = super(CompanyAdmin, self).get_fields(request, obj)
        if request.user.is_superuser or request.user.groups == "level1":
            pass
        else:
            # fields += ('isSuperUserPermition',)
            fields = tuple(x for x in fields if x != 'isSuperUserPermition')

        return fields

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:company-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:company-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:company-list')


@admin.register(models.News)
class NewsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }

    def get_fields(self, request, obj=None):
        fields = super(NewsAdmin, self).get_fields(request, obj)
        if request.user.is_superuser:
            pass
        else:
            # fields += ('isSuperUserPermition',)
            fields = tuple(x for x in fields if x != 'isSuperUserPermition' or x != 'hit_count')

        return fields

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:news-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:news-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:news-list')


@admin.register(models.Technical)
class TechnicalAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }

    def get_fields(self, request, obj=None):
        fields = super(TechnicalAdmin, self).get_fields(request, obj)
        if request.user.is_superuser or request.user.groups == "level1":
            pass
        else:
            fields = tuple(x for x in fields if x != 'isSuperUserPermition')

        return fields

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        # print(obj, obj.company.pk)
        models.RequestSymbol.objects.filter(company=obj.company.pk).update(isAnalyzed=True, analyzedAt=obj.createAt)
        return redirect('bourseapp:technical-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:technical-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:technical-list')


@admin.register(models.Webinar)
class WebinarAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }

    def get_fields(self, request, obj=None):
        fields = super(WebinarAdmin, self).get_fields(request, obj)
        if request.user.is_superuser or request.user.groups == "level1":
            pass
        else:
            fields = tuple(x for x in fields if x != 'isSuperUserPermition')

        return fields

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:webinar-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:webinar-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:webinar-list')


@admin.register(models.Bazaar)
class BazaarAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }

    def get_fields(self, request, obj=None):
        fields = super(BazaarAdmin, self).get_fields(request, obj)
        if request.user.is_superuser or request.user.groups == "level1":
            pass
        else:
            fields = tuple(x for x in fields if x != 'isSuperUserPermition')

        return fields

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:bazaar-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:bazaar-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:bazaar-list')


@admin.register(models.Fundamental)
class FundamentalAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
    }

    def get_fields(self, request, obj=None):
        fields = super(FundamentalAdmin, self).get_fields(request, obj)
        if request.user.is_superuser or request.user.groups == "level1":
            pass
        else:
            fields = tuple(x for x in fields if x != 'isSuperUserPermition')

        return fields

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:fundamental-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:fundamental-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:fundamental-list')


@admin.register(models.Chart)
class ChartAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("company", "createAt", "lastCandleDate", "timeFrame")
    list_filter = ("timeFrame", "company", )


@admin.register(models.TechnicalUser)
class ChartAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("user", "title", "company", "createAt", "isShare")
    list_filter = ("user", "company", "isShare", )


@admin.register(models.Candle)
class CandleAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("company", "dateTime", "timeFrame", "open", "close", "high", "low", "volume")
    list_filter = ("company", "timeFrame", )


@admin.register(models.CandleJson)
class CandleJsonAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("company", "createAt", "lastCandleDate", "timeFrame")
    list_filter = ("timeFrame","company", )


@admin.register(models.StockPortfolio)
class StockPortfolioAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("company", "user", "createAt")
    list_filter = ("company", )


@admin.register(models.RequestSymbol)
class RequestSymbolAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("company", "user", "createAt", "isAnalyzed", "analyzedAt")
    list_filter = ("company", )


@admin.register(models.Tutorial)
class TutorialAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("title", "user", "description", "subCategory", "externalLink", "isSuperUserPermition", "createAt",)
    list_filter = ("subCategory", "isSuperUserPermition", )

    def get_fields(self, request, obj=None):
        fields = super(TutorialAdmin, self).get_fields(request, obj)
        if request.user.is_superuser or request.user.groups == "level1":
            pass
        else:
            fields = tuple(x for x in fields if x != 'isSuperUserPermition')

        return fields

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:tutorial-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:tutorial-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:tutorial-list')


@admin.register(models.Message)
class MessageAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):

    # override add function
    def response_add(self, request, obj, post_url_continue=None):
        return redirect('bourseapp:message-list')

    # override edit function
    def response_change(self, request, obj):
        return redirect('bourseapp:message-list')

    # override delete function
    def response_delete(self, request, obj_display, obj_id):
        return redirect('bourseapp:message-list')


@admin.register(models.TutorialCategory)
class TutorialCategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("title", "user", "description", "createAt",)
    list_filter = ("user", )


@admin.register(models.MapBazaar)
class MapBazaarAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("user", "createAt",)
    list_filter = ("user", )


@admin.register(models.ChatMessage)
class ChatMessageAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("sender", "receiver", "createAt", "isSeen", "description",)
    list_filter = ("sender", "receiver", "isSeen", )


@admin.register(models.TutorialSubCategory)
class TutorialSubCategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("title", "categoryLevel", "user", "description", "category", "createAt",)
    list_filter = ("category", )


@admin.register(models.CompanyFinancial)
class CompanyFinancialAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("company", "user", "createAt",)
    list_filter = ("company", )
    fields = (
        ('user', 'company', 'createAt'),
        ('file', 'isSuperUserPermition'),
        ('previousFinancialPeriodProfitability', 'previousFinancialPeriodSell', 'previousFinancialPeriodProduction',
         'previousFinancialPeriodAccumulatedProfits', 'previousFinancialPeriodSymbolPrice'),
        ('newFinancialPeriodProfitability', 'newFinancialPeriodSell', 'newFinancialPeriodProduction',
         'newFinancialPeriodAccumulatedProfits', 'newFinancialPeriodSymbolPrice'),
        ('forecastProfitability', 'forecastSell', 'forecastProduction',
         'forecastAccumulatedProfits', 'forecastSymbolPrice')
    )


@admin.register(models.FileRepository)
class TutorialSubCategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("file", "fileTag", "user", "description", "createAt",)
    list_filter = ("fileTag", )
