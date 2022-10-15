# generic
from datetime import datetime

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from bourseapp import models
from . import serializers
import operator
import functools

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from drf_rw_serializers import generics, viewsets, mixins

from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from django.db.models import Count, F

"""
-- Category class --
"""


class CategoryAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.CategorySerializer

    # permission_classes = []#[IsOwnerOrReadOnly]
    # queryset                = BlogPost.objects.all()

    # search, ?q=tt
    def get_queryset(self):
        qs = models.Category.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
                # | Q(pic__icontains=query)
            ).distinct()

        query_list = self.request.GET.get("list")
        if query_list is not None:
            ls = query_list.split('_')
            for itm in ls:
                param = itm.split(':')
                itmId = param[0]
                itmVar = param[1]
                models.Category.objects.filter(pk=itmId).update(orderNum=itmVar)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def get_serializer_context(self, *args, **kwargs):
    # return {"request": self.request}


class CategoryRudView(generics.RetrieveUpdateDestroyAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    # queryset                = BlogPost.objects.all()

    def get_queryset(self):
        return models.Category.objects.all()

    # def get_serializer_context(self, *args, **kwargs):
    #     return {"request": self.request}

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return BlogPost.objects.get(pk=pk)


class SymbolsAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.SymbolSerializer

    # search, ?q=tt
    def get_queryset(self):
        qs = models.Company.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(symbol__startswith=query)
                # | Q(pic__icontains=query)
            ).distinct()

        query_category = self.request.GET.get("c")
        if query_category is not None:
            qs = qs.filter(
                Q(category=query_category)
            ).distinct()

        return qs


class ChartSymbolsAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.ChartSymbolsSerializer

    # search, ?q=tt
    def get_queryset(self):
        qs = models.Chart.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(company__symbol__startswith=query)
                # | Q(pic__icontains=query)
            ).distinct()

        return qs


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserList(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]  # [IsOwnerOrReadOnly, IsAuthenticated]
    # pagination_class = StandardResultsSetPagination

    # search, ?q=tt
    def get_queryset(self):
        qs = User.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(username__icontains=query)
            ).distinct()

        return qs[:20]


class ChatMessageAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.ChatMessageSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    # search, ?q=tt
    def get_queryset(self):
        qs = models.ChatMessage.objects.all()
        # limit msgs
        if self.request.user.groups.filter(name='level1').exists() is False and self.request.user.is_superuser is False:
            qs = qs.filter(
                Q(receiver=self.request.user) | Q(sender=self.request.user)
            ).distinct()

        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(description__icontains=query)
                # | Q(pic__icontains=query)
            ).distinct()

        query_target = self.request.GET.get("target")
        if query_target is not None:
            qs = qs.filter(
                (Q(receiver=query_target) & Q(sender=self.request.user))
                |
                (Q(receiver=self.request.user) & Q(sender=query_target))
            ).distinct()

        query_user2admin = self.request.GET.get("user2admin")
        query_admin = self.request.GET.get("admin")
        if query_user2admin is not None and query_admin is not None:
            qs = qs.filter(
                (Q(receiver=query_user2admin) & Q(sender=query_admin))
                |
                (Q(receiver=query_admin) & Q(sender=query_user2admin))
            ).distinct()

        return qs

    def perform_create(self, serializer):
        # serializer.save(sender=self.request.user)
        serializer.save()
        # tick all unseen messages
        if get_user_model().objects.get(id=self.request.data['sender']).username == 'admins':
            user_reciver = get_user_model().objects.get(id=self.request.data['receiver'])
            unReadMsg = models.ChatMessage.objects.filter(Q(sender=user_reciver) & Q(isSeen=False))
            unReadMsg.update(isSeen=True)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def get_serializer_context(self, *args, **kwargs):
    # return {"request": self.request}


