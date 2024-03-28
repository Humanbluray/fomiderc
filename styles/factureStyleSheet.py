import flet as ft

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
table_container_style: dict = dict(
    # expand=True,
    padding=ft.padding.only(left=5, right=5, top=2, bottom=2),
    border=ft.border.all(1, color="#ebebeb"),
    border_radius=8,
)
standard_ct_style: dict = dict(
    # expand=True,
    padding=ft.padding.only(left=10, right=10, top=10, bottom=10),
    border=ft.border.all(1, color="#ebebeb"),
    border_radius=8,
)
filter_name_style: dict = dict(
    width=250,
    label="Numero facture",
    height=40, dense=True,
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color=ft.colors.BLACK87),
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium", color=ft.colors.BLACK87),
)
standard_tf_style: dict = dict(
    width=300,
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
remise_tf_style: dict = dict(
    width=100,
    height=50,
    suffix_text="%",
    label="remise",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
lettres_tf_style: dict = dict(
    width=600,
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    label="Montant en lettres",
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
date_tf_style: dict = dict(
    width=130,
    height=50,
    label="date",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
statut_tf_style: dict = dict(
    width=200,
    height=50,
    label="BC client",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
devis_tf_style: dict = dict(
    width=200,
    height=50,
    label="N° Devis",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
montant_tf_style: dict = dict(
    width=180,
    height=50,
    label="montant",
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
table_details_devis_style: dict = dict(
    columns=[
        ft.DataColumn(ft.Text('reference', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('designation', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('qté', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('prix', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('total', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
    ],
    rows=[]
)
devis_num_style: dict = dict(
    width=180,
    label="N° devis",
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
client_name_style: dict = dict(
    width=350,
    label="selection client",
    height=40, dense=True,
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color=ft.colors.BLACK87),
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium", color=ft.colors.BLACK87),
)
new_remise_style: dict = dict(
    width=70,
    label="Remise",
    suffix_text="%",
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
new_ref_style: dict = dict(
    width=200,
    label="reference",
    height=40, dense=True,
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color=ft.colors.BLACK87),
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium", color=ft.colors.BLACK87),
)
new_qte_style: dict = dict(
    width=70,
    label="Qté",
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
new_prix_style: dict = dict(
    width=150,
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
mt_lettres_style: dict = dict(
    width=600,
    label="montant en lettres",
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
table_new_devis_style: dict = dict(
    columns=[
        ft.DataColumn(ft.Text('reference', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('designation', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('qté', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('prix', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
    ],
    rows=[]
)
bc_tf_style: dict = dict(
    width=300,
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
table_edit_devis_style: dict = dict(
    columns=[
        ft.DataColumn(ft.Text('id', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('reference', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('designation', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('qté', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('prix', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
    ],
    rows=[]
)
new_payment_style: dict = dict(
    width=200,
    height=50,
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium"),
    text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
    dense=True,
    capitalization=ft.TextCapitalization.CHARACTERS,
    border_radius=6,
    text_size=14,
    content_padding=12
)
payment_mode_style: dict = dict(
    width=200,
    label="Mode paiement",
    height=40, dense=True,
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color=ft.colors.BLACK87),
    label_style=ft.TextStyle(size=11, font_family="Poppins Medium", color=ft.colors.BLACK87),
)
table_paiements_style: dict = dict(
    columns=[
        ft.DataColumn(ft.Text('montant', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('type', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
        ft.DataColumn(ft.Text('date', size=12, style=ft.TextStyle(font_family="Poppins Black"))),
    ],
    rows=[]
)