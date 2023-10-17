import os

import requests

from service.Interceptor import Interceptor

url_repository = os.environ['URL_REPOSITORY'] + '/'


class HttpRepository(Interceptor):
    def __init__(self):
        super().__init__()

    def save(self, table, data, headers=None):
        try:
            response = requests.post(url_repository + table, headers=headers, json=data)
            if response.status_code < 200 or response.status_code > 299:
                raise Exception(f'Error inserting data: {response.text}')
        except Exception as e:
            raise e

    def update(self, table, keys=[], data={}, headers=None):
        params = {}
        for key in keys:
            params[key] = data[key]
        try:
            response = requests.post(url_repository + table, headers=headers, json=data, params=params)
            if response.status_code < 200 or response.status_code > 299:
                raise Exception(f'Error updating data: {response.text}')
        except Exception as e:
            raise e

    def delete_all(self, table, headers=None):
        self.delete(table, {}, headers)

    def delete(self, table, data={}, headers=None):
        params = {}
        for key in data.keys():
            params[key] = data[key]
        try:
            response = requests.post(url_repository + "delete/" + table, headers=headers, json=data, params=params)
            if response.status_code < 200 or response.status_code > 299:
                raise Exception(f'Error deleting data: {response.text}')
        except Exception as e:
            raise e

    def get_object(self, table, data={}, headers=None):
        params = {}
        for key in data.keys():
            params[key] = data[key]
        try:
            response = requests.get(url_repository + 'single/' + table, params=params, headers=headers)
            if response.status_code < 200 or response.status_code > 299:
                raise Exception(f'Error getting data: {response.text}')
            return response.json()
        except Exception as e:
            raise e

    def get_all_objects(self, table, headers=None):
        return self.get_objects(table, {}, headers)

    def get_objects(self, table, data={}, headers=None):
        params = {}
        for key in data.keys():
            params[key] = data[key]
        try:
            response = requests.get(url_repository + table, params=params, headers=headers)
            if response.status_code < 200 or response.status_code > 299:
                raise Exception(f'Error getting data: {response.text}')
            return response.json()
        except Exception as e:
            raise e

    def execute_select(self, select, headers=None):
        command = {
            'command': select
        }
        try:
            response = requests.post(url_repository + "command/select", headers=headers, json=command)
            if response.status_code < 200 or response.status_code > 299:
                raise Exception(f'Error getting data: {response.text}')
            return response.json()
        except Exception as e:
            raise e