class ChatMessageRudView(generics.RetrieveUpdateDestroyAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.ChatMessageSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    # queryset                = BlogPost.objects.all()

    def get_queryset(self):
        return models.ChatMessage.objects.all()


class TechnicalUserAPIView(mixins.CreateModelMixin, generics.ListAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.TechnicalUserSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    # search, ?q=tt
    def get_queryset(self):

        query = self.request.GET.get("share")
        query_company = self.request.GET.get("company")
        if query is not None and query_company is not None:
            qs = models.TechnicalUser.objects.filter(
                Q(isShare=True)
                & Q(company=query_company)
            ).distinct()
            return qs

        qs = models.TechnicalUser.objects.filter(user=self.request.user)

        if query_company is not None:
            qs = qs.filter(
                Q(company=query_company)
                # | Q(pic__icontains=query)
            ).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TechnicalUserRudView(generics.RetrieveUpdateDestroyAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.TechnicalUserSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    # queryset                = BlogPost.objects.all()

    def get_queryset(self):
        return models.TechnicalUser.objects.all()


def chart_detail(request, company_id):
    chart = get_object_or_404(models.Chart, company=company_id, timeFrame='D1')
    profile_json = {
        "data": chart.data.url,
    }
    return JsonResponse(profile_json, safe=False)


def ChartView(request):

    # chart = get_object_or_404(models.Chart, company__symbol__icontains='شاخص بازار بورس', timeFrame='D1')
    chart_list = models.Chart.objects.filter(Q(company__symbol__icontains='شاخص کل')
                                             & Q(timeFrame='D1'))
    # print(chart_list)
    if len(chart_list) > 0:
        chart = chart_list.first()
        # print(chart.data.url)
        profile_json = {
            "data": chart.data.url,
        }
    else:
        profile_json = {
            "data": "not found",
        }
    return JsonResponse(profile_json, safe=False)


@login_required
def AddSymbolAnalyze(request):

    symbols = request.GET.getlist('symbols[]')
    if symbols is not None:
        company_list = models.Company.objects.filter(id__in=symbols)
        for item in symbols:
            company = get_object_or_404(models.Company, pk=int(item))
            obj, created = models.RequestSymbol.objects.get_or_create(
                user=request.user,
                company=company,
            )
    else:
        return JsonResponse({'data': 'nothing to add'}, safe=False)
    return JsonResponse({'data': 'symbols added'}, safe=False)


class ListSymbolAnalyze(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.ListSymbolSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = []

        query_rem = self.request.GET.get("remove")
        if query_rem is not None:
            models.RequestSymbol.objects.filter(id=query_rem).delete()
            return qs

        query = self.request.GET.get("q")
        if query is not None:
            qs = models.RequestSymbol.objects.filter(
                Q(user=query)
            ).distinct()

        return qs



@login_required
def AddPortfolio(request):

    symbols = request.GET.getlist('symbols[]')
    if symbols is not None:
        company_list = models.Company.objects.filter(id__in=symbols)
        for item in symbols:
            company = get_object_or_404(models.Company, pk=int(item))
            obj, created = models.StockPortfolio.objects.get_or_create(
                user=request.user,
                company=company,
            )
    else:
        return JsonResponse({'data': 'nothing to add'}, safe=False)
    return JsonResponse({'data': 'symbols added'}, safe=False)


class ListPortfolio(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.ListStockPortfolio
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]
    # pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = []

        query_rem = self.request.GET.get("remove")
        if query_rem is not None:
            models.StockPortfolio.objects.filter(id=query_rem).delete()
            return qs

        query = self.request.GET.get("q")
        if query is not None:
            qs = models.StockPortfolio.objects.filter(
                Q(user=query)
            ).distinct()

        return qs


@api_view(['POST'])
def symbol_candle(request, company_name, time_frame):
    # date = request.data.getlist('date[]')
    candle = request.data
    # print(request.data)
    # json = loads(request.data)
    # print(json)
    if candle is not None:
        # print('company')
        company = get_object_or_404(models.Company, alias=company_name)
        # print(company)
        for itm in candle:
            if len(itm) > 0 and models.Candle.objects.filter(Q(dateTime=itm['date'])&Q(company=company)).exists() is False:
                # print(itm['date'])
                models.Candle.objects.create(
                    open=itm['open']
                    , close=itm['close']
                    , high=itm['high']
                    , low=itm['low']
                    , volume=itm['vol']
                    , company=company
                    , timeFrame=time_frame
                    , dateTime=itm['date']
                )

    profile_json = {
        "data": 'data recieved',
    }

    return JsonResponse(profile_json, safe=False)

from django.db import models as md
@api_view(['POST'])
# def symbol_candle_file(request, company_name, time_frame, last_date):
def symbol_candle_file(request, company_name, time_frame, last_date):
    # print('request')
    # print(company_name)
    # print(time_frame)
    # print(last_date)
    # print(request.user)

    company = get_object_or_404(models.Company, alias=company_name)
    # print(company)

    chart = models.Chart.objects.filter(Q(timeFrame=time_frame) & Q(company=company))
    # new item
    if chart.exists() is False:
        models.Chart.objects.create(company=company
                                    , data=request.FILES['file']
                                    , timeFrame=time_frame
                                    , user=request.user
                                    , lastCandleDate=last_date)
    # update
    else:
        print('updated')
        # dummy_obj = models.Chart.objects.first()
        # dummy_obj.lastCandleDate = last_date
        # new_date = dummy_obj.lastCandleDate
        new_date = datetime.strptime(last_date, "%Y-%m-%d").date()
        chart = chart.first()
        chart_date = chart.lastCandleDate
        # type(chart_date)
        # type(new_date)
        # print(chart_date, new_date)
        if new_date > chart_date:
            print('updated success')
            chart.lastCandleDate = last_date
            chart.data = request.FILES['file']
            chart.save()

    profile_json = {
        "msg": 'data recieved',
        "symbol": company_name,
        "lastDate": last_date,
        "timeFrame": time_frame,
    }

    return JsonResponse(profile_json, safe=False)


@api_view(['POST'])
def symbol_candle_json(request, company_name, time_frame):
    # date = request.data.getlist('date[]')
    candle = request.data['jsonStr']
    last_date = request.data['lastdate']
    # print(request.data)
    # print(candle)
    # json = loads(request.data)

    # return JsonResponse({ "data": 'data recieved',}, safe=False)

    # print(json)
    if candle is not None and last_date is not None:
        print('company')
        company = get_object_or_404(models.Company, alias=company_name)
        print(company)
        candleJson = models.CandleJson.objects.filter(Q(timeFrame=time_frame)&Q(company=company))
        print(candleJson)

        if len(candleJson) == 0:
            # create new entry
            models.CandleJson.objects.create(company=company
                                             , timeFrame=time_frame
                                             , candleData=candle
                                             , lastCandleDate=last_date)
        else:
            # update las entry
            candleJson_u = candleJson[0]
            print(candleJson_u)
            candleJson_u.candleData = candle
            candleJson_u.lastCandleDate = last_date
            candleJson_u.save()
            # remove other entry
            cntr = 0
            for itm in candleJson:
                if cntr == 0:
                    pass
                else:
                    itm.delete()
                cntr = cntr + 1

    profile_json = {
        "data": 'data recieved',
    }

    return JsonResponse(profile_json, safe=False)


class SymbolCandleListAPIView(generics.ListAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = serializers.CandleSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = []

        query = self.request.GET.get("company")
        query_timeFrame = self.request.GET.get("timeFrame")
        # query_last = self.request.GET.get("last")
        if query is not None and query_timeFrame is not None:

            # if query_last is not None:
            #     return models.Candle.objects.latest('pk')

            qs = models.Candle.objects.filter(
                Q(company=query)
                & Q(timeFrame=query_timeFrame)
            ).distinct()


        return qs


class SymbolCandleJsonListAPIView(generics.ListAPIView):  # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = serializers.ChartSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = []
        # qs = models.CandleJson.objects.all()

        query = self.request.GET.get("company")
        # query_time_frame = self.request.GET.get("timeFrame")
        # if query is not None and query_time_frame is not None:
        if query is not None:
            qs = models.Chart.objects.filter(
                Q(company=query)
                # & Q(timeFrame=query_time_frame)
            ).distinct()

        return qs


def SymbolListTitle(request):

    if request.GET.get("timeframe") is not None:
        list_symbol_tf = models.Chart.objects.values('company__id', 'company__symbol', 'company__alias'
                                                          , 'timeFrame', 'lastCandleDate').order_by('company__id')
        return JsonResponse(list(list_symbol_tf), safe=False)

    list_symbol = models.Chart.objects.values('company__id', 'company__symbol', 'company__alias')\
        .order_by('company__id')\
        .annotate(dcount=Count('company__id'))\
        .distinct()
    # print(list_symbol)
    return JsonResponse(list(list_symbol), safe=False)
