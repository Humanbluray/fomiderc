import flet as ft
from vues import view_handler


def main(page: ft.Page):
    page.window_width = 1330
    page.window_height = 830
    page.fonts = {
        "Poppins Regular": "fonts/Poppins-Regular.ttf",
        "Poppins Bold": "fonst/Poppins-Bold.ttf",
        "Poppins Black": "fonts/Poppins-Black.ttf",
        "Poppins Italic": "fonts/Poppins-Italic.ttf",
        "Poppins Medium": "fonts/Poppins-Medium.ttf",
        "Poppins ExtraBold": "fonts/Poppins-ExtraBold.ttf"
    }

    def route_change(route):
        page.views.clear()
        page.views.append(view_handler(page)[page.route])
        page.update()

    page.on_route_change = route_change
    page.go('/')


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")

