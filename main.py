import requests
import json
import csv
import glob
import os

def clear_places():
    """
    Clears the places directory.
    """
    if os.path.exists('./places.json'):
        os.remove('./places.json')
    if os.path.exists('./places.csv'):
        os.remove('./places.csv')
    
def make_places_dir():
    """
    Creates the places directory if it doesn't exist.
    """
    if not os.path.exists('./places'):
        os.makedirs('./places')

def get_first_page_ids(place, key):
    """
    Returns the json object from the google places api query.
    """
    clear_places()
    query = f'halal%food%restaurant%in%{place.replace(" ", "%")}' #Treating the query as a string
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={key}" #Treating the url as a string
    places_result = requests.request("GET", url, headers={}, data={}).json() #Getting the json data from the url
    try: 
        return places_result['results'], places_result['next_page_token'] #Discarding header info, returning the results and token for next 20 results
    except KeyError: #If there is no next_page_token, it will return the results and None
        return places_result['results'], None

def get_next_page_ids(next_page, key):
    """
    Returns the json object from the google places api query.
    """
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_page}&key={key}" #Treating the url as a string
    places_result = requests.request("GET", url, headers={}, data={}).json() #Getting the json data from the url
    try:
        return places_result['results'], places_result['next_page_token'] #Discarding header info, returning the results and token for next 20 results
    except KeyError: #If there is no next_page_token, it will return the results and None
        return places_result['results'], None
    
def get_id_details_json(json_object, key):
    """
    Creates json files with the details of each place.
    """
    make_places_dir()
    for place, i in zip(json_object, range(20)):
        place_id = place['place_id']
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={key}" #Treating the url as a string
        places_result =  requests.request("GET", url, headers={}, data={}).json() #Getting the json data from the url
        with open(f'./places/place{i}.json', 'w') as f:
            json.dump(places_result, f, indent=4) #Saving the json data serialized into a file

def unite_json():
    """
    Unites all the json files into one json file.
    """
    file_exists = os.path.exists('./places.json')
    with open('./places.json', 'a', encoding='utf-8', newline='\n') as f:
        
        glob_obj = glob.glob('./places/*.json')
        
        if file_exists == True:
            with open('./places.json', 'r', encoding='utf-8') as j:
                existing_file = json.dumps(json.load(j), indent=4)
                existing_file = existing_file.strip('[\n]')
                f.truncate(0)
                f.write('[\n')
                f.write(existing_file)
                f.write(',\n')

        else:
            f.write('[\n')
    
        for json_file, i in zip(glob_obj, range(len(glob_obj))): #Get all the json files in the places folder
            places_result = json.load(open(json_file, 'r'))
            f.write(json.dumps(places_result, indent=4, ensure_ascii=False)) #Saving the json data serialized into a file
            if i == 19:
                f.write('\n]')
                break
            f.write(',\n')

def save_to_csv():

    """
    Saves the info to CSV file.

    If user wants any other info into the csv file, just pick the name of it from places.json and add it to the header and rows list.
    """

    #Defining the rows, as is on json file
    rows = ['name', 'formatted_address', 'rating', 'user_ratings_total', 'price_level', 'website',
            'current_opening_hours', 'international_phone_number', 'delivery', 'dine_in', 'reviews']
    #Defining the headers, human readable
    header = ['Name', 'Address', 'Rating', 'Total User Ratings', 'Price Level', 'Website',
                'Current Opening Hours', 'International Phone Number', 'Delivery', 'Dine In', 'Reviews']
    #Translates the boolean value to human readable
    bool_dict = {True: 'Open', False: 'Closed'}
    
    with open('./places.json', 'r', encoding='utf-8') as f:
        places = json.load(f)
    exists_file = os.path.exists('./places.csv') #Checks if file exists
    with open('./places.csv', 'a', newline='', encoding='utf-8-sig') as f:
        csv_writer = csv.writer(f, delimiter=';')
        if exists_file == False:
            csv_writer.writerow(header) #Writes the headers if the file is empty
    
        for place in places:
            place = place['result']
            place_list = []
            for row in rows:
                if row in place:
                    if row == 'current_opening_hours': #If the row is current_opening_hours, it will write only the open hours
                        place_list.append(place[row]['weekday_text'])
                    elif row == 'reviews': #If the row is reviews, it will write only the text on the reviews
                        place_list.append([review['text'] for review in place[row]])
                    elif row in ('delivery', 'dine_in'): #If the row is delivery or dine_in, it will translate the boolean value to human readable
                        place_list.append(bool_dict[place[row]])
                    else:
                        place_list.append(place[row])
                else: #If the row is not in the place, it will write None
                    place_list.append('')
            csv_writer.writerow(place_list)

def main():
    key = input("Enter API Key:")
    place = input("Enter Place to Search for:")
    pages = int(input("Enter Number of Pages to Search (Each page = 20 places):"))

    query_result, next_page = get_first_page_ids(place, key)
    get_id_details_json(query_result, key) #Gets the details of the first 20 places
    unite_json() #Unites all the json files into one json file
    for i in range(pages-1): #Gets the details of the next 20 places
        if next_page == None:
            break
        query_result, next_page = get_next_page_ids(next_page, key)
        get_id_details_json(query_result, key)
        unite_json()
    save_to_csv() #Saves the info to CSV file

if __name__ == '__main__':
    main() 





