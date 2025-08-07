# Получить картинки кошек по API с сайта cataas.com с текстом
#     Нужен текст для картинки
#     Поэтому тексту можно найти/получить картинку
#     Загрузить искомую картинку на Я.диск по "воздуху"
#         Загружаем в папку на Я.диск, в папку с названием нашей группы
#             если нет папки, нужно создать папку, присвоить папке имя моей группы
#         Картинка должна иметь наименование такое же, как текст по которому мы её нашли
#     После загрузки нужен файл с отчетом
#         файл с информацией о размере файла картинки в json-файл
#         файл поместить в папку report репозитории
#             если нет папки, нужно создать папку, присвоить папке имя report

import requests
import Yandex_token

text = 'hi'

class DownloadsImage:
    yd_url = 'https://cloud-api.yandex.net/'
    name_group = 'pd-130'
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_yd_folder(self):
        url = 'v1/disk/resources'
        responses = requests.put(f'{self.yd_url}{url}?path={self.name_group}', headers=self.headers)
        print(responses)


class DownloadsImageCat(DownloadsImage):
    cat_url = 'https://cataas.com/cat/says/'
    def __init__(self, token, text):
        super().__init__(token)
        self.text = text

    def download_cat_for_yd(self):
        url = 'v1/disk/resources/upload'
        name = f'{self.text}_{requests.get('https://cataas.com/cat/says/').headers['Date']}'
        responses = requests.post(f'{self.yd_url}{url}?path={self.name_group}%2F{self.text}&url={self.cat_url}{self.text}', headers=self.headers)
        print(responses)


class DownloadsImageDog(DownloadsImage):
    dog_url = ''
    pass

# responses = requests.get(f'{base_url}{random_cat}')
# print(responses.content)
# with open('image\cat.jpeg', 'wb') as f:
#     f.write(responses.content)

Example = DownloadsImage(Yandex_token.yd_t)
Example_cat = DownloadsImageCat(Yandex_token.yd_t, text)
Example_cat.download_cat_for_yd()
# print(requests.get('https://cataas.com/cat/says/').headers['Date'])