from django.conf.urls import url
from . import views

app_name = 'bourseapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # manager panel urls
    url(r'^manager-panel/$', views.manager_panel, name='manager-panel'),
    url(r'^user-panel/$', views.user_panel, name='user-panel'),
    url(r'^(?P<user_id>[0-9]+)/user-approve/$', views.user_approve, name='user-approve'),
    url(r'^(?P<user_id>[0-9]+)/(?P<status>[0-9]+)/user-vip/$', views.user_vip, name='user-vip'),

    # message urls
    url(r'^messenger/$', views.messenger, name='messenger'),

    # category urls
    url(r'^category-list/$', views.category_list, name='category-list'),
    url(r'^(?P<category_id>[0-9]+)/category-detail/$', views.category_detail, name='category-detail'),

    # company urls
    url(r'^company-list/$', views.company_list, name='company-list'),
    url(r'^(?P<company_id>[0-9]+)/company-detail/$', views.company_detail, name='company-detail'),
    url(r'^(?P<company_id>[0-9]+)/company-technical-view/$', views.company_technical_view, name='company-technical-view'),
    url(r'^company-analyzed/$', views.company_analyzed, name='company-analyzed'),

    # new urls
    url(r'^news-list/$', views.new_list, name='news-list'),
    url(r'^news-create/$', views.news_create, name='news-create'),
    url(r'^(?P<news_id>[0-9]+)/news-detail/$', views.news_detail, name='news-detail'),
    url(r'^(?P<news_id>[0-9]+)/news-approve/$', views.news_approve, name='news-approve'),
    url(r'^news-important/$', views.news_important, name='news-important'),
    # path('create', views.ContactCreate.as_view(), name='contact_create'),

    # technical urls
    url(r'^technical-list/$', views.technical_list, name='technical-list'),
    url(r'^(?P<technical_id>[0-9]+)/technical-detail/$', views.technical_detail, name='technical-detail'),

    # webinar urls
    url(r'^webinar-list/$', views.webinar_list, name='webinar-list'),
    url(r'^(?P<webinar_id>[0-9]+)/webinar-detail/$', views.webinar_detail, name='webinar-detail'),

    # bazaar urls
    url(r'^bazzar-list/$', views.bazaar_list, name='bazaar-list'),
    url(r'^(?P<bazaar_id>[0-9]+)/bazaar-detail/$', views.bazaar_detail, name='bazaar-detail'),

    # fundamental urls
    url(r'^fundamental-list/$', views.fundamental_list, name='fundamental-list'),
    url(r'^(?P<fundamental_id>[0-9]+)/fundamental-detail/$', views.fundamental_detail, name='fundamental-detail'),

    # tutorial urls
    url(r'^tutorial-list/$', views.tutorial_list, name='tutorial-list'),
    url(r'^(?P<tutorial_id>[0-9]+)/tutorial-detail/$', views.tutorial_detail, name='tutorial-detail'),
    url(r'^(?P<tutorialCategory_id>[0-9]+)/tutorial-category/$', views.tutorial_category, name='tutorial-category'),
    url(r'^(?P<tutorialSubCategory_id>[0-9]+)/tutorial-subCategory/$', views.tutorial_subCategory, name='tutorial-subCategory'),

    # message urls
    url(r'^message-list/$', views.message_list, name='message-list'),

]
