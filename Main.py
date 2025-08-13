import requests
import json
import os
import Yandex_token
from tqdm import tqdm


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
            pass
        # we gain need data and make dictionary
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

    def download_cat_in_yd(self):
        """
        load cat image in disk and make report
        """
        responses = requests.get(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{text}', headers=self.headers)
        print('Загружаем файл с котиками на Яндекс диск')
        # check if file name exist in yandex disk
        if str(responses) != '<Response [200]>':
            responses = requests.post(f'{self.yd_url}{self.yd_url_2}?path={self.name_group}%2F{self.text}&url={self.cat_url}{self.text}', headers=self.headers)
            try:
                # check if folder exists on yandex disk
                if str(responses.json()['error']) == 'DiskPathDoesntExistsError':
                    self.create_yd_folder_for_group()
                    return self.download_cat_in_yd()
            except KeyError:
                pass
        else:
            print('Файл с котиками с таким именем уже имеется на Яндекс диске')
            return
        self.cat_report()
        print('Файл с котиками загружен на Яндекс диск')


# inherited class for dogs
class DownloadsImageDog(DownloadsImage):
    url_list_all_breeds = 'https://dog.ceo/api/breeds/list/all'
    def __init__(self, token, breed):
        super().__init__(token)
        self.breed = breed
        self._for_name = 0
        self._sub_breed = 0
        self._sb = 0
        self._url_random_image_by_breed = f'https://dog.ceo/api/breed/{self.breed}/images/random'
        self._url_random_image_by_sub_breed = f'https://dog.ceo/api/breed/{self.breed}/'

    def check_breed_in_list(self):
        """
        check if the breeds are on the list
        """
        responses = requests.get(self.url_list_all_breeds)
        if breed in responses.json()['message']:
            return True
        else:
            return False

    def check_sub_breed_in_list(self):
        """
        check if the sub-breeds are on the list
        """
        responses = requests.get(self.url_list_all_breeds)
        # check if there is a sub breeds in list and create folders for them
        if len(responses.json()['message'][breed]) != 0:
            return True
        else:
            return False

    def create_yd_folder_for_dogs(self):
        """
        after check create folder for dogs in YD
        """
        if self.check_breed_in_list():
            print('Создание папки для породы')
            responses = requests.put(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{self.breed}', headers=self.headers)
            # check if there is a path
            try:
                if str(responses.json()['error']) == 'DiskPathDoesntExistsError':
                    print(f'Не найдена папка с {self.name_group}')
                    self.create_yd_folder_for_group()
                    return self.create_yd_folder_for_dogs()
            except KeyError:
                pass
            if self.check_sub_breed_in_list():
                print('Создание папок для подпород')
                responses = requests.get(self.url_list_all_breeds)
                for sb in tqdm(responses.json()['message'][breed]): # make progress bar
                    requests.put(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{self.breed}%2F{sb}',
                                 headers=self.headers)
        else:
            print('Указанной породы нет в списке')

    def dog_breed_report(self):
        """
        report is making of file in yandex disk
        it will work only after method download_random_breed_in_yd, him need self.sb and self.for_name
        """
        # we do the request until we get response
        while str(requests.get(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{self.breed}%2F{self.breed + '_' + self.for_name[-1]}',
            headers=self.headers)) != '<Response [200]>':
            pass
        # we gain need data and make dictionary
        responses = requests.get(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{self.breed}%2F{self.breed + '_' + self.for_name[-1]}',
            headers=self.headers)
        self.dog_create_json(responses)

    def dog_sub_breed_report(self):
        """
        report is making of file in yandex disk
        it will work only after method download_random_sub_breed_in_yd, him need self.sb and self.for_name
        """
        # we do the request until we get response
        while str(requests.get(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{self.breed}%2F{self.sb}%2F{self.sb + '_' + self.for_name[-1]}',
                    headers=self.headers)) != '<Response [200]>':
            pass
        responses = requests.get(
                f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{self.breed}%2F{self.sb}%2F{self.sb + '_' + self.for_name[-1]}',
                headers=self.headers)
        self.dog_create_json(responses)

    def dog_create_json(self, responses):
        """
         write data to file, it only with dog_breed_report and dog_sub_breed_report
        """
        data = {
            'name': responses.json()['name'],
            'created': responses.json()['created'],
            'size': responses.json()['size']
        }
        # check a file .json in repository, if he is then refresh file, if he is not then create file
        if str(os.path.exists('dog_report.json')) == 'True':
            with open("dog_report.json", "r") as file:
                list_data = json.load(file)
            list_data.append(data)
            with open(f'dog_report.json', 'w', encoding='utf-8') as file:
                json.dump(list_data, file, indent=4, ensure_ascii=False)
        else:
            with open(f'dog_report.json', 'w', encoding='utf-8') as file:
                list_data = []
                list_data.append(data)
                json.dump(list_data, file, indent=4, ensure_ascii=False)

    def download_random_breed_in_yd(self):
        """
        load a random gog image in disk
        """
        if self.check_breed_in_list():
            # create folder for dogs
            self.create_yd_folder_for_dogs()
            # start download image
            print('Загружаем фото с выбранной породой')
            responses_dog = (requests.get(self.url_random_image_by_breed)).json()['message'] # get reference for loading
            self.for_name = responses_dog.split('/') # highlight a piece for name
            responses = requests.get(f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{self.breed}%2F{self.breed+'_'+self.for_name[-1]}',
                    headers=self.headers) # check file name exist in yandex disk
            # check if file name exist in yandex disk
            if str(responses) != '<Response [200]>':
                responses = requests.post(
                    f'{self.yd_url}{self.yd_url_2}?path={self.name_group}%2F{self.breed}%2F{self.breed+'_'+self.for_name[-1]}&url={responses_dog}',
                    headers=self.headers)
                # make report
                self.dog_breed_report()
            else:
                pass
            self.download_random_sub_breed_in_yd() # start loading sub-breed
        else:
            print('Указанной породы нет в списке')

    def download_random_sub_breed_in_yd(self):
        """
        load for sub-breed
        it will work only after method download_random_breed_in_yd
        """
        if self.check_sub_breed_in_list():
            print('Загружаем фото с подпородами')
            responses = requests.get(self.url_list_all_breeds)
            #
            self.sub_breed = responses.json()['message'][self.breed]
            # do not create a folder, this is not an independent method
            # self.create_yd_folder_for_dogs()
            for sb in tqdm(self.sub_breed): # make progress bar
                self.sb = sb
                responses_dog = (requests.get(f'{self.url_random_image_by_sub_breed}{self.sb}/images/random')).json()[
                    'message']  # get reference for loading
                self.for_name = responses_dog.split('/')  # highlight a piece for name
                responses = requests.get(
                    f'{self.yd_url}{self.yd_url_1}?path={self.name_group}%2F{self.breed}%2F{self.sb}%2F{self.sb + '_' + self.for_name[-1]}',
                    headers=self.headers)  # check file name exist in yandex disk
                # check if file name exist in yandex disk
                if str(responses) != '<Response [200]>':
                    responses = requests.post(
                        f'{self.yd_url}{self.yd_url_2}?path={self.name_group}%2F{self.breed}%2F{self.sb}%2F{self.sb + '_' + self.for_name[-1]}&url={responses_dog}',
                        headers=self.headers)
                    # make report
                    self.dog_sub_breed_report()
                else:
                    print('Файл с собачками с таким именем уже имеется на Яндекс диске')
        else:
            pass


# spot for choose image CATS, write your text in variable 'text'
text = 'hello'

# spot for choose image DOGS, write your text in variable 'breed'
breed = 'terrier'
# without sub-breed - african, havanese
# with sub-breed - hound (7 files), terrier (23 files)

# check work
# Example_cat = DownloadsImageCat(Yandex_token.yd_t, text)
# Example_cat.download_cat_in_yd()
# Example_dogs = DownloadsImageDog(Yandex_token.yd_t, breed)
# Example_dogs.download_random_breed_in_yd()

# СДЕЛАТЬ README, ПРОВЕРИТЬ ДЛИННУ СТРОК, ПРИЧЕСАТЬ КОД ПО PEP8
# ПЕРЕПРОВЕРИТЬ ЗАДАНИЕ