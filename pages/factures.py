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
        self.title_page = ft.Text("FACTURES", style=ft.TextStyle(size=26, font_family="Poppins ExtraBold"))
        # filtres container ____________________________________________________________________
        self.filtre = ft.Text("Filtre", style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.search_facture = ft.Dropdown(**filter_name_style, on_change=self.on_change_facture)
        self.client_id = ft.Text(visible=False)
        self.actions = ft.Text("actions", style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.bill = ft.IconButton(icon=ft.icons.ADD_CARD_OUTLINED, tooltip="paiment", on_click=self.open_payment_window)

        self.filter_container = ft.Container(
            **filter_container_style,
            content=ft.Row(
                [
                    ft.Row([self.filtre, self.search_facture, self.client_id]),
                    ft.Row([self.actions, self.bill])
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
                    ft.Row([self.client_name, self.date, self.montant, self.remise, self.bc_client]),
                    ft.Row([self.devis, self.lettres])
                ]
            )
        )
        # table details devis__________________________________________________________________________
        self.table_facture = ft.DataTable(**table_details_devis_style)
        self.facture_container = ft.Container(
            **standard_ct_style,
            height=300, width=650,
            content=ft.Column(
                [self.table_facture], expand=True,
                height=360,
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        self.table_paiments = ft.DataTable(**table_paiements_style)
        self.table_paiments_container = ft.Container(
            **table_container_style,
            expand=True,
            height=250, width=300,
            content=ft.Column(
                expand=True,
                height=250,
                controls=[self.table_paiments]
            )
        )
        # impressions options _____________________________________________________________________
        self.fp = ft.FilePicker(on_result=self.imprimer_facture)
        self.print_button = ft.ElevatedButton(
            icon=ft.icons.PRINT_OUTLINED,
            icon_color="white",
            color="white",
            text="imprimer",
            height=50,
            bgcolor="red",
            tooltip="imprimer devis",
            on_click=lambda e: self.fp.save_file()
        )
        self.options_container = ft.Container(
            **standard_ct_style,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[self.print_button, self.fp]
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
        self.message = ft.Text(visible=False, style=ft.TextStyle(size=13, font_family="Poppins Medium"))

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
        # fonctions à loader sans evenements ____________________________________________________________
        self.load_facture_list()

    # functions ___________________________________________________________________________________________________
    def switch_page(self, e):
        pages = [
            "stocks", "clients", "fournisseurs", "commandes",
            "devis", "factures"
        ]
        self.page.go(f"/{pages[e.control.selected_index]}")

    # first content stack
    def load_facture_list(self):
        # chargement des factures
        for name in backend.all_factures():
            self.search_facture.options.append(
                ft.dropdown.Option(name)
            )

    def on_change_facture(self, e):
        """actions when facture number change"""
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
                        ft.DataCell(ft.Text(data["reference"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["designation"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["qte"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["prix"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["total"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
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
                            ft.Text(data["montant"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(
                            ft.Text(data["type"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(
                            ft.Text(data["date"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
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
            backend.add_reglement(self.m_facture.value, montant, self.mode.value, self.date_paiement.value)
            self.message.value = "paiement validé"
            self.message.visible = True
            self.message.update()

            for widget in (self.m_facture, self.total, self.deja_solde, self.montant_regle, self.mode, self.date_paiement):
                widget.value = ""
                widget.update()

    # fonctions d'impression ______________________________________
    def imprimer_facture(self, e: ft.FilePickerResultEvent):
        save_location = e.path
        fichier = os.path.abspath(save_location)
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
                can.drawCentredString(5.5 * cm, 24.5 * cm, "FACTURE")
                can.setFont("Helvetica", 13)
                can.drawCentredString(5.5 * cm, 23.8 * cm, f"N°: {self.search_facture.value}")
                can.setFont("Helvetica", 12)
                can.drawCentredString(5.5 * cm, 23.3 * cm, f"date: {self.date.value}")
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

                can.drawCentredString(10.5 * cm, (y - 4) * cm, f"arrêtée à la somme de: {self.lettres.value.lower()}")
                can.setFont("Helvetica", 10)
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

                can.setFont("Helvetica", 11)
                can.drawCentredString(10.5 * cm, (y - 3) * cm, f"arrêtée à la somme de: {self.lettres.value.lower()}")
                can.setFont("Helvetica", 10)
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
                                        ft.Container(**title_container_style, content=ft.Row([self.title_page, ft.Image(src="logo.jpg", height=70, width=70)], alignment="spaceBetween")),
                                        self.filter_container,
                                        self.infos_container,
                                        ft.Row([self.facture_container, self.table_paiments_container]),
                                        self.options_container,
                                    ]
                                )
                            ]
                        )
                    ),

                    # dialog boxes
                    self.good_impression,
                    self.bad_impression,
                    self.payment_window,
                    self.date_picker

                ]
            )
        )
