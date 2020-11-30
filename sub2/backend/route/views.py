from django.shortcuts import render
from .serializers import TempSerializer
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics, status
from rest_framework.pagination import PageNumberPagination
from .models import Temp
from route import models, serializers

# 1. temp 해당 user임시저장 삭제 .delete(http://127.0.0.1:8000/route/tempCreate?username=())
# 2. 임시저장 버튼을 누르면 temp 생성 list로 받아옴 .create(http://127.0.0.1:8000/route/tempCreate)
# 3. 다시 로그아웃 하고 들어오면 temp에 저장된 것들 가져오기 .get(http://127.0.0.1:8000/route/tempRead?username=())
#
# 4. 루트 생성 버튼을 누르면 route먼저 생성 .create(http://127.0.0.1:8000/route/route)
# 5. 그와 동시에 루트디테일 생성 list로 받아옴 .create(http://127.0.0.1:8000/route/routeDetail)
#  [username, route_id(루트의PK), type, typeid, img, title, lat, lon]
#
# 6. 인기루트 목록으로 보여주기 .get(http://127.0.0.1:8000/route/route)
# 7. 거기서 자세히 보기 위해 선택을 하면 .get(http://127.0.0.1:8000/route/routeDetail)
#
# 8. 마이페이지에서 내가 만든 루트만 볼 수 있게 .get(http://127.0.0.1:8000/route/route?username=())
# 9. 루트 삭제하기 .delete(http://127.0.0.1:8000/route/route)
# 10. 동시에 루트 디테이 테이블도 삭제 .delete(http://127.0.0.1:8000/route/routeDetail?route_id=(route의PK))
# 
# 생성 : 루트 -> 루트디테일
# 삭제 : 루트디테일 -> 루트



class SmallPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 50

# Temp
# http://localhost:8000/route/tempDelete?username=()
class TempDelectViewSet(viewsets.ModelViewSet):
    queryset=Temp.objects.all()
    serializer_class = serializers.TempSerializer
    pagination_class = SmallPagination

    def delete(self, request, *args, **kwargs):
        username = self.request.query_params.get("username", "")
        instance = Temp.objects.filter(temp_username=username)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TempCreateViewSet(viewsets.ModelViewSet):
    queryset=Temp.objects.all()
    serializer_class = serializers.TempSerializer
    pagination_class = SmallPagination

    def create(self, request):
        print("22222222222")
        print(request.data.get('params').get('username'))
        username = request.data.get('params').get('username')
        word = request.data.get('params').get('word')
        print(username)
        print(word)

        for tl in word:
            # serializer=self.get_serializer(data=tl)
            print(username)
            print(tl)
            print(tl.get('id'))
            print(tl.get('title'))
            print(tl.get('lat'))
            print(tl.get('lng'))
            print(tl.get('type'))

            temp=Temp(temp_username=username,temp_type=tl.get('type'),temp_typeid=tl.get('id'),temp_title=tl.get('title'),temp_lat=tl.get('lat'),temp_lon=tl.get('lng'))
            temp.save(force_insert=True)
        return Response(
            {
                "temp": TempSerializer(
                    temp, context=self.get_serializer_context()
                ).data
            }
        )

class TempReadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TempSerializer
    pagination_class = SmallPagination

    # R : 임시저장은 본인 것만 불러들여야 함
    def get_queryset(self):
        username = self.request.query_params.get("username", "")
        if username is not None:
            print(username)
            queryset = (
                models.Temp.objects.all().filter(temp_username=username).order_by('temp_id')
            )
            print(queryset)
            return queryset


