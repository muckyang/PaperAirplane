from api import models, serializers
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F, Q
import random
from .models import Route,RouteDetail
from .serializers import RouteSerializer
import pandas as pd
import surprise

class SmallPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 50


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        region = self.request.query_params.get("region", "")
        name = self.request.query_params.get("name", "")
        # categoryid = 1 -> 지역 관계 없이 가게 이름으로 검색
        if region == "전체" and name is not None:
            queryset = models.Store.objects.all().filter(store_name__contains=name).order_by("id")
            return queryset
        # categoryid = 2 -> 선택한 지역의 가게 이름으로 검색
        elif region is not None and name is not None:
            queryset =  models.Store.objects.all().filter(address__contains=region, store_name__contains=name).order_by("id")
            return queryset
        # 전체 검색
        else:
            queryset =  models.Store.objects.all()
            return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        storeid = self.request.query_params.get("storeid", "")
        if storeid=="":
            queryset = (
                models.Review.objects.all().filter(storeid__contains=storeid).order_by("id")
            )
            return queryset
        if storeid!="":
            queryset = (
                models.Review.objects.all().filter(storeid=storeid).order_by("id")
            )
            return queryset

class TourSpotViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TourSpotSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        region = self.request.query_params.get("region", "")
        name = self.request.query_params.get("name", "")
        # categoryid = 1 -> 지역 관계 없이 가게 이름으로 검색
        if region == "전체" and name is not None:
            queryset = models.TourSpot.objects.all().filter(title__contains=name).order_by("-readcount")
            return queryset
        # categoryid = 2 -> 선택한 지역의 가게 이름으로 검색
        elif region is not None and name is not None:
            queryset =  models.TourSpot.objects.all().filter(addr1__contains=region, title__contains=name).order_by("-readcount")
            return queryset
        # 전체 검색
        else:
            queryset =  models.TourSpot.objects.all()
            return queryset

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        areacode = self.request.query_params.get("areacode", "")
        if areacode !="":
            queryset = (
                models.Course.objects.all().filter(areacode=areacode).order_by("-readcount")
            )
            return queryset
        else:
            queryset = (
                models.Course.objects.all().order_by("-readcount")
            )
            return queryset

class OverviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OverviewSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        contentid = self.request.query_params.get("contentid", "")
        if contentid=="":
            queryset = (
                models.Overview.objects.all().filter(contentid__contains=contentid).order_by("contentid")
            )
            return queryset
        if contentid!="":
            queryset = (
                models.Overview.objects.all().filter(contentid=contentid).order_by("contentid")
            )
            return queryset
 
