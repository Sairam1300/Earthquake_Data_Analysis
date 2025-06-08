
"""
Author : Pulyala Sairam Reddy
Filename : final_project.py
Purpose : Acquiring, selecting, analyzing and vizulating data
Revisions:
    00 : import the required modules
    01 : define getCityData,coord2rad,havDist,findCities,
         getQuakeData functions
    02 : Announce and call the getCityData and getQuakeData functions
    03 : Prompt the user for selecting the various range of categories 
         for analyzing the data
    04 : plot the graphs for the selected data
    
    
"""
### Step 1 : Import the required modules
from datetime import datetime as dt # importing datetime module
import csv # importing csv module
# importing various functions from math module
from math import radians,cos,sin,asin,sqrt 
# importing matplotlib library 
import matplotlib.pyplot as plt

### Step 2 : define getCityData,coord2rad,havDist,findCities,
###          getQuakeData functions
# defining getCityData function
def getCityData():
    '''
    Description: reading the data from a csv file and returing the data 
                 in a dictionary.
    Returns : a dictionary with location as key and the rest of the 
              data as a dictionary.
  
    '''
    # Open the world cities data CSV file in read mode.
    with open("worldcitiesF23.csv","r") as f:
        read=csv.DictReader(f)
        #  Convert a everyline into  dictinaries
        data=[line for line in read]
        new_data={}
        for item in data:
            lat=float(item.pop('lat')) # converting string into a float
            lng=float(item.pop('lng')) # converting string into a float
            location=(lat,lng)  # create a tuple representing the location
            item['pop']=0 if item['pop']=="" else int(item['pop'])
            new_data[location]=item
    # Returns dictionary containing city data
    return new_data

def coord2rad(location):
    '''
    Input:
        location : coordinates in degrees (tuple:lat,lng)
        
    Returns:
        location : coordinates in degrees (tuple:lat,lng)

    '''
    coordinates = {'lat':radians(location[0]),'lng':radians(location[1])}
    return coordinates

def havDist(loc1,loc2,unit="km"):
    '''
    Input:
        loc1 : coordinates in degrees (tuple:lat,lng)
        loc2 : coordinates in degrees (tuple:lat,lng)
        unit : optional paramter The default is "km" for kilometers,
               otherwise miles.

    Returns:
        Distance between two locations

    '''
    # convert coordinate tuple into dictionaries in radians
    loc1 = coord2rad(loc1)
    loc2 = coord2rad(loc2)   
    # Haversine formula
    dlng = loc2['lng']-loc1['lng']
    dlat = loc2['lat']-loc1['lat']
    a = sin(dlat/2)**2 + \
        cos(loc1['lat']) * cos(loc2['lat']) * \
        sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers.
    r = 6371 if unit=="km" else 3956 # miles if not km
    # calculate the result
    return (c*r)
    
def findCities(loc,cityDict,r):
    '''
    Description : accepts a target location, dictionary of cities,
                  and radius value as input and returns a list of cities 
                  
    Input : 
    loc : coordinates in degrees (tuple:lat,lng)
    cityDict : Dictionary of cities data
    r : radius value
    
    Returns:
    close_cities : return a list of close cities to the given location.

    '''
    close_cities=[]
    for co,data in cityDict.items():
        # Compute the haversine distance between 
        # the specified location and the city
        distance=havDist(loc,co)
        # To verify whether the city falls within the designated radius.
        if distance<r:
            # Append city details to the result list
            close_cities.append({'city':data['city'],
                    'country':data['country'],'pop':data['pop'],
                    'distance':round(distance,2)})
            # sort the data based on the distance
            close_cities.sort(key=lambda x:x['distance'])
    return close_cities

