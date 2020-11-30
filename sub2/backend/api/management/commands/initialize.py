from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from backend import settings
from api import models


class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent.parent / "data"
    DATA_FILE = str(DATA_DIR / "dump.pkl")

    def _load_dataframes(self):
        try:
            data = pd.read_pickle(Command.DATA_FILE)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data

    def _initialize(self):
        """
        Sub PJT 1에서 만든 Dataframe을 이용하여 DB를 초기화합니다.
        """
        print("[*] Loading data...")
        dataframes = self._load_dataframes()

        print("[*] Initializing stores...")
        models.Store.objects.all().delete()
        stores = dataframes["stores"]
        stores_bulk = [
            models.Store(
                id=store.id,
                store_name=store.store_name,
                branch=store.branch,
                area=store.area,
                tel=store.tel,
                address=store.address,
                latitude=store.latitude,
                longitude=store.longitude,
                category=store.category,
                menu=store.menu,
                bhour=store.bhour,
            )
            for store in stores.itertuples()
        ]
        models.Store.objects.bulk_create(stores_bulk)


        print("[*] Initializing reviews...")
        models.Review.objects.all().delete()
        reviews = dataframes["reviews"]
        reviews_bulk = [
            models.Review(
                storeid = review.store,
                userid = review.user,
                score = review.score,
                content = review.content,
                regtime = review.reg_time,
                gender = review.gender,
                bornyear = review.born_year,
            )
            for review in reviews.itertuples()
        ]
        models.Review.objects.bulk_create(reviews_bulk)

        print("[*] Initializing tourspot...")
        models.TourSpot.objects.all().delete()
        print(dataframes)
        tourspots = dataframes["tourspot"]
        tourspots_bulk = [
            models.TourSpot(
                addr1 =  tourspot.addr1,
                addr2 = tourspot.addr2,
                areacode = tourspot.areacode,
                cat1 = tourspot.cat1,
                cat2 = tourspot.cat2,
                cat3 = tourspot.cat3,
                content_id = tourspot.content_id,
                content_type_id = tourspot.content_type_id,
                first_image = tourspot.first_image,
                first_image2 = tourspot.first_image2,
                mapx = tourspot.mapx,
                mapy = tourspot.mapy,
                sigungucode = tourspot.sigungucode,
                tel = tourspot.tel,
                title = tourspot.title,
                readcount= tourspot.readcount,
            )
            for tourspot in tourspots.itertuples()
        ]
        models.TourSpot.objects.bulk_create(tourspots_bulk)
        print("[+] Done")
        
        print("[*] Initializing Course...")
        models.Course.objects.all().delete()
        print(dataframes)
        course = dataframes["course"]
        course_bulk = [
            models.Course(
                addr1 =  course.addr1,
                addr2 = course.addr2,
                areacode = course.areacode,
                cat1 = course.cat1,
                cat2 = course.cat2,
                cat3 = course.cat3,
                content_id = course.content_id,
                content_type_id = course.content_type_id,
                first_image = course.first_image,
                first_image2 = course.first_image2,
                mapx = course.mapx,
                mapy = course.mapy,
                sigungucode = course.sigungucode,
                tel = course.tel,
                title = course.title,
                readcount= course.readcount,
            )
            for course in course.itertuples()
        ]
        models.Course.objects.bulk_create(course_bulk)
        print("[+] Done")

        print("[*] Initializing Recommand...")
        models.Recommand.objects.all().delete()
        print(dataframes)
        recommandspots = dataframes["recommandspot"]
        recommandspot_bulk = [
            models.Recommand(
                contentid = recommandspots.contentid,
                contenttypeid = recommandspots.contenttypeid,
                subcontentid = recommandspots.subcontentid,
                subdetailalt = recommandspots.subdetailalt,
                subdetailimg = recommandspots.subdetailimg,
                subdetailoverview = recommandspots.subdetailoverview,
                subname = recommandspots.subname,
                subnum = recommandspots.subnum,
    
            )
            for recommandspots in recommandspots.itertuples()
        ]
        models.Recommand.objects.bulk_create(recommandspot_bulk)
        print("[+] Done")


        print("[*] Initializing Overview...")
        models.Overview.objects.all().delete()
        print(dataframes)
        overviews = dataframes["overviews"]
        overviews_bulk = [
            models.Overview(           
                contentid = overviews.contentid,
                contenttypeid = overviews.contenttypeid,         
                homepage = overviews.homepage,            
                overview = overviews.overview,
                tel = overviews.tel,
                title = overviews.title,
            )
           for overviews in overviews.itertuples()
        ]
        models.Overview.objects.bulk_create(overviews_bulk)
        print("[+] Done")

    def handle(self, *args, **kwargs):
        self._initialize()
