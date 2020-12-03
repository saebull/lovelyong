import requests
from bs4 import BeautifulSoup
import re
from flask import Flask
import heapq
import request
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('ongkey.json')
defaul_app = firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://ie-project-292614.firebaseio.com/'
})

lat = db.reference('/lat').get().values()
lng = db.reference('/lng').get().values()
keyname = db.reference('/p1lat').get().keys()
p1lat = db.reference('/p1lat').get().values()
p1lng = db.reference('/p1lng').get().values()
p2lat = db.reference('/p2lat').get().values()
p2lng = db.reference('/p2lng').get().values()
ref = db.reference('/finalscore')
lst = ref.get() ## finalscore
ref_road = db.reference('/road')
lst2 = ref_road.get()

p1p2 = pd.DataFrame({'p1위도':list(p1lat), 'p1경도':list(p1lng),
                       'p2위도':list(p2lat),'p2경도':list(p2lng)})
roaddf = pd.DataFrame({'도로명':list(keyname)})
df3 = pd.DataFrame({'도로명':list(keyname),'위도':list(lat),'경도':list(lng)})


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
    for i in range(len(p1p2)):
        if abs(x - p1p2.loc[i, 'p1위도']) + abs(y - p1p2.loc[i, 'p1경도']) > abs(x - p1p2.loc[i, 'p2위도']) + abs(y - p1p2.loc[i, 'p2경도']):
            position1.append([i, abs(x - p1p2.loc[i, 'p1위도']) + abs(y - p1p2.loc[i, 'p1경도'])])
        else:
            position2.append([i, abs(x - p1p2.loc[i, 'p2위도']) + abs(y - p1p2.loc[i, 'p2경도'])])
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
        road =roaddf.loc[result1, '도로명']
        return road
    else :
        road =roaddf.loc[result2, '도로명']
        return road
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


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)