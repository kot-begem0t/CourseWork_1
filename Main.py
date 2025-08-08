# получить картинки кошек по API с сайта cataas.com с текстом
#     нужен текст для картинки
#     поэтому тексту можно найти/получить картинку
#     загрузить искомую картинку на Я.диск по "воздуху"
#         загружаем в папку на Я.диск, в папку с названием нашей группы
#             если нет папки, нужно создать папку, присвоить папке имя моей группы
#         картинка должна иметь наименование такое же, как текст по которому мы её нашли
#     после загрузки нужен файл с отчетом
#         файл с информацией о размере файла картинки в json-файл
#         файл поместить в папку report репозитории
#             если нет папки, нужно создать папку, присвоить папке имя report

import requests
import Yandex_token

text = 'hello'

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


class DownloadsImageCat(DownloadsImage):
    cat_url = 'https://cataas.com/cat/says/'
    def __init__(self, token, text):
        super().__init__(token)
        self.text = text

    def download_cat_for_yd(self):
        url = 'v1/disk/resources/upload'
        responses = requests.post(f'{self.yd_url}{url}?path={self.name_group}%2F{self.text}&url={self.cat_url}{self.text}', headers=self.headers)
        if str(responses) == '<Response [409]>':
            self.create_yd_folder()
            return self.download_cat_for_yd()


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