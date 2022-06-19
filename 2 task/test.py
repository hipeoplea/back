import requests

#получение мемов
print(requests.get('http://127.0.0.1:5000/get_memes').json())
#лайк
print(requests.get('http://127.0.0.1:5000/like_meme/51').json())
#скип
print(requests.get('http://127.0.0.1:5000/skip_meme/55').json())
