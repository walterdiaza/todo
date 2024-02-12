import flet as ft
from flet import Page, View, AppBar,Text, ElevatedButton, colors
from login import login
from sign_up import sign_up
from menu import menu
from task import task_page, create_task_page
from categories import categories_page, create_category_page

def main(page: Page):
    
    page.title = "to-do App"

    print("Initial route: ", page.route)

    def route_changed(e):
        print("Route changed: ", e.route)
        #page.views.clear()

        if page.route == "/":
            page.views.append(
                View(
                    "/",
                [
                    AppBar(title=Text("Login"), bgcolor=colors.LIGHT_BLUE_700 ),
                ] + login(page)
            )
        )
        if page.route == "/sign-up":
            page.views.append(
                View(
                    "/sign-up",
                    [AppBar(title=Text("Registro de usuario"), bgcolor=colors.LIGHT_BLUE_700 ),]+
                    sign_up(page)
                )
            )
        if page.route == "/menu":
            page.views.append(
                View(
                    "/menu",
                    [AppBar(title=Text("menu"), bgcolor=colors.LIGHT_BLUE_700 ),]+
                    menu(page)
                )
            )
        if page.route == "/tasks":
            page.views.append(
                View(
                    "/tasks",
                    [AppBar(title=Text("Tareas"), bgcolor=colors.LIGHT_BLUE_700 ),]+
                    task_page(page)
                )
            )
        if page.route == "/create-task":
            page.views.append(
                View(
                    "/create-task",
                    [AppBar(title=Text("Crear Tarea"), bgcolor=colors.LIGHT_BLUE_700 ),]+
                    create_task_page(page)
                )
            )
        page.update()

        if page.route == "/categories":
            page.views.append(
                View(
                    "/categories",
                    [AppBar(title=Text("Categorias"), bgcolor=colors.LIGHT_BLUE_700 ),]+
                    categories_page(page)
                )
            )
        if page.route == "/create-category":
            page.views.append(
                View(
                    "/create-category",
                    [AppBar(title=Text("Crear Categoria"), bgcolor=colors.LIGHT_BLUE_700 ),]+
                    create_category_page(page)
                )
            )



    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)


    page.on_route_change = route_changed
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER, port=8080)


    