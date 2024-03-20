import flet as ft

name_bar_style: dict = dict(
    prefix_icon=ft.icons.SEARCH,
    width=250,
    label="Désignation",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium"),
    dense=True,
    border_radius=6,
    text_size=12,
    content_padding=12,
)
menu_container_style: dict = dict(
    padding=ft.padding.only(left=8, right=8, top=8, bottom=8),
    border=ft.border.all(1, color="#ebebeb"),
    border_radius=ft.border_radius.all(10)
)
table_container_style: dict = dict(
    # expand=True,
    padding=ft.padding.only(left=5, right=5, top=2, bottom=2),
    border=ft.border.all(1, color="#ebebeb"),
    border_radius=10
)
filter_container_style: dict = dict(
    # expand=True,
    padding=ft.padding.only(left=10, right=10, top=20, bottom=20),
    border=ft.border.all(1, color="#ebebeb"),
    border_radius=8,
)
filter_name_style: dict = dict(
    width=250,
    label="nom fournisseur",
    height=40, dense=True,
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color=ft.colors.BLACK87),
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium", color=ft.colors.BLACK87),
)
table_commande_style: dict = dict(
    columns=[
        ft.DataColumn(ft.Text('N° Commande', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('date', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('fournisseur', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('Montant', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('statut', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
    ],
    rows=[]
)
table_details_style: dict = dict(
    columns=[
        ft.DataColumn(ft.Text('reference', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('designation', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('qté', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('prix', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
    ],
    rows=[]
)
infos_style: dict = dict(
    width=200,
    multiline=True,
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
new_init_style: dict = dict(
    width=200,
    multiline=True,
    height=70,
    max_length=3,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
new_tel_style: dict = dict(
    width=200,
    multiline=True,
    height=70,
    max_length=9,
    prefix_text="+237 ",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
new_mail_style: dict = dict(
    width=200,
    multiline=True,
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    border_radius=6,
    text_size=14,
    content_padding=12
)