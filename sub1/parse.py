# -*- coding: utf-8 -*-
import json
import pandas as pd
import os
import shutil

DATA_DIR = "../data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")
DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")
DATA_FILE2 = os.path.join(DATA_DIR, "tour.json")
DUMP_FILE2 = os.path.join(DATA_DIR, "spotdump.pkl")
DATA_FILE3 = os.path.join(DATA_DIR, "recommand.json")
DUMP_FILE3 = os.path.join(DATA_DIR, "redump.pkl")
DATA_FILE4 = os.path.join(DATA_DIR, "overview.json")
DUMP_FILE4 = os.path.join(DATA_DIR, "overdump.pkl")
DATA_FILE5 = os.path.join(DATA_DIR, "newtour.json")
DUMP_FILE5 = os.path.join(DATA_DIR, "newtour.pkl")


store_columns = (
    "id",  # 음식점 고유번호
    "store_name",  # 음식점 이름
    "branch",  # 음식점 지점 여부
    "area",  # 음식점 위치
    "tel",  # 음식점 번호
    "address",  # 음식점 주소
    "latitude",  # 음식점 위도
    "longitude",  # 음식점 경도
    "category",  # 음식점 카테고리
    "menu",
    "bhour"
)


review_columns = (
    "id",  # 리뷰 고유번호
    "store",  # 음식점 고유번호
    "user",  # 유저 고유번호
    "score",  # 평점
    "content",  # 리뷰 내용
    "reg_time",  # 리뷰 등록 시간
    "gender",
    "born_year",
)

tourspot_columns =(
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
)

newtourspot_columns =(
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
)


recommand_columns = (
    "contentid",
	"contenttypeid",
	"subcontentid",
	"subdetailalt",
	"subdetailimg",
	"subdetailoverview",
	"subname",
	"subnum",
)

overview_columns = (
    "booktour",
	"contentid",
	"contenttypeid",
    "createdtime",
	"homepage",	
    "modifiedtime",
	"overview",
    "tel",
	"title",
)

class AreaCodes:
    SEOUL = 1
    INCHEON = 2
    DAEJEON = 3
    DAEGU = 4
    GWANGJU = 5
    BUSAN = 6
    ULSAN = 7
    SEJONG = 8
    GYEONGGI = 31
    KANGWON = 32
    CHUNGBUK = 33
    CHUNGNAM = 34
    GYUNGBUK = 35
    GYUNGNAM = 36
    JEONBUK = 37
    JEONNAM = 38
    JEJU = 39

