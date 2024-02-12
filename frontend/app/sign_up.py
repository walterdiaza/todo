import flet as ft
from connectors import backend
import time
from pop_up import PopUp



def sign_up(page: ft.Page):
    def create_user_clicked(e):
        status, response = backend.create_user(username.value, password.value)
        if status != 201:
            message = f"No se pudo crear el usuario: {response.get('detail')}"
            pop_up = PopUp(page, message)
            pop_up.show()
        else:
            message = f"Usuario {username.value} creado exitosamente"
            pop_up = PopUp(page, message)
            pop_up.show()
            time.sleep(5000)
            page.go('/')
        page.update()
    header = ft.Text("Crear usuario")
    username = ft.TextField(hint_text="Usuario")
    password = ft.TextField(hint_text="Contrasena", password=True)
    create_user_button = ft.ElevatedButton(text="Crear usuario", on_click=create_user_clicked)
    
    return [username, password, create_user_button]


