import flet as ft

class PopUp():
    def __init__(self, page: ft.Page, message: str) -> None:
        self.dlg = ft.AlertDialog(
            title=ft.Text(message), on_dismiss=lambda e: print("Dialog dismissed!")
        )
        self.page = page

    def show(self):
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()


    


    
    
