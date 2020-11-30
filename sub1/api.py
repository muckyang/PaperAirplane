from urllib.request import urlopen
import json
import re
import pandas as pd
import os
import shutil

_API_ENDPOINT = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService'
_PARAMS = 'areaCode={0}&ServiceKey={1}&MobileOS={2}&MobileApp={3}&_type=json'

_URLS = {
    'tour_list': _API_ENDPOINT + '/areaBasedList?' + _PARAMS,
    'detail_common': _API_ENDPOINT + '/detailCommon?defaultYN=Y&overviewYN=Y&' + _PARAMS,
    'detail_intro': _API_ENDPOINT + '/detailIntro?' + _PARAMS,
    'additional_images': _API_ENDPOINT + '/detailImage?imageYN=Y&' + _PARAMS
}


areaCode=[1, 2, 3, 4, 5, 6, 7, 8, 31, 32, 33, 34, 35, 36, 37, 38, 39]


def _dict_key_changer(_dict, keychains):
    # _dict - 타겟 딕셔너리
    for k, v in keychains.items():
        # k - 바꿔야 할 legacy key
        # v - (바꿀 key, default 값)
        _dict[v[0]] = _dict.pop(k, v[1])


class TourAPI:
    def __init__(self, area_code, service_key, mobile_os='ETC', app_name='PlanB'):
        """
        :param area_code: Area code to initialize API
        :param service_key: Service code from data.go.kr
        :param mobile_os: Application os(AND, IOS, ETC)
        :param app_name: Service name
        :type area_code: int
        :type service_key: str
        :type mobile_os: str
        :type app_name: str
        """
        self.tour_list_url = _URLS['tour_list'].format(area_code, service_key, mobile_os, app_name) + '&numOfRows={0}'
        self.detail_common_url = _URLS['detail_common'].format(area_code, service_key, mobile_os, app_name) + '&contentId={0}'
        self.detail_intro_url = _URLS['detail_intro'].format(area_code, service_key, mobile_os, app_name) + '&contentId={0}&contentTypeId={1}'
        self.additional_images_url = _URLS['additional_images'].format(area_code, service_key, mobile_os, app_name) + '&contentId={0}&numOfRows={1}'

    def get_tour_list(self):
        """
        Inquire all tour list

        :rtype: list
        """
        resp = json.loads(urlopen(self.tour_list_url.format(1)).read().decode('utf-8'))
        total_count = resp['response']['body']['totalCount']
        # Get total count

        resp = json.loads(urlopen(self.tour_list_url.format(total_count)).read().decode('utf-8'))
        data = resp['response']['body']['items']['item']
        # Extract data list
       
        keychain = {
            'addr1': ('addr1', None),
            'addr2': ('addr2', None),
            'areacode': ('areacode', 0),
            'cat1': ('cat1', None),
            'cat2': ('cat2', None),
            'cat3': ('cat3', None),
            'contentid': ('contentid', 0),
            'contenttypeid': ('contenttypeid', 0),
            'firstimage': ('firstimage', None),
            'firstimage2': ('firstimage2', None),
            'mapx': ('mapx', 0.0),
            'mapy': ('mapy', 0.0),
            'sigungucode': ('sigungucode', 0),
            'tel': ('tel', None),
            'title': ('title', None),
            'readcount': ('readcount', 0),
        }

        for tour in data:
            _dict_key_changer(tour, keychain)

            tour['creation_date'] = str(tour.pop('createdtime'))[:8] if 'createdtime' in tour else None
            tour['modified_date'] = str(tour.pop('modifiedtime'))[:8] if 'modifiedtime' in tour else None

            # tour.pop('areacode', None)
            tour.pop('zipcode', None)
            tour.pop('mlevel', None)
            # Manufacture

        return data

    def get_detail_common(self, content_id):
        """
        Inquire common detail data

        :param content_id: Content ID to inquire
        :type content_id: str

        :rtype: dict
        """
        resp = json.loads(urlopen(self.detail_common_url.format(str(content_id))).read().decode('utf-8'))
        data = resp['response']['body']['items']['item']
        # Extract data

        keychain = {
            'contenttypeid': ('content_type_id', None),
            'overview': ('overview', None),
            'tel': ('tel', None),
            'telname': ('tel_owner', None),
            'booktour': ('in_book', 0)
        }
        _dict_key_changer(data, keychain)

        try:
            data['homepage'] = re.findall('http\w?://[\w|.]+', data.pop('homepage'))[0] if 'homepage' in data else None
        except IndexError:
            data['homepage'] = None

        data.pop('contentid', None)
        data.pop('title', None)
        data.pop('createdtime', None)
        data.pop('modifiedtime', None)
        # Manufacture

        return data

    def get_detail_intro(self, content_id):
        """
        Inquire detail introduction

        :param content_id: Content ID to inquire
        :type content_id: str

        :rtype: dict
        """
        content_type_id = self.get_detail_common(content_id)['content_type_id']
        # Get content type id

        resp = json.loads(urlopen(self.detail_intro_url.format(content_id, content_type_id)).read().decode('utf-8'))
        data = resp['response']['body']['items']['item']
        # Extract data

        del data['contentid']
        del data['contenttypeid']

        if content_type_id == 12:
            # 관광지
            keychain = {
                'accomcount': ('capacity', None),
                'chkbabycarriage': ('baby_carriage', None),
                'chkcreditcard': ('credit_card', None),
                'chkpet': ('pet', None),
                'expagerange': ('age_range', None),
                'expguide': ('guide', None),
                'infocenter': ('info_center', None),
                'opendate': ('open_date', None),
                'parking': ('parking', None),
                'restdate': ('rest_date', None),
                'useseason': ('season', None),
                'usetime': ('use_time', None)
            }
            _dict_key_changer(data, keychain)

            data['cultural_heritage'] = data.pop('heritage1', None) == 1
            data['natural_heritage'] = data.pop('heritage2', None) == 1
            data['archival_heritage'] = data.pop('heritage3', None) == 1
        elif content_type_id == 14:
            # 문화시설
            keychain = {
                'accomcountculture': ('capacity', None),
                'chkbabycarriageculture': ('baby_carriage', None),
                'chkcreditcardculture': ('credit_card', None),
                'chkpetculture': ('pet', None),
                'discountinfo': ('discount_info', None),
                'infocenterculture': ('info_center', None),
                'parkingculture': ('parking', None),
                'parkingfee': ('parking_fee', None),
                'restdateculture': ('rest_date', None),
                'usefee': ('use_fee', None),
                'usetimeculture': ('use_time', None),
                # 이용시간
                'scale': ('scale', None),
                'spendtime': ('spend_time', None)
                # 관람 소요시간
            }
            _dict_key_changer(data, keychain)
        elif content_type_id == 15:
            # 축제/공연/행사
            keychain = {
                'agelimit': ('age_limit', None),
                'bookingplace': ('reservation_place', None),
                'eventstartdate': ('start_date', None),
                'eventenddate': ('end_date', None),
                'eventplace': ('place', None),
                'festivalgrade': ('festival_grade', None),
                'placeinfo': ('place_guide', None),
                'spendtimefestival': ('spend_time', None),
                'sponsor1': ('organizer', None),
                'sponsor2': ('host', None),
                'subevent': ('sub_event', None),
                'usetimefestival': ('use_fee', None)
            }
            _dict_key_changer(data, keychain)

            data.pop('eventhomepage', None)
        elif content_type_id == 25:
            # 여행코스
            keychain = {
                'distance': ('distance', None),
                'infocentertourcourse': ('info_center', None),
                'schedule': ('schedule', None),
                'taketime': ('spend_time', None),
                'theme': ('theme', None)
            }
            _dict_key_changer(data, keychain)
        elif content_type_id == 28:
            # 레포츠
            keychain = {
                'accomcountleports': ('capacity', None),
                'chkbabycarriageleports': ('baby_carriage', None),
                'chkcreditcardleports': ('credit_card', None),
                'chkpetleports': ('pet', None),
                'expagerangeleports': ('age_range', None),
                'infocenterleports': ('info_center', None),
                'openperiod': ('open_period', None),
                'parkingleports': ('parking', None),
                'parkingfeeleports': ('parking_fee', None),
                'reservation': ('reservation_info', None),
                'restdateleports': ('rest_date', None),
                'scaleleports': ('scale', None),
                'usetimeleports': ('use_time', None),
                'usefeeleports': ('use_fee', None),
            }
            _dict_key_changer(data, keychain)
        elif content_type_id == 32:
            # 숙박
            keychain = {
                'accomcountlodging': ('capacity', None),
                'checkintime': ('checkin_time', None),
                'checkouttime': ('checkout_time', None),
                'foodplace': ('food_field', None),
                'infocenterlodging': ('info_center', None),
                'parkinglodging': ('parking', None),
                'pickup': ('pickup_service', None),
                'reservationlodging': ('reservation_info', None),
                'roomtype': ('room_type', None),
                'scalelodging': ('scale', None),
                'subfacility': ('sub_facility', None)
            }
            _dict_key_changer(data, keychain)

            data['benikia'] = data.pop('benikia', False) == 1
            data['cooking'] = data.pop('chkcooking', False) == 1
            data['goodstay'] = data.pop('goodstay', False) == 1
            data['korean_house'] = data.pop('hanok', False) == 1
            data['barbecue'] = data.pop('barbecue', False) == 1
            data['beauty'] = data.pop('beauty', False) == 1
            data['beverage'] = data.pop('beverage', False) == 1
            data['bicycle'] = data.pop('bicycle', False) == 1
            data['campfire'] = data.pop('campfire', False) == 1
            data['fitness'] = data.pop('fitness', False) == 1
            data['karaoke'] = data.pop('karaoke', False) == 1
            data['public_bath'] = data.pop('publicbath', False) == 1
            data['public_pc'] = data.pop('publicpc', False) == 1
            data['sauna'] = data.pop('sauna', False) == 1
            data['seminar'] = data.pop('seminar', False) == 1
            data['sports'] = data.pop('sports', False) == 1
        elif content_type_id == 38:
            # 쇼핑
            keychain = {
                'chkbabycarriageshopping': ('baby_carriage', None),
                'chkcreditcardshopping': ('credit_card', None),
                'chkpetshopping': ('pet', None),
                'fairday': ('fair_day', None),
                'infocentershopping': ('info_center', None),
                'opendateshopping': ('open_date', None),
                'opentime': ('use_time', None),
                'parkingshopping': ('parking', None),
                'restdateshopping': ('rest_date', None),
                'restroom': ('restroom_info', None),
                'saleitem': ('sale_item', None),
                'saleitemcost': ('sale_item_cost', None),
                'scaleshopping': ('scale', None),
                'shopguide': ('guide', None)
            }
            _dict_key_changer(data, keychain)
        elif content_type_id == 39:
            # 음식
            keychain = {
                'chkcreditcardfood': ('credit_card', None),
                'discountinfofodd': ('discount_info', None),
                'firstmenu': ('rep_menu', None),
                'infocenterfood': ('info_center', None),
                'kidsfacility': ('kids_facility', None),
                'opendatefood': ('open_date', None),
                'opentimefood': ('open_time', None),
                'packing': ('packing', None),
                'parkingfood': ('parking', None),
                'reservationfood': ('reservation_info', None),
                'restdatefood': ('rest_date', None),
                'scalefood': ('scale', None),
                'seat': ('seat', None),
                'smoking': ('smoking', None),
                'treatmenu': ('treat_menus', None)
            }
            _dict_key_changer(data, keychain)

            data['kids_facility'] = data.pop('kidsfacility') == 1 if 'kidsfacility' in data else False

        return data

    def get_detail_images(self, content_id):
        """
        Inquire detail images

        :param content_id: Content ID to inquire
        :type content_id: str

        :rtype: list
        """
        resp = json.loads(urlopen(self.additional_images_url.format(content_id, 1)).read().decode('utf-8'))
        total_count = resp['response']['body']['totalCount']
        # Get total count

        resp = json.loads(urlopen(self.additional_images_url.format(content_id, total_count)).read().decode('utf-8'))
        try:
            data = resp['response']['body']['items']['item']
            # Extract data list
            if type(data) is dict:
                data.pop('contentid', None)
                data.pop('serialnum', None)
                data['origin'] = data.pop('originimgurl', None)
                data['small'] = data.pop('smallimageurl', None)
                # Manufacture
            else:
                for img in data:
                    if type(img) is dict:
                        img.pop('contentid', None)
                        img.pop('serialnum', None)
                        img['origin'] = img.pop('originimgurl', None)
                        img['small'] = img.pop('smallimageurl', None)
                        # Manufacture
                    else:
                        del img

            return data if type(data) is list else [data]
        except TypeError:
            return None



if __name__ == '__main__':
        with open('../data/tour.json', 'r', encoding='UTF8') as f:
            json_data = json.load(f)
            for a in json_data:             
                c = a['contenttypeid']
                if(c!=25 and c!=39):    
                    with open('../data/tour1.json', 'a', encoding="utf-8") as make_file:
                        json.dump(a, make_file, ensure_ascii=False, indent="\t")
                # for code in areaCode:
                # api = TourAPI(code, 'KXHJixjWCXP3fBBZ5NueQ9THlpZV2IyPrZeZvDSuxyoL6DT9wfMij3zZqZTeQZYeulfeh0rToqNpNXeF9Todyg%3D%3D')
             
                # with open('../data/tour1.json', 'a', encoding="utf-8") as make_file:
                # json.dump(api.get_tour_list(), make_file, ensure_ascii=False, indent="\t")