from django.shortcuts import render
from .serializers import CommentSerializer, CommentUpdateSerializer, CommentDeleteSerializer
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics, status
from comment import models
from .models import Comment
# Create your views here.
class CreateAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    
    def post(self, request, *args, **kwargs):
        # if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
        #     body = {"message": "short field"}
        #     return Response(body, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        return Response(
            {
                "comment": CommentSerializer(
                    comment, context=self.get_serializer_context()
                ).data
            }
        )

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_queryset(self):
        userid = self.request.query_params.get("userid", "")
        storeid = self.request.query_params.get("storeid", "")
        tourspotid = self.request.query_params.get("tourspotid", "")
        print(userid + " " + storeid + " " + tourspotid)
        # 상점 댓글 불러오기
        if userid is not None and storeid is not None and len(tourspotid)==0:
            print("1111111")
            queryset = (
                models.Comment.objects.all().filter(userid = int(userid), storeid = int(storeid))
            )
            return queryset
        
        # 관광지 댓글 불러오기
        elif userid is not None and tourspotid is not None and len(storeid)==0:
            print("2222222")
            queryset = (
                models.Comment.objects.all().filter(userid = int(userid), tourspotid = int(tourspotid))
            )
            return queryset
        else:
            queryset = (
                models.Comment.objects.all()
            )
            return queryset

class CommentUpdateAPI(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentUpdateSerializer

    def get_object(self):
        return self.request.user

class CommentDeleteAPI(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteSerializer