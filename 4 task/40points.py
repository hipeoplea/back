import vk
import sqlite3

con = sqlite3.connect('memes.db')
cursor = con.cursor()

session = vk.Session(access_token='vk1.a.VghFXpzy8XLo1FyJtHbKJjo1-zcxlCkX44170sVr0ULDG4qsCPn68GUNHs6NJfhfci55TEb_zRW429i7AlOUKzyjjtHCMfquh4jOLDBaUf1voC8C0psOx8HKkMVi4Vnnya2ZjGDphhsk2SmAxfYnUVo5eT0EhQ4-yeFCxPS26V2fgyeA-VFG-OIQ9NjJY0B4')
vk_api = vk.API(session)
#несколько альбомов с мемами вездекода
resp = vk_api.photos.get(owner_id='-197700721', album_id='274262016', extended=1,  v=5.131)['items']
res2 = vk_api.photos.get(owner_id='-197700721', album_id='284717200', extended=1,  v=5.131)['items']
res3 = vk_api.photos.get(owner_id='-197700721', album_id='281940823', extended=1,  v=5.131)['items']
#добавление мемов в бд
for i in resp + res2 + res3:
    fio = vk_api.users.get(user_ids=i['user_id'], v=5.131)[0]
    gg = cursor.execute('INSERT into mem(url, author, likes, priority) values (?, ?, ?, ?)',
                        (i['sizes'][-1]['url'], fio['first_name'] + " " + fio['last_name'], i['likes']['count'], 0))
    print(i['sizes'][-1]['url'], '\n', 'user:', fio['first_name'], fio['last_name'],'likes:', i['likes']['count'], '\n')

con.commit()