import time

from ScrapingTool.Generic.constant import *
from ScrapingTool.controller.get_model_names.brand_name_scraping import *
from ScrapingTool.controller.get_review_from_forum.Gsmarena_get_issue import gsmarena_get_issue
from ScrapingTool.controller.get_review_from_forum.android_forum_get_issue import android_forum_get_issue
from ScrapingTool.controller.get_review_from_forum.sonyforum_get_issue import sony_forum_get_issue
from ScrapingTool.controller.get_model_names.model_name_scraping import *


from ScrapingTool.Generic.parser import parse
from ScrapingTool.controller.get_review_from_forum.gadget360_get_issue import gadget360_get_issue


def get_brand_names(request):
    """

    :param url:
    :return:
    """
    url = request.session.get('mainurl')
    if ANDROID_FORUM_STRING in url:
        url = url+"devices/list/"
    elif ANDROID_PIT_FORUM_STRING in url:
        url = url + "forum/"
    elif GADGETS_FORUM_STRING in url:
        url = url + "mobiles/all-brands"
    elif SONY_FORUM_STRING in url:
        url = url + "/t5/Phones-Tablets/ct-p/Phones"
    print("url",url)
    soup = parse(url)
    mobile_brand_list = []
    mobile_brand_links_list = []

    if GSMARRENS_STRING in url:
        get_brand_name_from_gsmarena(soup,mobile_brand_list,mobile_brand_links_list)
    elif ANDROID_FORUM_STRING in url:
        get_brand_name_from_androidforum(soup,mobile_brand_list,mobile_brand_links_list)
    elif ANDROID_PIT_FORUM_STRING in url:
        get_brand_name_from_androidpit_forum(soup,mobile_brand_list,mobile_brand_links_list)
    elif GADGETS_FORUM_STRING in url:
        get_brand_name_from_gadget360(soup, mobile_brand_list, mobile_brand_links_list)
    elif SONY_FORUM_STRING in url:
        get_brand_name_forum_sonyforum(soup, mobile_brand_list, mobile_brand_links_list)

    return mobile_brand_list,mobile_brand_links_list


def get_models_names(request,url):
    model_name_dic=()

    soup = parse(url)

    if GSMARRENS_STRING in url:
        model_name_dic = get_models_names_from_gsmarena(request,soup,url)
    elif ANDROID_FORUM_STRING in url:
        model_name_dic = get_models_names_from_android_forum(request,soup)
    elif ANDROID_PIT_FORUM_STRING in url:
        model_name_dic = get_models_names_from_android_pit_forum(request,soup,url)
    elif GADGETS_FORUM_STRING in url:
        model_name_dic = get_models_names_from_gadgets360(request,soup)
    elif SONY_FORUM_STRING in url:
        model_name_dic = get_models_names_from_sonyforum(request, soup)
        
    return model_name_dic


def get_data_from_url(request,url,selected_model_url,selected_dates):
    data_dictionary = {}
    start_time = time.time()
    if ANDROID_FORUM_STRING in url:
        data_dictionary = android_forum_get_issue(request, selected_model_url, selected_dates)
    elif GSMARRENS_STRING in url:
        data_dictionary = gsmarena_get_issue(request, selected_model_url, selected_dates)
    elif GADGETS_FORUM_STRING in url :
        data_dictionary = gadget360_get_issue(request, selected_model_url, selected_dates)
    elif SONY_FORUM_STRING in url:
        data_dictionary = sony_forum_get_issue(request, selected_model_url, selected_dates)
    end_time = time.time()

    execution_time_in_sec = end_time-start_time
    execution_time = convert(execution_time_in_sec)

    print("Time taken to fetch the data ",execution_time )

    return data_dictionary


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)