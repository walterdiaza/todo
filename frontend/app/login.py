import flet as ft
from connectors import backend
from pop_up import PopUp

def login(page: ft.Page):

    def login_clicked(e):
        status, response = backend.login(username.value, password.value)
        if status != 200:
            message = f"No se pudo iniciar sesion: {response.get('detail')}"
            pop_up = PopUp(page, message)
            pop_up.show()
        else:
            page.session.set('access_token', response.get('access_token'))
            page.session.set('user_name', username.value)
            page.go('/menu')
        page.update()
    
    def sign_up_clicked(e):
        page.go('/sign-up')
    
    username = ft.TextField(hint_text="Usuario", autofocus=True)
    password = ft.TextField(hint_text="Contrasena", password=True)
    login_button = ft.ElevatedButton(text="Ingresar", on_click=login_clicked)
    sign_up_button = ft.ElevatedButton(text="Registrarse", on_click=sign_up_clicked)
    
    return [username, password, ft.Row([login_button, sign_up_button])]






# def login(page: ft.Page):
    
#     def page_login(error = None):
#         page.clean()
#         ft.AppBar(title=ft.Text("Iniciar sesion", color=ft.colors.RED), bgcolor=ft.colors.RED)
#         if error:
#             page.add(ft.Text(error))
#         page.add(username, password, ft.Row([login_button, sign_up_button]))
#         page.update()

#     def login_clicked(e):
#         status, response = backend.login(username.value, password.value)
#         if status != 200:
#             page_login(f"No se pudo iniciar sesion: {response.get('detail')}")
#         else:
#             page.session.set('access_token', response.get('access_token'))
#         page.update()
    
#     def sign_up_clicked(e):
#         sign_up_page.page(page)

#         page.update()

#     username = ft.TextField(hint_text="Usuario", autofocus=True)
#     password = ft.TextField(hint_text="Contrasena", password=True)
#     login_button = ft.ElevatedButton(text="Ingresar", on_click=login_clicked)
#     sign_up_button = ft.ElevatedButton(text="Registrarse", on_click=sign_up_clicked)

#     page.appbar = ft.CupertinoAppBar(
#         leading=ft.Icon(ft.icons.ARROW_BACK),
#         bgcolor=ft.colors.LIGHT_BLUE_700,
#         trailing=ft.Icon(ft.icons.MENU),
#       middle=ft.Text("CupertinoAppBar Example"),
#     )


#     page_login()
# ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)