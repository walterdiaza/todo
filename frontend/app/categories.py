import flet as ft
from flet import Column
from connectors import backend
from pop_up import PopUp


def categories(page: ft.Page):
    token = page.session.get('access_token')
    status, response = backend.get_categories(token)
    if status != 200:
        message = f"No se pudo obtener las categorias: {response.get('detail')}"
        pop_up = PopUp(page, message)
        pop_up.show()
    else:
        return response
    
class Categories(ft.UserControl):
    def __init__(self, page: ft.Page, id: int, name: str, description: str) -> None:
        super().__init__()
        self.page = page
        self.id = id
        self.name = name
        self.description = description

    def delete_category(self,e):
        token = self.page.session.get('access_token')
        status, response = backend.delete_category(token,self.id)
        if status != 200:
            message = f"No se pudo eliminar la categoria: {response.get('detail')}"
            pop_up = PopUp(self.page, message)
            pop_up.show()
        self.page.go('/menu')
        self.page.update()

    def build(self):
        return ft.Row([
            ft.Text(f"name: {self.name}, description: {self.description}"),
            ft.IconButton(ft.icons.DELETE_FOREVER_ROUNDED, on_click=self.delete_category)
        ])
    
def categories_page(page: ft.Page):
    def routing_create_category_page(e):
        page.go('/create-category')
    token = page.session.get('access_token')
    categories = Column()
    if token is None:
        page.go('/')
        return [categories]
    category_status, categories_request = backend.get_categories(token)
    if category_status != 200:
        message = f"No se pudo obtener las categorias: {categories_request.get('detail')}"
        pop_up = PopUp(page, message)
        pop_up.show()
    else:
        for category in categories_request:
            categories.controls.append(Categories(page, category.get('id'), category.get('name'), category.get('description')))
    return [ft.ElevatedButton(text="Crear categoria", on_click=routing_create_category_page), categories]


def create_category_page(page: ft.Page):
    def create_category_clicked(e):
        token = page.session.get('access_token')
        status, response = backend.create_category(token, name.value, description.value)
        if status != 201:
            message = f"No se pudo crear la categoria: {response.get('detail')}"
            pop_up = PopUp(page, message)
            pop_up.show()
        else:
            message = f"Categoria {name.value} creada exitosamente"
            pop_up = PopUp(page, message)
            pop_up.show()
            page.go('/categories')
        page.update()
    
    name = ft.TextField(hint_text="category_name")
    description = ft.TextField(hint_text="description")
    create_category_button = ft.ElevatedButton(text="Crear categoria", on_click=create_category_clicked)
    return [name, description, create_category_button]
    