def import_data(data_path=DATA_FILE, data_path2=DATA_FILE2, data_path3=DATA_FILE3, data_path4 = DATA_FILE4, data_path5 = DATA_FILE5):
    """
    Req. 1-1-1 음식점 데이터 파일을 읽어서 Pandas DataFrame 형태로 저장합니다
    """

    try:
        with open(data_path, encoding="utf-8-sig") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path}` 가 존재하지 않습니다.")
        exit(1)

    stores = []  # 음식점 테이블
    reviews = []  # 리뷰 테이블

    for d in data:

        categories = [c["category"] for c in d["category_list"]]
        menus = [m["menu"]+":"+str(m["price"]) for m in d["menu_list"]]
        bhour_list = []

        for b in d["bhour_list"]:
            bhour_list.append(
                "(" + str(b["type"]) + "," + str(b["week_type"]) + "," + str(b["mon"]) + "," + str(b["tue"]) + "," + str(b["wed"]) + "," + str(b["thu"]) + "," + str(b["fri"]) + "," + str(b["sat"]) + "," + str(b["sun"]) + "," + str(b["start_time"]) + "," + str(b["end_time"]) + "," + str(b["etc"]) + ")"
            )

        stores.append(
            [
                d["id"],
                d["name"],
                d["branch"],
                d["area"],
                d["tel"],
                d["address"],
                d["latitude"],
                d["longitude"],
                "|".join(categories),
                "|".join(menus),
                "|".join(bhour_list),
            ]
        )

        for review in d["review_list"]:
            r = review["review_info"]
            u = review["writer_info"]

            reviews.append(
                [r["id"], d["id"], u["id"], r["score"], r["content"], r["reg_time"],u["gender"],u["born_year"]]
            )

    try:
        with open(data_path2, encoding="utf-8-sig") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path2}` 가 존재하지 않습니다.")
        exit(1)

    tourspot = []  # 관광지 데이터
    for d in data:

        if d["areacode"]==1:
            d["areacode"]="서울"
        elif d["areacode"]==2:
            d["areacode"]="인천"
        elif d["areacode"]==3:
            d["areacode"]="대전"
        elif d["areacode"]==4:
            d["areacode"]="대구"
        elif d["areacode"]==5:
            d["areacode"]="광주"
        elif d["areacode"]==6:
            d["areacode"]="부산"
        elif d["areacode"]==7:
            d["areacode"]="울산"
        elif d["areacode"]==8:
            d["areacode"]="세종"
        elif d["areacode"]==31:
            d["areacode"]="경기"
        elif d["areacode"]==32:
            d["areacode"]="강원"
        elif d["areacode"]==33:
            d["areacode"]="충북"
        elif d["areacode"]==34:
            d["areacode"]="충남"
        elif d["areacode"]==35:
            d["areacode"]="경북"
        elif d["areacode"]==36:
            d["areacode"]="경남"
        elif d["areacode"]==37:
            d["areacode"]="전북"
        elif d["areacode"]==38:
            d["areacode"]="전남"
        elif d["areacode"]==39:
            d["areacode"]="제주"
            
        tourspot.append(
            [
                d["addr1"] if "addr1" in d else "",
                d["addr2"] if "addr2" in d else "",
                d["areacode"],
                d["cat1"] if "cat1" in d else "",
                d["cat2"] if "cat2" in d else "",
                d["cat3"] if "cat3" in d else "",
                d["contentid"],
                d["contenttypeid"],
                d["firstimage"] if "firstimage" in d else "",
                d["firstimage2"] if "firstimage2" in d else "",
                d["mapx"] if "mapx" in d else 0.0,
                d["mapy"] if "mapy" in d else 0.0,
                d["sigungucode"] if "sigungucode" in d else 0,
                d["tel"] if "tel" in d else "",
                d["title"] if "title" in d else "",
                d["readcount"] if "readcount" in d else 0,
            ]
        )

    try:
        with open(data_path3, encoding='utf-8-sig') as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path3}` 가 존재하지 않습니다.")
        exit(1)

    recommandspot = []  # 추천코스 데이터
    for d in data:
        recommandspot.append(
            [
                d["contentid"],
                d["contenttypeid"],
                d["subcontentid"],
                d["subdetailalt"] if "subdetailalt" in d else "",
                d["subdetailimg"] if "subdetailimg" in d else "",
                d["subdetailoverview"] if "subdetailoverview" in d else "",
                d["subname"] if "subname" in d else "",
                d["subnum"],             
            ]
        )

    try:
        with open(data_path4, encoding='utf-8-sig') as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path4}` 가 존재하지 않습니다.")
        exit(1)

    overviews = []
    for d in data:
        overviews.append(
            [
               d["booktour"] if "booktour" in d else 0,
               d["contentid"] if "contentid" in d else "",
               d["contenttypeid"] if "contenttypeid" in d else "",
               d["createdtime"],
               d["homepage"] if "homepage" in d else "",
               d["modifiedtime"],
               d["overview"],
               d["tel"] if "tel" in d else "",
               d["title"] if "title" in d else "",
            ]
        )

    try:
        with open(data_path5, encoding="utf-8-sig") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path5}` 가 존재하지 않습니다.")
        exit(1)

    newtourspot = []  # 관광지 데이터
    for d in data:

        if d["areacode"]==1:
            d["areacode"]="서울"
        elif d["areacode"]==2:
            d["areacode"]="인천"
        elif d["areacode"]==3:
            d["areacode"]="대전"
        elif d["areacode"]==4:
            d["areacode"]="대구"
        elif d["areacode"]==5:
            d["areacode"]="광주"
        elif d["areacode"]==6:
            d["areacode"]="부산"
        elif d["areacode"]==7:
            d["areacode"]="울산"
        elif d["areacode"]==8:
            d["areacode"]="세종"
        elif d["areacode"]==31:
            d["areacode"]="경기"
        elif d["areacode"]==32:
            d["areacode"]="강원"
        elif d["areacode"]==33:
            d["areacode"]="충북"
        elif d["areacode"]==34:
            d["areacode"]="충남"
        elif d["areacode"]==35:
            d["areacode"]="경북"
        elif d["areacode"]==36:
            d["areacode"]="경남"
        elif d["areacode"]==37:
            d["areacode"]="전북"
        elif d["areacode"]==38:
            d["areacode"]="전남"
        elif d["areacode"]==39:
            d["areacode"]="제주"
            
        newtourspot.append(
            [
                d["addr1"] if "addr1" in d else "",
                d["addr2"] if "addr2" in d else "",
                d["areacode"],
                d["cat1"] if "cat1" in d else "",
                d["cat2"] if "cat2" in d else "",
                d["cat3"] if "cat3" in d else "",
                d["contentid"],
                d["contenttypeid"],
                d["firstimage"] if "firstimage" in d else "",
                d["firstimage2"] if "firstimage2" in d else "",
                d["mapx"] if "mapx" in d else 0.0,
                d["mapy"] if "mapy" in d else 0.0,
                d["sigungucode"] if "sigungucode" in d else 0,
                d["tel"] if "tel" in d else "",
                d["title"] if "title" in d else "",
                d["readcount"] if "readcount" in d else 0,
            ]
        )



    store_frame = pd.DataFrame(data=stores, columns=store_columns)
    review_frame = pd.DataFrame(data=reviews, columns=review_columns)
    tourspot_frame = pd.DataFrame(data=tourspot, columns=tourspot_columns)
    new_tourspot_frame = pd.DataFrame(data=newtourspot, columns=newtourspot_columns)
    recommand_frame = pd.DataFrame(data=recommandspot, columns=recommand_columns)
    is_course = tourspot_frame['content_type_id'] == 25
    course_frame = tourspot_frame[is_course]
    print(course_frame)
    overview_frame = pd.DataFrame(data=overviews, columns=overview_columns)
    return {"stores": store_frame, "reviews": review_frame, "tourspot": new_tourspot_frame, "course": course_frame, "recommandspot": recommand_frame, "overviews": overview_frame}

def dump_dataframes(dataframes):
    pd.to_pickle(dataframes, DUMP_FILE)


def load_dataframes():
    return pd.read_pickle(DUMP_FILE)


def main():

    print("[*] Parsing data...")
    data = import_data()
    print("[+] Done")

    print("[*] Dumping data...")
    dump_dataframes(data)
    print("[+] Done\n")

    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    print("[음식점]")
    print(f"{separater}\n")
    print(data["stores"].head())
    print(f"\n{separater}\n\n")

    print("[리뷰]")
    print(f"{separater}\n")
    print(data["reviews"].head())
    print(f"\n{separater}\n\n")

    print("[관광지]")
    print(f"{separater}\n")
    print(data["tourspot"].head())
    print(f"\n{separater}\n\n")

    print("[추천코스]")
    print(f"{separater}\n")
    print(data["recommandspot"].head())
    print(f"\n{separater}\n\n")

    print("[관광개요]")
    print(f"{separater}\n")
    print(data["overviews"].head())
    print(f"\n{separater}\n\n")

if __name__ == "__main__":
    main()
