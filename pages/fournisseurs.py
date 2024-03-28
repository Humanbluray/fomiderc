import fontTools.misc.psCharStrings

import backend
from styles.fournisseursStyleSheet import *


class Fournisseurs(ft.UserControl):
    def __init__(self, page):
        super(Fournisseurs, self).__init__()

        # Menu ________________________________________________________________________
        self.page = page
        self.page.auto_scroll = True
        self.rail = ft.NavigationRail(
            selected_index=2,
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
                ),
            ],
            on_change=self.switch_page
        )
        # titre ___________________________________________________________________________
        self.title_page = ft.Text("FOURNISSEURS", style=ft.TextStyle(size=26, font_family="Poppins ExtraBold"))
        # filtre containers ______________________________________________________
        self.filtre = ft.Text("Filtre", style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.fournisseur_name = ft.Dropdown(**filter_name_style, on_change=self.on_change_fournisseur_name)
        self.fourniseur_id = ft.Text("", visible=False)
        self.actions = ft.Text("actions", style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.add = ft.IconButton(icon=ft.icons.ADD_OUTLINED, tooltip="Créer fournisseur", on_click=self.open_new_fournisseur_window)
        self.edit = ft.IconButton(icon=ft.icons.EDIT_OUTLINED, tooltip="Modifier fournisseur", on_click=self.open_edit_fournisseur_window)

        self.filter_container = ft.Container(
                **filter_container_style,
                content=ft.Row(
                    [
                        ft.Row([self.filtre, self.fournisseur_name, self.fourniseur_id]),
                        ft.Row([self.actions, self.add, self.edit])
                    ], alignment="spaceBetween"
                )
            )

        # container commandes table ___________________________________________________________________________
        self.table_commandes = ft.DataTable(**table_commande_style)
        self.data_not_found = ft.Text(
            "Aucune donnée trouvée",
            style=ft.TextStyle(size=14, font_family="Poppins ExtraBold", color=ft.colors.RED_300),
            visible=False)
        self.table_container = ft.Container(
            **menu_container_style, expand=True, height=200,
            content=ft.Column(
                [self.table_commandes, self.data_not_found], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True, height=200, scroll=ft.ScrollMode.ADAPTIVE, width=700
            )
        )
        # details commandes table_________________________________________________________________
        self.table_details_commandes = ft.DataTable(**table_details_style)
        self.data_not_found2 = ft.Text(
            "Aucune donnée trouvée",
            style=ft.TextStyle(size=14, font_family="Poppins ExtraBold", color="red"),
            visible=False)
        self.table_details_container = ft.Container(
            **menu_container_style, height=200, expand=True,
            content=ft.Column(
                [self.table_details_commandes, self.data_not_found2],
                expand=True, height=200, scroll=ft.ScrollMode.ADAPTIVE, width=700
            )
        )
        # details fournisseur _________________________________________________________
        self.fourn_rcmm = ft.TextField(**infos_style, label="RCMM", disabled=True)
        self.fourn_nui = ft.TextField(**infos_style, label="NUI", disabled=True)
        self.fourn_tel = ft.TextField(**infos_style, label="Contact", disabled=True)
        self.fourn_init = ft.TextField(**infos_style, label="initiales", disabled=True)
        self.fourn_mail = ft.TextField(**infos_style, label="courriel", disabled=True)
        self.fourn_comm = ft.TextField(**infos_style, label="Commercial", disabled=True)
        self.news_container = ft.Container(
            **filter_container_style,
            content=ft.Row([
                ft.Column([self.fourn_rcmm, self.fourn_nui, self.fourn_tel]),
                ft.Column([self.fourn_mail, self.fourn_comm, self.fourn_init])
            ])
        )
        # fenetre de creation fournisseur
        self.n_f_name = ft.TextField(**infos_style, label="Nom fournisseur")
        self.n_f_initiales = ft.TextField(**new_init_style, label="initiales")
        self.n_f_tel = ft.TextField(**new_tel_style, label="Contact", input_filter=ft.NumbersOnlyInputFilter())
        self.n_f_rc = ft.TextField(**infos_style, label="RCMM")
        self.n_f_nui = ft.TextField(**infos_style, label="NUI")
        self.n_f_courriel = ft.TextField(**new_mail_style, label="E-mail")
        self.n_f_comm = ft.TextField(**infos_style, label="Commercial")
        self.n_error = ft.Text(visible=False, style=ft.TextStyle(size=12, font_family="Poppins Medium", color="red"))

        self.new_fournisseur_window = ft.AlertDialog(
            title=ft.Text("Nouveau fournisseur"),
            content=ft.Column(
                [
                    self.n_f_name, self.n_f_initiales, self.n_f_tel, self.n_f_nui, self.n_f_rc, self.n_f_courriel, self.n_f_comm,
                    self.n_error
                ]
            ),
            actions=[
                ft.ElevatedButton("Creer", icon=ft.icons.ADD, icon_color="white", color="white",
                                  bgcolor="red", height=40, on_click=self.create_fournisseur),
                ft.FilledTonalButton("Quitter", height=40, on_click=self.close_new_fournisseur_window)
            ]
        )
        # fenetre de modification fournisseur
        self.m_f_id = ft.TextField(**infos_style, label="ID", disabled=True)
        self.m_f_name = ft.TextField(**infos_style, label="Nom fournisseur")
        self.m_f_initiales = ft.TextField(**new_init_style, label="initiales", disabled=True)
        self.m_f_tel = ft.TextField(**new_tel_style, label="Contact", input_filter=ft.NumbersOnlyInputFilter())
        self.m_f_rc = ft.TextField(**infos_style, label="RCMM")
        self.m_f_nui = ft.TextField(**infos_style, label="NUI")
        self.m_f_courriel = ft.TextField(**new_mail_style, label="E-mail")
        self.m_f_comm = ft.TextField(**infos_style, label="Commercial")
        self.m_error = ft.Text(visible=False, style=ft.TextStyle(size=12, font_family="Poppins Medium", color="red"))

        self.edit_fournisseur_window = ft.AlertDialog(
            title=ft.Text("Modifier fournisseur"),
            content=ft.Column(
                [
                    self.m_f_id, self.m_f_name, self.m_f_initiales,
                    self.m_f_tel, self.m_f_nui,
                    self.m_f_rc, self.m_f_courriel,
                    self.m_f_comm,
                    self.m_error
                ]
            ),
            actions=[
                ft.ElevatedButton("Modifier", icon=ft.icons.EDIT, icon_color="white", color="white",
                                  bgcolor="red", height=40, on_click=self.modifier_fournisseur),
                ft.FilledTonalButton("Quitter", height=40, on_click=self.close_edit_fournisseur_window)
            ]
        )
        # fonctions à executer sans venements ____________________________________________
        self.load_fournisseurs_list()
        self.fill_command_table()

    # functions ___________________________________________________________________________________________________
    def switch_page(self, e):
        pages = [
            "stocks", "clients", "fournisseurs", "commandes",
            "devis", "factures"
        ]
        self.page.go(f"/{pages[e.control.selected_index]}")

    def load_fournisseurs_list(self):
        for data in backend.all_fournisseur_name():
            self.fournisseur_name.options.append(
                ft.dropdown.Option(data)
            )

    def fill_command_table(self):
        for row in self.table_commandes.rows[:]:
            self.table_commandes.rows.remove(row)

        for data in backend.all_commandes():
            if data[4] == "en cours":
                self.table_commandes.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(data[0].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(data[1].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(data[2].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(data[3], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Icon(ft.icons.CIRCLE, color=ft.colors.RED_300))
                        ],
                        on_select_changed=lambda e: self.select_command(e.control.cells[0].content.value)
                    )
                )
            else:
                self.table_commandes.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(data[0].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(data[1].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(
                                ft.Text(data[2].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(data[3], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Icon(ft.icons.CIRCLE, color="green"))
                        ],
                        on_select_changed=lambda e: self.select_command(e.control.cells[0].content.value)
                    )
                )

    def on_change_fournisseur_name(self, e):
        for row in self.table_commandes.rows[:]:
            self.table_commandes.rows.remove(row)

        command_list = backend.all_commandes()
        datas = []
        for data in command_list:
            dico = {
                "N° commande": data[0],
                "date": data[1],
                "fournisseur": data[2],
                "montant": data[3],
                "statut": data[4]
            }
            datas.append(dico)

        f = self.fournisseur_name.value

        myfiler = list(filter(lambda x: f in x['fournisseur'], datas))

        if f != "":
            if len(myfiler) > 0:
                self.data_not_found.visible = False
                self.data_not_found.update()
                for data in myfiler:
                    if data["statut"] == "en cours":
                        self.table_commandes.rows.append(
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(data["N° commande"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                    ft.DataCell(ft.Text(data["date"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                    ft.DataCell(ft.Text(data["fournisseur"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                    ft.DataCell(ft.Text(data["montant"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                    ft.DataCell(ft.Icon(ft.icons.CIRCLE, color=ft.colors.RED_300))
                                ],
                                on_select_changed=lambda e: self.select_command(e.control.cells[0].content.value)
                            )
                        )
                        self.table_commandes.update()
                    else:
                        self.table_commandes.rows.append(
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(data["N° commande"].upper(),
                                                        style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                    ft.DataCell(ft.Text(data["date"],
                                                        style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                    ft.DataCell(ft.Text(data["fournisseur"].upper(),
                                                        style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                    ft.DataCell(ft.Text(data["montant"],
                                                        style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                    ft.DataCell(ft.Icon(ft.icons.CIRCLE, color="green"))
                                ],
                                on_select_changed=lambda e: self.select_command(e.control.cells[0].content.value)
                            )
                        )
                        self.table_commandes.update()

            else:
                for row in self.table_commandes.rows[:]:
                    self.table_commandes.rows.remove(row)

                self.table_commandes.update()
                self.data_not_found.visible = True
                self.data_not_found.update()

                for row in self.table_details_commandes.rows[:]:
                    self.table_details_commandes.rows.remove(row)

                self.table_details_commandes.update()
        else:
            for data in backend.all_commandes():
                if data[4] == "en cours":
                    self.table_commandes.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(
                                    ft.Text(data[0].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(data[1].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(data[2].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(ft.Text(data[3], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(ft.Icon(ft.icons.CIRCLE, color=ft.colors.RED_300))
                            ],
                            on_select_changed=lambda e: self.select_command(e.control.cells[0].content.value)
                        )
                    )
                else:
                    self.table_commandes.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(
                                    ft.Text(data[0].upper(),
                                            style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(data[1].upper(),
                                            style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(data[2].upper(),
                                            style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(data[3], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(ft.Icon(ft.icons.CIRCLE, color="green"))
                            ],
                            on_select_changed=lambda e: self.select_command(e.control.cells[0].content.value)
                        )
                    )

            self.table_commandes.update()

        infos_fournisseur = backend.infos_fournisseur_by_name(self.fournisseur_name.value)

        self.fourniseur_id.value = infos_fournisseur[0]
        self.fourn_rcmm.value = infos_fournisseur[5]
        self.fourn_nui.value = infos_fournisseur[4]
        self.fourn_tel.value = infos_fournisseur[3]
        self.fourn_init.value = infos_fournisseur[2]
        self.fourn_mail.value = infos_fournisseur[6]
        self.fourn_comm.value = infos_fournisseur[7]
        self.fourniseur_id.update()
        self.fourn_rcmm.update()
        self.fourn_nui.update()
        self.fourn_tel.update()
        self.fourn_init.update()
        self.fourn_mail.update()
        self.fourn_comm.update()

    def select_command(self, e):
        for row in self.table_details_commandes.rows[:]:
            self.table_details_commandes.rows.remove(row)

        fournisseur = e
        details_commande = backend.show_commande_details(fournisseur)

        for data in details_commande:
            self.table_details_commandes.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data[2].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(backend.search_designation(data[2])[0].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data[3], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data[4], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                    ]
                )
            )
        self.table_details_commandes.update()

    def open_new_fournisseur_window(self, e):
        self.n_error.visible = False
        self.n_error.update()
        self.new_fournisseur_window.open = True
        self.new_fournisseur_window.update()

    def close_new_fournisseur_window(self, e):
        self.new_fournisseur_window.open = False
        self.new_fournisseur_window.update()

    def create_fournisseur(self, e):
        if self.n_f_initiales.value in backend.all_initiales_fournisseurs():
            self.n_error.value = "Initiales déja utlisées!"
            self.n_error.visible = True
            self.n_error.update()
        else:
            if self.n_f_name.value == "" or self.n_f_initiales.value == "":
                self.n_error.value = "les champs nom et initiales sont obligatoires!"
                self.n_error.visible = True
                self.n_error.update()
            else:
                backend.add_fournisseur(self.n_f_name.value, self.n_f_initiales.value, self.n_f_tel.value,
                                        self.n_f_nui.value, self.n_f_rc.value, self.n_f_courriel.value, self.n_f_comm.value)
                self.n_error.value = "fournisseur ajouté"
                self.n_error.visible = True
                self.n_error.update()

                for widget in (self.n_f_name, self.n_f_initiales, self.n_f_tel, self.n_f_nui, self.n_f_rc, self.n_f_courriel, self.n_f_comm):
                    widget.value = ""
                    widget.update()

    def open_edit_fournisseur_window(self, e):
        if self.fourniseur_id.value is None or self.fourniseur_id.value == "":
            pass
        else:
            self.m_f_id.value = self.fourniseur_id.value
            self.m_f_name.value = self.fournisseur_name.value
            self.m_f_initiales.value = self.fourn_init.value
            self.m_f_tel.value = self.fourn_tel.value
            self.m_f_nui.value = self.fourn_nui.value
            self.m_f_rc.value = self.fourn_rcmm.value
            self.m_f_courriel.value = self.fourn_mail.value
            self.m_f_comm.value = self.fourn_comm.value

            for widget in (self.m_f_id, self.m_f_name, self.m_f_initiales, self.m_f_tel, self.m_f_nui, self.m_f_rc, self.m_f_courriel, self.m_f_comm):
                widget.update()

            self.m_error.visible = False
            self.m_error.update()
            self.edit_fournisseur_window.open = True
            self.edit_fournisseur_window.update()

    def close_edit_fournisseur_window(self, e):
        self.edit_fournisseur_window.open = False
        self.edit_fournisseur_window.update()

    def modifier_fournisseur(self, e):
        if self.m_f_name.value == "":
            self.m_error.value = "le nom du fournisseur est vide!"
            self.m_error.visible = True
            self.m_error.update()
        else:
            idval = int(self.m_f_id.value)
            backend.update_fournisseur_by_id(self.m_f_name.value, self.m_f_initiales.value, self.m_f_tel.value, self.m_f_nui.value,
                                             self.m_f_rc.value, self.m_f_courriel.value, self.m_f_comm.value, idval)
            self.m_error.value = "fournisseur modifié"
            self.m_error.visible = True
            self.m_error.update()

            for widget in (self.m_f_name, self.m_f_initiales, self.m_f_tel, self.m_f_nui, self.m_f_rc, self.m_f_courriel, self.m_f_comm, self.m_f_id):
                widget.value = ""
                widget.update()

    def build(self):
        return ft.Container(
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
                        height=820,
                        alignment=ft.alignment.center,
                        spacing=10,
                        controls=[
                            ft.Container(**menu_container_style, content=self.title_page),
                            self.filter_container,
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            self.table_container, self.table_details_container
                                        ], expand=True, height=500
                                    ),
                                    self.news_container
                                ], vertical_alignment=ft.CrossAxisAlignment.START
                            )

                        ]
                    ),
                    # dialogs boxes
                    self.new_fournisseur_window,
                    self.edit_fournisseur_window
                ]
            )
        )
