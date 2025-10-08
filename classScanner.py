import requests
from mySession import mySession

session_id = mySession
session = requests.Session()
session.cookies.set("session", session_id)

session.get()