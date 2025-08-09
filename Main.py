import requests
import json
import os
import Yandex_token

# spot for choose image cats, write your text in variable 'text'
text = 'hello'

# main class
class DownloadsImage:
    yd_url = 'https://cloud-api.yandex.net/'
    yd_url_1 = 'v1/disk/resources'
    yd_url_2 = 'v1/disk/resources/upload'
    name_group = 'pd-130'
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_yd_folder(self):
        """
        create folder in yandex disk with name group
        """
        responses = requests.put(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}', headers=self.headers)

# inherited class for cats
class DownloadsImageCat(DownloadsImage):
    cat_url = 'https://cataas.com/cat/says/'
    def __init__(self, token, text):
        super().__init__(token)
        self.text = text

    def cat_report(self):
        """
        report is making of file in yandex disk
        """
        # we do the request until we get response
        while str(requests.get(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{text}', headers=self.headers)) != '<Response [200]>':
            print('Ждем загрузки файла на Яндекс диск')
        # we gain a need data and make dictionary
        responses = requests.get(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{text}', headers=self.headers)
        data = {
            'name': responses.json()['name'],
            'created': responses.json()['created'],
            'size': responses.json()['size']
        }
        # we check a file .json in repository, if he is then refresh file, if he is not then create file
        if str(os.path.exists('cat_report.json')) == 'True':
            with open("cat_report.json", "r") as file:
                list_data = json.load(file)
            list_data.append(data)
            with open(f'cat_report.json', 'w', encoding='utf-8') as file:
                json.dump(list_data, file, indent=4, ensure_ascii=False)
        else:
            with open(f'cat_report.json', 'w', encoding='utf-8') as file:
                list_data = []
                list_data.append(data)
                json.dump(list_data, file, indent=4, ensure_ascii=False)

    def download_cat_for_yd(self):
        """
        load cat image in disk and make report
        """
        responses = requests.get(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{text}', headers=self.headers)
        # check if file name exist in yandex disk
        if str(responses) != '<Response [200]>':
            responses = requests.post(f'{self.yd_url}{self.yd_url_2}?path={self.name_group}%2F{self.text}&url={self.cat_url}{self.text}', headers=self.headers)
            # check if folder exists on yandex disk
            if str(responses) == '<Response [409]>':
                self.create_yd_folder()
                print('Создаем папку на Яндекс диске')
                return self.download_cat_for_yd()
        else:
            print('Файл с таким именем уже имеется на диске')
        self.cat_report()
        print('Файл загружен на диск')

# inherited class for dogs
class DownloadsImageDog(DownloadsImage):
    dog_url = ''
    pass


Example_cat = DownloadsImageCat(Yandex_token.yd_t, text)
Example_cat.download_cat_for_yd()