def getQuakeData():
    '''
    Description: reading the data from a csv file and returing the data 
                 in a dictionary.
    Returns : a dictionary with location as key and the rest of the 
              data as a dictionary.
    '''
    with open("earthquakesF23.csv") as f:
        #  Convert a everyline into  dictinaries
        read=csv.DictReader(f)
        data=[line for line in read]
        quake_data={}
        for item in data:
            # Extract latitude and longitude values and 
            # create a tuple representing the location
            
            lat=float(item.pop('Latitude'))
            lng=float(item.pop('Longitude'))
            location=(lat,lng)
            # Converted  Magnitude to float
            item['Magnitude']=float(item['Magnitude'])
            try:
                # Extract date and time, then create a datetime object
                datetime=dt.strptime(f'{item["Date"]} {item["Time"]}',
                                      '%m/%d/%Y %H:%M:%S')
                del item['Date'] # deleting the data
                del item['Time'] # deleting the data
                item['datetime']=datetime
                quake_data[location]=item
                # extract date and time for bad values
                # then convert to datetime object
            except:
                datetime=dt.strptime(f'{item["Date"]}',
                                     "%Y-%m-%dT%H:%M:%S.%fZ")
                del item['Date']
                del item['Time']
                item['datetime']=datetime
                quake_data[location]=item
                
    return quake_data # return data as a dictionary
        
### Step 3 :  Announce and call the getCityData and getQuakeData functions
# announce 
print("\n*** Earthquake Data ***")
# calling getCityData and getQuakeData functions
cityDict=getCityData()
qDict=getQuakeData()

# print the length of the data
print(f"\nAcquired data {len(cityDict)} cities.")
print(f"Acquired data {len(qDict)} earthquakes.")

### Step 4 : Prompt the user for selecting the various range of categories 
###               for analyzing the data

# prompt the user for the selection if yes 
# select the type else proceed for latitude
sel=input("\nRespond with 'yes' for selection?")
#ty_list for getting all the types as a list
ty_list=set(data['Type'] for loc,data in qDict.items())
# checking the user input, if yes go for the selection
# else select the entire data anad move to next item
if sel=="yes":
    print("\nSELECT tremor type : ")
    print("Choices are... : Earthquake,Explosion,Nuclear Explosion,Rock Burst")
    # prompt the user for the type of the data
    while True:
        
        ty=input("Enter tremor type (also accpets first three characters) :")
        # check for user input if nothing is given select the entire data
        if ty=="":
            ty_selected=list(map(lambda x:x,qDict.items()))
            print("Accepted..")
            tys=f"{ty_list}"
            print(f"{ty_list}")
            # print the no of records selected
            print(f"Selected {len(ty_selected)} records")
            break
        else:
        # if user input is not empty check for the type in ty_list
            for i in ty_list:
                if ty in i[:3]:
                    ty = i  
        # check if the user input is in list of types
        
        # if yes proceed else prompt the user for correct response
        if ty in ty_list:
            # select the records with user input type
            ty_selected=list(filter(lambda x:x[1]['Type']==ty,qDict.items()))
            tys=f"{ty}"
            print("Accepted..")
            print(tys)
            # print the no of records selected
            print(f"Selected {len(ty_selected)} records")
            # prompt the user to move to next selection
            res=input("\nRespond with 'yes' if Want to move to latitude?")
            # if yes break the loop else continue
            if res=="yes":
                break
            else:
                continue
        
        else:
            # prompt the user for correct response
            print("Please enter the correct choice")
# if the type of selection is not yes select the entire data
# and move to next item
else:
    ty_selected=list(map(lambda x:x,qDict.items()))
    tys=f"{ty_list}"
    print("Accepted..")
    print(f"{ty_list}")
    # print the no of records selected
    print(f"Selected {len(ty_selected)} records")
    
        
    
# list of latitudes from the previous selceted records 
lat_list=sorted([lat for (lat,lng),data in ty_selected])
print("\nSELECT latitude : Enter two values seperated by comma")
print(f"range is {min(lat_list)} through {max(lat_list)}")
  
