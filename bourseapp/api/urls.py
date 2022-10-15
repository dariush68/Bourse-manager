from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .views import *

app_name = 'api-bourseapp'

urlpatterns = [
    url(r'^Category$', views.CategoryAPIView.as_view(), name='post-listcreate'),
    # url(r'^Category/(?P<pk>\d+)/$', views.CategoryRudView.as_view(), name='post-rud'),

    url(r'^Symbols$', views.SymbolsAPIView.as_view(), name='symbols-view'),
    url(r'^chart-symbols$', views.ChartSymbolsAPIView.as_view(), name='chart-symbols'),
    url(r'^user-list$', views.UserList.as_view(), name='user-list'),

    url(r'^add-symbol-analyze$', views.AddSymbolAnalyze, name='add-symbol-analyze'),
    url(r'^list-symbol-analyze$', views.ListSymbolAnalyze.as_view(), name='list-symbol-analyze'),

    url(r'^add-symbol-portfolio$', views.AddPortfolio, name='add-symbol-portfolio'),
    url(r'^list-symbol-portfolio$', views.ListPortfolio.as_view(), name='list-symbol-portfolio'),

    # url(r'^set-candle$', views.UserList.as_view(), name='user-list'),

    url(r'^ChatMessage$', views.ChatMessageAPIView.as_view(), name='post-listcreate-chatMessage'),
    url(r'^ChatMessage/(?P<pk>\d+)/$', views.ChatMessageRudView.as_view(), name='post-rud-chatMessage'),

    url(r'^TechnicalUser$', views.TechnicalUserAPIView.as_view(), name='post-listcreate-technicalUser'),
    url(r'^TechnicalUser/(?P<pk>\d+)/$', views.TechnicalUserRudView.as_view(), name='post-rud-technicalUser'),

    url(r'^ChartBazaar$', views.ChartView, name='chart-bazaar-view'),
    url(r'^(?P<company_id>[0-9]+)/chart-detail/$', views.chart_detail, name='chart-detail'),
    url(r'^(?P<company_name>[a-zA-Z]+)/(?P<time_frame>[a-zA-Z0-9]+)/symbol-candle/$', views.symbol_candle, name='symbol-candle'),
    url(r'^symbol-candle-list$', views.SymbolCandleListAPIView.as_view(), name='post-symbol-candle-list'),

    url(r'^(?P<company_name>[a-zA-Z]+)/(?P<time_frame>[a-zA-Z0-9]+)/symbol-candle-json/$', views.symbol_candle_json,
        name='symbol-candle-json'),
    # url(r'^(?P<company_name>[a-zA-Z]+)/(?P<time_frame>[a-zA-Z0-9]+)/(?P<last_date>[a-zA-Z0-9]+)/symbol-candle-file/$'
    #     , views.symbol_candle_file, name='symbol-candle-file'),
    url(r'^(?P<company_name>[a-zA-Z_]+)/(?P<time_frame>[a-zA-Z0-9]+)/(?P<last_date>\d{4}-\d{2}-\d{2})/symbol-candle-file/$'
        , views.symbol_candle_file, name='symbol-candle-file'),
    url(r'^symbol-candle-json-list$', views.SymbolCandleJsonListAPIView.as_view(), name='symbol-candle-json-list'),
    url(r'^symbol-candle-json-list-title$', views.SymbolListTitle, name='csymbol-candle-json-list-title'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
