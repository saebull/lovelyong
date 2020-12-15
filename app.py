import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask import Flask, render_template, redirect, request, url_for
import requests
from bs4 import BeautifulSoup
import re
import heapq

cred = credentials.Certificate('ongkey.json')
defaul_app = firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://ie-project-292614.firebaseio.com/'
})
keyname = ['강남대로1',
'강남대로2',
'강남대로3',
'강남대로4',
'강남대로5',
'강남대로6',
'강남대로7',
'강남대로8',
'강남대로8_9',
'강남대로9',
'강남대로91길1',
'강남대로91길2',
'강남대로93길1',
'강남대로93길2',
'강남대로93길3',
'강남대로93길3_4',
'강남대로93길4',
'강남대로93길4_5',
'강남대로93길5',
'강남대로95길1',
'강남대로95길1_2_1',
'강남대로95길1_2_2',
'강남대로95길2',
'강남대로95길3',
'강남대로95길4',
'강남대로95길4_5_1',
'강남대로95길4_5_2',
'강남대로95길5',
'강남대로95길6',
'강남대로95길7',
'강남대로95길8',
'강남대로97길1',
'강남대로97길2',
'강남대로97길3',
'강남대로97길4',
'강남대로97길5',
'강남대로97길5_6_1',
'강남대로97길5_6_2',
'강남대로97길6',
'강남대로99길1',
'강남대로99길2',
'강남대로99길2_3',
'강남대로99길3',
'강남대로99길3_4',
'강남대로99길4',
'강남대로99길5',
'강남대로100길1',
'강남대로100길2',
'강남대로100길3',
'강남대로100길4',
'강남대로100길5',
'강남대로101안길1',
'강남대로101안길2',
'강남대로101안길3',
'강남대로101안길4',
'강남대로105길1',
'강남대로105길2',
'강남대로109길1',
'강남대로109길2',
'강남대로109길3',
'강남대로109길4',
'강남대로109길4_5_1',
'강남대로109길4_5_2',
'강남대로109길5',
'강남대로109길6',
'나루터로1',
'나루터로2',
'나루터로2_3',
'나루터로3',
'나루터로4',
'나루터로5',
'나루터로6',
'나루터로7',
'나루터로8',
'나루터로4길1',
'나루터로4길2',
'나루터로4길3',
'나루터로4길4',
'나루터로4길4_5',
'나루터로4길5',
'나루터로8길1',
'나루터로8길2',
'나루터로8길3',
'나루터로8길4',
'나루터로10길1',
'나루터로10길2',
'나루터로10길3',
'나루터로12길1',
'나루터로12길2',
'나루터로12길3',
'나루터로12길3_4_1',
'나루터로12길3_4_2',
'나루터로12길3_4_3',
'나루터로12길4',
'나루터로15길1',
'나루터로15길2',
'나루터로15길3',
'신반포로1',
'신반포로2',
'신반포로3',
'신반포로4',
'신반포로5',
'신반포로6',
'신반포로7',
'신반포로33길1',
'신반포로33길2',
'신반포로33길3',
'신반포로33길4',
'신반포로33길4_5',
'신반포로33길5',
'신반포로33길5_6',
'신반포로33길6',
'신반포로33길6_7',
'신반포로33길7',
'신반포로41길1',
'신반포로41길2',
'신반포로41길3',
'신반포로41길4',
'신반포로41길5',
'신반포로43길1',
'신반포로43길1_2_1',
'신반포로43길1_2_2',
'신반포로43길2',
'신반포로43길2_3',
'신반포로43길3',
'신반포로43길3__1',
'신반포로43길3__2',
'신반포로45길1',
'신반포로45길2',
'신반포로45길4',
'신반포로45길5',
'신반포로45길6',
'신반포로45길6_7',
'신반포로45길7',
'신반포로45길7_8',
'신반포로45길8',
'신반포로47길1',
'신반포로47길2',
'신반포로47길3',
'신반포로47길4',
'신반포로47길5',
'신반포로47길6',
'신반포로47길7',
'신반포로47길8',
'신반포로47길9',
'신반포로47길10',
'신반포로47길10_11',
'신반포로47길11',
'신반포로47길11_12',
'신반포로47길12',
'신반포로47길12_13',
'신반포로47길13',
'신반포로49길1',
'신반포로49길2',
'잠원로1',
'잠원로2',
'잠원로2_3_1',
'잠원로2_3_2',
'잠원로3',
'잠원로4',
'잠원로5',
'잠원로5_6',
'잠원로6',
'잠원로7',
'잠원로7_8_1',
'잠원로7_8_2',
'잠원로7_8_3',
'잠원로8',
'잠원로4길1',
'잠원로4길1_2_1',
'잠원로4길1_2_2',
'잠원로4길1_2_3',
'잠원로4길1_2_3_1',
'잠원로4길1_2_4',
'잠원로4길2',
'잠원로4길3',
'잠원로8길1',
'잠원로8길2',
'잠원로8길3',
'잠원로8길4',
'잠원로12길1',
'잠원로12길2',
'잠원로12길3',
'잠원로12길4',
'잠원로12길5',
'잠원로14길1',
'잠원로14길2']
lat = db.reference('/lat').get()
lng = db.reference('/lng').get()
p1lat = db.reference('/p1lat').get()
p1lng = db.reference('/p1lng').get()
p2lat = db.reference('/p2lat').get()
p2lng = db.reference('/p2lng').get()

