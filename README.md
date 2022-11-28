# PlacesAPI Restaurants Finder

This CLI program uses Google's "Places API" to find Halal restaurants and all the available info on them in a determined place.

The method to get the data follows this steps:
  - Sends a query using the "textsearch" method to the api, that returns some info, including the place_id of each place.
  - Loop through all the place_id's and sends a query using the place_details method for each place.
  - Joins all the info together in a single json file.
  - Does that again for whatever number of pages the user chooses
  - Creates a CSV file containing all the useful info
  
The outputs are two files, a places.json, with all the raw info returned from google's API and a places.csv, which contains data in a more refined manner. 