while True:
    try:
        # split the 2 latitudes and assign to lat1,lat2
        # if nothing is given or single value is is given
        # select the entire data
        lat1,lat2=input("Enter minimum/maximum latitude values:").split(",")
        # converting to floating numbers
        lat1,lat2=float(lat1),float(lat2)
        lat_min,lat_max=min(lat1,lat2),max(lat1,lat2)
        # checking the given inputs are in the range of latitude list
        # if yes select the data records
        # else prompt the user again for the response
        if min(lat_list)<lat_min and lat_max<max(lat_list):
            # list of selected records with in the range 
            # from the previous selected data
            lat_selected=[((lat,lng),data) for (lat,lng),data in ty_selected
                      if lat_min<=lat<=lat_max]
            print("Accepted...")
            print({'min':lat_min,'max':lat_max})
            # print the no of records selected
            print(f"Selected {len(lat_selected)} records")
            # prompt the user for moving to next item
            res=input("\nRespond with 'yes' if Want to move to longitude?")
            # if yes break the loop
            # else prompt the user for latitude values
            if res=="yes":
                break
            else:
                continue
        else:
            # print the vales are not in range 
            # if the above if statement is failed
            print("one or more values out of range <(lat1,lat2)>")
    # if the above try mthod fails select entire data 
    # from the previous selected data      
    except:
        # selecting the all records from the previous selected data
        lat_selected=[((lat,lng),data) for (lat,lng),data in ty_selected]
        print("Accepted...")
        print({'min':min(lat_list),'max':max(lat_list)})
        # print the no of records selected
        print(f"Selected {len(lat_selected)} records")
        # prompt the user for moving to next item
        res=input("\nRespond with 'yes' if Want to move to longitude?")
        # if yes break the loop
        # else prompt the user for latitude values
        if res=="yes":
            break
        else:
            continue

# list of longitudes from the previous selceted records 
lng_list=sorted([lng for (lat,lng),data in lat_selected])
print("\nSELECT longitude : Enter two values seperated by comma")
print(f"range is {min(lng_list)} through {max(lng_list)}")
while True: 
    try:
        # split the 2 longitudes and assign to lng1,lng2
        # if nothing is given or single value is is given
        # select the entire data
        lng1,lng2=input("Enter minimum/maximum longitude values:").split(",")
        # converting to floating numbers
        lng1,lng2=float(lng1),float(lng2)
        lng_min,lng_max=min(lng1,lng2),max(lng1,lng2)
        # checking the given inputs are in the range of longitude list
        # if yes select the data records
        # else prompt the user again for the response
        if min(lng_list)<lng_min and lng_max<max(lng_list):
            # list of selected records with in the range 
            # from the previous selected data
            lng_selected=[((lat,lng),data) for (lat,lng),data in lat_selected
                      if lng_min<=lng<=lng_max]
            print("Accepted...")
            print({'min':lng_min,'max':lng_max})
            # print the no of records selected
            print(f"Selected {len(lng_selected)} records")
            # prompt the user for moving to next item
            res=input("\nRespond with 'yes' if Want to move to dates?")
            # if yes break the loop
            # else prompt the user for longitude values
            if res=="yes":
                break
            else:
                continue
        # print the vales are not in range 
        # if the above if statement is failed    
        else:
            print(f"one or more values out of range <({lng1},{lng2})>")
    # if the above try method fails select entire data 
    # from the previous selected data        
    except:
        # selecting the all records from the previous selected data
        lng_selected=[((lat,lng),data) for (lat,lng),data in lat_selected]
        print("Accepted...")
        print({'min':min(lng_list),'max':max(lng_list)})
        # print the no of records selected
        print(f"Selected {len(lng_selected)} records")
        # prompt the user for moving to next item
        res=input("\nRespond with 'yes' if Want to move to dates?")
        # if yes break the loop
        # else prompt the user for latitude values
        if res=="yes":
            break
        else:
            continue
