from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
import requests
import pandas as pd
import xmltodict
import json
from datetime import datetime
import requests
import folium


#공공데이터 인증키
key='NRxNDmekGlpS%2BgZup4LjaVD59FfRC9VD3nc%2Bxznuu1U1gCLnlRPjyq88E4KsvMZKRnM0bf3kXac3xzbhnrAn4A%3D%3D'


#공공데이터 url json 파일로 불러오기
url=f'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?serviceKey={NRxNDmekGlpS%2BgZup4LjaVD59FfRC9VD3nc%2Bxznuu1U1gCLnlRPjyq88E4KsvMZKRnM0bf3kXac3xzbhnrAn4A%3D%3D}&'
queryParams =urlencode({quote_plus('numOfRows') : '31', quote_plus('pageNo') : '1',quote_plus('itemCode') : 'PM10', quote_plus('dataGubun') : 'DAILY',quote_plus('searchCondition') : 'MONTH'})

#받은 데이터에서 필요한 값만 빼는 과정
url2 = url + queryParams
response = urlopen(url2) 
results = response.read().decode("utf-8")
results_to_json = xmltodict.parse(results)
data = json.loads(json.dumps(results_to_json))
rdata=data['response']['body']['items']['item']


df=pd.DataFrame(rdata)
df=df.drop(['itemCode','dataGubun'],axis=1)
df=df.set_index('dataTime')
df=df.astype(int)
region=pd.DataFrame(df.mean(axis=0),columns=['avg_pm10'])
region=region.reset_index()

#주요 17개 도시의 미세먼지 값 받기
kor=['서울특별시','부산광역시','대구광역시','인천광역시','광주광역시','대전광역시','울산광역시','경기도','강원도','충청북도','충청남도','전라북도','전라남도','경상북도','경상남도','제주특별자치도','세종특별자치시']
region['name']=kor
region.drop(['index'],axis=1,inplace=True)

region['avg_pm10']=region['avg_pm10'].astype(int)

#한국 사진 json 파일로 불러오기
geo_json='https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_provinces_geo_simple.json'

m=folium.Map(
    location=[36.97884521132491, 127.86224884213675],
    tiles='Stamen Terrain'
)

#측정된 미세먼지 값에 따라서 시각화 하는 과정
folium.Choropleth(
    geo_data=geo_json,
    name='choropleth',
    data=region,
    columns=['name','avg_pm10'],
    key_on='feature.properties.name',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)
