import backend
from styles.accueilStyleSheet import *


class Accueil(ft.UserControl):
    def __init__(self, page):
        super(Accueil, self).__init__()
        self.page = page
        self.logo = ft.Image(src="assets/logo.jpg")
        self.login = ft.TextField(**loginstyle)
        self.password = ft.TextField(**passwordstyle, on_change=self.check_connexion)
        self.check_password_icon = ft.Icon(**check_password_icon_style)
        self.button = ft.ElevatedButton(**button_connect_style, on_click=self.connect)
        self.alert = ft.AlertDialog(
            title=ft.Text("Erreur", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.icons.DANGEROUS_OUTLINED, size=26),
                    ft.Text("Login et/ou mot de passe incorrect(s)"),
                ]
            ),
            actions=[
                ft.FilledTonalButton(text="Close", on_click=self.close_alert)
            ]
        )
        self.user_news = ft.Container(
            **user_news_style,
            expand=True,
            height=700,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True,
                height=700,
                controls=[
                    ft.Text("Enter user account", size=20, style=ft.TextThemeStyle.LABEL_MEDIUM),
                    ft.Divider(height=2, color="transparent"),
                    self.login,
                    self.password,
                    ft.Divider(height=5, color="transparent"),
                    self.button,
                    self.check_password_icon
                ]
            )
        )

    def close_alert(self, e):
        self.alert.open = False
        self.alert.update()

    # when we press the button to connect
    def connect(self, e):
        if self.login.value == "" or self.password.value == "":
            self.alert.open = True
            self.alert.update()
        else:
            if (self.login.value, self.password.value) in backend.all_users():
                self.page.go('/stocks')
            else:
                self.alert.open = True
                self.alert.update()

    def check_connexion(self, e):
        if backend.find_user_password(self.login.value) == self.password.value:
            self.check_password_icon.scale = 1
        else:
            self.check_password_icon.scale = 0
            self.check_password_icon.animate_scale = ft.animation.Animation(600, ft.AnimationCurve.BOUNCE_IN)
        self.check_password_icon.update()

    def build(self):
        return ft.Container(
            padding=ft.padding.only(top=30),
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                height=700,
                controls=[
                    self.logo,
                    ft.Divider(height=10, color="transparent"),
                    self.user_news,
                    self.alert
                ]
            )
        )