# list of dates from the previous selceted records
date_list=sorted([data['datetime'].date()
                  for loc,data in lng_selected])

print("\nSELECT date mm/dd/yy: Enter two values seperated by comma")
print(f"range is {dt.strftime(min(date_list),'%m/%d/%Y')} through {dt.strftime(max(date_list),'%m/%d/%Y')}")

while True:
    try:
        # split the 2 dates and assign to date1,date2
        # if nothing is given or single value is is given
        # select the entire data
        date1,date2=input("Enter minimum/maximum date values:").split(",")
        date1,date2=dt.strptime(date1,'%m/%d/%Y'),dt.strptime(date2,'%m/%d/%Y')
        date_min,date_max=min(date1,date2).date(),max(date1,date2).date()
        # checking the given inputs are in the range of date list
        # if yes select the data records
        # else prompt the user again for the response
        if min(date_list)<date_min and date_max<max(date_list):
            # list of selected records with in the range 
            # from the previous selected data
            date_selected=[((lat,lng),data) for (lat,lng),data in lng_selected
                      if date_min<=data['datetime'].date()<=date_max]
            print("Accepted...")
            d=f"{dt.strftime(date1,'%m/%d/%Y')} to {dt.strftime(date2,'%m/%d/%Y')}"
            print({'min':dt.strftime(date1,'%m/%d/%Y'),
                   'max':dt.strftime(date2,'%m/%d/%Y')})
            # print the no of records selected
            print(f"Selected {len(date_selected)} records")
            # prompt the user for moving to next item
            res=input("\nRespond with 'yes' if Want to move to magnitude?")
            # if yes break the loop
            # else prompt the user for dates
            if res=="yes":
                break
            else:
                continue
        # print the vales are not in range 
        # if the above if statement is failed            
        else:
            print(f"one or more values out of range <{dt.strftime(date1,'%m/%d/%Y')},{dt.strftime(date2,'%m/%d/%Y')}>")
    # if the above try method fails select entire data 
    # from the previous selected data         
    except:
        # selecting the all records from the previous selected data
        date_selected=[((lat,lng),data) for (lat,lng),data in lng_selected]
        d=f"{dt.strftime(min(date_list),'%m/%d/%Y')} to {dt.strftime(max(date_list),'%m/%d/%Y')}"
        print("Accepted...")
        print({'min':dt.strftime(min(date_list),'%m/%d/%Y'),
               'max':dt.strftime(max(date_list),'%m/%d/%Y')})
        # print the no of records selected
        print(f"Selected {len(date_selected)} records")
        # prompt the user for moving to next item
        res=input("\nRespond with 'yes' if Want to move to magnitude?")
        # if yes break the loop
        # else prompt the user for dates
        if res=="yes":
            break
        else:
            continue

# list of magnitudes from the previous selceted records
mag_list=sorted([data['Magnitude'] for (lat,lng),data in date_selected])
print("\nSELECT Magnitude : Enter two values seperated by comma")
print(f"range is {min(mag_list)} through {max(mag_list)}")
while True: 
    try:
        # split the 2 magnitudes and assign to mag1,mag2
        # if nothing is given or single value is is given
        # select the entire data
        mag1,mag2=input("Enter minimum/maximum magnitude values:").split(",")
        # converting to floating numbers
        mag1,mag2=float(mag1),float(mag2)
        mag_min,mag_max=min(mag1,mag2),max(mag1,mag2)
        # checking the given inputs are in the range of magnitude list
        # if yes select the data records
        # else prompt the user again for the response
        if min(mag_list)<mag_min and mag_max<max(mag_list):
            # list of selected records with in the range 
            # from the previous selected data
            mag_selected=[((lat,lng),data) for (lat,lng),data in date_selected
                      if mag_min<=data['Magnitude']<=mag_max]
            print("Accepted...")
            print({'min':mag_min,'max':mag_max})
            # print the no of records selected
            print(f"Selected {len(mag_selected)} records")
            # prompt the user for moving to next item
            res=input("\nRespond with 'yes' if Want to move to Analysis?")
            # if yes break the loop
            # else prompt the user for magnitude values
            if res=="yes":
                break
            else:
                continue
        # print the vales are not in range 
        # if the above if statement is failed   
        else:
            print(f"one or more values out of range <({mag1},{mag2})>")
    # if the above try method fails select entire data 
    # from the previous selected data        
    except:
        # selecting the all records from the previous selected data
        mag_selected=[((lat,lng),data) for (lat,lng),data in date_selected]
        print("Accepted...")
        print({'min':min(mag_list),'max':max(mag_list)})
        # print the no of records selected
        print(f"Selected {len(mag_selected)} records")
        # prompt the user for moving to next item
        res=input("\nRespond with 'yes' if Want to move to Analysis?")
        # if yes break the loop
        # else prompt the user for magnitudes
        if res=="yes":
            break
        else:
            continue
 
