import requests;

API_KEY = '0e20fded-24a7-457c-a908-9c8f5f74fe29';
country = 'Canada';
#http://api.airvisual.com/v2/city?city=Los Angeles&state=California&country=USA&key={{YOUR_API_KEY}}

try:
    # submit the request using the session
    response = requests.get('http://api.airvisual.com/v2/nearest_city?key='+ API_KEY);
    print(response.status_code)
 
    # raise an exception in case of http errors
    response.raise_for_status()

    print(response.json())  

 
except requests.exceptions.HTTPError as e:
    # handle any errors here
    print(e)