# 1. 지역만 
# 2. 위도경도만 
# 3. 검색어만 
# 4. 지역, 위도경도만 
# 5. 지역, 검색어만
# 6. 위도경도, 검색어만
# 7. 지역,위도경도,검색어
# 8. 아무것도 선택 X
# http://127.0.0.1:8000/api/recommendStores?region=&lat=&lon=&name=
class RecommendStoreSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    pagination_class = SmallPagination
    def get_queryset(self):
        region = self.request.query_params.get("region", "")
        lat = self.request.query_params.get("lat", "")
        lon = self.request.query_params.get("lon", "")
        name = self.request.query_params.get("name", "")
        
        # 0. 아무것도 선택 X
        if region == "전체" and len(lat)==0 and len(lon)==0 and len(name)==0:
            queryset =  models.Store.objects.all().order_by("id")
            return queryset

        # 1. 지역만
        elif region is not None and len(lat)==0 and len(lon)==0 and len(name)==0:
            queryset = models.Store.objects.all().filter(address__contains=region).order_by("id")
            return queryset


        # 2. 장바구니(위도, 경도)만
        elif region == "전체" and lat is not None and lon is not None and len(name)==0:
            # 위도 경도 계산 -> 가까운 순 부터
            print("22222222")
            dlat = Radians(F('latitude') - float(lat))
            dlong = Radians(F('longitude') - float(lon))

            a = (Power(Sin(dlat/2), 2) + Cos(Radians(float(lat))) 
                * Cos(Radians(F('latitude'))) * Power(Sin(dlong/2), 2)
            )

            c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
            d = 6371 * c

            queryset =  models.Store.objects.annotate(distance=d).exclude(Q(latitude=lat)&Q(longitude=lon)).order_by('distance')
            return queryset

        # 3. 검색어만 
        elif region == "전체" and len(lat)==0 and len(lon)==0 and name is not None:
            queryset = models.Store.objects.all().filter(store_name__contains=name).order_by("id")
            return queryset

        # 4. 지역, 장바구니(위도, 경도) 선택했을 때
        elif region is not None and lat is not None and lon is not None and len(name)==0:
            print("22222222")
            dlat = Radians(F('latitude') - float(lat))
            dlong = Radians(F('longitude') - float(lon))

            a = (Power(Sin(dlat/2), 2) + Cos(Radians(float(lat))) 
                * Cos(Radians(F('latitude'))) * Power(Sin(dlong/2), 2)
            )

            c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
            d = 6371 * c
            queryset =  models.Store.objects.annotate(distance=d).filter(address__contains=region).exclude(Q(latitude=lat)&Q(longitude=lon)).order_by('distance')
            return queryset

        # 5. 지역, 검색어 선택했을 때
        elif region is not None and len(lat)==0 and len(lon)==0 and name is not None:
            queryset =  models.Store.objects.filter(address__contains=region,store_name__contains=name)
            return queryset

        # 6. 장바구니(위도, 경도), 검색어 선택했을 때
        elif region == "전체" and lat is not None and lon is not None and name is not None:
            dlat = Radians(F('latitude') - float(lat))
            dlong = Radians(F('longitude') - float(lon))

            a = (Power(Sin(dlat/2), 2) + Cos(Radians(float(lat))) 
                * Cos(Radians(F('latitude'))) * Power(Sin(dlong/2), 2)
            )

            c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
            d = 6371 * c
            queryset =  models.Store.objects.annotate(distance=d).filter(store_name__contains=name).exclude(Q(latitude=lat)&Q(longitude=lon)).order_by('distance')
            return queryset

        # 7. 지역, 장바구니(위도, 경도), 검색어 선택했을 때
        elif region is not None and lat is not None and lon is not None and name is not None:
            dlat = Radians(F('latitude') - float(lat))
            dlong = Radians(F('longitude') - float(lon))

            a = (Power(Sin(dlat/2), 2) + Cos(Radians(float(lat))) 
                * Cos(Radians(F('latitude'))) * Power(Sin(dlong/2), 2)
            )

            c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
            d = 6371 * c
            queryset =  models.Store.objects.annotate(distance=d).filter(address__contains=region,store_name__contains=name).exclude(Q(latitude=lat)&Q(longitude=lon)).order_by('distance')
            return queryset

        else:
            queryset =  models.Store.objects.all().order_by("id")
            return queryset

