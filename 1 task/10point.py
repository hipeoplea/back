import vk

session = vk.Session(access_token='vk1.a.VghFXpzy8XLo1FyJtHbKJjo1-zcxlCkX44170sVr0ULDG4qsCPn68GUNHs6NJfhfci55TEb_zRW429i7AlOUKzyjjtHCMfquh4jOLDBaUf1voC8C0psOx8HKkMVi4Vnnya2ZjGDphhsk2SmAxfYnUVo5eT0EhQ4-yeFCxPS26V2fgyeA-VFG-OIQ9NjJY0B4')
vk_api = vk.API(session)
resp = vk_api.photos.get(owner_id='-197700721', album_id='284717200', extended=1,  v=5.131)['items']
for i in resp:
    fio = vk_api.users.get(user_ids=i['user_id'], v=5.131)[0]
    print(i['sizes'][-1]['url'], '\n', 'user:', fio['first_name'], fio['last_name'],'likes:', i['likes']['count'], '\n')
