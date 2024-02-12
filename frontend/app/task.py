import flet as ft
from flet import Column
from connectors import backend 
from pop_up import PopUp

categories_cache = {}

def create_radio_button(page: ft.Page, category_id: int, category_name: str):
    return ft.Radio(label=category_name, value=category_id)

def get_categories(page : ft.Page):
    token = page.session.get('access_token')
    status, response = backend.get_categories(token)
    if status != 200:
        message = f"No se pudo obtener las categorias: {response.get('detail')}"
        pop_up = PopUp(page, message)
        pop_up.show()
    else:
        return {category.get('id'): category.get('name') for category in response}

class Task(ft.UserControl):
    def __init__(self, page: ft.Page, id:int, description: str, create_date: str, finish_date: str,  status: str, category_id: int ) -> None:
        super().__init__()
        self.page = page
        self.id = id
        self.description = description
        self.create_date = create_date
        self.finish_date = finish_date
        self.status = status
        self.category_id = category_id

    def delete_task(self,e):
        token = self.page.session.get('access_token')
        status, response = backend.delete_task(token,self.id)
        if status != 200:
            message = f"No se pudo eliminar la tarea: {response.get('detail')}"
            pop_up = PopUp(self.page, message)
            pop_up.show()
        self.page.go('/menu')
        self.page.update()
    def build(self):
        category_name = categories_cache.get(self.category_id)
        if category_name is None:
            category_name = get_categories(self.page).get(self.category_id)
            categories_cache[self.category_id] = category_name
        return ft.Row([
            ft.Text(f"description: {self.description}, category: {category_name}, status: {self.status}, create_date: {self.create_date}, finish_date: {self.finish_date}"),
            ft.IconButton(ft.icons.DELETE_FOREVER_ROUNDED, on_click=self.delete_task)
        ])
    
def task_page(page: ft.Page):
    def routing_create_task_page(e):
        page.go('/create-task')
    
    token = page.session.get('access_token')
    tasks = Column()
    if token is None:
        page.go('/')
        return [tasks]
    task_status, tasks_request = backend.get_tasks_by_user(token)
    create_task_button = ft.ElevatedButton(text="Crear tarea", on_click=routing_create_task_page)
    if task_status != 200:
        message = f"No se pudo obtener las tareas: {tasks_request.get('detail')}"
        pop_up = PopUp(page, message)
        pop_up.show()
        page.go('/')
        return [create_task_button,tasks]
    task_list =tasks_request
    

    for task in task_list:
        tasks.controls.append(Task(page,task['id'], task["description"], task["create_date"], task["finish_date"], task["status"], task["category_id"]))
    page.update()
    return [create_task_button, tasks]

def create_task_page(page: ft.Page):
    def create_clicked(e):
        token = page.session.get('access_token')
        status, response = backend.create_task(token, description.value, finish_day.value, categorie_groups.value)
        if status != 201:
            message = f"No se pudo crear la tarea: {response.get('detail')}"
            pop_up = PopUp(page, message)
            pop_up.show()
        else:
            page.go('/tasks')
        page.update()

    description = ft.TextField(hint_text="descripcion tarea", autofocus=True)
    finish_day = ft.TextField(hint_text="finish_day")
    categories = get_categories(page)
    categories_list = [create_radio_button(page, item[0], item[1]) for item in list(categories.items())]
    categorie_groups =  ft.RadioGroup(
        content=ft.Column(categories_list)
    )
    create_button = ft.ElevatedButton(text="Registrarse", on_click=create_clicked)
    token = page.session.get('access_token')
    if token is None:
        page.go('/')
        return []
    categories = get_categories(page)
    categories_list = [create_radio_button(page, item[0], item[1]) for item in list(categories.items())]
    categorie_groups =  ft.RadioGroup(
        content=ft.Column(categories_list)
    )
    return [description, finish_day, categorie_groups, create_button]




