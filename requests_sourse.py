# this file save the Curl requests
get_token = """
curl --request POST \
  --url https://epidemicapi.ncut.edu.tw/api/login \
  --header 'content-type: application/json;charset=UTF-8' \
  --header 'origin: https://epidemic.ncut.edu.tw' \
  --header 'referer: https://epidemic.ncut.edu.tw/login' \
  --data '{
	"userId": "3A123456",
	"password": "abc123",
	"remember": false
}'
"""

get_departments = """
curl --request GET \
  --url https://epidemicapi.ncut.edu.tw/api/departments \
  --header 'authorization: Bearer <token>' \
  --header 'origin: https://epidemic.ncut.edu.tw' \
  --header 'referer: https://epidemic.ncut.edu.tw/bodyTemp'
"""

get_config = """
curl --request GET \
  --url https://epidemicapi.ncut.edu.tw/api/config \
  --header 'authorization: Bearer <token>' \
  --header 'origin: https://epidemic.ncut.edu.tw' \
  --header 'referer: https://epidemic.ncut.edu.tw/bodyTemp'
"""

get_activityData = """
curl --request GET \
  --url https://epidemicapi.ncut.edu.tw/api/activityData \
  --header 'authorization: Bearer <token>' \
  --header 'origin: https://epidemic.ncut.edu.tw' \
  --header 'referer: https://epidemic.ncut.edu.tw/bodyTemp'
"""

get_temperatureSurveys = """
curl --request GET \
  --url https://epidemicapi.ncut.edu.tw/api/temperatureSurveys/3A513103-2020-03-01 \
  --header 'authorization: Bearer <token>' \
  --header 'origin: https://epidemic.ncut.edu.tw' \
  --header 'referer: https://epidemic.ncut.edu.tw/bodyTemp'
"""

post_data = """
curl --request POST \
  --url https://epidemicapi.ncut.edu.tw/api/temperatureSurveys \
  --header 'authorization: Bearer <token>' \
  --header 'content-type: application/json;charset=UTF-8' \
  --header 'origin: https://epidemic.ncut.edu.tw' \
  --header 'referer: https://epidemic.ncut.edu.tw/bodyTemp' \
  --data '{
	"id": "3A123456-undefined",
	"saveDate": "2020-03-01",
	"morningTemp": 34,
	"noonTemp": 37.5,
	"nightTemp": 34,
	"isValid": false,
	"morningManner": 0,
	"noonManner": 0,
	"nightManner": 0,
	"isMorningFever": null,
	"isNoonFever": false,
	"isNightFever": null,
	"morningActivity": "工作(At work)",
	"noonActivity": "工作(At work)",
	"nightActivity": "家中(Home)",
	"measureTime": "01:11",
	"userId": "3A123456",
	"departmentId": "14",
	"className": "四X四X",
	"departmentName": "OO系",
	"type": "1"
}'
"""
