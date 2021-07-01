from flask import Flask,render_template
from geopy.geocoders import Nominatim
import pickle
geolocator = Nominatim(user_agent="geoapiExercises")
app = Flask(__name__)
air = pickle.load(open("C:/Users/User/Desktop/Nearby/nearby/Files/airports.pkl",'rb'))
sea = pickle.load(open("C:/Users/User/Desktop/Nearby/nearby/Files/seaports.pkl",'rb'))
beach = pickle.load(open("C:/Users/User/Desktop/Nearby/nearby/Files/beaches.pkl",'rb'))
bus = pickle.load(open("C:/Users/User/Desktop/Nearby/nearby/Files/busstop.pkl",'rb'))
rail = pickle.load(open("C:/Users/User/Desktop/Nearby/nearby/Files/railway.pkl",'rb'))
lake = pickle.load(open("C:/Users/User/Desktop/Nearby/nearby/Files/lakes.pkl",'rb'))
from math import radians, cos, sin, asin, sqrt
def distance(lat1, lat2, lon1, lon2):
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * asin(sqrt(a))
	r = 6371
	return(c * r)
def int1(s):
  if s[0]=='-':
    return -(float(s[1:]))
  return float(s)
def get_coords(s1):
  try:
    # print(s1)
    l = s1.split()
    # print(l)
    lat = int1(l[1][:-1])
    # print(lat)
    lon = int1(l[0].split('(')[-1])
    # print(lon)
    return [lat,lon]
  except:
    return [1000,1000]
d = {"Lakes & Reservoirs":lake,"Airports":air,"Railway Stations":rail,"Sea ports":sea,"Beaches":beach,"Bus stops":bus}
@app.route("/<name>")
def abc(name):
    print(name)
    l1 = name.split("_")
    if len(l1)==2:
        l2 = l1[1]
        l1 = l1[0]
        Latitude = str(l1)
        Longitude = str(l2)
        location = geolocator.reverse(Latitude+","+Longitude)
        return str(location)
    l = l1
    l1 = l[0]
    l2 = l[1]
    ent = l[2]
    dist = l[3]
    if(ent in d):
        Latitude = str(l1)
        Longitude = str(l2)
        location = geolocator.reverse(Latitude+","+Longitude)
        ent = d[ent]
        # print(location.raw)
        code = location.raw['address']['country_code']
        if code  in ent:
            lis = []
            for i in ent[code]:
                lat2,lon2 = get_coords(i[-2])
                c_dist = distance(int1(Latitude),lat2,int1(Longitude),lon2)
                # print(c_dist)
                if c_dist<=int1(dist):
                    i.append(round(c_dist,1))
                    lis.append(i)
            print(lis)
            return {'status':"success",'list' : lis}
    return {'status':"failed"}

@app.route("/")
def hello():
    return render_template("maps1.html")
app.run(debug = True)