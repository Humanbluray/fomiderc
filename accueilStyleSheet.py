import flet as ft

# Accueil page styles_____________________________________________
loginstyle: dict = dict(
    prefix_icon=ft.icons.PERSON_OUTLINED,
    width=200,
    height=50,
    label="username",
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    # dense=True,
    border_radius=5,
    text_size=14,
    content_padding=12
)
passwordstyle: dict = dict(
    prefix_icon=ft.icons.LOCK_OUTLINE_ROUNDED,
    width=200,
    height=50,
    label="password",
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    # dense=True,
    border_radius=5,
    text_size=14,
    content_padding=12,
    can_reveal_password=True,
    password=True
)
user_news_style: dict = dict(
    # bgcolor=ft.colors.GREY_50,
    width=300,
    padding=ft.padding.only(left=25, right=25, top=25, bottom=50),
    border=ft.border.all(1, color="#ebebeb"),
    border_radius=40,
)
check_password_icon_style: dict = dict(
    name=ft.icons.CHECK_CIRCLE_ROUNDED,
    color="green",
    size=150,
    scale=ft.transform.Scale(scale=0),
    animate_scale=ft.animation.Animation(600, ft.AnimationCurve.BOUNCE_OUT)
)
button_connect_style: dict = dict(
    height=50,
    width=200,
    color="white",
    bgcolor="#3410B9",
    elevation=10,
)
