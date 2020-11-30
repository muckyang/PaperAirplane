from .models import Store
from .models import Review
from .models import TourSpot
from .models import Course
from .models import Recommand
from .models import Overview
from .models import CollaborMenu
from .models import Route
from .models import RouteDetail
from rest_framework import serializers



class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "store_name",
            "branch",
            "area",
            "tel",
            "address",
            "latitude",
            "longitude",
            "category_list",
            "menu_list",
            "bhour_list",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "storeid",
            "userid",
            "score",
            "content",
            "regtime",
            "gender",
            "bornyear",
        ]

class TourSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourSpot
        fields = [
            "id",
            "addr1",
            "addr2",
            "areacode",
            "cat1",
            "cat2",
            "cat3",
            "content_id",
            "content_type_id",
            "first_image",
            "first_image2",
            "mapx",
            "mapy",
            "sigungucode",
            "tel",
            "title",
            "readcount",
        ]

class CourseSerializer(serializers.ModelSerializer):
   class Meta:
        model = Course
        fields = [
            "id",
            "addr1",
            "addr2",
            "areacode",
            "cat1",
            "cat2",
            "cat3",
            "content_id",
            "content_type_id",
            "first_image",
            "first_image2",
            "mapx",
            "mapy",
            "sigungucode",
            "tel",
            "title",
            "readcount",
        ]

class RecommandSerializer(serializers.ModelSerializer):
   class Meta:
        model = Recommand
        fields = [
            "contentid",
            "contenttypeid",
            "subcontentid",
            "subdetailalt",
            "subdetailimg",
            "subdetailoverview",
            "subname",
            "subnum", 
        ]

class OverviewSerializer(serializers.ModelSerializer):
   class Meta:
        model = Overview
        fields = [
            "contentid",
            "contenttypeid",
            "homepage",
            "overview",
            "tel",
            "title", 
        ]

class CollaborMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollaborMenu
        fields = [
            "index",
            "selected_store",
            "recommended_store",
            "similarity",
        ]  

class RouteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteDetail
        fields = ['rdid','rdusername','rid','rdtype','rdtypeid','rdimg','rdtitle','rdoverview','rdlat','rdlon']

class RouteSerializer(serializers.ModelSerializer):
    # Detail=RouteDetailSerializer(many=True)

    class Meta:
        model = Route
        fields = ['route_id','route_username','route_title','route_img','route_click']