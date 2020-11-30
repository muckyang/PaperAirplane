from rest_framework import serializers
from .models import Temp

class TempSerializer(serializers.ModelSerializer):
    # def __init__(self,temp_id,temp_username,temp_type,temp_typeid,temp_title,temp_lat,temp_lon):
    #     self.temp_id=temp_id
    #     self.temp_username=temp_username
    #     self.temp_type=temp_type
    #     self.temp_typeid=temp_typeid
    #     self.temp_title=temp_title
    #     self.temp_lat=temp_lat
    #     self.temp_lon=temp_lon

    class Meta:
        model = Temp
        fields =['temp_id','temp_username','temp_type','temp_typeid','temp_title','temp_lat','temp_lon']
    