# http://127.0.0.1:8000/api/recommendTourSpot?region=&mapy=&mapx=&name=
class RecommendTourSpotSet(viewsets.ModelViewSet):
    serializer_class = serializers.TourSpotSerializer
    pagination_class = SmallPagination
    def get_queryset(self):
        region = self.request.query_params.get("region", "")
        mapy = self.request.query_params.get("mapy", "")
        mapx = self.request.query_params.get("mapx", "")
        name = self.request.query_params.get("name", "")
        
        # 0. 아무것도 선택 X
        if region == "전체" and len(mapy)==0 and len(mapx)==0 and len(name)==0:
            queryset =  models.TourSpot.objects.all().order_by("-readcount")
            return queryset

        # 1. 지역만
        elif region is not None and len(mapy)==0 and len(mapx)==0 and len(name)==0:
            queryset = models.TourSpot.objects.all().filter(addr1__contains=region).order_by("-readcount")
            return queryset


        # 2. 장바구니(위도, 경도)만
        elif region == "전체" and mapy is not None and mapx is not None and len(name)==0:
            # 위도 경도 계산 -> 가까운 순 부터
            print("22222222")
            dlat = Radians(F('mapy') - float(mapy))
            dlong = Radians(F('mapx') - float(mapx))

            a = (Power(Sin(dlat/2), 2) + Cos(Radians(float(mapy))) 
                * Cos(Radians(F('mapy'))) * Power(Sin(dlong/2), 2)
            )

            c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
            d = 6371 * c

            queryset =  models.TourSpot.objects.annotate(distance=d).exclude(Q(mapy=mapy)&Q(mapx=mapx)).order_by('distance')
            return queryset

        # 3. 검색어만 
        elif region == "전체" and len(mapy)==0 and len(mapx)==0 and name is not None:
            queryset = models.TourSpot.objects.all().filter(Q(title__contains=name)|Q(addr1__contains=name)).order_by("-readcount")
            return queryset

        # 4. 지역, 장바구니(위도, 경도) 선택했을 때
        elif region is not None and mapy is not None and mapx is not None and len(name)==0:
            print("22222222")
            dlat = Radians(F('mapy') - float(mapy))
            dlong = Radians(F('mapx') - float(mapx))

            a = (Power(Sin(dlat/2), 2) + Cos(Radians(float(mapy))) 
                * Cos(Radians(F('mapy'))) * Power(Sin(dlong/2), 2)
            )

            c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
            d = 6371 * c
            queryset =  models.TourSpot.objects.annotate(distance=d).filter(addr1__contains=region).exclude(Q(mapy=mapy)&Q(mapx=mapx)).order_by('distance')
            return queryset

        # 5. 지역, 검색어 선택했을 때
        elif region is not None and len(mapy)==0 and len(mapx)==0 and name is not None:
            queryset =  models.TourSpot.objects.filter(Q(addr1__contains=region),(Q(title__contains=name)|Q(addr1__contains=name)))
            return queryset

        # 6. 장바구니(위도, 경도), 검색어 선택했을 때
        elif region == "전체" and mapy is not None and mapx is not None and name is not None:
            print("22222222")
            dlat = Radians(F('mapy') - float(mapy))
            dlong = Radians(F('mapx') - float(mapx))

            a = (Power(Sin(dlat/2), 2) + Cos(Radians(float(mapy))) 
                * Cos(Radians(F('mapy'))) * Power(Sin(dlong/2), 2)
            )

            c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
            d = 6371 * c
            queryset =  models.TourSpot.objects.annotate(distance=d).filter(Q(title__contains=name)|Q(addr1__contains=name)).exclude(Q(mapy=mapy)&Q(mapx=mapx)).order_by('distance')
            return queryset

        # 7. 지역, 장바구니(위도, 경도), 검색어 선택했을 때
        elif region is not None and mapy is not None and mapx is not None and name is not None:
            print("22222222")
            dlat = Radians(F('mapy') - float(mapy))
            dlong = Radians(F('mapx') - float(mapx))

            a = (Power(Sin(dlat/2), 2) + Cos(Radians(float(mapy))) 
                * Cos(Radians(F('mapy'))) * Power(Sin(dlong/2), 2)
            )

            c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
            d = 6371 * c
            queryset =  models.TourSpot.objects.annotate(distance=d).filter(Q(addr1__contains=region),(Q(title__contains=name)|Q(addr1__contains=name))).exclude(Q(mapy=mapy)&Q(mapx=mapx)).order_by('distance')
            return queryset

        else:
            queryset =  models.TourSpot.objects.all().order_by("id")
            return queryset


class RecommandViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecommandSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        contentid = self.request.query_params.get("contentid", "")
        if len(contentid) != 0:
            queryset = (
                models.Recommand.objects.all().filter(contentid=contentid).order_by("contentid")
            )
            return queryset
        else:
           
            queryset = (
                models.Recommand.objects.all().order_by("contentid")
            )
            return queryset

class TopFiveViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    pagination_class = SmallPagination
    def get_queryset(self):
        random = self.request.query_params.get("random", "")
        storeid = self.request.query_params.get("storeid", "")
        tourspotid = self.request.query_params.get("tourspotid", "")
        # 홈 화면에 유사도 높은 애들 5개 뽑아오기
        # http://127.0.0.1:8000/api/topFiveStores?random=()&storeid=
        if random is not None and len(storeid)==0:
            cnt=0
            if cnt==0:
                five=pick_number(random)
                cnt=cnt+1
            print(five)
            queryset=models.Store.objects.all().filter(id=five[0].recommended_store+1)
            print(int(five[0].recommended_store+1))
            for i in range(1,5):
                print(int(five[i].recommended_store+1))
                topfive=models.Store.objects.all().filter(id=int(five[i].recommended_store+1))
                queryset=topfive|queryset
            print(queryset)
            return queryset

        # 검색창에서 선택 시, 유사한 것 5개 뽑아오기
        # http://127.0.0.1:8000/api/topFiveStores?storeid=()
        elif storeid is not None:
            print("1111")
            print(storeid)
            five=similar(storeid)
            print(len(five))

            if len(five)==0:
                print("해당 선택 음식점에는 유사한 음식점이 없습니다.")
                body = {"message": "해당 선택 음식점에는 유사한 음식점이 없습니다."}
                queryset =  models.Store.objects.all().filter(id=0)
                return queryset

            elif five is not None:
                queryset=models.Store.objects.all().filter(id=five[0].recommended_store+1)
                print(int(five[0].recommended_store+1))
                for i in range(1,5):
                    print(int(five[i].recommended_store+1))
                    topfive=models.Store.objects.all().filter(id=int(five[i].recommended_store+1))
                    queryset=topfive|queryset
                print(queryset)
                return queryset

                
            
            


def pick_number(random):
    # number=random.randrange(0,2367)
    # print(number)
    storeid=models.CollaborMenu.objects.all().filter(index=random)
    print(storeid[0].selected_store)
    queryset = models.CollaborMenu.objects.all().filter(selected_store=storeid[0].selected_store)
    print(">>>>>")
    return queryset

def similar(storeid):
    print(storeid)
    queryset = models.CollaborMenu.objects.all().filter(selected_store=int(storeid)-1)
    print(">>>>>")
    return queryset


# Route, RouteDetail
class RouteCreateViewSet(viewsets.ModelViewSet):
    queryset=Route.objects.all()
    serializer_class = serializers.RouteSerializer

    def create(self, request):
        print("나의루트 만들기")
        print(request.data)
        username = request.data.get('params').get('username')
        title = request.data.get('params').get('title')
        list = request.data.get('params').get('list')
        # print(username)
        print(list)
        try:
            first_type=list[0].get('type')
            first_typeid=list[0].get('id')
            img=None # 음식점은 기본으로 없음
            if first_type=="T": # 그래서 관광지만 찾아보면 됨
                img=models.TourSpot.objects.all().filter(content_id=first_typeid)
                img=img[0].first_image
            print(img)
            route=Route.objects.create(
                route_username=username,
                route_title=title,
                route_img=img
            )
            print(Route.objects.last().route_id)
            route_id=Route.objects.last().route_id
            for rd in list:
                rdtype=rd.get('type')
                print(rdtype)
                if rdtype=="F": # 음식점일때
                    get_StoreDB(username,route_id,rd)
                elif rdtype=="T": # 관광지일때
                    TourspotDB(username,route_id,rd)
                
        except KeyError:
            return Response({"message": "INVALID_KEYS"}, status = 400)
        return Response(status = 200)

def get_StoreDB(username,route_id,rd):
    serializer_class = serializers.StoreSerializer
    
    print("음식점")
    print(rd.get('id'))
    print(route_id)
    store=models.Store.objects.all().filter(id=rd.get('id'))
    print(store[0].menu)
    routedetail=RouteDetail(rdusername=username,rid=route_id,rdtype=rd.get('type'),rdtypeid=rd.get('id'),rdtitle=rd.get('title'),rdoverview=store[0].menu,rdlat=rd.get('lat'),rdlon=rd.get('lng'))
    routedetail.save(force_insert=True)
    

def TourspotDB(username,routeid,rd):
    print("관광지")
    tourspot=models.Overview.objects.all().filter(contentid=rd.get('id'))
    tourimg=models.TourSpot.objects.all().filter(content_id=rd.get('id'))
    # print(len(tourspot))
    if len(tourspot)==0:
        routedetail=RouteDetail(rdusername=username,rid=routeid,rdtype=rd.get('type'),rdtypeid=rd.get('id'),rdimg=tourimg[0].first_image,rdtitle=rd.get('title'),rdoverview=None,rdlat=rd.get('lat'),rdlon=rd.get('lng'))
        routedetail.save(force_insert=True)
    else:
        routedetail=RouteDetail(rdusername=username,rid=routeid,rdtype=rd.get('type'),rdtypeid=rd.get('id'),rdimg=tourimg[0].first_image,rdtitle=rd.get('title'),rdoverview=tourspot[0].overview,rdlat=rd.get('lat'),rdlon=rd.get('lng'))
        routedetail.save(force_insert=True)

