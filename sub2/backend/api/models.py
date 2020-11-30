from django.utils import timezone
from django.db import models


class Store(models.Model):
    id = models.IntegerField(primary_key=True)
    store_name = models.CharField(max_length=50)
    branch = models.CharField(max_length=20, null=True)
    area = models.CharField(max_length=50, null=True)
    tel = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(max_length=10, null=True)
    longitude = models.FloatField(max_length=10, null=True)
    category = models.CharField(max_length=200, null=True)
    menu = models.CharField(max_length=200, null=True)
    bhour = models.CharField(max_length=200, null=True)

    @property
    def category_list(self):
        return self.category.split("|") if self.category else []
        
    @property
    def menu_list(self):
        return self.menu.split("|") if self.menu else []
    
    @property
    def bhour_list(self):
        return self.bhour.split("|") if self.bhour else []

class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    storeid = models.IntegerField(null=True)
    userid = models.IntegerField(null=True)
    score = models.FloatField(max_length=40, null=True)
    content = models.CharField(max_length=1000, null=True)
    regtime = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10, null=True)
    bornyear = models.CharField(max_length=10, null=True)


class TourSpot(models.Model):
    addr1 = models.CharField(max_length=200, null=True)
    addr2 = models.CharField(max_length=200, null=True)
    areacode = models.CharField(max_length=200, null=True)
    cat1 = models.CharField(max_length=3, null=True)
    cat2 = models.CharField(max_length=5, null=True)
    cat3 = models.CharField(max_length=10, null=True)
    content_id = models.IntegerField(null=True)
    content_type_id = models.IntegerField(null=True)
    first_image = models.CharField(max_length=200, null=True)
    first_image2 = models.CharField(max_length=200, null=True)
    mapx = models.FloatField(null = True)
    mapy = models.FloatField(null = True)
    sigungucode = models.IntegerField(null=True)
    tel = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    readcount = models.IntegerField(null=True)

class Course(models.Model):
    addr1 = models.CharField(max_length=200, null=True)
    addr2 = models.CharField(max_length=200, null=True)
    areacode = models.CharField(max_length=200, null=True)
    cat1 = models.CharField(max_length=3, null=True)
    cat2 = models.CharField(max_length=5, null=True)
    cat3 = models.CharField(max_length=10, null=True)
    content_id = models.IntegerField(null=True)
    content_type_id = models.IntegerField(null=True)
    first_image = models.CharField(max_length=200, null=True)
    first_image2 = models.CharField(max_length=200, null=True)
    mapx = models.FloatField(null = True)
    mapy = models.FloatField(null = True)
    sigungucode = models.IntegerField(null=True)
    tel = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    readcount = models.IntegerField(null=True)

class Recommand(models.Model):
    contentid = models.IntegerField(null=True)
    contenttypeid = models.IntegerField(null=True)
    subcontentid = models.IntegerField(null=True)
    subdetailalt = models.CharField(max_length=1000, null=True)
    subdetailimg = models.CharField(max_length=200, null=True)
    subdetailoverview = models.CharField(max_length=1000, null=True)
    subname = models.CharField(max_length=200, null=True)
    subnum = models.IntegerField(null=True)

class Overview(models.Model):
    contentid = models.IntegerField(null=True)
    contenttypeid = models.IntegerField(null=True)
    homepage = models.CharField(max_length=1000, null=True)
    overview = models.CharField(max_length=3000, null=True)
    tel = models.CharField(max_length=500, null=True)
    title = models.CharField(max_length=500, null=True)

class CollaborMenu(models.Model):
    index = models.IntegerField(null=True)
    selected_store = models.FloatField(null=True)
    recommended_store = models.FloatField(null=True)
    similarity = models.FloatField(null = True)

class Route(models.Model):
    route_id=models.IntegerField(primary_key=True,auto_created=True)
    route_username=models.CharField(max_length=50, null=True)
    route_title=models.CharField(max_length=200, null=True)
    route_img=models.CharField(max_length=200, null=True) #detail중 대표사진으로
    route_tag=models.CharField(max_length=200, null=True)
    route_click= models.IntegerField(default=0,null=True) 

class RouteDetail(models.Model):
    rdid=models.IntegerField(primary_key=True,auto_created=True)
    rdusername=models.CharField(max_length=50, null=True)
    rid=models.IntegerField(null=True)
    # rid=models.ForeignKey(Route, on_delete=models.CASCADE, db_column="rid") #Route의 외래키
    rdtype=models.CharField(max_length=50, null=True) #맛집=F, 관광지=T
    rdtypeid=models.IntegerField(null=True)
    rdimg=models.CharField(max_length=200, null=True)
    rdtitle=models.CharField(max_length=200, null=True)
    rdoverview=models.CharField(max_length=500, null=True) #맛집은 메뉴, 관광지는 overview
    rdlat=models.FloatField(max_length=10, null=True)
    rdlon=models.FloatField(max_length=10, null=True)