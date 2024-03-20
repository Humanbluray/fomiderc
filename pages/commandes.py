import backend
from styles.commandeStyleSheet import *
from others.useful_fonctions import milSep, ecrire_en_lettres
from datetime import date, datetime


class Commandes(ft.UserControl):
    def __init__(self, page):
        super(Commandes, self).__init__()

        # Menu ________________________________________________________________________
        self.page = page
        self.page.auto_scroll = True
        self.rail = ft.NavigationRail(
            selected_index=3,
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
        self.title_page = ft.Text("COMMANDES", style=ft.TextStyle(size=26, font_family="Poppins ExtraBold"))

        self.filtre = ft.Text("Filtre",
                              style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.search_commande = ft.Dropdown(**drop_style, label="N° Commande", on_change=self.on_change_command)
        self.client_id = ft.Text(visible=False)
        self.actions = ft.Text("actions",
                               style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.add = ft.IconButton(icon=ft.icons.ADD_OUTLINED, tooltip="Créer commande", on_click=self.open_new_commande_window)
        self.receive = ft.IconButton(icon=ft.icons.INVENTORY_OUTLINED, tooltip="Modifier commande", on_click=self.open_receipt_window)

        self.filter_container = ft.Container(
            **filter_container_style,
            content=ft.Row(
                [
                    ft.Row([self.filtre, self.search_commande, self.client_id]),
                    ft.Row([self.actions, self.add, self.receive])
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        # infos du devis __________________________________________________________________________________
        self.fournisseur = ft.TextField(**infos_style, label="Nom du fournisseur", disabled=True)
        self.date = ft.TextField(**infos_style, disabled=True, label="date")
        self.montant = ft.TextField(**infos_style, disabled=True, label="Montant")
        self.lettres = ft.TextField(**lettres_style, disabled=True, label="Montant en lettres")
        self.statut = ft.TextField(**infos_style, disabled=True, label="statut")

        self.infos_container = ft.Container(
            **menu_container_style,
            content=ft.Column(
                [
                    ft.Row([self.fournisseur, self.date, self.montant, self.statut]),
                    self.lettres
                ]
            )
        )
        # table details devis__________________________________________________________________________
        self.table_commande = ft.DataTable(**table_commande_style)
        self.commande_container = ft.Container(
            **menu_container_style,
            height=300, width=650,
            content=ft.Column(
                [self.table_commande], expand=True,
                height=360,
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        # Stack ecran de creatiuon de commande________________________________________________________
        self.n_com = ft.TextField(**infos_style, disabled=True)
        self.n_fournisseur = ft.Dropdown(**drop_style, label="Fournisseur", on_change=self.on_change_new_fournisseur)
        self.n_fournisseur_id = ft.Text(visible=False)
        self.n_initiales = ft.Text(visible=False)

        self.ct_first = ft.Container(
            **menu_container_style,
            content=ft.Row(
                [
                    ft.Row([self.n_com, self.n_fournisseur_id]),
                    ft.Row([self.n_fournisseur, self.n_fournisseur_id, self.n_initiales])
                ]
            )
        )
        self.reference = ft.Dropdown(**drop_style, on_change=self.on_change_ref, label="reference")
        self.designation = ft.TextField(**designation_style, label="designation", disabled=True)
        self.qte = ft.TextField(**qte_style, label="qté", input_filter=ft.NumbersOnlyInputFilter())
        self.prix = ft.TextField(**prix_style, label="prix", input_filter=ft.NumbersOnlyInputFilter())
        self.total = ft.TextField(**infos_style, label="total", disabled=True)
        self.total_lettres = ft.TextField(**lettres_style, disabled=True)
        self.button_add = ft.ElevatedButton(
            icon=ft.icons.ADD, text="Ajouter",
            icon_color="white", color="white", height=40,
            bgcolor=ft.colors.BLACK87,
            on_click=self.add_table_line
        )
        self.ct_second = ft.Container(
            **menu_container_style,
            content=ft.Column(
                [
                    ft.Row([self.reference, self.designation]),
                    ft.Row([self.qte, self.prix, self.total]),
                    ft.Row([self.total_lettres, self.button_add])
                ]
            )
        )

        self.table_new_commande = ft.DataTable(**table_details_style)
        self.new_commande_window = ft.Card(
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
                                ft.Text("Créer commande", style=ft.TextStyle(size=20, font_family="Poppins Regular"))
                            ]
                        ),
                        self.ct_first,
                        self.ct_second,
                        ft.Container(
                            **menu_container_style,
                            content=ft.Column(
                                [self.table_new_commande],
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
                                    on_click=self.valider_commande
                                ),
                                ft.ElevatedButton(
                                    "Quitter",
                                    icon=ft.icons.ARROW_BACK_OUTLINED,
                                    icon_color="white", color="white", bgcolor=ft.colors.BLACK87, height=40,
                                    on_click=self.close_new_commande_window
                                )
                            ]
                        )

                    ]
                )
            )
        )
        # receptions de commandes ______________________________________________________________
        self.m_com = ft.TextField(**infos_style, label="N° Commande", disabled=True)
        self.receipt_number = ft.TextField(**infos_style, label="N° Bon recption", disabled=True)
        self.delivery_number = ft.TextField(**infos_style, label="Bon de livraison")
        self.delivery_date = ft.TextField(**infos_style, label="date", disabled=True)
        self.check_deliv_number = ft.Text(visible=False, style=ft.TextStyle(size=13, color="red", font_family="Poppins Medium"))

        self.date_picker = ft.DatePicker(
            on_change=self.change_date,
            on_dismiss=None,
            first_date=datetime(2024, 1, 1),
            last_date=datetime(2030, 12, 1),
        )
        self.date_button = ft.ElevatedButton(
            bgcolor=ft.colors.BLACK87,
            text="Pick date",
            height=40,
            icon=ft.icons.CALENDAR_MONTH_OUTLINED,
            icon_color="white",
            color="white",
            on_click=lambda _: self.date_picker.pick_date(),
        )
        self.receipt_window = ft.AlertDialog(
            title=ft.Text("Reception de commande"),
            content=ft.Column(
                [
                    self.m_com, self.receipt_number, self.delivery_number, self.delivery_date, self.date_button, self.check_deliv_number
                ],
                height=300
            ),
            actions=[
                ft.ElevatedButton(
                    text="Valider réception", color="white", bgcolor="red", height=40,
                    icon=ft.icons.INVENTORY_OUTLINED, icon_color="white", on_click=self.create_receipt
                ),
                ft.FilledTonalButton(
                    text="fermer", height=40, on_click=self.close_receipt_window
                )
            ]
        )

        # sel a dialog box for mutiples errors ____________________________________________________________________________
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
        # Fonctions à charger sans évènements
        self.load_all_commandes()
        self.load_all_fournisseurs()
        self.load_edit_ref_list()

    # functions __________________________________________________________________________________________
    def switch_page(self, e):
        pages = [
            "stocks", "clients", "fournisseurs", "commandes",
            "devis", "factures"
        ]
        self.page.go(f"/{pages[e.control.selected_index]}")

    def open_new_commande_window(self, e):
        self.new_commande_window.scale = 1
        self.new_commande_window.update()

    def load_all_commandes(self):
        for data in backend.list_commandes():
            self.search_commande.options.append(
                ft.dropdown.Option(data)
            )

    def load_all_fournisseurs(self):
        for data in backend.all_fournisseur_name():
            self.n_fournisseur.options.append(
                ft.dropdown.Option(data)
            )

    def on_change_ref(self, e):
        self.designation.value = backend.search_designation(self.reference.value)[0].upper()
        self.designation.update()

    def on_change_new_fournisseur(self, e):
        self.n_fournisseur_id.value = backend.infos_fournisseur_by_name(self.n_fournisseur.value)[0]
        f_id = int(self.n_fournisseur_id.value)
        self.n_com.value = backend.create_numero_commande(f_id)
        self.n_com.update()
        self.n_fournisseur_id.update()

    def load_edit_ref_list(self):
        for name in backend.all_references_stock():
            self.reference.options.append(
                ft.dropdown.Option(name)
            )

    def on_change_command(self, e):
        details = backend.show_commande_details(self.search_commande.value)

        self.m_com.value = self.search_commande.value
        self.m_com.update()
        self.receipt_number.value = self.search_commande.value.replace("CM", "RC")
        self.receipt_number.update()

        for row in self.table_commande.rows[:]:
            self.table_commande.rows.remove(row)

        for data in details:
            self.table_commande.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data[2].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(backend.search_designation(data[2])[0].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data[3], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(milSep(data[4]), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(str(milSep(data[4] * data[3])), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                    ]
                )
            )
        self.table_commande.update()

        infos = backend.show_infos_commandes(self.search_commande.value)
        self.montant.value = infos[4]
        self.lettres.value = infos[5].upper()
        self.fournisseur.value = backend.infos_fournisseur_by_id(infos[3])[1]
        self.date.value = infos[2]
        self.statut.value = infos[6].upper()
        self.montant.update()
        self.lettres.update()
        self.fournisseur.update()
        self.date.update()
        self.statut.update()

    def add_table_line(self, e):
        if self.prix.value != "" and self.qte.value != "":
            tot = int(self.prix.value) * int(self.qte.value)
            self.table_new_commande.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(self.reference.value.upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(self.designation.value.upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(self.qte.value, style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(self.prix.value, style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(tot, style=ft.TextStyle(font_family="poppins Medium", size=11))),
                    ]
                )
            )
            # recuperer la liste des lignes dans un tableau
            data_list = []
            lines = self.table_new_commande.rows[:]  # liste de DataRow
            for i in range(len(lines)):
                sous_liste = []
                for j in range(len(lines[i].cells)):
                    sous_liste.append(lines[i].cells[j].content.value)
                data_list.append(sous_liste)

            somme = 0

            for row in data_list:
                somme += int(row[2]) * int(row[3])

            self.total.value = str(somme)
            self.total_lettres.value = ecrire_en_lettres(int(self.total.value))

            self.reference.value = ""
            self.prix.value = ""
            self.qte.value = ""
            self.reference.update()
            self.table_new_commande.update()
            self.total.update()
            self.montant.update()
            self.prix.update()
            self.qte.update()
            self.total_lettres.update()
        else:
            pass

    def open_receipt_window(self, e):
        if self.search_commande.value is None:
            self.error_text.value = "Aucune commande sélectionnée"
            self.error_text.update()
            self.error_box.open = True
            self.error_box.update()
        elif self.statut.value.lower() == "clôturée":
            self.error_text.value = "La commande a déja été réceptionnée"
            self.error_text.update()
            self.error_box.open = True
            self.error_box.update()
        else:
            self.receipt_window.open = True
            self.receipt_window.update()

    def close_receipt_window(self, e):
        self.receipt_window.open = False
        self.receipt_window.update()

    def create_receipt(self, e):
        if self.delivery_number.value == "" or self.delivery_number is None:
            self.check_deliv_number.value = "Bon de livraison obligatoire"
            self.check_deliv_number.visible = True
            self.check_deliv_number.update()

        elif self.m_com.value is None or self.m_com.value == "":
            self.check_deliv_number.value = "Opération impossible"
            self.check_deliv_number.visible = True
            self.check_deliv_number.update()

        else:
            # fill details recption
            data_list = backend.commande_details_by_num(self.m_com.value)

            for data in data_list:
                backend.add_reception_details(self.receipt_number.value, data[0], data[1], data[2])
                # update stock by ref
                ancien_stock = backend.find_stock_ref(data[0])
                nouveau_stock = data[1] + ancien_stock
                backend.update_stock(nouveau_stock, data[0])

                # update price by ref
                ancien_prix = backend.find_prix_ref(data[0])
                nouveau_prix = data[2]
                pmp = ((ancien_prix * ancien_stock) + (nouveau_prix * data[1])) // nouveau_stock
                backend.maj_prix_ref(pmp, data[0])

                # add historique line
                backend.add_historique(data[0], "RC", self.m_com.value, ancien_stock, data[1], nouveau_stock)

            # fill table reception
            backend.add_reception(self.receipt_number.value, self.delivery_number.value, self.m_com.value, self.delivery_date.value)

            # update status command
            backend.update_commande_statut("clôturée", self.m_com.value)

            self.check_deliv_number.value = "Bon de récption créé"
            self.check_deliv_number.visible = True
            self.check_deliv_number.update()

            for widget in (self.m_com, self.receipt_number, self.delivery_number, self.delivery_date):
                widget.value = ""
                widget.update()

    def change_date(self,e ):
        self.delivery_date.value = self.date_picker.value
        self.delivery_date.update()

    def valider_commande(self, e):
        # add commande
        if self.n_com.value == "":
            self.error_text.value = "Aucun fournisseur sélectionné"
            self.error_text.update()
            self.error_box.open = True
            self.error_box.update()

        else:
            montant = int(self.total.value)
            fournisseur_id = int(self.n_fournisseur_id.value)
            backend.add_commande(self.n_com.value, date.today(), fournisseur_id, montant, self.total_lettres.value)

            data_list = []
            lines = self.table_new_commande.rows[:]  # liste de DataRow
            for i in range(len(lines)):
                sous_liste = []
                for j in range(len(lines[i].cells)):
                    sous_liste.append(lines[i].cells[j].content.value)
                data_list.append(sous_liste)

            # add commandes details
            for data in data_list:
                backend.add_commande_detail(self.n_com.value, data[0], data[2], data[3])

            self.n_fournisseur.value = ""
            self.reference.value = ""
            self.n_fournisseur.update()
            self.reference.update()
            self.n_com.value = ""
            self.n_com.update()
            self.designation.value = ""
            self.designation.update()
            self.total.value = ""
            self.total.update()
            self.total_lettres.value = ""
            self.total_lettres.update()
            self.confirmation_text.value = "Commande validée"
            self.confirmation_text.update()
            self.confirmation_box.open = True
            self.confirmation_box.update()

            for row in self.table_new_commande.rows[:]:
                self.table_new_commande.rows.remove(row)

            self.table_new_commande.update()

    def close_error_box(self, e):
        self.error_box.open = False
        self.error_box.update()

    def close_confirmation_box(self, e):
        self.confirmation_box.open = False
        self.confirmation_box.update()

    def close_new_commande_window(self, e):
        self.new_commande_window.scale = 0
        self.new_commande_window.update()

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
                                        ft.Container(**menu_container_style, content=self.title_page),
                                        self.filter_container,
                                        self.infos_container,
                                        self.commande_container,
                                    ]
                                )
                            ]
                        )
                    ),
                    self.new_commande_window,
                    # dialog boxes
                    self.error_box,
                    self.confirmation_box,
                    self.receipt_window,
                    self.date_picker
                ]
            )
        )