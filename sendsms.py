import requests
result:str = requests.post('https://textbelt.com/text', {
    'phone': '6476438856',
    'message': 'Hello world',
    'key': 'textbelt',
})

print(result)