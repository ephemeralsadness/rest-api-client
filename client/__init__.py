from collections import namedtuple
from copy import deepcopy
import json
from os import path
import requests
from urllib.parse import urljoin
import shutil

TodoElement = namedtuple('TodoElement', ['task_id', 'name', 'done'])


class Client:

    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.data = {
            'username': username,
            'password': password
        }
        self.USER_ROUTE = '/user/'
        self.TODO_ROUTE = '/todo/'
        self.FILES_ROUTE = '/files/'

        requests.post(urljoin(url, self.USER_ROUTE), data=self.data)

    # returns a list of TodoElements
    def get_todo_list(self) -> list[TodoElement]:
        response = requests.get(urljoin(self.url, self.TODO_ROUTE), data=self.data)
        response.raise_for_status()

        content = json.loads(response.content)
        if not content['success']:
            raise Exception('No changes! Please make correct request next time!')

        return list(map(lambda d: TodoElement(**d), content['todo_list']))

    # returns True if user successfully logged into a system
    def add_todo(self, task_name: str) -> None:
        data = deepcopy(self.data)
        data['task_name'] = task_name
        response = requests.post(urljoin(self.url, self.TODO_ROUTE), data=data)
        response.raise_for_status()

        content = json.loads(response.content)
        if not content['success']:
            raise Exception('No changes! Please make correct request next time!')

    # returns True if user successfully logged into a system
    def change_todo(self, task_id: int, task_done: bool) -> None:
        data = deepcopy(self.data)
        data['task_done'] = json.dumps(task_done)
        response = requests.put(urljoin(self.url, path.join(self.TODO_ROUTE, str(task_id))), data=data)
        response.raise_for_status()

        content = json.loads(response.content)
        if not content['success']:
            raise Exception('No changes! Please make correct request next time!')

    # returns True if user successfully logged into a system
    def remove_todo(self, task_id: int) -> None:
        data = deepcopy(self.data)
        response = requests.delete(urljoin(self.url, path.join(self.TODO_ROUTE, str(task_id))), data=data)
        response.raise_for_status()

        content = json.loads(response.content)
        if not content['success']:
            raise Exception('No changes! Please make correct request next time!')

    def get_file(self, filename: str, filepath) -> None:
        data = deepcopy(self.data)
        response = requests.get(urljoin(self.url, path.join(self.FILES_ROUTE, filename)), data=data, stream=True)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

    def get_available_files(self) -> list[str]:
        data = deepcopy(self.data)
        response = requests.get(urljoin(self.url, self.FILES_ROUTE), data=data)

        content = json.loads(response.content)
        if not content['success']:
            raise Exception('You did never upload any files!')

        return content['files']

    def send_file(self, filepath: str) -> None:
        data = deepcopy(self.data)
        files = {'file': open(filepath, 'rb')}
        response = requests.post(urljoin(self.url, self.FILES_ROUTE), data=data, files=files)
        response.raise_for_status()

        content = json.loads(response.content)
        if not content['success']:
            raise Exception('There is an error with your file!')

    def remove_file(self, filename: str) -> None:
        data = deepcopy(self.data)
        response = requests.delete(urljoin(self.url, path.join(self.FILES_ROUTE, filename)), data=data)
        response.raise_for_status()

        content = json.loads(response.content)
        if not content['success']:
            raise Exception('No changes! Please make correct request next time!')

