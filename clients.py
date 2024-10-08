import backend
from clientStyleSheet import *


class Clients(ft.UserControl):
    def __init__(self, page):
        super(Clients, self).__init__()

        # Menu ________________________________________________________________________
        self.page = page
        self.page.auto_scroll = True
        self.rail = ft.NavigationRail(
            selected_index=1,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=140,
            min_extended_width=400,
            leading=ft.Image(src="logo.jpg", height=80, width=80),
            group_alignment=-0.7,
            indicator_color="#3410B9",
            indicator_shape=ft.ContinuousRectangleBorder(radius=20),
            elevation=0,
            bgcolor="white",
            on_change=self.switch_page,
            destinations=[
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.HOME_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.HOME, color="white"),
                    label_content=ft.Text("Stocks", style=ft.TextStyle(font_family="Poppins Medium"))
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.GROUP_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.GROUP, color="white"),
                    label_content=ft.Text("Clients", style=ft.TextStyle(font_family="Poppins Medium")),

                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.GROUPS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.GROUPS, color="white"),
                    label_content=ft.Text("Fournisseurs", style=ft.TextStyle(font_family="Poppins Medium")),
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK, color="white"),
                    label_content=ft.Text("Commandes", style=ft.TextStyle(font_family="Poppins Medium")),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.MONETIZATION_ON_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.MONETIZATION_ON, color="white"),
                    label_content=ft.Text("Devis", style=ft.TextStyle(font_family="Poppins Medium")),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PAYMENTS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.PAYMENTS, color="white"),
                    label_content=ft.Text("Factures", style=ft.TextStyle(font_family="Poppins Medium")),
                ),
            ]
        )
        # page title ____________________________________________________________________________________________________
        self.title_page = ft.Text("CLIENTS", style=ft.TextStyle(size=26, font_family="Poppins ExtraBold", color="white"))

        # widgets du filter container ___________________________________________________________________________________
        self.client_id = ft.Text("", visible=False)
        self.filtre_clients = ft.TextField(**standard_tf_style, hint_text="rechercher client...",
                                           on_change=self.on_change_look_clients)
        self.choix = ft.Text("", visible=False)
        self.search_nomclient = ft.TextField(**search_style, on_change=self.changement_client)
        self.afficher_infos = ft.IconButton(icon_color="black", icon=ft.icons.PERSON_SEARCH_OUTLINED, tooltip="rechercher",
                                            on_click=self.open_select_cli_windows)
        self.look_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("Nom client", style=ft.TextStyle(size=12, font_family="Poppins Black")))],
            rows=[]
        )
        self.select_cli_window = ft.Card(
            elevation=30, expand=True,
            top=5, left=300,
            height=700, width=500,
            scale=ft.transform.Scale(scale=0),
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN),
            content=ft.Container(
                padding=10,
                bgcolor="white",
                content=ft.Column(
                    expand=True, height=600,
                    controls=[
                        ft.Text("Selectionner client", size=20, font_family="Poppins Regular"),
                        ft.Divider(height=20, color="transparent"),
                        self.filtre_clients,
                        self.choix,
                        ft.Column([self.look_table], scroll=ft.ScrollMode.ADAPTIVE, height=500),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
        # actions
        self.actions = ft.Text("actions", style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.add = ft.IconButton(icon_color="black", icon=ft.icons.ADD_OUTLINED, tooltip="Créer client", on_click=self.open_new_cli_window)
        self.edit = ft.IconButton(icon_color="black", icon=ft.icons.EDIT_OUTLINED, tooltip="Modifier client", on_click=self.open_edit_cli_window)

        self.filter_container = ft.Container(
            **filter_container_style,
            content=ft.Row(
                [
                    ft.Row(
                        [
                            self.search_nomclient, self.client_id,
                            self.afficher_infos,
                         ]
                           ),
                    ft.Row([self.actions, self.add, self.edit])
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        # widget du conteneur factures _______________________________________________________________________________________________________
        self.table_factures = ft.DataTable(**table_factures_style)
        self.data_not_found = ft.Text(
            "Aucune donnée trouvée",
            style=ft.TextStyle(size=14, font_family="Poppins ExtraBold", color="#3410B9"),
            visible=False
        )
        self.table_factures_container = ft.Container(
            **table_container_style,
            expand=True,
            height=250, width=600,
            content=ft.Column(
                [self.table_factures, self.data_not_found],
                expand=True,
                height=250, width=600,
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        # table des details de factures ___________________________________________________________________________________________________
        self.table_details_facture = ft.DataTable(**table_details_factures_style)
        self.info_detfac = ft.Text("    Détails de la facture", style=ft.TextStyle(color="grey", size=12, font_family="Poppins Medium"))
        self.table_details_factures_container = ft.Container(
            **table_container_style,
            expand=True,
            height=250, width=800,
            content=ft.Column(
                expand=True,
                height=250, scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.table_details_facture]
            )
        )
        self.table_paiments = ft.DataTable(**table_paiements_style)
        self.table_paiments_container = ft.Container(
            **table_container_style,
            expand=True,
            height=250, width=350,
            content=ft.Column(
                expand=True,
                height=250, scroll=ft.ScrollMode.ADAPTIVE,
                controls=[self.table_paiments]
            )
        )
        # Widgets des news container ___________________________________________________________________________
        self.cli_rcmm = ft.TextField(**infos_style, label="RCMM", disabled=True)
        self.cli_nui = ft.TextField(**infos_style, label="NUI", disabled=True)
        self.cli_tel = ft.TextField(**infos_style, label="Contact", disabled=True)
        self.cli_init = ft.TextField(**infos_style, label="initiales", disabled=True)
        self.cli_mail = ft.TextField(**infos_style, label="courriel", disabled=True)
        self.cli_comm = ft.TextField(**infos_style, label="Commercial", disabled=True)
        self.news_container = ft.Container(
            **filter_container_style,
            content=ft.Row([
                ft.Column([self.cli_rcmm, self.cli_nui, self.cli_tel]),
                ft.Column([self.cli_mail, self.cli_comm, self.cli_init])
            ])
        )
        # fenetre creer client ____________________________________________________________________________
        self.n_cli_nom = ft.TextField(**new_cli_style, label="Nom")
        self.n_cli_rcmm = ft.TextField(**new_cli_style, label="RCMM")
        self.n_cli_nui = ft.TextField(**new_cli_style, label="NUI")
        self.n_cli_tel = ft.TextField(**contact_style, label="Contact")
        self.n_cli_init = ft.TextField(**initiales_style, label="initiales")
        self.n_cli_mail = ft.TextField(**courrier_style, label="courriel")
        self.n_cli_comm = ft.TextField(**new_cli_style, label="Commercial")
        self.error = ft.Text(visible=False,
                             style=ft.TextStyle(font_family="Poppins Medium", size=12, color="red"))
        self.new_cli_window = ft.AlertDialog(
            title=ft.Text("Nouveau client"),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=8,
                controls=[self.n_cli_nom, self.n_cli_init, self.n_cli_tel,
                          self.n_cli_nui, self.n_cli_rcmm, self.n_cli_mail, self.n_cli_comm, self.error]
            ),
            actions=[
                ft.ElevatedButton(
                    text="créer", icon=ft.icons.ADD,
                    on_click=self.add_client,
                    icon_color="white", color="white", bgcolor="#3410B9",
                    height=50
                ),
                ft.FilledTonalButton(text="fermer", on_click=self.close_new_cli_window, height=50)
            ]
        )
        # fenetre pour modifier client _________________________________________________________________
        self.m_cli_id = ft.TextField(**new_cli_style, label="id", disabled=True)
        self.m_cli_nom = ft.TextField(**new_cli_style, label="Nom")
        self.m_cli_rcmm = ft.TextField(**new_cli_style, label="RCMM")
        self.m_cli_nui = ft.TextField(**new_cli_style, label="NUI")
        self.m_cli_tel = ft.TextField(**new_cli_style, label="Contact")
        self.m_cli_init = ft.TextField(**new_cli_style, label="initiales", disabled=True)
        self.m_cli_mail = ft.TextField(**courrier_style, label="courriel")
        self.m_cli_comm = ft.TextField(**new_cli_style, label="Commercial")
        self.confirm = ft.Text(visible=False, style=ft.TextStyle(font_family="Poppins Medium", size=12, color="red"))
        self.edit_cli_window = ft.AlertDialog(
            title=ft.Text("Modifier client"),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=8,
                controls=[self.m_cli_id, self.m_cli_nom, self.m_cli_init, self.m_cli_tel, self.m_cli_nui, self.m_cli_rcmm,
                          self.m_cli_mail, self.m_cli_comm, self.confirm]
            ),
            actions=[
                ft.ElevatedButton(
                    text="Modifier", icon=ft.icons.EDIT,
                    on_click=self.update_cli,
                    icon_color="white", color="white", bgcolor="#3410B9",
                    height=50
                ),
                ft.FilledTonalButton(text="fermer", on_click=self.close_edit_cli_window, height=50)
            ]
        )
        # self.load_clients_list()
        self.load_all_client_name()

    # functions _______________________________________________________________________________________________________________________________
    def switch_page(self, e):
        pages = [
            "stocks", "clients", "fournisseurs", "commandes",
            "devis", "factures"
        ]
        self.page.go(f"/{pages[e.control.selected_index]}")

    def open_select_cli_windows(self, e):
        self.select_cli_window.scale = 1
        self.select_cli_window.update()

    def load_all_client_name(self):
        for row in self.look_table.rows[:]:
            self.look_table.rows.remove(row)

        datas = backend.all_clients()
        for data in datas:
            self.look_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(f"{data.upper()}", style=ft.TextStyle(font_family="poppins Medium", size=12))
                        )
                    ],
                    on_select_changed=lambda e: self.on_select_change_filtre(e.control.cells[0].content.value)
                )
            )

    def on_change_look_clients(self, e):
        for row in self.look_table.rows[:]:
            self.look_table.rows.remove(row)

        datas = []
        for data in backend.all_clients():
            dico = {"client": data}
            datas.append(dico)

        myfiler = list(filter(lambda x: self.filtre_clients.value.lower() in x['client'].lower(), datas))

        for row in myfiler:
            self.look_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(f"{row['client']}", style=ft.TextStyle(font_family="Poppins Medium", size=12)))
                ],
                    on_select_changed=lambda e: self.on_select_change_filtre(e.control.cells[0].content.value)
                )
            )
        self.look_table.update()

    def on_select_change_filtre(self, e):
        self.choix.value = e
        self.choix.update()
        self.search_nomclient.value = self.choix.value
        self.search_nomclient.update()
        self.select_cli_window.scale = 0
        self.select_cli_window.animate_scale = ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT)
        self.select_cli_window.update()
        self.changement_client_2()

    def changement_client(self, e):
        self.client_id.value = backend.id_client_by_name(self.search_nomclient.value)[0]
        self.client_id.update()
        cli_id = int(self.client_id.value)
        datas = []

        for item in backend.factures_client(cli_id):
            dico = {"facture": item[1], "montant": item[2], "perçu": item[3],
                    "reste": item[4], "statut": item[5]}
            datas.append(dico)

        for item in self.table_factures.rows[:]:
            self.table_factures.rows.remove(item)

        for item in self.table_details_facture.rows[:]:
            self.table_details_facture.rows.remove(item)

        self.table_details_facture.update()

        if len(datas) > 0:

            for data in datas:
                if data["statut"] == "en cours":
                    self.table_factures.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(data["facture"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Text(data["montant"],
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(
                                    ft.Text(data["perçu"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(
                                    ft.Text(data["reste"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Text(data["statut"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Icon(ft.icons.CIRCLE, size=20, color=ft.colors.RED)),
                            ],
                            on_select_changed=lambda e: self.select_facture(e.control.cells[0].content.value)
                        )
                    )
                else:
                    self.table_factures.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(data["facture"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Text(data["montant"],
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(
                                    ft.Text(data["perçu"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(
                                    ft.Text(data["reste"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Text(data["statut"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Icon(ft.icons.CIRCLE, size=20, color=ft.colors.GREEN)),
                            ],
                            on_select_changed=lambda e: self.select_facture(e.control.cells[0].content.value)
                        )
                    )

            self.data_not_found.visible = False
            self.data_not_found.update()
            self.table_factures.update()
        else:
            self.data_not_found.visible = True
            self.data_not_found.update()
            self.table_factures.update()

        infos = backend.infos_clients(self.client_id.value)
        self.cli_rcmm.value = infos[5]
        self.cli_nui.value = infos[4]
        self.cli_tel.value = infos[3]
        self.cli_init.value = infos[2]
        self.cli_mail.value = infos[6]
        self.cli_comm.value = infos[7]
        self.cli_rcmm.update()
        self.cli_nui.update()
        self.cli_tel.update()
        self.cli_init.update()
        self.cli_mail.update()
        self.cli_comm.update()

    def changement_client_2(self):
        self.client_id.value = backend.id_client_by_name(self.search_nomclient.value)[0]
        self.client_id.update()
        cli_id = int(self.client_id.value)

        datas = []
        for item in backend.factures_client(cli_id):
            dico = {"facture": item[1], "montant": item[2], "perçu": item[3],
                    "reste": item[4], "statut": item[5]}
            datas.append(dico)

        for item in self.table_factures.rows[:]:
            self.table_factures.rows.remove(item)

        for item in self.table_details_facture.rows[:]:
            self.table_details_facture.rows.remove(item)

        self.table_details_facture.update()

        if len(datas) > 0:

            for data in datas:
                if data["statut"] == "en cours":
                    self.table_factures.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(data["facture"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Text(data["montant"],
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(
                                    ft.Text(data["perçu"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(
                                    ft.Text(data["reste"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Text(data["statut"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Icon(ft.icons.CIRCLE, size=20, color=ft.colors.RED)),
                            ],
                            on_select_changed=lambda e: self.select_facture(e.control.cells[0].content.value)
                        )
                    )
                else:
                    self.table_factures.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(data["facture"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Text(data["montant"],
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(
                                    ft.Text(data["perçu"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(
                                    ft.Text(data["reste"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Text(data["statut"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=12))),
                                ft.DataCell(ft.Icon(ft.icons.CIRCLE, size=20, color=ft.colors.GREEN)),
                            ],
                            on_select_changed=lambda e: self.select_facture(e.control.cells[0].content.value)
                        )
                    )

            self.data_not_found.visible = False
            self.data_not_found.update()
            self.table_factures.update()
        else:
            self.data_not_found.visible = True
            self.data_not_found.update()
            self.table_factures.update()

        infos = backend.infos_clients(self.client_id.value)
        self.cli_rcmm.value = infos[5]
        self.cli_nui.value = infos[4]
        self.cli_tel.value = infos[3]
        self.cli_init.value = infos[2]
        self.cli_mail.value = infos[6]
        self.cli_comm.value = infos[7]
        self.cli_rcmm.update()
        self.cli_nui.update()
        self.cli_tel.update()
        self.cli_init.update()
        self.cli_mail.update()
        self.cli_comm.update()

    def select_facture(self, e):
        selected_facture = e
        self.info_detfac.value = f"   Details de la facture: {e}"
        self.info_detfac.update()

        datas = []
        for item in backend.search_factures_details(selected_facture):
            dico={"reference": item[1], "designation": item[2], "qté": item[3], "prix": item[4], "total": item[5]}
            datas.append(dico)

        for item in self.table_details_facture.rows[:]:
            self.table_details_facture.rows.remove(item)

        for data in datas:
            self.table_details_facture.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["reference"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["designation"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["qté"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["prix"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["total"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Icon(ft.icons.LOCK_OPEN_OUTLINED, size=14)),
                    ],
                )
            )
        self.table_details_facture.update()

        # table des paiements
        for row in self.table_paiments.rows[:]:
            self.table_paiments.rows.remove(row)

        datas = []
        for item in backend.reglements_par_facture(selected_facture):
            dico = {"montant": item[0], "type": item[1], "date": item[2]}
            datas.append(dico)

        for data in datas:
            self.table_paiments.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["montant"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(
                            ft.Text(data["type"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(
                            ft.Text(data["date"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                    ]
                )
            )
        self.table_paiments.update()

    def open_new_cli_window(self, e):
        self.new_cli_window.open = True
        self.new_cli_window.update()

    def close_new_cli_window(self, e):
        self.error.visible = False
        self.error.update()
        self.new_cli_window.open = False
        self.new_cli_window.update()

    def add_client(self, e):
        if self.n_cli_nom.value != "" and self.n_cli_init.value != "":
            if self.n_cli_init.value not in backend.all_initiales():
                backend.add_client(
                    self.n_cli_nom.value,
                    self.n_cli_init.value,
                    self.n_cli_tel.value,
                    self.n_cli_nui.value,
                    self.n_cli_rcmm.value,
                    self.n_cli_mail.value,
                    self.n_cli_comm.value
                )
                self.error.value = "Client ajouté!"
                self.error.visible = True
                self.error.update()

                for widget in [self.n_cli_nom, self.n_cli_init, self.n_cli_tel, self.n_cli_nui, self.n_cli_rcmm,self.n_cli_mail, self.n_cli_comm]:
                    widget.value = ""
                    widget.update()
            else:
                self.error.value = "Ces initiales sont déja utilisées"
                self.error.visible = True
                self.error.update()

        else:
            self.error.value = "les champs noms et initiales sont obligatoires"
            self.error.visible = True
            self.error.update()

    def open_edit_cli_window(self, e):
        self.m_cli_nom.value = self.search_nomclient.value
        self.m_cli_rcmm.value = self.cli_rcmm.value
        self.m_cli_nui.value = self.cli_nui.value
        self.m_cli_tel.value = self.cli_tel.value
        self.m_cli_init.value = self.cli_init.value
        self.m_cli_mail.value = self.cli_mail.value
        self.m_cli_comm.value = self.cli_comm.value
        self.m_cli_id.value = self.client_id.value

        for widget in [self.m_cli_id, self.m_cli_nom, self.m_cli_init, self.m_cli_tel,
                       self.m_cli_nui, self.m_cli_rcmm, self.m_cli_mail, self.m_cli_comm]:
            widget.update()

        self.edit_cli_window.open = True
        self.edit_cli_window.update()

    def close_edit_cli_window(self, e):
        self.confirm.visible = False
        self.confirm.update()
        self.edit_cli_window.open = False
        self.edit_cli_window.update()

    def update_cli(self, e):
        if self.m_cli_nom != "":
            backend.update_client(
                self.m_cli_nom.value,
                self.m_cli_init.value,
                self.m_cli_tel.value,
                self.m_cli_nui.value,
                self.m_cli_rcmm.value,
                self.m_cli_mail.value,
                self.m_cli_comm.value,
                self.m_cli_id.value
            )
            for widget in [self.m_cli_id, self.m_cli_nom, self.m_cli_init, self.m_cli_tel,
                           self.m_cli_nui, self.m_cli_rcmm, self.m_cli_mail, self.m_cli_comm]:
                widget.value = ""
                widget.update()

            self.confirm.value = "Client mis à jour"
            self.confirm.visible = True
            self.confirm.update()

        else:
            self.confirm.value = "le champ nom ne peut pas être vide"
            self.confirm.visible = True
            self.confirm.update()

    def build(self):
        return ft.Container(
            expand=True,
            height=768,
            padding=ft.padding.only(top=10, bottom=10, left=20, right=20),
            content=ft.Stack(
                controls=[
                    ft.Row(
                        expand=True,
                        height=768,
                        controls=[
                            self.rail,
                            ft.VerticalDivider(width=10, color="transparent"),
                            ft.Column(
                                expand=True,
                                height=768,
                                alignment=ft.alignment.center,
                                spacing=10,
                                controls=[
                                    ft.Container(**title_container_style,
                                                 content=ft.Row([self.title_page], alignment="spaceBetween")),
                                    self.filter_container,
                                    ft.Column(
                                        controls=[
                                            ft.Row([self.table_factures_container, self.news_container],
                                                   vertical_alignment=ft.CrossAxisAlignment.START),
                                            self.info_detfac,
                                            ft.Row(
                                                [self.table_details_factures_container, self.table_paiments_container],
                                                vertical_alignment=ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.START
                                            )
                                        ]
                                    ),
                                    self.new_cli_window, self.edit_cli_window
                                ]
                            )
                        ]
                    ),
                    self.select_cli_window
                ]
            )
        )
