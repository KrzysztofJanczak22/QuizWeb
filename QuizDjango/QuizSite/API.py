import requests

base_url = 'http://127.0.0.1:5000'

def fn_CheckCorrect(idAnswer):
    global base_url
    url = f'{base_url}/api/Correct/{idAnswer}'
    response = requests.get(url)
    return response.text

def fn_GetQuestion(category):
    global base_url
    url =f'{base_url}/api/Question/{category}'
    response = requests.get(url)
    return response.json()


fn_GetQuestion(100)