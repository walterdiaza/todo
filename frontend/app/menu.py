import flet as ft

def menu(page: ft.Page):
    def categories_clicked(e):
        page.go('/categories')

    def task_clicked(e):
        page.go('/tasks')

    def logout_button_clicked(e):
        page.session.clear()
        page.go('/')



    categories_button = ft.Container(
                    content=ft.Text("Gestion de Categorias"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.GREEN_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    on_click=categories_clicked,
                )
    
    task_button = ft.Container(
                    content=ft.Text("Gestion de Tareas"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.ORANGE_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    on_click=task_clicked,
                )
    
    logout_button = ft.Container(
                    content=ft.Text("Cerrar Sesion"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.RED_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    on_click=logout_button_clicked,
                )
    
    return [ft.Row([categories_button, task_button, logout_button])]
    
