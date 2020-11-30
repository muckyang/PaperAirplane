from django.shortcuts import render
from rest_framework import viewsets
from custom import models, serializers
from .models import Custom
from .serializers import CustomSerializer
from rest_framework.response import Response

class CustomViewSet(viewsets.ModelViewSet):
    queryset = Custom.objects.all()
    serializer_class = CustomSerializer
    def get_queryset(self):
        # 장바구니 담은거
        customuserid = self.request.query_params.get("customuserid", "")
        customorderid = self.request.query_params.get("customorderid", "")
        isRoute = self.request.query_params.get("isRoute", "")
        #len(customorderid)==0 is None 이 안 먹어서 이렇게 함 / 이렇게하면 파라메타 값 주소에 안들어가도 괜찮
        if customuserid is not None and len(customorderid)==0 and isRoute=="False":
            print("1111111")
            queryset = (
                models.Custom.objects.all().filter(userid = int(customuserid))
            )
            return queryset
        
        # 나만의 루트
        elif customuserid is not None and customorderid is not None and isRoute=="True":
            print("2222222")
            queryset = (
                models.Custom.objects.all().filter(userid = int(customuserid), orderid = int(customorderid))
            )
            return queryset
        else:
            queryset = (
                models.Custom.objects.all()
            )
            return queryset