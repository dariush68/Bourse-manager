from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth.models import User
import json
from django.core.serializers.json import DjangoJSONEncoder

from bourseapp import models


class CategorySerializer(serializers.ModelSerializer):  # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Category
        fields = [
            'url',
            'id',
            'user',
            'title',
            'pic',
            'date',
            'orderNum',
        ]
        read_only_fields = ['id', 'user', 'date', 'url']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        qs = models.Category.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title has already been used")
        return value


class SymbolSerializer(serializers.ModelSerializer):  # forms.ModelForm

    class Meta:
        model = models.Company
        fields = [
            'id',
            'symbol',
            'fullName',
            'bourseType',
            'tse',
            'site',
            'isTarget',
            'category',
        ]
        read_only_fields = ['id', 'symbol', 'fullName', 'bourseType', 'tse', 'site', 'isTarget']


class ChartSymbolsSerializer(serializers.ModelSerializer):  # forms.ModelForm

    class Meta:
        model = models.Chart
        fields = [
            'id',
            'company',
            'createAt',
            'timeFrame',
            'data',
        ]
        read_only_fields = ['id', 'company', 'createAt', 'timeFrame', 'data']
        depth = 1


class UserSerializer(serializers.ModelSerializer):  # forms.ModelForm

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
        ]
        read_only_fields = ['id', 'username', 'first_name', 'last_name']


class ChatMessageSerializer(serializers.ModelSerializer):  # forms.ModelForm
    receiver_name = serializers.SerializerMethodField(read_only=True)
    sender_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.ChatMessage
        fields = [
            'id',
            'sender',
            'sender_name',
            'receiver',
            'receiver_name',
            'createAt',
            'isSeen',
            'description',
        ]
        read_only_fields = ['id', 'receiver_name', 'sender_name']

    def get_receiver_name(self, obj):
        return str(obj.receiver.username)

    def get_sender_name(self, obj):
        return str(obj.sender.username)


class TechnicalUserSerializer(serializers.ModelSerializer):  # forms.ModelForm
    user_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.TechnicalUser
        fields = [
            'id',
            'user',
            'user_name',
            'createAt',
            'company',
            'title',
            'isShare',
            'data',
        ]
        read_only_fields = ['id', 'user', 'user_name']

    def get_user_name(self, obj):
        return str(obj.user.username)

    def validate_title(self, value):
        qs = models.TechnicalUser.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title has already been used")
        return value


class ListSymbolSerializer(serializers.ModelSerializer):  # forms.ModelForm
    symbol = serializers.SerializerMethodField(read_only=True)
    symbolPic = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.RequestSymbol
        fields = [
            'id',
            'company',
            'symbol',
            'symbolPic',
            'user',
            'createAt',
            'analyzedAt',
            'isAnalyzed',
        ]
        read_only_fields = ['id', 'symbol', 'user', 'createAt']

    def get_symbol(self, obj):
        return str(obj.company.symbol)

    def get_symbolPic(self, obj):
        return str(obj.company.pic)


class ListStockPortfolio(serializers.ModelSerializer):  # forms.ModelForm
    symbol = serializers.SerializerMethodField(read_only=True)
    symbolPic = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.StockPortfolio
        fields = [
            'id',
            'company',
            'symbol',
            'symbolPic',
            'user',
            'createAt',
        ]
        read_only_fields = ['id', 'symbol', 'user', 'createAt']

    def get_symbol(self, obj):
        return str(obj.company.symbol)

    def get_symbolPic(self, obj):
        return str(obj.company.pic)


class CandleSerializer(serializers.ModelSerializer):  # forms.ModelForm

    class Meta:
        model = models.Candle
        fields = [
            # 'id',
            # 'company',
            # 'timeFrame',
            'dateTime',
            'open',
            'close',
            'high',
            'low',
            'volume',
        ]
        read_only_fields = ['dateTime', 'open', 'close', 'high', 'low', 'volume']


class ChartSerializer(serializers.ModelSerializer):  # forms.ModelForm
    symbol = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Chart
        fields = [
            # 'id',
            'lastCandleDate',
            'company',
            'symbol',
            'timeFrame',
            'data',
        ]
        read_only_fields = ['lastCandleDate', 'company', 'timeFrame', 'data']

    def get_symbol(self, obj):
        return str(obj.company.symbol)

