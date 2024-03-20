from tkinter.filedialog import asksaveasfilename
import backend
from styles.devisStyleSheet import *
from others.useful_fonctions import *
from datetime import date
import os
# import openpyxl
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


class Devis(ft.UserControl):
    def __init__(self, page):
        super(Devis, self).__init__()

        # Menu ________________________________________________________________________
        self.page = page
        self.page.auto_scroll = True
        self.rail = ft.NavigationRail(
            selected_index=5,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            # min_extended_width=400,
            leading=ft.Text("MENU", style=ft.TextStyle(size=20, font_family="Poppins Bold", decoration=ft.TextDecoration.UNDERLINE)),
            group_alignment=-0.7,
            destinations=[
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.HOME_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.HOME),
                    label_content=ft.Text("Stocks", style=ft.TextStyle(font_family="Poppins Medium"))
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.GROUP_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.GROUP),
                    label_content=ft.Text("Clients", style=ft.TextStyle(font_family="Poppins Medium")),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.GROUPS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.GROUPS),
                    label_content=ft.Text("Fournisseurs", style=ft.TextStyle(font_family="Poppins Medium")),
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label_content=ft.Text("Commandes", style=ft.TextStyle(font_family="Poppins Medium")),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.MONETIZATION_ON_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.MONETIZATION_ON),
                    label_content=ft.Text("Devis", style=ft.TextStyle(font_family="Poppins Medium")),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PAYMENTS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.PAYMENTS),
                    label_content=ft.Text("Factures", style=ft.TextStyle(font_family="Poppins Medium")),
                )
            ],
            on_change=self.switch_page
        )
        self.title_page = ft.Text("DEVIS", style=ft.TextStyle(size=26, font_family="Poppins ExtraBold"))
        # filtres container ____________________________________________________________________
        self.filtre = ft.Text("Filtre", style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.search_devis = ft.Dropdown(**filter_name_style, on_change=self.on_change_devis)
        self.client_id = ft.Text(visible=False)
        self.actions = ft.Text("actions", style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.add = ft.IconButton(icon=ft.icons.ADD_OUTLINED, tooltip="Créer devis", on_click=self.open_new_devis_window)
        self.edit = ft.IconButton(icon=ft.icons.EDIT_OUTLINED, tooltip="Modifier devis", on_click=self.open_edit_devis_window)
        self.delivery = ft.IconButton(icon=ft.icons.PRINT_OUTLINED, tooltip="imprimer bordereau livraison", on_click=self.imprimer_bordereau)
        self.bill = ft.IconButton(icon=ft.icons.EURO_OUTLINED, tooltip="facturer", on_click=self.facturer_devis)
        self.delete = ft.IconButton(icon=ft.icons.DELETE_OUTLINED, tooltip="supprimer devis", on_click=self.delete_devis)

        self.filter_container = ft.Container(
            **filter_container_style,
            content=ft.Row(
                [
                    ft.Row([self.filtre, self.search_devis, self.client_id]),
                    ft.Row([self.actions, self.add, self.edit, self.delivery, self.bill, self.delete])
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        # infos du devis __________________________________________________________________________________
        self.client_name = ft.TextField(**standard_tf_style, label="Nom du client", disabled=True)
        self.date = ft.TextField(**date_tf_style, disabled=True)
        self.montant = ft.TextField(**montant_tf_style, disabled=True)
        self.remise = ft.TextField(**remise_tf_style, disabled=True)
        self.lettres = ft.TextField(**lettres_tf_style, disabled=True)
        self.statut = ft.TextField(**statut_tf_style, disabled=True)

        self.infos_container = ft.Container(
            **standard_ct_style,
            content=ft.Column(
                [
                    ft.Row([self.client_name, self.date, self.montant, self.remise, self.statut]),
                    self.lettres
                ]
            )
        )
        # table details devis__________________________________________________________________________
        self.table_devis = ft.DataTable(**table_details_devis_style)
        self.devis_container = ft.Container(
            **standard_ct_style,
            height=300, width=650,
            content=ft.Column(
                [self.table_devis], expand=True,
                height=360,
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        # impressions options _____________________________________________________________________
        self.options = ft.RadioGroup(
            content=ft.Row(
                spacing=5,
                controls=[
                    ft.Radio(value="etat", label="Etat(TVA, IR, NAP)", active_color=ft.colors.BLACK87),
                    ft.Radio(value="personnel", label="particulier(sans taxes)", active_color=ft.colors.BLACK87),
                    ft.Radio(value="tva", label="avec TVA (seule)", active_color=ft.colors.BLACK87),
                    ft.Radio(value="ir", label="avec IR sans NAP", active_color=ft.colors.BLACK87)
                ]
            )
        )
        self.print_button = ft.IconButton(
            icon=ft.icons.SAVE, tooltip="imprimer devis",
            on_click=self.imprimer
        )
        self.options_container = ft.Container(
            **standard_ct_style,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[self.options, self.print_button]
            )
        )
        # Stack ecran de creatiuon de devis________________________________________________________
        self.n_dev = ft.TextField(**devis_num_style, disabled=True)
        self.n_cliname = ft.Dropdown(**client_name_style, on_change=self.on_change_client)
        self.n_cli_id = ft.Text(visible=False)
        self.n_initiales = ft.Text(visible=False)
        self.object = ft.TextField(**standard_tf_style, label="objet")
        self.n_remise = ft.TextField(**new_remise_style, value="0")
        self.up = ft.IconButton(ft.icons.ADD_CIRCLE_OUTLINE, icon_size=24, on_click=self.add_remise)
        self.down = ft.IconButton(ft.icons.REMOVE_CIRCLE_OUTLINE, icon_size=24, on_click=self.remove_remise)
        self.ct_first = ft.Container(
            **standard_ct_style,
            content=ft.Column(
                [
                    ft.Row([self.n_dev, self.object, self.n_cli_id, ft.Row([self.up, self.n_remise, self.down])]),
                    ft.Row([self.n_cliname, self.n_cli_id, self.n_initiales])
                ]
            )
        )
        self.reference = ft.Dropdown(**new_ref_style, on_change=self.on_change_ref)
        self.designation = ft.TextField(**standard_tf_style, label="designation", disabled=True)
        self.prix_stock = ft.TextField(**new_prix_style, label="prix indiqué", disabled=True)
        self.qte = ft.TextField(**new_qte_style, input_filter=ft.NumbersOnlyInputFilter())
        self.prix = ft.TextField(**new_prix_style, label="prix", input_filter=ft.NumbersOnlyInputFilter())
        self.total = ft.TextField(**new_prix_style, label="total", disabled=True)
        self.total_lettres = ft.TextField(**mt_lettres_style, disabled=True)
        self.button_add = ft.ElevatedButton(
            icon=ft.icons.ADD, text="Ajouter",
            icon_color="white", color="white", height=40,
            bgcolor=ft.colors.BLACK87,
            on_click=self.add_table_line
        )
        self.ct_second = ft.Container(
            **standard_ct_style,
            content=ft.Column(
                [
                    ft.Row([self.reference, self.designation]),
                    ft.Row([self.qte, self.prix_stock, self.prix, self.total]),
                    ft.Row([self.total_lettres, self.button_add])
                ]
            )
        )
        self.msg_error = ft.AlertDialog(
            title=ft.Text("Erreur"),
            content=ft.Text("Veuillez vérifier les champs client"),
            actions=[
                ft.FilledTonalButton(text="Quitter", on_click=self.close_error)
            ]
        )
        self.msg_confirm = ft.AlertDialog(
            title=ft.Text("Confirmation"),
            content=ft.Text(
                "Devis généré avec succès",
                style=ft.TextStyle(font_family="Poppins Medium", size=16)
            ),
            actions=[
                ft.FilledTonalButton(text="Quitter", on_click=self.close_confirm)
            ]
        )
        self.table_new_devis = ft.DataTable(**table_new_devis_style)
        self.new_devis_window = ft.Card(
            elevation=30, expand=True,
            top=5, left=300,
            scale=ft.transform.Scale(scale=0),
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN),
            content=ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=8,
                opacity=1,
                expand=True,
                height=700,
                padding=ft.padding.all(20),
                content=ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.Icon(ft.icons.POST_ADD_OUTLINED),
                                ft.Text("Créer devis", style=ft.TextStyle(size=20, font_family="Poppins Regular"))
                            ]
                        ),
                        self.ct_first,
                        self.ct_second,
                        ft.Container(
                            **standard_ct_style,
                            content=ft.Column(
                                [self.table_new_devis],
                                expand=True,
                                height=200, width=600,
                                scroll=ft.ScrollMode.ADAPTIVE
                            )
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Valider",
                                    icon=ft.icons.CHECK_OUTLINED,
                                    icon_color="white", color="white", bgcolor="red", height=40,
                                    on_click=self.add_new_devis
                                ),
                                ft.ElevatedButton(
                                    "Quitter",
                                    icon=ft.icons.ARROW_BACK_OUTLINED,
                                    icon_color="white", color="white", bgcolor=ft.colors.BLACK87, height=40,
                                    on_click=self.close_new_devis_window
                                )
                            ]
                        )

                    ]
                )
            )
        )
        # Validation impression _____________________________________________________________________
        self.good_impression = ft.AlertDialog(
            title=ft.Text("Confirmation"),
            content=ft.Text("Devis imprimé avec succès", style=ft.TextStyle(size=16, font_family="Poppins Regular")),
            actions=[
                ft.FilledTonalButton(text="Fermer", on_click=self.close_good_impression)
            ]
        )
        self.bad_impression = ft.AlertDialog(
            title=ft.Text("Erreur"),
            content=ft.Text("Veuillez choisir une option avant d'imprimer", style=ft.TextStyle(size=16, font_family="Poppins Regular")),
            actions=[
                ft.FilledTonalButton(text="Fermer", on_click=self.close_bad_impression)
            ]
        )
        # fenetre de facturation de devis __________________________________________________________________________
        self.bc_client = ft.TextField(**bc_tf_style, label="bc client")
        self.confirmation_facturation = ft.Text("devis facturé", visible=False, style=ft.TextStyle(size=16, font_family="Poppins Regular", color="red"))
        self.facturer_window = ft.AlertDialog(
            title=ft.Text("facturer devis"),
            content=ft.Column(
                [
                    ft.Text("Entrez le numéro de BC du client", style=ft.TextStyle(size=12, font_family="Poppins Regular")),
                    self.bc_client,
                    self.confirmation_facturation
                ],
                height=200
            ),
            actions=[
                ft.ElevatedButton(
                    text="facturer", height=40, icon=ft.icons.EURO_OUTLINED, icon_color="white",
                    color="white", bgcolor="red", on_click=self.finish_facture
                ),
                ft.FilledTonalButton(text="Fermer", on_click=self.close_facturer_window)
            ]
        )
        self.error_facture = ft.AlertDialog(
            title=ft.Text("Erreur"),
            content=ft.Text("Ce devis est déja associé à une facture",
                            style=ft.TextStyle(size=16, font_family="Poppins Regular")),
            actions=[
                ft.FilledTonalButton(text="Fermer", on_click=self.close_error_facture)
            ]
        )
        self.error_stock = ft.AlertDialog(
            title=ft.Text("Erreur"),
            content=ft.Text(f"Facturation impossible\nles quantités en stock sont insuffisantes",
                            style=ft.TextStyle(size=16, font_family="Poppins Regular")),
            actions=[
                ft.FilledTonalButton(text="Fermer", on_click=self.close_error_stock)
            ]
        )
        # impression de bordereau de livraison
        self.error_bordereau = ft.AlertDialog(
            title=ft.Text("Erreur"),
            content=ft.Text(f"Impression du bordereau impossible\nLe devis n'est pas facturé",
                            style=ft.TextStyle(size=16, font_family="Poppins Regular")),
            actions=[
                ft.FilledTonalButton(text="Fermer", on_click=self.close_error_bordereau)
            ]
        )
        self.confirm_bordereau = ft.AlertDialog(
            title=ft.Text("Confirmation"),
            content=ft.Text("Bordereau imprimé avec succès",
                            style=ft.TextStyle(size=16, font_family="Poppins Regular")),
            actions=[
                ft.FilledTonalButton(text="Fermer", on_click=self.close_confirm_bordereau)
            ]
        )
        # fenetre de modification de devis ______________________________________________________________
        self.table_edit_devis = ft.DataTable(**table_edit_devis_style)
        self.m_devis = ft.TextField(**devis_num_style, disabled=True)
        self.table_container_edit = ft.Container(
            **standard_ct_style, expand=True, height=100, width=600,
            content=ft.Column([self.table_edit_devis], expand=True, width=600, height=100, scroll=ft.ScrollMode.ADAPTIVE)
        )
        self.m_reference = ft.Dropdown(**new_ref_style)
        self.id_ligne = ft.Text(visible=False)
        self.m_remise = ft.TextField(**new_remise_style)
        self.m_designation = ft.TextField(**standard_tf_style, label="designation", disabled=True)
        self.m_prix_stock = ft.TextField(**new_prix_style, label="prix indiqué", disabled=True)
        self.m_qte = ft.TextField(**new_qte_style, input_filter=ft.NumbersOnlyInputFilter())
        self.m_prix = ft.TextField(**new_prix_style, label="prix", input_filter=ft.NumbersOnlyInputFilter())
        self.m_total = ft.TextField(**new_prix_style, label="total", disabled=True)
        self.m_total_lettres = ft.TextField(**mt_lettres_style, disabled=True)
        self.m_button_add = ft.ElevatedButton(
            icon=ft.icons.ADD, text="Ajouter",
            icon_color="white", color="white", height=40,
            bgcolor=ft.colors.BLACK87,
            on_click=self.add_table_line
        )
        # dialog box for add ligne
        self.mn_ref = ft.Dropdown(**new_ref_style, on_change=self.on_change_ref_ligne)
        self.mn_des = ft.TextField(**standard_tf_style, label="designation", disabled=True)
        self.mn_qte = ft.TextField(**new_qte_style, input_filter=ft.NumbersOnlyInputFilter())
        self.mn_prix_stock = ft.TextField(**new_prix_style, label="Prix indiqué", disabled=True)
        self.mn_prix = ft.TextField(**new_prix_style, label="prix", input_filter=ft.NumbersOnlyInputFilter())
        self.mn_error = ft.Text("Veuillez remplir tous les champs", style=ft.TextStyle(size=16, font_family="Poppins Regular"), visible=False)
        self.new_ligne_window = ft.AlertDialog(
            title=ft.Text("Ajouter ligne"),
            content=ft.Column([self.mn_ref, self.mn_des, self.mn_qte, self.mn_prix_stock, self.mn_prix], height=300),
            actions=[
                ft.ElevatedButton("Ajouter", icon=ft.icons.ADD, color="white", icon_color="white",
                                  bgcolor="red", height=40, on_click=self.add_new_ligne_edit_devis),
                ft.FilledTonalButton(text="Fermer", height=40, on_click=self.close_new_ligne_window)
            ]
        )
        # sel a dialog box for mutiples errors
        self.error_text = ft.Text("", style=ft.TextStyle(color="red", font_family="Poppins Regular", size=14))
        self.error_box = ft.AlertDialog(
            title=ft.Text("Erreur"),
            content=self.error_text,
            actions=[ft.FilledTonalButton(text="Fermer", on_click=self.close_error_box)]
        )
        self.confirmation_text = ft.Text("", style=ft.TextStyle(color="red", font_family="Poppins Regular", size=14))
        self.confirmation_box = ft.AlertDialog(
            title=ft.Text("Confirmation"),
            content=self.confirmation_text,
            actions=[ft.FilledTonalButton(text="Fermer", on_click=self.close_confirmation_box)]
        )
        self.question = ft.Text("Confirmez vous la supression ?")
        self.quit = ft.FilledTonalButton("quitter", on_click=self.close_modal_box)
        self.modal_box = ft.AlertDialog(
            title=ft.Text("Confirmation"),
            content=self.question,
            actions=[
                ft.FilledTonalButton("oui", on_click=self.finish_delete_devis),
                self.quit
            ]
        )
        # edit devis card _________________________________________________________
        self.edit_devis_window = ft.Card(
            elevation=30, expand=True,
            top=5, left=300,
            scale=ft.transform.Scale(scale=0),
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN),
            content=ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=8,
                opacity=1,
                expand=True,
                height=700,
                padding=ft.padding.all(20),
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Row(
                            [
                                ft.Icon(ft.icons.EDIT_DOCUMENT),
                                ft.Text("Modifier devis", style=ft.TextStyle(size=20, font_family="Poppins Regular")),
                                self.id_ligne
                            ]
                        ),
                        ft.Container(
                            **standard_ct_style,
                            content=ft.Row([self.m_devis, self.m_total_lettres])
                        ),
                        self.table_container_edit,
                        ft.Container(
                            **standard_ct_style,
                            content=ft.Row([self.m_reference, self.m_designation, self.m_qte, self.m_prix])
                        ),
                        ft.Container(
                            **standard_ct_style,
                            content=ft.Row(
                                [
                                    ft.ElevatedButton("Modifier ligne", icon=ft.icons.EDIT, icon_color="white",
                                                      color="white", height=40, bgcolor="red", on_click=self.update_ligne),
                                    ft.ElevatedButton("Ajouter ligne", icon=ft.icons.ADD, icon_color="white", color="white",
                                                      height=40, bgcolor="red", on_click=self.open_new_ligne_window),
                                    ft.ElevatedButton("Supprimer ligne", icon=ft.icons.DELETE, icon_color="white",
                                                      color="white", height=40, bgcolor="red", on_click=self.delete_detail_line)
                                ]
                            )
                        ),
                        ft.Container(
                            **standard_ct_style,
                            width=800, height=80,
                            content=ft.Row(
                                [
                                    ft.Row(
                                        [
                                            ft.IconButton(ft.icons.REMOVE_CIRCLE_OUTLINE, icon_size=24, on_click=self.edit_remise_down),
                                            self.m_remise,
                                            ft.IconButton(ft.icons.ADD_CIRCLE_OUTLINE, icon_size=24,
                                                          on_click=self.edit_remise_up),
                                            self.m_total
                                        ]
                                    ),
                                    ft.ElevatedButton("valider remise", icon=ft.icons.EDIT, icon_color="white",
                                                      color="white", height=40, bgcolor="red", on_click=self.on_change_edit_remise)
                                ],
                                alignment="spaceBetween", expand=True
                            )
                        ),
                        ft.Container(
                            **standard_ct_style,
                            content=ft.Row(
                                [
                                    ft.ElevatedButton("Valider modifications",
                                                      icon=ft.icons.CHECK, icon_color="white", color="white",
                                                      height=40, bgcolor="red", on_click=self.finish_edit_devis),
                                ]
                            )
                        )
                    ]
                )
            )
        )
        # fonctions à loader sans evenements ____________________________________________________________
        self.load_devis_list()
        self.load_clients_list()
        self.load_ref_list()
        self.load_edit_ref_list()
        self.load_edit_ref_list2()

    # functions ___________________________________________________________________________________________________
    def switch_page(self, e):
        pages = [
            "stocks", "clients", "fournisseurs", "commandes",
            "devis", "factures"
        ]
        self.page.go(f"/{pages[e.control.selected_index]}")

    # first content stack
    def load_devis_list(self):
        for name in backend.all_devis():
            self.search_devis.options.append(
                ft.dropdown.Option(name)
            )

    def on_change_devis(self, e):
        """actions when devis number change"""
        infos = backend.show_info_devis(self.search_devis.value)
        self.client_id.value = infos[0]
        self.client_name.value = backend.infos_clients(id_client=int(self.client_id.value))[1]
        self.date.value = infos[1]
        self.montant.value = infos[3]
        self.remise.value = infos[4]
        self.lettres.value = infos[5]
        self.statut.value = infos[6].upper()

        for widget in [self.client_name, self.date, self.montant, self.statut,
                       self.remise, self.lettres, self.client_id]:
            widget.update()

        details = backend.search_devis_details(self.search_devis.value)
        datas = []
        for item in details:
            dico = {
                "reference": item[1],
                "designation": item[2],
                "qte": item[3],
                "prix": item[4],
                "total": item[5]
                    }
            datas.append(dico)

        for item in self.table_devis.rows[:]:
            self.table_devis.rows.remove(item)

        for data in datas:
            self.table_devis.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["reference"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["designation"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["qte"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["prix"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["total"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                    ]
                )
            )
        self.table_devis.update()

    # second content stack
    def open_new_devis_window(self, e):
        self.new_devis_window.scale = 1
        self.new_devis_window.update()

    def close_new_devis_window(self, e):

        for row in self.table_new_devis.rows[:]:
            self.table_new_devis.rows.remove(row)

        self.table_new_devis.update()
        self.n_remise.value = "0"
        self.remise.value = ""
        self.designation.value = ""
        self.n_dev.value = ""
        self.prix.value = ""
        self.prix_stock.value = ""
        self.total.value = ""
        self.total_lettres.value = ""
        self.object.value = ""
        self.n_cliname.value = ""
        self.n_cli_id.value = ""

        self.remise.update()
        self.designation.update()
        self.n_dev.update()
        self.prix.update()
        self.prix_stock.update()
        self.total.update()
        self.total_lettres.update()
        self.object.update()
        self.n_cliname.update()
        self.n_cli_id.update()

        self.new_devis_window.scale = 0
        self.new_devis_window.animate_scale = ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT)
        self.new_devis_window.update()

    def load_ref_list(self):
        for name in backend.all_references_stock():
            self.reference.options.append(
                ft.dropdown.Option(name)
            )

    def load_clients_list(self):
        for name in backend.all_clients():
            self.n_cliname.options.append(
                ft.dropdown.Option(name)
            )

    def add_remise(self, e):
        self.n_remise.value = str(int(self.n_remise.value) + 5)
        self.n_remise.update()

    def remove_remise(self, e):
        self.n_remise.value = str(int(self.n_remise.value) - 5)
        self.n_remise.update()

    def on_change_ref(self, e):
        self.designation.value = backend.search_designation(self.reference.value)[0]
        self.prix_stock.value = backend.search_designation(self.reference.value)[1]
        self.designation.update()
        self.prix_stock.update()

    def on_change_client(self, e):
        self.n_cli_id.value = backend.id_client_par_nom(self.n_cliname.value)
        self.n_initiales.value = backend.search_initiales_nom(self.n_cliname.value)
        self.n_dev.value = backend.find_devis_num(self.n_cli_id.value)

        self.n_cli_id.update()
        self.n_initiales.update()
        self.n_dev.update()

    def add_table_line(self, e):
        if self.prix.value != "" and self.qte.value != "":
            self.table_new_devis.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(self.reference.value.upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(self.designation.value.upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(self.qte.value, style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(self.prix.value, style=ft.TextStyle(font_family="poppins Medium", size=11))),
                    ]
                )
            )
        else:
            pass

        # recuperer la liste des lignes dans un tableau
        grande_liste = []
        l = self.table_new_devis.rows[:] # liste de DataRow
        for i in range(len(l)):
            sous_liste = []
            for j in range(len(l[i].cells)):
                sous_liste.append(l[i].cells[j].content.value)
            grande_liste.append(sous_liste)

        somme = 0
        remise = int(self.n_remise.value)
        for row in grande_liste:
            somme += (int(row[2]) * int(row[3]))

        self.total.value = str(somme - (somme * remise // 100))
        self.total_lettres.value = ecrire_en_lettres(int(self.total.value))

        self.reference.value = ""
        self.prix.value = ""
        self.qte.value = ""
        self.reference.update()
        self.table_new_devis.update()
        self.total.update()
        self.montant.update()
        self.prix.update()
        self.qte.update()
        self.total_lettres.update()

    def add_new_devis(self, e):
        grande_liste = []
        l = self.table_new_devis.rows[:]  # liste de DataRow
        for i in range(len(l)):
            sous_liste = []
            for j in range(len(l[i].cells)):
                sous_liste.append(l[i].cells[j].content.value)
            grande_liste.append(sous_liste)

        # add devis
        if self.n_cliname.value == "":
            self.msg_error.open = True
            self.msg_error.update()

        else:
            mt_remise = int(self.n_remise.value)
            montant = int(self.total.value)
            cli_id = int(self.n_cli_id.value)
            backend.add_devis(self.n_dev.value, date.today(), cli_id, montant,
                              self.object.value, mt_remise, self.total_lettres.value)

            # add devis details
            for data in grande_liste:
                backend.add_devis_details(self.n_dev.value, data[0], data[2], data[3])

            self.n_cliname.value = ""
            self.object.value = ""
            self.reference.value = ""
            self.n_cliname.update()
            self.reference.update()
            self.object.update()
            self.msg_confirm.open = True
            self.msg_confirm.update()
            self.n_dev.update()
            self.designation.update()
            self.prix_stock.update()
            self.total.update()
            self.total_lettres.update()

            for row in self.table_new_devis.rows[:]:
                self.table_new_devis.rows.remove(row)

            self.table_new_devis.update()

    def close_confirm(self, e):
        self.msg_confirm.open = False
        self.msg_confirm.update()

    def close_error(self, e):
        self.msg_error.open = False
        self.msg_error.update()

    # fonctions d'impression ______________________________________
    def imprimer_personnel(self):
        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)
        can = Canvas("{0}".format(fichier), pagesize=A4)

        # dessin des entêtes
        def draw_headers():
            logo = "assets/logo 1.jpg"
            signature = "assets/signature.png"
            # dessin logo et dignature
            can.drawImage(logo, 1.5 * cm, 26 * cm)
            can.drawImage(signature, 12 * cm, 2 * cm)
            # infos de l'entreprise
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica-Bold", 14)
            can.drawCentredString(4 * cm, 24.8 * cm, f"{ENTITE_NOM}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)
            can.drawCentredString(4 * cm, 24.3 * cm, f"RC: {ENTITE_RC}")
            can.drawCentredString(4 * cm, 23.8 * cm, f"NUI: {ENTITE_NUI}")
            can.setFont("Helvetica-Bold", 24)
            can.setFillColorRGB(0, 0, 0)
            can.drawCentredString(15 * cm, 27.5 * cm, "Proforma")
            can.setFont("Helvetica", 14)
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {self.search_devis.value}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(self.date.value)}")

            # infos du client
            infos_client = backend.infos_clients(self.client_id.value)
            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{self.client_name.value}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[3] is not None:
                can.drawString(11 * cm, 23.4 * cm, f"Contact: {infos_client[3]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[4] is not None:
                can.drawString(11 * cm, 22.7 * cm, f"NUI: {infos_client[4]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[5] is not None:
                can.drawString(11 * cm, 22 * cm, f"RC: {infos_client[5]}")

        draw_headers()

        y = 21.5

        # details factures
        can.setStrokeColorRGB(0, 0, 0)
        # Lignes horizontales
        can.line(1 * cm, (y - 1) * cm, 20 * cm, (y - 1) * cm)
        can.line(1 * cm, (y - 2) * cm, 20 * cm, (y - 2) * cm)
        # lignes verticales
        can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 2) * cm)
        can.line(11 * cm, (y - 1) * cm, 11 * cm, (y - 2) * cm)
        can.line(12.5 * cm, (y - 1) * cm, 12.5 * cm, (y - 2) * cm)
        can.line(14 * cm, (y - 1) * cm, 14 * cm, (y - 2) * cm)
        can.line(17 * cm, (y - 1) * cm, 17 * cm, (y - 2) * cm)
        can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 2) * cm)
        # draw headers
        can.setFont("Helvetica-Bold", 10)
        can.drawCentredString(6 * cm, (y - 1.6) * cm, "Désignation")
        can.drawCentredString(11.75 * cm, (y - 1.6) * cm, "Qté")
        can.drawCentredString(13.25 * cm, (y - 1.6) * cm, "unité")
        can.drawCentredString(15.5 * cm, (y - 1.6) * cm, "Prix unitaire")
        can.drawCentredString(18.5 * cm, (y - 1.6) * cm, "Montant")

        ref_list = []
        total_devis = 0
        l = self.table_devis.rows[:]  # liste de DataRow
        for i in range(len(l)):
            sous_liste = []
            for j in range(len(l[i].cells)):
                sous_liste.append(l[i].cells[j].content.value)
            ref_list.append(sous_liste)

        for row in ref_list:
            total_devis += row[4]
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[1]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{backend.look_unit(row[0])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[3])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            # lignes verticales
            can.setStrokeColorRGB(0, 0, 0)
            can.line(1 * cm, (y - 2) * cm, 1 * cm, (y - 3) * cm)
            can.line(11 * cm, (y - 2) * cm, 11 * cm, (y - 3) * cm)
            can.line(12.5 * cm, (y - 2) * cm, 12.5 * cm, (y - 3) * cm)
            can.line(14 * cm, (y - 2) * cm, 14 * cm, (y - 3) * cm)
            can.line(17 * cm, (y - 2) * cm, 17 * cm, (y - 3) * cm)
            can.line(20 * cm, (y - 2) * cm, 20 * cm, (y - 3) * cm)
            # lignes horizontales
            can.setStrokeColorRGB(0, 0, 0)
            can.line(1 * cm, (y - 3) * cm, 20 * cm, (y - 3) * cm)
            y -= 1

        y = y - 1.5

        can.setFillColorRGB(0, 0, 0)
        can.setFont("Helvetica-Bold", 10)
        can.drawCentredString(15.5 * cm, (y - 1) * cm, "Total:")
        can.setFont("Helvetica", 11)
        can.drawCentredString(18.5 * cm, (y - 1) * cm, f"{milSep(total_devis)}")

        if int(self.remise.value) != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - 1.5) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2) * cm, "Après remise:")
            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - 1.5) * cm, f"{int(self.remise.value)}%")
            can.drawCentredString(18.5 * cm, (y - 2) * cm, f"{milSep(int(self.montant.value))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 3) * cm, f"arrêtée à la somme de: {self.lettres.value.lower()}")
            can.drawCentredString(10.5 * cm, (y - 3.5) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        else:
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 2) * cm, f"arrêtée à la somme de: {self.lettres.value.lower()}")
            can.drawCentredString(10.5 * cm, (y - 2.5) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")
        can.save()

    def imprimer_etat(self):
        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)
        can = Canvas("{0}".format(fichier), pagesize=A4)

        # dessin des entêtes
        def draw_headers():
            logo = "assets/logo 1.jpg"
            signature = "assets/signature.png"
            # dessin logo et dignature
            can.drawImage(logo, 1.5 * cm, 26 * cm)
            can.drawImage(signature, 12 * cm, 2 * cm)
            # infos de l'entreprise
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica-Bold", 14)
            can.drawCentredString(4 * cm, 24.8 * cm, f"{ENTITE_NOM}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)
            can.drawCentredString(4 * cm, 24.3 * cm, f"RC: {ENTITE_RC}")
            can.drawCentredString(4 * cm, 23.8 * cm, f"NUI: {ENTITE_NUI}")
            can.setFont("Helvetica-Bold", 24)
            can.setFillColorRGB(0, 0, 0)
            can.drawCentredString(15 * cm, 27.5 * cm, "Proforma")
            can.setFont("Helvetica", 14)
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {self.search_devis.value}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(self.date.value)}")
            # infos du client
            infos_client = backend.infos_clients(int(self.client_id.value))
            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{self.client_name.value}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[3] is not None:
                can.drawString(11 * cm, 23.4 * cm, f"Contact: {infos_client[3]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[4] is not None:
                can.drawString(11 * cm, 22.7 * cm, f"NUI: {infos_client[4]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[5] is not None:
                can.drawString(11 * cm, 22 * cm, f"RC: {infos_client[5]}")

        draw_headers()

        y = 21.5

        can.setStrokeColorRGB(0, 0, 0)
        # Lignes horizontales
        can.line(1 * cm, (y - 1) * cm, 20 * cm, (y - 1) * cm)
        can.line(1 * cm, (y - 2) * cm, 20 * cm, (y - 2) * cm)
        # lignes verticales
        can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 2) * cm)
        can.line(11 * cm, (y - 1) * cm, 11 * cm, (y - 2) * cm)
        can.line(12.5 * cm, (y - 1) * cm, 12.5 * cm, (y - 2) * cm)
        can.line(14 * cm, (y - 1) * cm, 14 * cm, (y - 2) * cm)
        can.line(17 * cm, (y - 1) * cm, 17 * cm, (y - 2) * cm)
        can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 2) * cm)
        # draw headers
        can.setFont("Helvetica-Bold", 10)
        can.drawCentredString(6 * cm, (y - 1.6) * cm, "Désignation")
        can.drawCentredString(11.75 * cm, (y - 1.6) * cm, "Qté")
        can.drawCentredString(13.25 * cm, (y - 1.6) * cm, "unité")
        can.drawCentredString(15.5 * cm, (y - 1.6) * cm, "Prix unitaire")
        can.drawCentredString(18.5 * cm, (y - 1.6) * cm, "Montant")

        ref_list = []
        total_devis = 0
        l = self.table_devis.rows[:]
        for i in range(len(l)):
            sous_liste = []
            for j in range(len(l[i].cells)):
                sous_liste.append(l[i].cells[j].content.value)
            ref_list.append(sous_liste)

        for row in ref_list:
            total_devis += row[4]
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[1]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{backend.look_unit(row[0])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[3])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            # lignes verticales
            can.setStrokeColorRGB(0, 0, 0)
            can.line(1 * cm, (y - 2) * cm, 1 * cm, (y - 3) * cm)
            can.line(11 * cm, (y - 2) * cm, 11 * cm, (y - 3) * cm)
            can.line(12.5 * cm, (y - 2) * cm, 12.5 * cm, (y - 3) * cm)
            can.line(14 * cm, (y - 2) * cm, 14 * cm, (y - 3) * cm)
            can.line(17 * cm, (y - 2) * cm, 17 * cm, (y - 3) * cm)
            can.line(20 * cm, (y - 2) * cm, 20 * cm, (y - 3) * cm)
            # lignes horizontales
            can.setStrokeColorRGB(0, 0, 0)
            can.line(1 * cm, (y - 3) * cm, 20 * cm, (y - 3) * cm)
            y -= 1

        y = y - 1.5

        can.setFillColorRGB(0, 0, 0)
        can.setFont("Helvetica-Bold", 10)
        can.drawCentredString(15.5 * cm, (y - 1) * cm, "Total:")
        can.setFont("Helvetica", 11)
        can.drawCentredString(18.5 * cm, (y - 1) * cm, f"{milSep(total_devis)}")

        y = y - 1
        pas = 0.5

        if int(self.remise.value) != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Après remise:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "NAP:")
            can.drawCentredString(15.5 * cm, (y - 5 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 6 * pas) * cm, "Total TTC:")
            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{int(self.remise.value)}%")
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(self.montant.value))}")

            if int(self.montant.value) < 5000000:
                mt_ir = int(self.montant.value) * 5.5 / 100
            else:
                mt_ir = int(self.montant.value) * 2.2 / 100

            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_ir))}")
            mt_nap = int(self.montant.value) - mt_ir
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_nap))}")
            mt_tva = int(self.montant.value) * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 5 * pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = int(self.montant.value) + mt_tva
            can.drawCentredString(18.5 * cm, (y - 6 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 8 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc).lower()}")
            can.drawCentredString(10.5 * cm, (y - 9 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        else:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "NAP:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "Total TTC:")
            can.setFont("Helvetica", 11)

            if int(self.montant.value) < 5000000:
                mt_ir = int(self.montant.value) * 5.5 / 100
            else:
                mt_ir = int(self.montant.value) * 2.2 / 100

            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{milSep(int(mt_ir))}")
            mt_nap = int(self.montant.value) - mt_ir
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(mt_nap))}")
            mt_tva = int(self.montant.value) * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = int(self.montant.value) + mt_tva
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 6 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc).lower()}")
            can.drawCentredString(10.5 * cm, (y - 7 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")
        can.save()

    def imprimer_seul_TVA(self):
        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)
        can = Canvas("{0}".format(fichier), pagesize=A4)

        # dessin des entêtes
        def draw_headers():
            logo = "assets/logo 1.jpg"
            signature = "assets/signature.png"
            # dessin logo et dignature
            can.drawImage(logo, 1.5 * cm, 26 * cm)
            can.drawImage(signature, 12 * cm, 2 * cm)
            # infos de l'entreprise
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica-Bold", 14)
            can.drawCentredString(4 * cm, 24.8 * cm, f"{ENTITE_NOM}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)
            can.drawCentredString(4 * cm, 24.3 * cm, f"RC: {ENTITE_RC}")
            can.drawCentredString(4 * cm, 23.8 * cm, f"NUI: {ENTITE_NUI}")
            can.setFont("Helvetica-Bold", 24)
            can.setFillColorRGB(0, 0, 0)
            can.drawCentredString(15 * cm, 27.5 * cm, "Proforma")
            can.setFont("Helvetica", 14)
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {self.search_devis.value}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(self.date.value)}")
            # infos du client
            infos_client = backend.infos_clients(self.client_id.value)
            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{self.client_name.value}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[3] is not None:
                can.drawString(11 * cm, 23.4 * cm, f"Contact: {infos_client[3]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[4] is not None:
                can.drawString(11 * cm, 22.7 * cm, f"NUI: {infos_client[4]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[5] is not None:
                can.drawString(11 * cm, 22 * cm, f"RC: {infos_client[5]}")

        draw_headers()

        y = 21.5

        can.setStrokeColorRGB(0, 0, 0)
        # Lignes horizontales
        can.line(1 * cm, (y - 1) * cm, 20 * cm, (y - 1) * cm)
        can.line(1 * cm, (y - 2) * cm, 20 * cm, (y - 2) * cm)
        # lignes verticales
        can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 2) * cm)
        can.line(11 * cm, (y - 1) * cm, 11 * cm, (y - 2) * cm)
        can.line(12.5 * cm, (y - 1) * cm, 12.5 * cm, (y - 2) * cm)
        can.line(14 * cm, (y - 1) * cm, 14 * cm, (y - 2) * cm)
        can.line(17 * cm, (y - 1) * cm, 17 * cm, (y - 2) * cm)
        can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 2) * cm)
        # draw headers
        can.setFont("Helvetica-Bold", 10)
        can.drawCentredString(6 * cm, (y - 1.6) * cm, "Désignation")
        can.drawCentredString(11.75 * cm, (y - 1.6) * cm, "Qté")
        can.drawCentredString(13.25 * cm, (y - 1.6) * cm, "unité")
        can.drawCentredString(15.5 * cm, (y - 1.6) * cm, "Prix unitaire")
        can.drawCentredString(18.5 * cm, (y - 1.6) * cm, "Montant")

        ref_list = []
        total_devis = 0
        l = self.table_devis.rows[:]  # liste de DataRow
        for i in range(len(l)):
            sous_liste = []
            for j in range(len(l[i].cells)):
                sous_liste.append(l[i].cells[j].content.value)
            ref_list.append(sous_liste)

        for row in ref_list:
            total_devis += row[4]
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[1]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{backend.look_unit(row[0])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[3])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            # lignes verticales
            can.setStrokeColorRGB(0, 0, 0)
            can.line(1 * cm, (y - 2) * cm, 1 * cm, (y - 3) * cm)
            can.line(11 * cm, (y - 2) * cm, 11 * cm, (y - 3) * cm)
            can.line(12.5 * cm, (y - 2) * cm, 12.5 * cm, (y - 3) * cm)
            can.line(14 * cm, (y - 2) * cm, 14 * cm, (y - 3) * cm)
            can.line(17 * cm, (y - 2) * cm, 17 * cm, (y - 3) * cm)
            can.line(20 * cm, (y - 2) * cm, 20 * cm, (y - 3) * cm)
            # lignes horizontales
            can.setStrokeColorRGB(0, 0, 0)
            can.line(1 * cm, (y - 3) * cm, 20 * cm, (y - 3) * cm)
            y -= 1

        y = y - 1.5

        can.setFillColorRGB(0, 0, 0)
        can.setFont("Helvetica-Bold", 10)
        can.drawCentredString(15.5 * cm, (y - 1) * cm, "Total:")
        can.setFont("Helvetica", 11)
        can.drawCentredString(18.5 * cm, (y - 1) * cm, f"{milSep(total_devis)}")

        y = y - 1
        pas = 0.5

        if int(self.remise.value) != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Montant après remise:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "Total TTC:")
            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{int(self.remise.value)}%")
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(self.montant.value))}")
            mt_tva = int(self.montant.value) * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = int(self.montant.value) + mt_tva
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 6 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc).lower()}")
            can.drawCentredString(10.5 * cm, (y - 7 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        else:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Total TTC:")
            can.setFont("Helvetica", 11)
            mt_tva = int(self.montant.value) * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = int(self.montant.value) + mt_tva
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 4 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc).lower()}")
            can.drawCentredString(10.5 * cm, (y - 5 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")
        can.save()

    def imprimer_IR_sans_NAP(self):
        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)
        can = Canvas("{0}".format(fichier), pagesize=A4)

        # Dessin des entêtes
        def draw_headers():
            logo = "assets/logo 1.jpg"
            signature = "assets/signature.png"
            # dessin logo et dignature
            can.drawImage(logo, 1.5 * cm, 26 * cm)
            can.drawImage(signature, 12 * cm, 2 * cm)
            # infos de l'entreprise
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica-Bold", 14)
            can.drawCentredString(4 * cm, 24.8 * cm, f"{ENTITE_NOM}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)
            can.drawCentredString(4 * cm, 24.3 * cm, f"RC: {ENTITE_RC}")
            can.drawCentredString(4 * cm, 23.8 * cm, f"NUI: {ENTITE_NUI}")
            can.setFont("Helvetica-Bold", 24)
            can.setFillColorRGB(0, 0, 0)
            can.drawCentredString(15 * cm, 27.5 * cm, "Proforma")
            can.setFont("Helvetica", 14)
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {self.search_devis.value}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(self.date.value)}")
            # infos du client
            infos_client = backend.infos_clients(self.client_id.value)
            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{self.client_name.value}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[3] is not None:
                can.drawString(11 * cm, 23.4 * cm, f"Contact: {infos_client[3]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[4] is not None:
                can.drawString(11 * cm, 22.7 * cm, f"NUI: {infos_client[4]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[5] is not None:
                can.drawString(11 * cm, 22 * cm, f"RC: {infos_client[5]}")

        draw_headers()

        y = 21.5

        can.setStrokeColorRGB(0, 0, 0)
        # Lignes horizontales
        can.line(1 * cm, (y - 1) * cm, 20 * cm, (y - 1) * cm)
        can.line(1 * cm, (y - 2) * cm, 20 * cm, (y - 2) * cm)
        # lignes verticales
        can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 2) * cm)
        can.line(11 * cm, (y - 1) * cm, 11 * cm, (y - 2) * cm)
        can.line(12.5 * cm, (y - 1) * cm, 12.5 * cm, (y - 2) * cm)
        can.line(14 * cm, (y - 1) * cm, 14 * cm, (y - 2) * cm)
        can.line(17 * cm, (y - 1) * cm, 17 * cm, (y - 2) * cm)
        can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 2) * cm)

        # draw headers
        can.setFont("Helvetica-Bold", 10)
        can.drawCentredString(6 * cm, (y - 1.6) * cm, "Désignation")
        can.drawCentredString(11.75 * cm, (y - 1.6) * cm, "Qté")
        can.drawCentredString(13.25 * cm, (y - 1.6) * cm, "unité")
        can.drawCentredString(15.5 * cm, (y - 1.6) * cm, "Prix unitaire")
        can.drawCentredString(18.5 * cm, (y - 1.6) * cm, "Montant")

        ref_list = []
        total_devis = 0
        l = self.table_devis.rows[:]  # liste de DataRow
        for i in range(len(l)):
            sous_liste = []
            for j in range(len(l[i].cells)):
                sous_liste.append(l[i].cells[j].content.value)
            ref_list.append(sous_liste)

        for row in ref_list:
            total_devis += row[4]
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[1]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{backend.look_unit(row[0])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[3])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            # lignes verticales
            can.setStrokeColorRGB(0, 0, 0)
            can.line(1 * cm, (y - 2) * cm, 1 * cm, (y - 3) * cm)
            can.line(11 * cm, (y - 2) * cm, 11 * cm, (y - 3) * cm)
            can.line(12.5 * cm, (y - 2) * cm, 12.5 * cm, (y - 3) * cm)
            can.line(14 * cm, (y - 2) * cm, 14 * cm, (y - 3) * cm)
            can.line(17 * cm, (y - 2) * cm, 17 * cm, (y - 3) * cm)
            can.line(20 * cm, (y - 2) * cm, 20 * cm, (y - 3) * cm)
            # lignes horizontales
            can.setStrokeColorRGB(0, 0, 0)
            can.line(1 * cm, (y - 3) * cm, 20 * cm, (y - 3) * cm)

            y -= 1

        y = y - 1.5

        can.setFillColorRGB(0, 0, 0)
        can.setFont("Helvetica-Bold", 10)
        can.drawCentredString(15.5 * cm, (y - 1) * cm, "Total:")
        can.setFont("Helvetica", 11)
        can.drawCentredString(18.5 * cm, (y - 1) * cm, f"{milSep(total_devis)}")

        y = y - 1
        pas = 0.5

        if int(self.remise.value) != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Après remise:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 5 * pas) * cm, "Total TTC:")

            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{int(self.remise.value)}%")
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(self.montant.value))}")

            if int(self.montant.value) < 5000000:
                mt_ir = int(self.montant.value) * 5.5 / 100
            else:
                mt_ir = int(self.montant.value) * 2.2 / 100
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_ir))}")

            mt_tva = int(self.montant.value) * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = int(self.montant.value) + mt_tva
            can.drawCentredString(18.5 * cm, (y - 5 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 7 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc).lower()}")
            can.drawCentredString(10.5 * cm, (y - 8 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        else:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "Total TTC:")
            can.setFont("Helvetica", 11)

            if int(self.montant.value) < 5000000:
                mt_ir = int(self.montant.value) * 5.5 / 100
            else:
                mt_ir = int(self.montant.value) * 2.2 / 100

            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{milSep(int(mt_ir))}")
            mt_tva = int(self.montant.value) * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = int(self.montant.value) + mt_tva
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 5 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc).lower()}")
            can.drawCentredString(10.5 * cm, (y - 6 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")
        can.save()

    def close_good_impression(self, e):
        self.good_impression.open = False
        self.good_impression.update()

    def close_bad_impression(self, e):
        self.bad_impression.open = False
        self.bad_impression.update()

    def imprimer(self, e):
        if self.options.value == "etat":
            self.imprimer_etat()
            self.good_impression.open = True
            self.good_impression.update()

        elif self.options.value == "personnel":
            self.imprimer_personnel()
            self.good_impression.open = True
            self.good_impression.update()

        elif self.options.value == "tva":
            self.imprimer_seul_TVA()
            self.good_impression.open = True
            self.good_impression.update()

        elif self.options.value == "ir":
            self.imprimer_IR_sans_NAP()
            self.good_impression.open = True
            self.good_impression.update()

        else:
            self.bad_impression.open = True
            self.bad_impression.update()

    # facturation du devis _____________________________________________________
    def facturer_devis(self, e):
        details_factures = backend.find_devis_details(self.search_devis.value)
        count_nc = 0
        for row in details_factures:
            # vérifie les stocks
            if backend.find_nature_ref(row[2]) == "stock":
                ancien_stock = backend.find_stock_ref(row[2])

                if ancien_stock < row[3]:
                    count_nc += 1

        if self.statut.value.lower() == "facturé":
            self.error_facture.open = True
            self.error_facture.update()

        elif self.statut.value == "":
            pass

        else:
            if count_nc > 0:
                self.error_stock.open = True
                self.error_stock.update()

            else:
                self.facturer_window.open = True
                self.facturer_window.update()

    def finish_facture(self, e):
        info_facture = backend.show_info_devis(self.search_devis.value)
        numero_facture = backend.find_facture_num(info_facture[0])
        details_factures = backend.find_devis_details(self.search_devis.value)

        # table facture
        backend.add_facture(
            numero_facture, info_facture[0], info_facture[3], info_facture[2], info_facture[4], info_facture[5],
            self.search_devis.value, self.bc_client.value)

        # Table details facture
        for row in details_factures:
            backend.add_details_facture(numero_facture, row[2], row[3], row[4])
            # Mise à jour du stock
            if backend.find_nature_ref(row[2]) == "stock":
                ancien_stock = backend.find_stock_ref(row[2])
                nouveau_stock = ancien_stock - row[3]
                backend.update_stock(nouveau_stock, row[2])
                backend.add_historique(row[2], "S", numero_facture, ancien_stock, row[3], nouveau_stock)

        # mise à jour du statut du devis
        backend.maj_statut_devis(self.search_devis.value)

        # remplir les bordereaux de livraison
        initiales_client = backend.search_initiales(info_facture[0])
        numero_bordereau = backend.find_bordereau_num(initiales_client)
        backend.add_bordereau(numero_bordereau, self.search_devis.value, self.bc_client.value)

        for row in details_factures:
            backend.add_bordereau_details(numero_bordereau, row[2], row[3], row[4])

        self.bc_client.value = ""
        self.bc_client.update()
        self.facturer_window.open = False
        self.facturer_window.update()
        self.statut.value = backend.show_info_devis(self.search_devis.value)[6].upper()
        self.statut.update()

    def close_facturer_window(self, e):
        self.facturer_window.open = False
        self.facturer_window.update()

    def close_error_facture(self, e):
        self.error_facture.open = False
        self.error_facture.update()

    def close_error_stock(self, e):
        self.error_stock.open = False
        self.error_stock.update()

    def imprimer_bordereau(self, e):
        if not backend.verif_bordereau(self.search_devis.value):
            self.error_bordereau.open = True
            self.error_bordereau.update()

        else:
            chemin = asksaveasfilename(title='save as', defaultextension="pdf")
            fichier = os.path.abspath(chemin)
            can = Canvas("{0}".format(fichier), pagesize=A4)

            # dessin des entêtes
            def draw_headers():
                logo = "assets/logo 1.jpg"
                signature = "assets/signature.png"

                # dessin logo et signature
                can.drawImage(logo, 1.5 * cm, 26 * cm)
                can.drawImage(signature, 12 * cm, 2 * cm)

                # infos de l'entreprise
                can.setFillColorRGB(0, 0, 0)
                can.setFont("Helvetica-Bold", 14)
                can.drawCentredString(4 * cm, 24.8 * cm, f"{ENTITE_NOM}")
                can.setFont("Helvetica", 11)
                can.setFillColorRGB(0, 0, 0)
                can.drawCentredString(4 * cm, 24.3 * cm, f"RC: {ENTITE_RC}")
                can.drawCentredString(4 * cm, 23.8 * cm, f"NUI: {ENTITE_NUI}")
                can.setFont("Helvetica-Bold", 24)
                can.setFillColorRGB(0, 0, 0)
                can.drawCentredString(15 * cm, 27.5 * cm, "Bordereau de livraison")
                can.setFont("Helvetica", 12)
                num_bex = backend.search_bordereau(self.search_devis.value)[1]
                bc = backend.search_bordereau(self.search_devis.value)[3]
                can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {num_bex}")
                can.setFont("Helvetica", 12)
                can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(self.date.value)}")
                # infos du client
                infos_client = backend.infos_clients(self.client_id.value)
                # cadre des infos du client
                can.setStrokeColorRGB(0, 0, 0)
                can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
                can.setFont("Helvetica-Bold", 12)
                can.setFillColorRGB(0, 0, 0)
                can.drawString(11 * cm, 24.1 * cm, f"{self.client_name.value}")
                can.setFont("Helvetica", 12)
                can.setFillColorRGB(0, 0, 0)
                can.drawString(11 * cm, 23.4 * cm, f"BC client: {bc}")

                can.setFont("Helvetica", 11)
                can.setFillColorRGB(0, 0, 0)

                if infos_client[4] is not None:
                    can.drawString(11 * cm, 22.7 * cm, f"NUI: {infos_client[4]}")

                can.setFont("Helvetica", 11)
                can.setFillColorRGB(0, 0, 0)

                if infos_client[5] is not None:
                    can.drawString(11 * cm, 22 * cm, f"RC: {infos_client[5]}")

            draw_headers()

            y = 21.5

            can.setStrokeColorRGB(0, 0, 0)
            # Lignes horizontales
            can.line(1 * cm, (y - 1) * cm, 20 * cm, (y - 1) * cm)
            can.line(1 * cm, (y - 2) * cm, 20 * cm, (y - 2) * cm)
            # lignes verticales
            can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 2) * cm)
            can.line(11 * cm, (y - 1) * cm, 11 * cm, (y - 2) * cm)
            can.line(12.5 * cm, (y - 1) * cm, 12.5 * cm, (y - 2) * cm)
            can.line(14 * cm, (y - 1) * cm, 14 * cm, (y - 2) * cm)
            can.line(17 * cm, (y - 1) * cm, 17 * cm, (y - 2) * cm)
            can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 2) * cm)

            # draw headers
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(6 * cm, (y - 1.6) * cm, "Désignation")
            can.drawCentredString(11.75 * cm, (y - 1.6) * cm, "Qté")
            can.drawCentredString(13.25 * cm, (y - 1.6) * cm, "unité")
            can.drawCentredString(15.5 * cm, (y - 1.6) * cm, "Prix unitaire")
            can.drawCentredString(18.5 * cm, (y - 1.6) * cm, "Montant")

            ref_list = []
            total_devis = 0
            l = self.table_devis.rows[:]  # liste de DataRow
            for i in range(len(l)):
                sous_liste = []
                for j in range(len(l[i].cells)):
                    sous_liste.append(l[i].cells[j].content.value)
                ref_list.append(sous_liste)

            for row in ref_list:
                total_devis += row[4]
                can.setFillColorRGB(0, 0, 0)
                can.setFont("Helvetica", 10)
                can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[1]}")
                can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[2]}")
                can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{backend.look_unit(row[0])}")
                can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[3])}")
                can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
                can.setStrokeColorRGB(0, 0, 0)
                can.line(1 * cm, (y - 2) * cm, 1 * cm, (y - 3) * cm)
                can.line(11 * cm, (y - 2) * cm, 11 * cm, (y - 3) * cm)
                can.line(12.5 * cm, (y - 2) * cm, 12.5 * cm, (y - 3) * cm)
                can.line(14 * cm, (y - 2) * cm, 14 * cm, (y - 3) * cm)
                can.line(17 * cm, (y - 2) * cm, 17 * cm, (y - 3) * cm)
                can.line(20 * cm, (y - 2) * cm, 20 * cm, (y - 3) * cm)
                # lignes horizontales
                can.setStrokeColorRGB(0, 0, 0)
                can.line(1 * cm, (y - 3) * cm, 20 * cm, (y - 3) * cm)
                y -= 1

            y = y - 1.5

            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - 1) * cm, "Total:")
            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - 1) * cm, f"{milSep(total_devis)}")

            can.setFont("Helvetica-Bold", 12)
            can.drawCentredString(5.75 * cm, (y - 3) * cm, "Le client")
            can.line(4 * cm, (y - 3.2) * cm, 7.50 * cm, (y - 3.2) * cm)
            can.setFont("Helvetica-Oblique", 9)
            can.drawCentredString(5.75 * cm, (y - 3.7) * cm, "(Nom, date, signature)")

            can.setFont("Helvetica-Bold", 12)
            can.drawCentredString(15.25 * cm, (y - 3) * cm, "FOMIDERC")
            can.line(13.5 * cm, (y - 3.2) * cm, 17 * cm, (y - 3.2) * cm)
            can.setFont("Helvetica-Oblique", 9)
            can.drawCentredString(15.25 * cm, (y - 3.7) * cm, "(Nom, date, signature)")

            # pied de page
            can.setFont("Helvetica", 8)
            can.setFillColorRGB(0.25, 0.25, 0.25)
            can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
            can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
            can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")

            can.save()
            self.confirm_bordereau.open = True
            self.confirm_bordereau.update()

    def close_error_bordereau(self, e):
        self.error_bordereau.open = False
        self.error_bordereau.update()

    def close_confirm_bordereau(self, e):
        self.confirm_bordereau.open = False
        self.confirm_bordereau.update()

    # third content stack (modifier)___________________________________________________
    def load_edit_ref_list(self):
        for name in backend.all_references_stock():
            self.m_reference.options.append(
                ft.dropdown.Option(name)
            )

    def load_edit_ref_list2(self):
        for name in backend.all_references_stock():
            self.mn_ref.options.append(
                ft.dropdown.Option(name)
            )

    def open_edit_devis_window(self, e):
        if self.statut.value.lower() == "facturé":
            self.error_text.value = "Modification impossible! le devis est déja facturé"
            self.error_text.update()
            self.error_box.open = True
            self.error_box.update()

        elif self.statut.value == "":
            self.error_text.value = "Vous devez sélectionner un devis"
            self.error_text.update()
            self.error_box.open = True
            self.error_box.update()
        else:
            self.m_devis.value = self.search_devis.value
            self.m_devis.update()
            details = backend.find_devis_details(self.m_devis.value)

            for data in details:
                self.table_edit_devis.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f"{data[0]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(f"{data[2]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(f"{backend.search_designation(data[2])[0]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(f"{data[3]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(f"{data[4]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ],
                        on_select_changed=lambda e: self.select_item(
                            e.control.cells[0].content.value,
                            e.control.cells[1].content.value,
                            e.control.cells[3].content.value,
                            e.control.cells[4].content.value
                        )
                    )
                )
            self.table_edit_devis.update()

            infos_devis = backend.show_info_devis(self.m_devis.value)
            self.m_total.value = infos_devis[3]
            self.m_total_lettres.value = infos_devis[5]
            self.m_remise.value = str(infos_devis[4])

            for widget in (self.m_total, self.m_total_lettres, self.m_remise):
                widget.update()

            self.edit_devis_window.scale = 1
            self.edit_devis_window.update()

    def select_item(self, e, f, h, i):
        self.id_ligne.value = e
        self.m_reference.value = f
        self.m_designation.value = backend.search_designation(self.m_reference.value)[0]
        self.m_qte.value = str(h)
        self.m_prix.value = str(i)

        for widget in (self.id_ligne, self.m_designation, self.m_reference, self.m_qte, self.m_prix):
            widget.update()

    def delete_detail_line(self, e):
        if self.id_ligne.value == "":
            self.error_text.value = "Aucune ligne du tableau n'a été sélectionnéee"
            self.error_text.update()
            self.error_box.open = True
            self.error_box.update()
        else:
            id_ligne = int(self.id_ligne.value)
            backend.delete_devis_details(id_ligne)

            for row in self.table_edit_devis.rows[:]:
                self.table_edit_devis.rows.remove(row)

            details = backend.find_devis_details(self.m_devis.value)
            for data in details:
                self.table_edit_devis.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(f"{data[0]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(f"{data[2]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(f"{backend.search_designation(data[2])[0]}",
                                                style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(f"{data[3]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(f"{data[4]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ],
                        on_select_changed=lambda e: self.select_item(
                            e.control.cells[0].content.value,
                            e.control.cells[1].content.value,
                            e.control.cells[3].content.value,
                            e.control.cells[4].content.value
                        )
                    )
                )
            total = 0
            for row in details:
                total += (row[4] * row[3])

            total = total - (total * int(self.m_remise.value) // 100)
            self.m_total.value = str(total)
            self.m_total_lettres.value = ecrire_en_lettres(total)
            self.m_total.update()
            self.m_total_lettres.update()
            self.table_edit_devis.update()

    def update_ligne(self, e):
        if self.id_ligne.value == "":
            self.error_text.value = "Aucune ligne du tableau n'a été sélectionnée"
            self.error_text.update()
            self.error_box.open = True
            self.error_box.update()
        else:
            id_ligne = int(self.id_ligne.value)
            qte = int(self.m_qte.value)
            prix = int(self.m_prix.value)
            backend.update_devis_details(self.m_reference.value, qte, prix, id_ligne)

            for row in self.table_edit_devis.rows[:]:
                self.table_edit_devis.rows.remove(row)

            details = backend.find_devis_details(self.m_devis.value)
            for data in details:
                self.table_edit_devis.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(f"{data[0]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(f"{data[2]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(f"{backend.search_designation(data[2])[0]}",
                                                style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(f"{data[3]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(f"{data[4]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ],
                        on_select_changed=lambda e: self.select_item(
                            e.control.cells[0].content.value,
                            e.control.cells[1].content.value,
                            e.control.cells[3].content.value,
                            e.control.cells[4].content.value
                        )
                    )
                )
            total = 0
            for row in details:
                total += (row[4] * row[3])

            total = total - (total * (int(self.m_remise.value) // 100))
            self.m_total.value = str(total)
            self.m_total_lettres.value = ecrire_en_lettres(total)
            self.m_total.update()
            self.m_total_lettres.update()
            self.table_edit_devis.update()
            self.m_reference.value = ""
            self.m_qte.value = ""
            self.m_prix.value = ""
            for widget in (self.m_reference, self.m_qte, self.m_prix):
                widget.update()

    def open_new_ligne_window(self, e):
        self.new_ligne_window.open = True
        self.new_ligne_window.update()

    def close_new_ligne_window(self, e):
        self.new_ligne_window.open = False
        self.new_ligne_window.update()

    def on_change_ref_ligne(self, e):
        self.mn_des.value = backend.search_designation(self.mn_ref.value)[0]
        self.mn_prix_stock.value = backend.search_designation(self.mn_ref.value)[1]
        self.mn_des.update()
        self.mn_prix_stock.update()

    def add_new_ligne_edit_devis(self, e):
        if self.mn_ref.value == "" or self.mn_prix == "" or self.mn_qte == "":
            self.mn_error.visible = True
            self.mn_error.update()
        else:
            qte = int(self.mn_qte.value)
            prix = int(self.mn_prix.value)
            backend.add_devis_details(self.m_devis.value, self.mn_ref.value, qte, prix)

            for row in self.table_edit_devis.rows[:]:
                self.table_edit_devis.rows.remove(row)

            details = backend.find_devis_details(self.m_devis.value)
            for data in details:
                self.table_edit_devis.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(f"{data[0]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(f"{data[2]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(f"{backend.search_designation(data[2])[0]}",
                                                style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(f"{data[3]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(f"{data[4]}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ],
                        on_select_changed=lambda e: self.select_item(
                            e.control.cells[0].content.value,
                            e.control.cells[1].content.value,
                            e.control.cells[3].content.value,
                            e.control.cells[4].content.value
                        )
                    )
                )
            total = 0
            for row in details:
                total += (row[4] * row[3])

            total = total - (total * int(self.m_remise.value) // 100)
            self.m_total.value = str(total)
            self.m_total_lettres.value = ecrire_en_lettres(total)
            self.m_total.update()
            self.m_total_lettres.update()
            self.table_edit_devis.update()
            self.m_reference.value = ""
            self.m_qte.value = ""
            self.m_prix.value = ""
            for widget in (self.m_reference, self.m_qte, self.m_prix):
                widget.update()

            self.new_ligne_window.open = False
            self.new_ligne_window.update()

    def edit_remise_up(self, e):
        remise = int(self.m_remise.value)
        remise += 5
        self.m_remise.value = remise
        self.m_remise.update()

    def on_change_edit_remise(self, e):
        remise = int(self.m_remise.value)
        details = backend.find_devis_details(self.m_devis.value)
        somme = 0
        for row in details:
            somme += (row[4] * row[3])

        total = somme - ((somme * remise) // 100)

        self.m_total.value = str(total)
        self.m_total_lettres.value = ecrire_en_lettres(total)
        self.m_total.update()
        self.m_total_lettres.update()

    def edit_remise_down(self, e):
        remise = int(self.m_remise.value)
        remise -= 5
        self.m_remise.value = remise
        self.m_remise.update()

    def finish_edit_devis(self, e):
        montant = int(self.m_total.value)
        remise = int(self.m_remise.value)
        backend.update_devis(montant, remise, self.m_total_lettres.value, self.m_devis.value)
        self.edit_devis_window.scale = 0
        self.edit_devis_window.update()

        infos = backend.show_info_devis(self.search_devis.value)
        self.client_id.value = infos[0]
        self.client_name.value = backend.infos_clients(id_client=int(self.client_id.value))[1]
        self.date.value = infos[1]
        self.montant.value = infos[3]
        self.remise.value = infos[4]
        self.lettres.value = infos[5]
        self.statut.value = infos[6].upper()

        for widget in [self.client_name, self.date, self.montant, self.statut,
                       self.remise, self.lettres, self.client_id]:
            widget.update()

        details = backend.search_devis_details(self.search_devis.value)
        datas = []
        for item in details:
            dico = {
                "reference": item[1],
                "designation": item[2],
                "qte": item[3],
                "prix": item[4],
                "total": item[5]
            }
            datas.append(dico)

        for item in self.table_devis.rows[:]:
            self.table_devis.rows.remove(item)

        for data in datas:
            self.table_devis.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["reference"].upper(),
                                            style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["designation"].upper(),
                                            style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["qte"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["prix"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["total"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                    ]
                )
            )
        self.table_devis.update()

    def close_error_box(self, e):
        self.error_box.open = False
        self.error_box.update()

    def close_confirmation_box(self, e):
        self.confirmation_box.open = False
        self.confirmation_box.update()

    # delete devis_____________________________________________________
    def open_modal_dialog(self):
        self.modal_box.open = True
        self.modal_box.update()

    def close_modal_box(self, e):
        self.modal_box.open = False
        self.modal_box.update()

    def finish_delete_devis(self, e):
        backend.delete_devis_details_by_numero(self.search_devis.value)
        backend.delete_devis(self.search_devis.value)
        self.question.value = f"Devis N° {self.search_devis.value} supprimé"
        self.question.update()
        self.quit.visible = True
        self.quit.update()

    def delete_devis(self, e):
        if self.statut.value.lower() == "facturé":
            self.error_text.value = "Opération impossible. le devis est déja facturé"
            self.error_text.update()
            self.error_box.open = True
            self.error_box.update()
        elif self.statut.value == "":
            self.error_text.value = "Vous n'avez sélectionné aucun devis"
            self.error_text.update()
            self.error_box.open = True
            self.error_box.update()
        else:
            self.open_modal_dialog()

    # def build ________________________________________________________
    def build(self):
        return ft.Container(
            bgcolor="white",
            content=ft.Stack(
                controls=[
                    ft.Container(
                        # bgcolor="white",
                        opacity=1,
                        expand=True,
                        height=768,
                        padding=ft.padding.only(top=10, bottom=10, left=20, right=20),
                        content=ft.Row(
                            expand=True,
                            height=768,
                            controls=[
                                self.rail,
                                ft.VerticalDivider(width=20, color="#ededed"),
                                ft.Column(
                                    expand=True,
                                    height=768,
                                    alignment=ft.alignment.center,
                                    spacing=10,
                                    controls=[
                                        ft.Container(**title_container_style, content=self.title_page),
                                        self.filter_container,
                                        self.infos_container,
                                        self.devis_container,
                                        self.options_container,
                                    ]
                                )
                            ]
                        )
                    ),
                    self.new_devis_window,
                    self.edit_devis_window,
                    # dialog boxes
                    self.msg_error,
                    self.msg_confirm,
                    self.good_impression,
                    self.bad_impression,
                    self.facturer_window,
                    self.error_facture,
                    self.error_stock,
                    self.confirm_bordereau,
                    self.error_bordereau,
                    self.new_ligne_window,
                    self.error_box,
                    self.confirmation_box,
                    self.modal_box
                ]
            )
        )
