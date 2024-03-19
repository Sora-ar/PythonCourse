from pprint import pprint
import requests

url = "https://newsdata.io/api/1/news?apikey=pub_40345eaba0334c93c96d1236e5c53e73a2212&q=coronavirus"

response = requests.get(url)

pprint(response.json())
