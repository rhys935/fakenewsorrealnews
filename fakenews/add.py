import requests

url = 'http://127.0.0.1:5000/apiaddnewsstories'
myobj = {'content':'uh oh uh oh uh oh' , 'url':"https://www.riotgames.com/en", 'realOrFake':'Fake'}

x = requests.post(url, json= myobj)