latd = []
lngd = []
p1latd = []
p1lngd = []
p2latd = []
p2lngd = []
for i in keyname :
    latd.append(lat[i])
    lngd.append(lng[i])
    p1latd.append(p1lat[i])
    p1lngd.append(p1lng[i])
    p2latd.append(p2lat[i])
    p2lngd.append(p2lng[i])
roaddf = pd.DataFrame({'도로명':list(keyname)})
ddff = pd.DataFrame({'p1위도':p1latd, 'p1경도':p1lngd,
                       'p2위도':p2latd,'p2경도':p2lngd})

ref = db.reference('/finalscore')
lst = ref.get() ## finalscore
ref_road = db.reference('/road')
lst2 = ref_road.get()
df3 = pd.DataFrame({'도로명':keyname, '위도':latd,'경도':lngd})

def getlatlng(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/xml?address="
    url = base_url + address + "CA&key=AIzaSyBHLxYz1nqgbaj-SIxnBXtvWiLiXAr1LNQ"
    res = requests.get(url)
    html = BeautifulSoup(res.text,'html.parser')
    lat = re.sub('<[^>]*>', '',str(html.select("location > lat")) ,0)##위도
    lng = re.sub('<.+?>', '',str(html.select("location > lng")) ,0) ##경도
    lat = float(lat.replace('[', '').replace(']', ''))
    lng = float(lng.replace('[', '').replace(']', ''))
    return lat,lng
def getPos(x, y):
    x = float(x)
    y = float(y)
    position1=[]
    position2 =[]
    for i in range(len(ddff)):
        if abs(x - ddff.loc[i, 'p1위도']) + abs(y - ddff.loc[i, 'p1경도']) >\
                abs(x - ddff.loc[i, 'p2위도']) + abs(y - ddff.loc[i, 'p2경도']):

            position1.append([i, abs(x - ddff.loc[i, 'p1위도']) + abs(y - ddff.loc[i, 'p1경도'])])
        else:
            position2.append([i, abs(x - ddff.loc[i, 'p2위도']) + abs(y - ddff.loc[i, 'p2경도'])])

    minn = 1000
    result1 =0
    result2 = 0
    if min(position1[1]) > min(position2[1]):
        for j in position1 :
            if minn > j[1]:
                minn = j[1]
                result1 = j[0]
    else:
        for j in position2 :
            if minn > j[1]:
                minn = j[0]
                result2 = j[0]

    if result1 >0:
        road =df3.loc[result1, '도로명']

        return road
    else :
        road =df3.loc[result2, '도로명']

        return road

def allpath(graph, start, end):
    visited = {start: 0}
    h = [(0, start)]
    path = {}
    lst=[]
    distances = {vertex: float('inf') for vertex in graph} # 시작점과 모든 정점과의 사리의 거리를 무한으로 지정
    while distances:
        current_distance, current_vertex = heapq.heappop(h)
        try:
            while current_vertex not in distances:
                current_distance, current_vertex = heapq.heappop(h)
        except IndexError:
             break

        if current_vertex == end:
            way = end
            lst.append(way)
            path_output = end + '->'
            while path[way] != start:
                path_output += path[way] + '->'
                way = path[way]
                lst.append(way)
            lst.append(start)
            path_output += start

            return visited[end], path, lst

        del distances[current_vertex]

        for v, weihgt in graph[current_vertex].items():
            weihgt = current_distance + weihgt


            if v not in visited or weihgt < visited[v] :
                visited[v] = weihgt
                heapq.heappush(h,(weihgt,v))
                path[v] = current_vertex


    return visited,path,lst

def dijkstra(graph, start, end):
    visited = {start: 0}
    h = [(0, start)]
    path = {}
    lst=[]
    distances = {vertex: float('inf') for vertex in graph} # 시작점과 모든 정점과의 사리의 거리를 무한으로 지정
    #istances[start] = [0, start] # 시작점과 시작점 사이의 거리 0
    #queue = [] # [[거리,정점]]
    #print(distances[start][0])
    #heapq.heappush(queue, [distances[start][0], start])
    while distances:
        current_distance, current_vertex = heapq.heappop(h)
        try:
            while current_vertex not in distances:
                current_distance, current_vertex = heapq.heappop(h)
        except IndexError:
             break
        #if distances[current_vertex][0] < current_distance:
            #continue

        if current_vertex == end:
            way = end
            lst.append(way)
            path_output = end + '->'
            while path[way] != start:
                path_output += path[way] + '->'
                way = path[way]
                lst.append(way)
            lst.append(start)
            path_output += start
            #print(path_output)

            return visited[end], path, lst

        del distances[current_vertex]

        for v, weihgt in graph[current_vertex].items():
            weihgt = current_distance + weihgt
            #if weihgt < distances[adjacent][0]: # 현재까지 시작정점과 현재정점사이의 거리보다 짧다면
                #distances[adjacent] = [dis, current_vertex] # 현재정점과 시작정점 사이의 거리 업데이트
                #heapq.heappush(queue, [dis, adjacent])

            if v not in visited or weihgt < visited[v] :
                visited[v] = weihgt
                heapq.heappush(h,(weihgt,v))
                path[v] = current_vertex


    return visited,path,lst
def findlatlng(name):
    lat = df3[df3['도로명'] == name].loc[:, '위도'].values[0]
    lng = df3[df3['도로명'] == name].loc[:, '경도'].values[0]
    return lat, lng


app = Flask(__name__)

@app.route('/')
def inputTest():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
       dep = request.form['departure']
       des = request.form['destination']
       dep_lat, dep_lng = getlatlng(dep)
       des_lat, des_lng = getlatlng(des)
       s = getPos(dep_lat, dep_lng)
       e = getPos(des_lat, des_lng)
       dfs_a,dfs_b,dfs_c = allpath(lst,s,e)
       temp = []

       for i in dfs_c:
           ss,ee = findlatlng(i)
           temp.append((ss,ee))

       temp.reverse()

       return render_template("generic.html", dep=dep, des=des, dep_lat=dep_lat, dep_lng=dep_lng, des_lat=des_lat, des_lng=des_lng, temp=temp)

@app.route('/result2', methods=['POST'])
def result2():
    if request.method == 'POST':
       dep = request.form['departure']
       des = request.form['destination']
       dep_lat, dep_lng = getlatlng(dep)
       des_lat, des_lng = getlatlng(des)
       s = getPos(dep_lat, dep_lng)
       e = getPos(des_lat, des_lng)
       (a, b, c) = dijkstra(lst2, s, e)
       temp = []
       for i in c:
           ss,ee = findlatlng(i)
           temp.append((ss,ee))
       temp.reverse()
       return render_template("elements.html", dep_lat=dep_lat, dep_lng=dep_lng, des_lat=des_lat, des_lng=des_lng, temp=temp)

@app.route('/elements')
def elements():
       return render_template('elements.html')

@app.route('/index')
def index():
       return render_template('index.html')

@app.route('/generic')
def generic():
       return render_template('generic.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True )