mag_selected.sort(key=lambda x:x[1]['Magnitude'])
# list with location and severity radius as tuple from previous selected list
sev_list=[(loc,10**((0.5*data['Magnitude'])-2)) for loc,data in mag_selected]
sev_list.sort(key=lambda x : x[1])
# printing largest quake location and data
print(f"largest equake is at {sev_list[-1][0]}")
print(qDict[sev_list[-1][0]])
# calling findCities functions to check the affected cities
affected_cities=findCities(sev_list[-1][0], cityDict,sev_list[-1][1])
print(affected_cities)
print(f"{len(affected_cities)} affected cities within {sev_list[-1][1]} km..")
print("closest city is...")
# closest_cities for large quake location and 5000 km radius
close_cities=findCities(sev_list[-1][0], cityDict,5000)
# printing the closest city data
print(close_cities[0])



# latitude,longittude and magnitude lists for the selected data
lats=[lat for (lat,lng),data in mag_selected]
lngs=[lng for (lat,lng),data in mag_selected]
mags=[data['Magnitude'] for (lat,lng),data in mag_selected]
# scatter plot with x,y axis as longitude,latitude
# color based on magnitude values
plt.scatter(lngs,lats,c=mags)
# labelling x,y axis and color bar
plt.xlabel('longitude in degrees')
plt.ylabel('latitude in degrees')
plt.colorbar(label='magnitude')
nl='\n'
# title of scatter plot
plt.title(f"{tys}{nl}{d}")
# displaying the scatter plot
plt.show()

# list of unique years from the selected data
year_selected=sorted(set(map(lambda x: x[1]['datetime'].year,
                                  mag_selected)))
# creating a new dictionary for no of events
events={}
# traversing through years list
for year in year_selected:
    # list of data in particular year
    item=[data for loc,data in mag_selected
               if data['datetime'].year==year]
    # appending values to dictionary
    # key as year and value as length of list of data
    events[year]=len(item)
# bar plot with x,y axis as years and length of data 
# color of bar plot as blue
plt.bar(events.keys(),events.values(),color='blue')
# labelling x and y axis
plt.xlabel('year')
plt.ylabel('lNumber of events')
# title for bar plot
plt.title(f"{tys}{nl}{d}")
# displaying bar plot
plt.show()

# creating a new dictionary for average magintudes
avg_mags={}
# traversing through years list
for year in year_selected:
    # list of magnitudes in particular year
    item=[data['Magnitude'] for loc,data in mag_selected
               if data['datetime'].year==year]
    # appending values to dictionary
    # key as year and value as length of list of data
    avg_mags[year]=sum(item)/len(item)
# scatter plot with x,y axis as year and average magnitude
plt.scatter(avg_mags.keys(),avg_mags.values())
# labelling x and y axis
plt.xlabel('year')
plt.ylabel('average magnitude')
nl='\n'
# title of scatter plot
plt.title(f"{tys}{nl}{d}")
# displaying the scatter plot
plt.show()










