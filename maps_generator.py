import googlemaps
import pandas as pd
import folium
def geocode_place(key, place):
    gmaps = googlemaps.Client(key=key)
    geocode_result = gmaps.geocode(place)
    return geocode_result[0]['geometry']['location']

def get_directions(key, start, end, mode):
    if mode not in ('driving', 'walking', 'bicycling', 'transit'):
        mode = 'driving'
    gmaps = googlemaps.Client(key=key)
    directions_result = gmaps.directions(start, end, mode=mode, units='metric')
    return directions_result[0]['legs'][0]['steps']

def coordinates_to_df(data, start, end):
    df0 = pd.DataFrame(columns=['start_lat', 'start_lng', 'end_lat', 'end_lng'])
    
    for step, i in zip(data, range(len(data))):
        if i == 0:
            df1 = pd.DataFrame({'start_lat': start['lat'],
                                'start_lng': start['lng'],
                                'end_lat': step['end_location']['lat'],
                                'end_lng': step['end_location']['lng']}, index=[0])
            df0 = pd.concat([df0, df1], ignore_index=True)
        elif i == len(data) - 1:
            df1 = pd.DataFrame({'start_lat': step['start_location']['lat'],
                                'start_lng': step['start_location']['lng'],
                                'end_lat': end['lat'],
                                'end_lng': end['lng']}, index=[0])
            df0 = pd.concat([df0, df1], ignore_index=True)
        else:
            df1 = pd.DataFrame({'start_lat': step['start_location']['lat'],
                                'start_lng': step['start_location']['lng'],
                                'end_lat': step['end_location']['lat'],
                                'end_lng': step['end_location']['lng']}, index=[0])
            df0 = pd.concat([df0, df1], ignore_index=True)
    return df0
    
def create_map(df, start, end):
    f_map = folium.Map(location=[start['lat'], start['lng']], zoom_start=12)
    folium.Marker([start['lat'], start['lng']], popup='Start').add_to(f_map)
    folium.Marker([end['lat'], end['lng']], popup='End').add_to(f_map)
    for i in range(len(df)):
        folium.PolyLine(locations=[[df['start_lat'][i], df['start_lng'][i]],
                                   [df['end_lat'][i], df['end_lng'][i]]],
                        color='red', weight=2.5, opacity=1).add_to(f_map)
    return f_map    

def main():
    key = input("Enter API Key:")
    start = input("Enter starting location:")
    end = input("Enter destination:")
    mode = input("Enter mode of transport (driving, walking, bicycling, transit):")
    start_coords = geocode_place(key, start)
    end_coords = geocode_place(key, end)
    directions = get_directions(key, start_coords, end_coords, mode)
    df = coordinates_to_df(directions, start_coords, end_coords)
    f_map = create_map(df, start_coords, end_coords)
    f_map.save('map.html')
    #save dataframe to txt
    df.to_string('map.txt', index=False)

if __name__ == '__main__':
    main()
# key = 'AIzaSyDebkwR1_M9cGRW_bpdsA8qpZe2aMycv5g'
