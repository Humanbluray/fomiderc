import backend
from styles.factureStyleSheet import *
from others.useful_fonctions import *
import os
from datetime import datetime
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


class Factures(ft.UserControl):
    def __init__(self, page):
        super(Factures, self).__init__()

        # Menu ________________________________________________________________________
        self.page = page
        self.page.auto_scroll = True
        self.rail = ft.NavigationRail(
            selected_index=5,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            leading=ft.Image(src="logo.jpg", height=80, width=80),
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
        self.title_page = ft.Text("FACTURES", style=ft.TextStyle(size=26, font_family="Poppins ExtraBold"))

        # filtres conteneur ____________________________________________________________________
        self.client_id = ft.Text("", visible=False)
        self.filtre_clients = ft.TextField(**standard_tf_style, hint_text="rechercher client...", on_change=self.on_change_look_clients)
        self.choix = ft.Text("", visible=False)
        self.search_facture = ft.Text("", visible=False)
        self.aucun_facture = ft.Text("Aucune facture pour ce client", visible=False, size=12, color="red", font_family="Poppins Black")
        self.search_nomclient = ft.TextField(**search_style, on_change=self.changement_client)
        self.afficher_infos = ft.IconButton(ft.icons.PERSON_SEARCH_OUTLINED, tooltip="rechercher", on_click=self.open_select_cli_windows)
        self.chat = ft.IconButton(ft.icons.CHAT_BUBBLE_OUTLINE_SHARP, tooltip="Alertes", on_click=self.open_ecran_notifs)
        self.nombre_notifs = ft.Text("", size=11, weight="bold", color="white", top=3, right=6)
        self.notifs = ft.Icon(ft.icons.CIRCLE, color="red", size=20)

        # Notifications sur les alertes
        self.stats = ft.Stack(
            controls=[
                self.chat,
                ft.Stack(
                    [
                        self.notifs, self.nombre_notifs
                    ], top=-2, right=1
                )
            ]
        )
        self.table_notifs = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("N° devis", size=12, font_family="Poppins Black")),
                ft.DataColumn(ft.Text("date emission", size=12, font_family="Poppins Black")),
                ft.DataColumn(ft.Text("date butoire", size=12, font_family="Poppins Black")),
                ft.DataColumn(ft.Text("nb jours", size=12, font_family="Poppins Black")),
            ], rows=[]
        )
        self.ecran_notifs = ft.Card(
            elevation=30, height=500, width=600, expand=True, left=500, top=100,
            scale=ft.transform.Scale(scale=0),
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.ELASTIC_OUT),
            content=ft.Container(
                expand=True, height=500, padding=20, bgcolor="white",
                content=ft.Column(
                    height=500, expand=True,
                    controls=[
                        ft.Text("Alertes", size=24, font_family="Poppins Regular"),
                        ft.Divider(height=20, color="transparent"),
                        ft.Column([self.table_notifs], height=300, expand=True, scroll=ft.ScrollMode.ADAPTIVE),
                        ft.Divider(height=1),
                        ft.ElevatedButton(
                            height=50, color="white", bgcolor=ft.colors.BLACK87, text="Fermer",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=self.close_ecran_notifs
                        )
                    ]
                )
            )
        )
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
                padding=ft.padding.all(20),
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
        self.list_factures_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("N° Facture", size=12, font_family="Poppins Black"))],
            rows=[]
        )
        self.list_factures_container = ft.Container(
            **standard_ct_style,
            height=300, width=300,
            content=ft.Column(
                [self.list_factures_table, self.aucun_facture], expand=True,
                height=300,
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        self.actions = ft.Text("actions", style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.bill = ft.IconButton(icon=ft.icons.ADD_CARD_OUTLINED, tooltip="paiment", on_click=self.open_payment_window)
        self.fp = ft.FilePicker(on_result=self.imprimer_facture)
        self.print_button = ft.IconButton(
            ft.icons.PRINT_OUTLINED,
            tooltip="imprimer facture",
            on_click=lambda e: self.fp.save_file(allowed_extensions=["pdf"])
        )

        self.filter_container = ft.Container(
            **filter_container_style,
            content=ft.Row(
                [
                    ft.Row([self.search_facture, self.client_id, self.search_nomclient, self.afficher_infos, self.stats]),
                    ft.Row([self.actions, self.bill, self.fp, self.print_button])
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
        self.bc_client = ft.TextField(**statut_tf_style, disabled=True)
        self.devis = ft.TextField(**devis_tf_style, disabled=True)

        self.infos_container = ft.Container(
            **standard_ct_style,
            content=ft.Column(
                [
                    ft.Row([self.client_name, self.date, self.montant]),
                    ft.Row([self.devis, self.remise, self.bc_client]),
                    self.lettres
                ]
            )
        )
        # table details devis__________________________________________________________________________
        self.table_facture = ft.DataTable(**table_details_devis_style)
        self.facture_container = ft.Container(
            **standard_ct_style,
            height=300, width=800,
            content=ft.Column(
                [self.table_facture], expand=True,
                height=300,
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        self.table_paiments = ft.DataTable(**table_paiements_style)
        self.table_paiments_container = ft.Container(
            **table_container_style,
            expand=True,
            height=200, width=310,
            content=ft.Column(
                expand=True,
                height=200,
                controls=[self.table_paiments]
            )
        )

        # Validation impression _____________________________________________________________________
        self.good_impression = ft.AlertDialog(
            title=ft.Text("Confirmation"),
            content=ft.Text("Facture imprimée avec succès", style=ft.TextStyle(size=16, font_family="Poppins Regular")),
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
        # effectuer un paiement ________________________________________________________________________
        self.m_facture = ft.TextField(**new_payment_style, label="Facture", disabled=True)
        self.total = ft.TextField(**new_payment_style, label="Total facture", input_filter=ft.NumbersOnlyInputFilter(), disabled=True)
        self.deja_solde = ft.TextField(**new_payment_style, label="deja payé", disabled=True)
        self.check = ft.Checkbox(label="solder la facture", on_change=self.check_solde)
        self.montant_regle = ft.TextField(**new_payment_style, label="Montant à régler", input_filter=ft.NumbersOnlyInputFilter())
        self.mode = ft.Dropdown(
            **payment_mode_style,
            options=[
                ft.dropdown.Option("VIREMENT"),
                ft.dropdown.Option("CASH"),
                ft.dropdown.Option('OM/MOMO')
            ]
        )
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
        self.date_paiement = ft.TextField(**new_payment_style, label="date", disabled=True)
        self.message = ft.Text(visible=False, style=ft.TextStyle(size=12, font_family="Poppins Medium"))

        self.payment_window = ft.AlertDialog(
            title=ft.Text("Paiement"),
            content=ft.Column(
                [
                    self.m_facture, self.total, self.deja_solde, self.check, self.montant_regle, self.mode,
                    self.date_button, self.date_paiement, self.message
                ], height=500, spacing=15
            ),
            actions=[
                ft.ElevatedButton(
                    text="Effectuer paiement",
                    icon=ft.icons.PAYMENT_OUTLINED,
                    icon_color="white",
                    bgcolor="red",
                    color="white",
                    elevation=2, height=50,
                    on_click=self.finish_paiement
                ),
                ft.FilledTonalButton(height=50, text="Fermer", on_click=self.close_payment_window)
            ]
        )
        # fonctions à charger sans evenements ____________________________________________________________
        self.show_alertes()
        self.load_all_client_name()

    # functions ___________________________________________________________________________________________________
    def switch_page(self, e):
        pages = [
            "stocks", "clients", "fournisseurs", "commandes",
            "devis", "factures"
        ]
        self.page.go(f"/{pages[e.control.selected_index]}")

    # first content stack
    def show_alertes(self):
        datas = backend.delais_by_factures()
        if len(datas) == 0:
            self.nombre_notifs.visible = False
            self.notifs.visible = False
            self.chat.tooltip = "Aucune alerte"
            self.chat.disabled = True
        else:
            self.nombre_notifs.visible = True
            self.nombre_notifs.value = len(datas)
            self.notifs.visible = True
            self.chat.tooltip = f"{len(datas)} alertes"
            self.chat.disabled = False

    def close_ecran_notifs(self, e):
        self.ecran_notifs.scale = 0
        self.animate_scale = ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN)
        self.ecran_notifs.update()

    def open_ecran_notifs(self, e):
        datas = backend.delais_by_factures()
        if len(datas) == 0:
            pass
        else:
            self.ecran_notifs.scale = 1
            self.ecran_notifs.update()

            for row in self.table_notifs.rows[:]:
                self.table_notifs.rows.remove(row)

            for data in datas:
                self.table_notifs.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(data[0], size=12, font_family="Poppins Medium")),
                            ft.DataCell(ft.Text(ecrire_date(data[1]), size=12, font_family="Poppins Medium")),
                            ft.DataCell(ft.Text(ecrire_date(data[5]), size=12, font_family="Poppins Medium")),
                            ft.DataCell(ft.Text(data[6], size=12, font_family="Poppins Medium")),
                        ]
                    )
                )
            self.table_notifs.update()

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
        for row in self.list_factures_table.rows[:]:
            self.list_factures_table.rows.remove(row)

        if backend.id_client_by_name(self.search_nomclient.value) is None:
            self.aucun_facture.visible = True
            self.aucun_facture.update()

        else:
            self.client_id.value = backend.id_client_by_name(self.search_nomclient.value)[0]
            self.client_id.update()

            cli_id = int(self.client_id.value)
            datas = backend.all_factures_by_client_id(cli_id)

            if datas == [] or datas is None:
                self.aucun_facture.visible = True
                self.aucun_facture.update()
            else:
                for data in datas:
                    self.list_factures_table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(data, style=ft.TextStyle(font_family="poppins Medium", size=12)))
                            ],
                            on_select_changed=lambda e: self.on_change_facture(e.control.cells[0].content.value)
                        )
                    )
                self.aucun_facture.visible = False
                self.aucun_facture.update()

            self.list_factures_table.update()

    def changement_client_2(self):
        for row in self.list_factures_table.rows[:]:
            self.list_factures_table.rows.remove(row)

        if backend.id_client_by_name(self.search_nomclient.value) is None:
            self.aucun_facture.visible = True
            self.aucun_facture.update()

        else:
            self.client_id.value = backend.id_client_by_name(self.search_nomclient.value)[0]
            self.client_id.update()

            cli_id = int(self.client_id.value)
            datas = backend.all_factures_by_client_id(cli_id)

            if datas == [] or datas is None:
                self.aucun_facture.visible = True
                self.aucun_facture.update()
            else:
                for data in datas:
                    self.list_factures_table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(data, style=ft.TextStyle(font_family="poppins Medium", size=12)))
                            ],
                            on_select_changed=lambda e: self.on_change_facture(e.control.cells[0].content.value)
                        )
                    )
                self.aucun_facture.visible = False
                self.aucun_facture.update()

            self.list_factures_table.update()

    def on_change_facture(self, e):
        """actions when facture number change"""
        self.search_facture.value = e
        self.search_facture.update()
        infos = backend.show_info_factures(self.search_facture.value)
        self.client_id.value = infos[0]
        self.client_name.value = backend.infos_clients(id_client=int(self.client_id.value))[1]
        self.date.value = infos[1]
        self.montant.value = infos[3]
        self.remise.value = infos[4]
        self.lettres.value = infos[5]
        self.bc_client.value = infos[6].upper()
        self.devis.value = infos[7]
        self.devis.update()

        for widget in [self.client_name, self.date, self.montant, self.bc_client, self.devis,
                       self.remise, self.lettres, self.client_id]:
            widget.update()

        details = backend.search_factures_details(self.search_facture.value)
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

        for item in self.table_facture.rows[:]:
            self.table_facture.rows.remove(item)

        for data in datas:
            self.table_facture.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(data["reference"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["designation"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["qte"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["prix"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["total"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                    ]
                )
            )
        self.table_facture.update()

        self.m_facture.value = self.search_facture.value
        self.total.value = self.montant.value

        if backend.mt_deja_paye(self.m_facture.value) is None:
            self.deja_solde.value = 0
        else:
            self.deja_solde.value = backend.mt_deja_paye(self.m_facture.value)

        self.deja_solde.update()
        self.total.update()
        self.m_facture.update()

        # table des paiements
        for row in self.table_paiments.rows[:]:
            self.table_paiments.rows.remove(row)

        datas = []
        for item in backend.reglements_par_facture(self.search_facture.value):
            dico = {"montant": item[0], "type": item[1], "date": item[2]}
            datas.append(dico)

        for data in datas:
            self.table_paiments.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(data["montant"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(
                            ft.Text(data["type"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(
                            ft.Text(data["date"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                    ]
                )
            )
        self.table_paiments.update()

    def close_payment_window(self, e):
        self.payment_window.open = False
        self.payment_window.update()

    def open_payment_window(self, e):
        if self.search_facture.value is None or self.search_facture.value == "":
            pass
        else:
            if backend.montant_paiements_par_facture(self.search_facture.value) == backend.show_info_factures(self.search_facture.value)[3]:
                pass
            else:
                self.payment_window.open = True
                self.payment_window.update()

    def check_solde(self, e):
        if self.check.value is True:
            reste = int(self.total.value) - int(self.deja_solde.value)
            self.montant_regle.value = reste
            self.montant_regle.disabled = True
            self.montant_regle.update()
        else:
            self.montant_regle.value = ""
            self.montant_regle.disabled = False
            self.montant_regle.update()

    def change_date(self, e):
        self.date_paiement.value = self.date_picker.value
        self.date_paiement.update()

    def finish_paiement(self, e):
        if self.montant_regle.value is None or self.montant_regle.value == "" or self.mode.value is None or self.mode.value == "":
            self.message.value = "les champs mode et montant sont obligatioires"
            self.message.visible = True
            self.message.update()
        else:
            montant = int(self.montant_regle.value)
            backend.add_reglement(self.m_facture.value, montant, self.mode.value, str(self.date_paiement.value)[0:10])
            self.message.value = "paiement validé"
            self.message.visible = True
            self.message.update()

            for widget in (self.m_facture, self.total, self.deja_solde, self.montant_regle, self.mode, self.date_paiement):
                widget.value = ""
                widget.update()

    # fonctions d'impression ______________________________________
    def imprimer_facture(self, e: ft.FilePickerResultEvent):
        save_location = e.path
        fichier = f"{os.path.abspath(save_location)}.pdf"
        can = Canvas("{0}".format(fichier), pagesize=A4)

        if self.search_facture.value is None:
            self.bad_impression.open = True
            self.bad_impression.update()
        else:

            # dessin des entêtes
            def draw_headers():
                entete = "assets/header.png"
                signature = "assets/signature.png"
                footer = "assets/footer.png"
                # dessin logo et dignature
                # can.drawImage(logo, 1.5 * cm, 26 * cm)
                can.drawImage(entete, 0 * cm, 26.5 * cm)
                can.drawImage(footer, 0 * cm, 0 * cm)
                can.drawImage(signature, 12 * cm, 2 * cm)
                # infos de l'entreprise
                can.setFont("Helvetica-Bold", 24)
                can.setFillColorRGB(0, 0, 0)
                can.drawCentredString(5.5 * cm, 25 * cm, "FACTURE")
                can.setFont("Helvetica", 13)
                can.drawCentredString(5.5 * cm, 24.3 * cm, f"N°: {self.search_facture.value}")
                can.setFont("Helvetica", 12)
                can.drawCentredString(5.5 * cm, 23.8 * cm, f"date: {ecrire_date(self.date.value)}")
                bc = backend.show_info_factures(self.search_facture.value)[6]
                ov = backend.show_info_factures(self.search_facture.value)[8]
                can.setFont("Helvetica", 12)
                can.drawCentredString(5.5 * cm, 23.3 * cm, f"BC: {bc}")
                if ov is not None or ov != "":
                    can.setFont("Helvetica", 12)
                    can.drawCentredString(5.5 * cm, 22.8 * cm, f"OV: {ov}")

                # infos du client
                infos_client = backend.infos_clients(self.client_id.value)
                # cadre des infos du client
                can.setStrokeColorRGB(0, 0, 0)
                can.rect(10.5 * cm, 22.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
                can.setFont("Helvetica-Bold", 12)
                can.setFillColorRGB(0, 0, 0)
                can.drawString(11 * cm, 25.1 * cm, f"Client: {self.client_name.value}")
                can.setFont("Helvetica", 11)
                can.setFillColorRGB(0, 0, 0)

                if infos_client[3] is not None:
                    can.drawString(11 * cm, 24.4 * cm, f"Contact: {infos_client[3]}")

                can.setFont("Helvetica", 11)
                can.setFillColorRGB(0, 0, 0)

                if infos_client[4] is not None:
                    can.drawString(11 * cm, 23.7 * cm, f"NUI: {infos_client[4]}")

                can.setFont("Helvetica", 11)
                can.setFillColorRGB(0, 0, 0)

                if infos_client[5] is not None:
                    can.drawString(11 * cm, 23 * cm, f"RC: {infos_client[5]}")

            draw_headers()

            y = 22.5

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
            l = self.table_facture.rows[:]  # liste de DataRow
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
                rem = str(self.remise.value)
                mt_rem = int(total_devis * rem // 100)
                net = total_devis - mt_rem
                ir = int(net * 5.5 // 100)
                nap = net - ir
                can.setFont("Helvetica-Bold", 10)
                can.drawCentredString(15.5 * cm, (y - 1.5) * cm, "Remise:")
                can.drawCentredString(15.5 * cm, (y - 2) * cm, "net:")
                can.drawCentredString(15.5 * cm, (y - 2.5) * cm, "IR:")
                can.drawCentredString(15.5 * cm, (y - 3) * cm, "NAP:")

                can.setFont("Helvetica", 11)
                can.drawCentredString(18.5 * cm, (y - 1.5) * cm, f"{milSep(mt_rem)}")
                can.drawCentredString(18.5 * cm, (y - 2) * cm, f"{milSep(net)}")
                can.drawCentredString(15.5 * cm, (y - 2.5) * cm, f"{milSep(ir)}")
                can.drawCentredString(15.5 * cm, (y - 3) * cm, f"{milSep(nap)}")

                can.setFont("Helvetica-Bold", 11)
                can.drawString(1 * cm, (y - 4) * cm, f"Montant total: {ecrire_en_lettres(nap)}")
                can.setFont("Helvetica", 11)
                can.drawString(1 * cm, (y - 5) * cm, f"par virement à: {ENTITE_BANQUE}")
                can.drawString(1 * cm, (y - 5.5) * cm, f"IBAN: {ENTITE_IBAN}")
                can.drawString(1 * cm, (y - 6) * cm, f"Code swift: {ENTITE_SWIFT}")
                can.drawString(1 * cm, (y - 6.5) * cm, f"Titulaire: {ENTITE_NOM}")
            else:
                ir = int(total_devis * 5.5 // 100)
                nap = total_devis - ir
                can.setFont("Helvetica-Bold", 10)
                can.drawCentredString(15.5 * cm, (y - 1.5) * cm, "IR:")
                can.drawCentredString(15.5 * cm, (y - 2) * cm, "NAP:")

                can.setFont("Helvetica", 11)
                can.drawCentredString(18.5 * cm, (y - 1.5) * cm, f"{milSep(ir)} ")
                can.drawCentredString(18.5 * cm, (y - 2) * cm, f"{milSep(nap)}")

                can.setFont("Helvetica-Bold", 11)
                can.drawString(1 * cm, (y - 3) * cm, f"Montant total: {ecrire_en_lettres(nap)}")
                can.setFont("Helvetica", 11)
                can.drawString(1 * cm, (y - 4) * cm, f"par virement à: {ENTITE_BANQUE}")
                can.drawString(1 * cm, (y - 4.5) * cm, f"IBAN: {ENTITE_IBAN}")
                can.drawString(1 * cm, (y - 5) * cm, f"Code swift: {ENTITE_SWIFT}")
                can.drawString(1 * cm, (y - 5.5) * cm, f"Titulaire: {ENTITE_NOM}")

            can.save()
            self.good_impression.open = True
            self.good_impression.update()

    def close_good_impression(self, e):
        self.good_impression.open = False
        self.good_impression.update()

    def close_bad_impression(self, e):
        self.bad_impression.open = False
        self.bad_impression.update()

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
                                        ft.Container(**title_container_style, content=ft.Row([self.title_page], alignment="spaceBetween")),
                                        self.filter_container,
                                        ft.Row([self.list_factures_container, self.facture_container],
                                               vertical_alignment=ft.CrossAxisAlignment.START,
                                               alignment=ft.MainAxisAlignment.START,
                                               ),
                                        ft.Row([self.table_paiments_container, self.infos_container],
                                               vertical_alignment=ft.CrossAxisAlignment.START,
                                               alignment=ft.MainAxisAlignment.START,
                                               ),
                                    ]
                                )
                            ]
                        )
                    ),
                    self.select_cli_window,
                    self.ecran_notifs,
                    # dialog boxes
                    self.good_impression,
                    self.bad_impression,
                    self.payment_window,
                    self.date_picker

                ]
            )
        )
