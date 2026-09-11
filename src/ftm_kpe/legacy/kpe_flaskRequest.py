import requests
import os

def run():
    text = open("datas/500-KP/document/art_and_culture-20902975.txt", 'r', errors='backslashreplace').read()
    data = {'text1': text}
    url = 'http://127.0.0.1:5005/akpe'

    response = requests.post(url, json=data)
    scoredKpe = response.json()
    print(str(response.json()))
