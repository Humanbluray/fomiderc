import flet as ft

name_bar_style: dict = dict(
    prefix_icon=ft.icons.SEARCH,
    width=250,
    label="Désignation",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium"),
    dense=True,
    border_radius=0,
    text_size=12,
    content_padding=12,
    capitalization=ft.TextCapitalization.CHARACTERS,
)
type_bar_style: dict = dict(
    prefix_icon=ft.icons.SEARCH,
    width=150,
    hint_text="type...",
    hint_style=ft.TextStyle(size=14, italic=True),
    capitalization=ft.TextCapitalization.CHARACTERS,
    dense=True,
    border_radius=6,
    text_size=14,
    content_padding=12
)
menu_container_style: dict = dict(
    # expand=True,
    padding=ft.padding.only(left=5, right=5, top=2, bottom=2),
    border=ft.border.all(1, color="#ebebeb"),
    border_radius=ft.border_radius.only(top_left=10, top_right=10)
)
menu_style: dict = dict(
    # expand=True,
    padding=ft.padding.only(left=5, right=5, top=2, bottom=2),
    border=ft.border.all(1, color="#ebebeb"),
    border_radius=ft.border_radius.only(top_left=10, top_right=10)
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
title_container_style: dict = dict(
    border=ft.border.all(1, color="#ebebeb"),
    padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
    border_radius=8,
)
table_stocks_style: dict = dict(
    columns=[
        ft.DataColumn(ft.Text('reference', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('designation', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('nature', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('qté', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('prix', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('unité', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
    ],
    rows=[]
)
table_details_style: dict = dict(
    columns=[
        ft.DataColumn(ft.Text('reference', size=14, style=ft.TextThemeStyle.LABEL_SMALL)),
        ft.DataColumn(ft.Text('designation', size=14, style=ft.TextThemeStyle.LABEL_SMALL)),
        ft.DataColumn(ft.Text('nature', size=14, style=ft.TextThemeStyle.LABEL_SMALL)),
        ft.DataColumn(ft.Text('qté', size=14, style=ft.TextThemeStyle.LABEL_SMALL)),
        ft.DataColumn(ft.Text('prix', size=14, style=ft.TextThemeStyle.LABEL_SMALL)),
        ft.DataColumn(ft.Text('unité', size=14, style=ft.TextThemeStyle.LABEL_SMALL)),
    ],
    rows=[]
)
new_ref_style: dict = dict(
    width=300,
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=0,
    text_size=14,
    content_padding=12
)
edit_ref_style: dict = dict(
    width=150,
    height=50,
    label="reference",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=10),
    dense=True,
    border_radius=0,
    text_size=14,
    content_padding=12
)
edit_des_style: dict = dict(
    width=300,
    height=50,
    label="designation",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    multiline=True,
    max_lines=3,
    capitalization=ft.TextCapitalization.CHARACTERS,
    text_style=ft.TextStyle(font_family="Poppins Medium", size=10),
    dense=True,
    border_radius=0,
    text_size=14,
    content_padding=12
)
edit_qte_style_2: dict = dict(
    width=100,
    height=50,
    label="quantite",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    multiline=True,
    max_lines=3,
    text_style=ft.TextStyle(font_family="Poppins Medium", size=10),
    dense=True,
    border_radius=0,
    text_size=14,
    content_padding=12
)
edit_unit_style_2: dict = dict(
    width=100,
    height=50,
    label="unite",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    multiline=True,
    max_lines=3,
    text_style=ft.TextStyle(font_family="Poppins Medium", size=10),
    dense=True,
    border_radius=0,
    text_size=14,
    content_padding=12
)
edit_nat_style_2: dict = dict(
    width=200,
    height=50,
    label="nature",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    multiline=True,
    max_lines=3,
    text_style=ft.TextStyle(font_family="Poppins Medium", size=10),
    dense=True,
    border_radius=0,
    text_size=14,
    content_padding=12
)
edit_qte_style: dict = dict(
    width=80,
    height=50,
    label_style=ft.TextStyle(size=10, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=10),
    dense=True,
    border_radius=0,
    text_size=14,
    content_padding=12,
    label="qté",
)
edit_prix_style: dict = dict(
    width=100,
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=10),
    dense=True,
    border_radius=0,
    text_size=14,
    content_padding=12,
    label="prix",
)
edit_nat_style: dict = dict(
    width=150,
    label="nature",
    height=40, dense=True,
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color=ft.colors.BLACK87),
    options=[ft.dropdown.Option("stock"), ft.dropdown.Option("non-stock")]
)
edit_unit_style: dict = dict(
    width=120,
    label="unité",
    height=40, dense=True,
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color=ft.colors.BLACK87),
    options=[
        ft.dropdown.Option("u"),
        ft.dropdown.Option("ml"),
        ft.dropdown.Option("kg"),
    ]
)
table_histo_style: dict = dict(
    columns=[
        ft.DataColumn(ft.Text('reference', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('date', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('mvt', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('N°', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('stock av.', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('qté', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('stock ap.', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
    ],
    rows=[]
)
achat_ref_style: dict = dict(
    width=200,
    height=40,
    label="reference",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium", color=ft.colors.BLACK87),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=14, color=ft.colors.BLACK87),
    dense=True,
    border_radius=0,
    content_padding=12
)
achat_des_style: dict = dict(
    width=300,
    height=50,
    label="designation",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=14),
    dense=True,
    border_radius=0,
    capitalization=ft.TextCapitalization.CHARACTERS,
    content_padding=12
)
achat_qte_style: dict = dict(
    width=80,
    height=50,
    label="qte",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=14),
    dense=True,
    border_radius=0,
    capitalization=ft.TextCapitalization.CHARACTERS,
    content_padding=12,
    input_filter=ft.NumbersOnlyInputFilter(),
)
achat_stock_style: dict = dict(
    width=120,
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=14),
    dense=True,
    border_radius=0,
    capitalization=ft.TextCapitalization.CHARACTERS,
    content_padding=12,
    input_filter=ft.NumbersOnlyInputFilter(),
)
achat_prix_style: dict = dict(
    width=120,
    height=50,
    label="prix",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=14),
    dense=True,
    border_radius=0,
    capitalization=ft.TextCapitalization.CHARACTERS,
    input_filter=ft.NumbersOnlyInputFilter(),
    content_padding=12
)
achat_com_style: dict = dict(
    width=300,
    height=100,
    multiline=True,
    max_lines=3,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=14),
    dense=True,
    border_radius=0,
    capitalization=ft.TextCapitalization.CHARACTERS,
    content_padding=12
)