# http://127.0.0.1:8000/api/titlecheck/
class TitleCheckAPI(generics.GenericAPIView):
    serializer_class = RouteSerializer
    def post(self, request, *args, **kwargs):
        # print(request.data)
        routetitle = request.data["title"]
        username = request.data["username"]
        try:
            title = models.Route.objects.all().filter(route_username=username, route_title=routetitle)
        except:
            title = None
        if title:
            body = {"message": "존재하는 title 입니다."}
            return Response(body)
        else:
            body = {"message": "사용가능한 title 입니다."}
            return Response(body)
          
# route 목록 출력
# http://127.0.0.1:8000/api/routeRead
# http://127.0.0.1:8000/api/routeRead?title=()
# http://127.0.0.1:8000/api/routeRead?username=()
class RouteReadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RouteSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title", "")
        username = self.request.query_params.get("username", "")
        print(username)
        if len(username) ==0 and len(title)==0:
            queryset = (
                models.Route.objects.all().order_by("-route_id")
            )
            return queryset
        elif len(username)!=0:
            queryset = (
                models.Route.objects.all().filter(route_username=username).order_by("-route_id")
            )
            return queryset
        elif len(title)!=0:
            queryset = (
                models.Route.objects.all().filter(route_title__contains=title).order_by("-route_id")
            )
            return queryset
      
class RouteRankReadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RouteSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        title = self.request.query_params.get("title", "")
        username = self.request.query_params.get("username", "")

        if len(username)==0 and len(title)==0:
            queryset = (
                models.Route.objects.all().order_by("-route_click")
            )
            return queryset
        elif len(username)!=0:
            queryset = (
                models.Route.objects.all().filter(route_username=username).order_by("-route_click")
            )
            return queryset
        elif len(title)!=0:
            queryset = (
                models.Route.objects.all().filter(route_title__contains=title).order_by("-route_click")
            )
            return queryset
    

# route의 detail출력
# http://127.0.0.1:8000/api/routeDetailRead?routeid=(선택한 route의 PK)
class RouteDetailReadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RouteDetailSerializer

    def get_queryset(self):
        routeid = self.request.query_params.get("routeid", "")
        if len(routeid) != 0:
            queryset = (
                models.RouteDetail.objects.all().filter(rid=routeid).order_by("rdid")
            )
            return queryset
        else:
            queryset = (
                models.RouteDetail.objects.all().order_by("rdid")
            )
            return queryset

# http://127.0.0.1:8000/api/routeDetailRead?routeid=(선택한 route의 PK)
class RouteClickUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RouteSerializer

    def get_queryset(self):
        routeid = self.request.query_params.get("routeid", "")
        queryset = (
            models.Route.objects.all().filter(route_id=routeid)
        )
        print(type(queryset[0].route_click))
        plus = queryset[0].route_click + 1
        print(plus)
        models.Route.objects.all().filter(route_id=routeid).update(route_click=plus)
        
        return queryset
        # else:
        #     queryset = (
        #         models.RouteDetail.objects.all()
        #     )
        #     return queryset




class UserRecommandViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    pagination_class = SmallPagination
    # user_reviews = pd.DataFrame(list(models.Review.objects.all().values()))
    # df = user_reviews[['userid','storeid','bornyear']].head(100)
   
    def get_queryset(self):
        # user_reviews = pd.DataFrame(list(models.Review.objects.all().values()))
        # df = user_reviews[['userid','storeid','bornyear']].head(100)
        # userid = self.request.query_params.get("user", "")
        # if  userid is not None:
        user_reviews = pd.DataFrame(list(models.Review.objects.all().values()))
        df = user_reviews[['userid','storeid','bornyear']].head(1000)
       
        df_to_dict = recur_dictify(df)
        print(df_to_dict)
        name_list = [] # 사용자 목록을 담을 리스트 # 중복불가
        cos_set = set() # 맛집 목록을 담을 set # 중복 가능
       
        # user_key 는 음식점 id 가 나온다
        
        for user_key in df_to_dict:
           
            name_list.append(user_key)
                        # name_list [1070][1070, 6757][1070, 6757, 8272]
            for cos_key in df_to_dict[user_key]:
                            # cost_key = 음식점 id 가 나온다 (216, 58, 149)    
                cos_set.add(cos_key)
                            # cost_set = {216}{216, 58}
                            # for user_score in a[score]:
                            # user_gender.append[user_score]
                        
            
                # 학습할 데이터를 준비
        rating_dic = {
            'user': [],
            'store': [],
            'born_year': []
                    # 'gender': [],
                    # 'bornyear': []
        }
        cos_list = list(cos_set)
             
                # 사용자의 수 만큼 반복
        for name_key in df_to_dict :
                    # 해당 사용자가 본 맛집 수만큼 반복
            for cos_key in df_to_dict[name_key] :
                        # 사용자 인덱스 번호를 추출한다
                a1 = name_list.index(name_key) 
                        # 맛집 인덱스 번호를 추출한다.
                a2 = cos_list.index(cos_key)
                        # 나이를 가져온다.
                a3 = df_to_dict[name_key][cos_key]
                    
                    
                rating_dic['user'].append(a1)
                rating_dic['store'].append(a2)
                rating_dic['born_year'].append(a3)
                        # rating_dic['gender'].append(a4)
                        # rating_dic['bornyear'].append(a5)

                        # print((rating_dic['user']))
                        # print((rating_dic['store_name']))
                        # print(len(rating_dic['score']))
                    
        df = pd.DataFrame(rating_dic)
               
        reader = surprise.Reader(rating_scale = (1, 5))
            
        cos_list2 = ['user', 'store', 'born_year']
                
        data = surprise.Dataset.load_from_df(df[cos_list2], reader)
                
        trainset = data.build_full_trainset()
        option = {'name' : 'pearson'}
        algo = surprise.KNNBasic(sim_options=option)
        algo.fit(trainset)
                
        index = name_list.index(1070)

        print('user_index: ', index)
        print("\n")
        result = algo.get_neighbors(index, k=5)
        print("당신과 유사한 사용자? :" , result)
        print("\n")

        print("당신에게 추천할만한 맛집 :", "\n")
            
        a = []        
        for r1 in result :
                
            max_rating = data.df[data.df["user"]==r1]["born_year"].max()
            cos_id = data.df[(data.df["born_year"]==max_rating)&(data.df["user"]==r1)]["store"].values
            for cos_item in cos_id:
               
                a.append(cos_list[cos_item])
                
                # item_list = cos_list[a]
        print(a)
        queryset=models.Store.objects.all().filter(id=a[0])
        print(a[0])
        for i in a:
            select=models.Store.objects.all().filter(id=i)
            print(i)
            queryset=queryset|select
        
        print(queryset)
        return queryset
        
    
def recur_dictify(df):
    if len(df.columns) == 1:
        if df.values.size == 1: return df.values[0][0]
        return df.values.squeeze()
    grouped = df.groupby(df.columns[0])
    d = {k: recur_dictify(g.ix[:, 1:]) for k, g in grouped}

    return d     

# http://127.0.0.1:8000/api/recommendAuto?random=()&content_id=
class RecommandAutoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TourSpotSerializer
    pagination_class = SmallPagination
    # content_id
    def get_queryset(self):
        rec = self.request.query_params.get("rec", "")
        content_id = self.request.query_params.get("content_id", "")
        if len(rec) != 0:
            queryset = models.TourSpot.objects.all()
            list = []
            result = []
            
            ran = random.randint(0, 19018)

            for i in range(5):
                while ran in list:
                    ran = random.randint(0, 19018)
                list.append(ran)
            for i in range(0,5):
                result.append(queryset[list[i]])    

            queryset = result
            return queryset
        elif len(content_id) != 0:
            queryset = (
                models.TourSpot.objects.all().filter(content_id=content_id)
            )
            cat3 = queryset[0].cat3
            
            queryset = models.TourSpot.objects.all().filter(cat3=cat3)
            list = []
            result = []
            length = queryset.count()

            ran = random.randint(0, length)

            for i in range(5):
                while ran in list:
                    ran = random.randint(0, length)
                list.append(ran)
            for i in range(0,5):
                result.append(queryset[list[i]])    

            queryset = result
            return queryset
        else:
            queryset = (
                models.TourSpot.objects.all().order_by("content_id")
            )
            return queryset       