import requests
import time
import urllib3
from alive_progress import alive_bar
import mySession

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session_id = mySession.mySession #我把我的session藏在mySession，自己要用的話把import拿掉直接用字串輸入你的session!!!!
session = requests.Session()
session.cookies.set("session", session_id)
jumpScale = 120

def sendPost(url,start, end):
    payload = {"start": start, "end": end}
    response = session.post(url, json=payload, verify=False)  # ← 改這裡！
    # print(response.status_code)
    # print(response.text)

def getVideoTime(id):
    classCode = id
    aurl = f"https://eclass.yuntech.edu.tw/api/activities/{classCode}?sub_course_id=0"
    response = session.get(aurl,verify=False)  # ← 改這裡！
    data = response.json()

    # 取得第一個 upload 中第一個影片的 duration
    duration = data["uploads"][0]["videos"][0]["duration"]
    return int(duration)

def API_Skip(classCode):
    url = f"https://eclass.yuntech.edu.tw/api/course/activities-read/{classCode}"
    targetTime = getVideoTime(classCode)
    current = 0
    while current < targetTime:
        time.sleep(0.2)
        if current + jumpScale >= targetTime:
            sendPost(url, current, targetTime)
            yield targetTime - current  # 回傳「增加了多少」
            current = targetTime
        else:
            sendPost(url, current, current + jumpScale)
            yield jumpScale  # 每次 yield「增加 jumpScale」
            current += jumpScale


if __name__ == "__main__":
    classCode = input("輸入課程碼:")
    url = f"https://eclass.yuntech.edu.tw/api/course/activities-read/{classCode}"

    targetTime = getVideoTime(classCode)
    print(targetTime)
    with alive_bar(targetTime,title="爆破小隊爆破中") as bar:
        while current < targetTime:
            time.sleep(0.2)
            if current + jumpScale >= targetTime:
                sendPost(current, targetTime)
                bar(targetTime - current+1)
                current = targetTime
            else:
                sendPost(current, current + jumpScale)
                bar(jumpScale)
                current += jumpScale
    #     print(f"已送出範圍：{current}")
