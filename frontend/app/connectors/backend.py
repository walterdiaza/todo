import requests as r
from logging import getLogger

log = getLogger(__name__)

URL_PREFIX = 'http://app:8000'

def login(username, password):
    endpoint = URL_PREFIX + '/usuarios/iniciar-sesion'
    response = r.post(endpoint, json={'user_name': username, 'password': password})
    return response.status_code, response.json()

def create_user(username, password):
    endpoint = URL_PREFIX + '/usuarios'
    response = r.post(endpoint, json={'user_name': username, 'password': password})
    return response.status_code, response.json()

def get_tasks_by_user(access_token):
    endpoint = URL_PREFIX + '/tareas/usuario'
    response = r.get(endpoint, headers={'X-token': access_token})
    return response.status_code, response.json()

def create_task(access_token, description, finish_date, category_id):
    endpoint = URL_PREFIX + '/tareas'
    response = r.post(endpoint, headers={'X-token': access_token}, json={'description': description,
                                                                        'category_id': category_id,
                                                                        'finish_date': finish_date})
    return response.status_code, response.json()

def delete_task(access_token, task_id):
    endpoint = URL_PREFIX + f'/tareas/{task_id}'
    response = r.delete(endpoint, headers={'X-token': access_token})
    return response.status_code, response.json()

def get_categories(access_token):
    endpoint = URL_PREFIX + '/categorias'
    response = r.get(endpoint, headers={'X-token': access_token})
    return response.status_code, response.json()

def delete_category(access_token, category_id):
    endpoint = URL_PREFIX + f'/categorias/{category_id}'
    response = r.delete(endpoint, headers={'X-token': access_token})
    return response.status_code, response.json()

def create_category(access_token, name, description):
    endpoint = URL_PREFIX + '/categorias'
    response = r.post(endpoint, headers={'X-token': access_token}, json={'name': name, 'description': description})
    return response.status_code, response.json()