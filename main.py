import flet as ft;

class ChatMenu(ft.UserControl):
    def build():
        chatContainer = ft.Container(bgcolor = ft.colors.BLACK, width = "100%");
        col = ft.Column();
def main(page : ft.Page):
    page.add(ft.Container(bgcolor = ft.colors.BLACK, width = 100));
    
ft.app(target = main, view = ft.AppView.WEB_BROWSER);