import requests
import urllib3
from alive_progress import alive_bar
import TronClassSkiper
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()

#############################

session_id = "" #用字串輸入你的session!!!!

#############################
session.cookies.set("session", session_id)

classCode = input("輸入課程代碼: ")

url = f"https://eclass.yuntech.edu.tw/api/courses/{classCode}/activities?sub_course_id=0"

response = session.get(url, verify=False)
data = response.json()

# 取出 activities 陣列
activities = data.get("activities", [])

# 找出 completion_criterion_key == "none" 的 id
target_ids = [
    a["id"]
    for a in activities
    if a.get("type") == "online_video"
]
length = 0
for id in target_ids:
    length +=TronClassSkiper.getVideoTime(id)

with alive_bar(length,title="爆破大隊爆破中") as bar:
    for id in target_ids:
        for progress in TronClassSkiper.API_Skip(id):
            bar(progress)