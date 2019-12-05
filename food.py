import requests
from bs4 import BeautifulSoup




cok = {}
re = requests.get('https://food.razi.ac.ir',allow_redirects = False)
openid_cookie = (dict(re.cookies))
cok.update(openid_cookie)
re2 = requests.get(re.headers['location'],cookies=openid_cookie,allow_redirects = False)
SignInMessage_cookie =(dict(re2.cookies))
get_link = re2.headers['location']
cok.update(SignInMessage_cookie)
#get idsrv.xsrf
xsrf = requests.get(get_link,cookies=cok)
cok.update(xsrf.cookies)
textparse = xsrf.text
soup = BeautifulSoup(textparse,'html.parser')
scripts = soup.find_all('script')
xsrfcode = scripts[0].text[189:280]
#response COOKIES idsrv.session / idsrv
re4 = requests.post(get_link,cookies = cok,data={'username':'شماره دانشجویی','password':'رمزعبور','idsrv.xsrf':xsrfcode},allow_redirects = False)
re5_cookies = {'idsrv.xsrf':xsrfcode}
re5_cookies.update(dict(re4.cookies))
re5_cookies.update((openid_cookie))
#request cookies idsrv/idsrv.xsrf(NEED TO CHANGE!)/idsrv.session/openid
re5 = requests.get(re4.headers['location'],cookies = re5_cookies)
textparse2 = re5.text
soup = BeautifulSoup(textparse2,'html.parser')
#Parsing values from inputs //Request Requierments /*access_token/*id_token/*token_type/*expires_in/*scope/*state/*session_state
#Cookies Openid
access_token = soup.find('input',{'name':'access_token'})['value']
id_token = soup.find('input',{'name':'id_token'})['value']
token_type = soup.find('input',{'name':'token_type'})['value']
expires_in = soup.find('input',{'name':'expires_in'})['value']
scope = soup.find('input',{'name':'scope'})['value']
state = soup.find('input',{'name':'state'})['value']
session_state =soup.find('input',{'name':'session_state'})['value']
datas = {'access_token':access_token,'id_token':id_token,'token_type':token_type,'expires_in':expires_in,'scope':scope,'state':state,'session_state':session_state}
re6 = requests.post('https://food.razi.ac.ir/',data=datas,cookies = openid_cookie,allow_redirects = False)
#Finally We've got JahanGOstarSetare COOKIE
get_food_json = requests.get('https://food.razi.ac.ir/api/v0/Reservation?lastdate=&navigation=0',cookies = re6.cookies)
print(get_food_json.text)
for day in range(0,7):
    try:
        nahar1 = get_food_json.json()[day]['Meals'][1]['FoodMenu'][0]['FoodName']
        nahar2 = get_food_json.json()[day]['Meals'][1]['FoodMenu'][1]['FoodName']
        Daydate = get_food_json.json()[day]['DayDate']
        Day_title = get_food_json.json()[day]['DayTitle']
        sham1 = get_food_json.json()[day]['Meals'][2]['FoodMenu'][0]['FoodName']
        sham2 = get_food_json.json()[day]['Meals'][2]['FoodMenu'][1]['FoodName']
        print(Day_title,':',Daydate,'\n','Nahar1 :',nahar1,'\n','Nahar2 :',nahar2,'\n','Sham1 :',sham1,'\n','Sham2 :',sham2,'\n\n')
    except:
        print()



