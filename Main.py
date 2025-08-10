from idlelib.rpc import response_queue

import requests
import json
import os
import Yandex_token

# spot for choose image CATS, write your text in variable 'text'
text = 'hello'
# spot for choose image DOGS, write your text in variable 'breed'
breed = 'hound'

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

    def create_yd_folder_for_group(self):
        """
        create folder in yandex disk with name group
        """
        print(f'Создаем папку нашей группы {self.name_group} на Яндекс диске')
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
            print('Ждем загрузки файла с котиками на Яндекс диск')
        # we gain need data and make dictionary
        responses = requests.get(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{text}', headers=self.headers)
        data = {
            'name': responses.json()['name'],
            'created': responses.json()['created'],
            'size': responses.json()['size']
        }
        # we check a file .json in repository, if he is then refresh file, if he is not then create file
        if str(os.path.exists('cat_report.json')) == 'True':
            print('Обновляем файл .json с отчетом о котиках')
            with open("cat_report.json", "r") as file:
                list_data = json.load(file)
            list_data.append(data)
            with open(f'cat_report.json', 'w', encoding='utf-8') as file:
                json.dump(list_data, file, indent=4, ensure_ascii=False)
        else:
            print('Создаем файл .json с отчетом о котиках')
            with open(f'cat_report.json', 'w', encoding='utf-8') as file:
                list_data = []
                list_data.append(data)
                json.dump(list_data, file, indent=4, ensure_ascii=False)

    def download_cat_in_yd(self):
        """
        load cat image in disk and make report
        """
        responses = requests.get(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{text}', headers=self.headers)
        print('Загружаем файл с котиками на Яндекс диск')
        # check if file name exist in yandex disk
        if str(responses) != '<Response [200]>':
            responses = requests.post(f'{self.yd_url}{self.yd_url_2}?path={self.name_group}%2F{self.text}&url={self.cat_url}{self.text}', headers=self.headers)
            # check if folder exists on yandex disk
            if str(responses.json()['error']) == 'DiskPathDoesntExistsError':
                self.create_yd_folder_for_group()
                return self.download_cat_in_yd()
        else:
            print('Файл с котиками с таким именем уже имеется на Яндекс диске')
            return
        self.cat_report()
        print('Файл с котиками загружен на Яндекс диск')


# inherited class for dogs
class DownloadsImageDog(DownloadsImage):
    quantity_images = 5
    url_list_all_breeds = 'https://dog.ceo/api/breeds/list/all'
    url_random_image_by_breed = f'https://dog.ceo/api/breed/{breed}/images/random'
    # breed_collection = f'https://dog.ceo/api/breed/hound/images/random/{quantity_images}'
    def __init__(self, token, breed):
        super().__init__(token)
        self.breed = breed

    def check_breed_in_list(self):
        """
        check if the breeds are on the list
        """
        print('Проверяем наличие породы собаки в списке')
        responses = requests.get(self.url_list_all_breeds)
        if breed in responses.json()['message']:
            return True
        else:
            return False

    def create_yd_folder_for_dogs(self):
        """
        after check create folder for dogs in YD
        """
        if self.check_breed_in_list() == True:
            print('Создание папки для породы')
            responses = requests.put(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{self.breed}', headers=self.headers)
            # check if there is a path
            if str(responses.json()['error']) == 'DiskPathDoesntExistsError':
                self.create_yd_folder_for_group()
                return self.create_yd_folder_for_dogs()
            responses = requests.get(self.url_list_all_breeds)
            # check if there is a sub breeds in list and create folders for them
            if len(responses.json()['message'][breed]) != 0:
                print('Создание папок для подпород')
                for sb in responses.json()['message'][breed]:
                    requests.put(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{self.breed}%2F{sb}',
                                 headers=self.headers)
        else:
            print('Произошла ошибка с проверкой породы в create_yd_folder_for_dogs')

    def download_random_dog_in_yd(self):
        """

        """
        responses_dog = (requests.get(self.url_random_image_by_breed)).json()['message']
        for_name = responses_dog.split('/')
        responses = requests.post(
            f'{self.yd_url}{self.yd_url_2}?path={self.name_group}%2F{self.breed}%2F{self.breed+'_'+for_name[-1]}&url={responses_dog}',
            headers=self.headers)

    def download_collection_random_dog_in_yd(self):
        pass

# Example_cat = DownloadsImageCat(Yandex_token.yd_t, text)
# Example_cat.download_cat_for_yd()

Example_dogs = DownloadsImageDog(Yandex_token.yd_t, breed)
# print(Example_dogs.check_breed_in_list())
# Example_dogs.create_yd_folder_for_dogs()
Example_dogs.download_random_dog_in_yd()