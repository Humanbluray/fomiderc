import backend
from styles.stocksStyleSheets import *
import pandas


class Stocks(ft.UserControl):
    def __init__(self, page):
        super(Stocks, self).__init__()

        # Menu lateral________________________________________________________________________
        self.page = page
        self.page.auto_scroll = True
        self.rail = ft.NavigationRail(
            selected_index=0,
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
        self.title_page = ft.Text("STOCKS", style=ft.TextStyle(size=26, font_family="Poppins ExtraBold"))
        # new article dialog ____________________________________________________________________
        self.n_ref = ft.TextField(**new_ref_style, label="reference")
        self.n_des = ft.TextField(**new_ref_style, label="designation")
        self.n_nat = ft.Dropdown(
            width=150,
            label="nature",
            height=50, dense=True,
            options=[ft.dropdown.Option("stock"), ft.dropdown.Option("non-stock")]
        )
        self.n_qte = ft.TextField(**new_ref_style, value="0", disabled=True, label="qte")
        self.n_prix = ft.TextField(**new_ref_style, label="prix", disabled=True, value='0')
        self.n_unit = ft.Dropdown(
            width=150, label="unité",
            height=50, dense=True,
            options=[
                ft.dropdown.Option("u"),
                ft.dropdown.Option("ml"),
                ft.dropdown.Option("kg")
            ]
        )
        self.error = ft.Text("Veuillez remplir tous les champs", visible=False,
                             style=ft.TextStyle(font_family="Poppins Medium", size=12, color="red"))

        self.new_article_window = ft.AlertDialog(
            title=ft.Text("Nouvel article"),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=15,
                controls=[self.n_ref, self.n_des, self.n_nat, self.n_qte, self.n_prix, self.n_unit, self.error]
            ),
            actions=[
                ft.ElevatedButton(
                    text="créer", icon=ft.icons.ADD,
                    on_click=self.add_new_ref,
                    icon_color="white", color="white", bgcolor="red",
                    height=50
                ),
                ft.FilledTonalButton(text="fermer", on_click=self.close_new_ref_window, height=50)
            ]
        )
        # modifier article _______________________________________________________________________
        self.m_ref = ft.TextField(**edit_ref_style, disabled=True)
        self.m_des = ft.TextField(**edit_des_style, disabled=True)
        self.m_nat = ft.TextField(**edit_nat_style_2, disabled=True)
        self.m_qte = ft.TextField(**edit_qte_style_2, disabled=True)
        self.m_prix = ft.TextField(**edit_prix_style, disabled=True)
        self.m_unit = ft.TextField(**edit_unit_style_2, disabled=True)

        self.ref_id = ft.TextField(**new_ref_style, label="id", disabled=True)
        self.m_ref2 = ft.TextField(**edit_ref_style, disabled=True)
        self.m_des2 = ft.TextField(**edit_des_style)
        self.m_nat2 = ft.Dropdown(**edit_nat_style, disabled=True)
        self.m_qte2 = ft.TextField(**edit_qte_style, disabled=True)
        self.m_prix2 = ft.TextField(**edit_prix_style, disabled=True)
        self.m_unit2 = ft.Dropdown(**edit_unit_style, disabled=True)
        self.confirm = ft.Text("Article modifié!", visible=False, style=ft.TextStyle(font_family="Poppins Medium", size=12, color="red"))
        # edit container _________________________________________________________________________________
        self.edit_container = ft.Container(
            height=550,
            expand=True,
            **filter_container_style,
            content=ft.Column(
                height=300,
                expand=True,
                controls=[
                    self.m_ref, self.m_des, self.m_nat,
                    ft.Row([self.m_qte, self.m_prix, self.m_unit])
                ]
            )
        )
        self.edit_article_window = ft.AlertDialog(
            title=ft.Text("Modifier article"),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=15,
                controls=[self.ref_id, self.m_ref2, self.m_des2, self.m_nat2, self.m_qte2, self.m_prix2, self.m_unit2, self.confirm]
            ),
            actions=[
                ft.ElevatedButton(text="modifier", icon=ft.icons.EDIT, icon_color="white", height=50,
                                  color="white", bgcolor="red", on_click=self.update_article),
                ft.FilledTonalButton(text="fermer", height=50, on_click=self.close_edit_article_window)
            ]
        )
        # widgets _________________________________________________________
        self.data_not_found = ft.Text(
            "Aucune donnée trouvée",
            style=ft.TextStyle(size=14, font_family="Poppins ExtraBold", color="red"),
            visible=False)
        self.name_bar = ft.TextField(**name_bar_style, on_change=self.filter_data)
        self.type_bar = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="stock", label="stock", active_color=ft.colors.BLACK87),
                    ft.Radio(value="non-stock", label="non-stock", active_color=ft.colors.BLACK87)
                ]
            ),
            on_change=self.filter_data
        )
        self.table_stocks = ft.DataTable(**table_stocks_style)

        # icones ____________________________________________________________________
        self.add = ft.IconButton(icon=ft.icons.ADD_OUTLINED, on_click=self.open_new_ref_window, tooltip="Créer référence")
        self.edit = ft.IconButton(icon=ft.icons.EDIT_OUTLINED, tooltip="Modifier référence", on_click=self.open_edit_article_window)
        self.achat = ft.IconButton(icon=ft.icons.ADD_CARD_OUTLINED, tooltip="Entrée directe", on_click=self.open_achat_window)
        self.delete = ft.IconButton(icon=ft.icons.DELETE_OUTLINED, tooltip="supprimer référence", on_click=self.delete_reference)
        self.save_me = ft.FilePicker(on_result=self.extraire_stock)
        self.stock_bt = ft.IconButton(ft.icons.UPLOAD_FILE_OUTLINED, tooltip="Extraction excel du stock", on_click=lambda e: self.save_me.save_file())
        self.save_histo = ft.FilePicker(on_result=self.extraire_historique)
        self.histo_bt = ft.IconButton(ft.icons.FILE_OPEN, tooltip="Extraction excel de l'historique", on_click=lambda e: self.save_histo.save_file())

        # actions achat direct_______________________________________________________
        self.a_ref = ft.Dropdown(**achat_ref_style, on_change=self.on_change_achat_ref)
        self.a_des = ft.TextField(**achat_des_style, disabled=True)
        self.a_qte = ft.TextField(**achat_qte_style, on_change=self.on_change_achat_qte)
        self.stock_actuel = ft.TextField(**achat_stock_style, label="stock actuel", disabled=True)
        self.stock_apres = ft.TextField(**achat_stock_style, label="Stock après", disabled=True)
        self.a_prix = ft.TextField(**achat_prix_style)
        self.a_com = ft.TextField(**achat_com_style)
        self.a_error = ft.Text("", visible=False, style=ft.TextStyle(font_family="Poppins Medium", size=12, color="red"))
        self.achat_window = ft.AlertDialog(
            title=ft.Text("Achat direct"),
            content=ft.Column(
                controls=[
                    self.a_ref,
                    self.a_des,
                    self.a_qte,
                    self.a_prix,
                    self.stock_actuel,
                    self.stock_apres,
                    self.a_com,
                    self.a_error
                ]
            ),
            actions=[
                ft.ElevatedButton(
                    icon=ft.icons.ADD_CARD_OUTLINED,
                    text="Valider", icon_color="white",
                    color="white", bgcolor="red",
                    height=45,
                    on_click=self.add_achat),
                ft.FilledTonalButton(text="fermer", on_click=self.close_achat_window)
            ]
        )

        # Menu conteneur ___________________________________________________________

        # Table conteneur ______________________________________________________________________________
        self.table_container = ft.Container(
            **table_container_style,
            content=ft.Column(
                [self.table_stocks, self.data_not_found],
                expand=True,
                height=300,
                width=750,
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        # filter container _________________________________________________________________
        self.filter_container = ft.Container(
            **filter_container_style,
            content=ft.Row(
                alignment="spaceBetween",
                controls=[
                    ft.Row(
                        [ft.Text("Filtres", style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb")),
                         self.name_bar, self.type_bar],
                        spacing=20),
                    ft.Row(
                        [ft.Text("Actions", style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb")),
                         self.add, self.edit, self.achat, self.delete]
                    )
                ]
            )
        )
        # end conteneur _______________________________________________________________
        self.no_historic = ft.Text(value="Pas d'histoqrique", visible=False, style=ft.TextStyle(size=14, font_family="Poppins ExtraBold", color="red"))
        self.info_histo = ft.Text("    Historique de", style=ft.TextStyle(color="grey", size=12, font_family="Poppins Medium"))
        self.histo_table = ft.DataTable(**table_histo_style)
        self.histo_container = ft.Container(
            **table_container_style,
            expand=True,
            height=170,
            content=ft.Column(
                [self.histo_table, self.no_historic],
                expand=True, height=150, width=750, scroll=ft.ScrollMode.ADAPTIVE, horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.title_text = ft.Text("")
        self.content_text = ft.Text("", style=ft.TextStyle(color="red", font_family="Poppins Regular", size=14))
        self.dialog_box = ft.AlertDialog(
            title=self.title_text,
            content=self.content_text,
            actions=[ft.FilledTonalButton(text="Fermer", on_click=self.close_dialog_box)]
        )
        self.fill_table()
        self.load_refs()

    # functions ______________________________________________________________________________________________
    def switch_page(self, e):
        pages = [
            "stocks", "clients", "fournisseurs", "commandes",
            "devis", "factures"
        ]
        self.page.go(f"/{pages[e.control.selected_index]}")

    def fill_table(self):
        """display the datas of the table stocks by default"""
        datas = []
        for item in backend.all_articles():
            dico = {"reference": item[1], "designation": item[2], "nature": item[3],
                    "qté": item[4], "prix": item[5], "unité": item[6]}
            datas.append(dico)

        for item in self.table_stocks.rows[:]:
            self.table_stocks.rows.remove(item)

        for data in datas:
            self.table_stocks.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(data["reference"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(
                            ft.Text(data["designation"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(
                            ft.Text(data["nature"].upper(), style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["qté"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(f"{data['prix']}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ft.DataCell(ft.Text(data["unité"], style=ft.TextStyle(font_family="poppins Medium", size=11)))
                    ],
                    on_select_changed=lambda e: self.select_ref(e.control.cells[0].content.value,
                                                                e.control.cells[1].content.value,
                                                                e.control.cells[2].content.value,
                                                                e.control.cells[3].content.value,
                                                                e.control.cells[4].content.value,
                                                                e.control.cells[5].content.value,)
                )
            )

    def filter_data(self, e):
        datas = []
        for item in backend.all_articles():
            dico = {"reference": item[1], "designation": item[2], "nature": item[3],
                    "qté": item[4], "prix": item[5], "unité": item[6]}
            datas.append(dico)

        for item in self.table_stocks.rows[:]:
            self.table_stocks.rows.remove(item)

        search_name = self.name_bar.value
        search_type = self.type_bar.value

        if self.type_bar.value is None:
            myfiler = list(filter(lambda x: search_name.lower() in x['designation'].lower(), datas))
            if len(myfiler) > 0:
                for data in myfiler:
                    self.table_stocks.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(data["reference"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(ft.Text(data["designation"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(ft.Text(data["nature"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(data["qté"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(f"{data['prix']}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(data["unité"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ],
                            on_select_changed=lambda e: self.select_ref(e.control.cells[0].content.value,
                                                                        e.control.cells[1].content.value,
                                                                        e.control.cells[2].content.value,
                                                                        e.control.cells[3].content.value,
                                                                        e.control.cells[4].content.value,
                                                                        e.control.cells[5].content.value, )
                        )
                    )
                self.data_not_found.visible = False
            else:
                self.data_not_found.visible = True

            self.data_not_found.update()
            self.table_stocks.update()
        else:
            myfiler = list(filter(
                lambda x: search_name.lower() in x['designation'].lower() and search_type.lower() in x[
                    'nature'].lower(), datas))
            if len(myfiler) > 0:
                for data in myfiler:
                    self.table_stocks.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(data["reference"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(ft.Text(data["designation"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(ft.Text(data["nature"].upper(),
                                                    style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(data["qté"], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(f"{data['prix']}", style=ft.TextStyle(font_family="poppins Medium", size=11))),
                                ft.DataCell(
                                    ft.Text(data["unité"], style=ft.TextStyle(font_family="poppins Medium", size=11)))
                            ],
                            on_select_changed=lambda e: self.select_ref(e.control.cells[0].content.value,
                                                                        e.control.cells[1].content.value,
                                                                        e.control.cells[2].content.value,
                                                                        e.control.cells[3].content.value,
                                                                        e.control.cells[4].content.value,
                                                                        e.control.cells[5].content.value, )
                        )
                    )
                self.data_not_found.visible = False
            else:
                self.data_not_found.visible = True

            self.data_not_found.update()
            self.table_stocks.update()

    def open_new_ref_window(self, e):
        self.error.visible = False
        self.error.update()
        self.new_article_window.open = True
        self.new_article_window.update()

    def close_new_ref_window(self, e):
        self.new_article_window.open = False
        self.new_article_window.update()

    def select_ref(self, e, f, g, h, i, j):
        self.m_ref.value = e
        self.m_des.value = f
        self.m_nat.value = g
        self.m_qte.value = h
        self.m_prix.value = i
        self.m_unit.value = j
        for widget in (self.m_ref, self.m_des, self.m_nat, self.m_qte, self.m_prix, self.m_unit):
            widget.update()

        self.m_ref2.value = self.m_ref.value
        self.m_des2.value = self.m_des.value
        self.m_nat2.value = self.m_nat.value
        self.m_qte2.value = self.m_qte.value
        self.m_prix2.value = self.m_prix.value
        self.m_unit2.value = self.m_unit.value
        self.ref_id.value = backend.search_ref_id(self.m_ref2.value)
        for widget in (self.m_ref2, self.m_des2, self.m_nat2, self.m_qte2, self.m_prix2, self.m_unit2, self.ref_id):
            widget.update()

        historique = backend.all_historique_by_ref(e)

        if historique is None or historique == []:
            for row in self.histo_table.rows[:]:
                self.histo_table.rows.remove(row)
                self.histo_table.update()

            self.no_historic.visible = True
            self.no_historic.update()

        else:
            self.no_historic.visible = False
            self.no_historic.update()
            for row in self.histo_table.rows[:]:
                self.histo_table.rows.remove(row)
                self.histo_table.update()

            for data in historique:
                self.histo_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(data[1], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(data[2], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(data[3], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(data[4], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(data[5], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(data[6], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                            ft.DataCell(ft.Text(data[7], style=ft.TextStyle(font_family="poppins Medium", size=11))),
                        ]
                    )
                )
            self.histo_table.update()

        self.info_histo.value = f'   Historique de {e}: {f}'
        self.info_histo.update()

    def add_new_ref(self, e):
        null_counter = 0
        for widget in (self.n_ref, self.n_des, self.n_nat, self.n_qte, self.n_unit):
            if widget.value == "":
                null_counter += 1

        if null_counter == 0:
            if self.n_ref.value in backend.find_unique_ref():
                self.error.value = "cette référence existe déja"
                self.error.visible = True
                self.error.update()
            else:
                backend.add_ref(ref=self.n_ref.value, des=self.n_des.value, nat=self.n_nat.value, qte=self.n_qte.value,
                                prix=0, unite=self.n_unit.value)
                for widget in (self.n_ref, self.n_des, self.n_nat, self.n_prix, self.n_unit):
                    widget.value = ""

                self.error.value = "Nouvel article ajouté !"
                self.error.visible = True
                self.fill_table()
                self.table_stocks.update()
                self.error.update()
                self.new_article_window.update()
        else:
            self.error.visible = True
            self.error.update()

    def open_edit_article_window(self, e):
        self.edit_article_window.open = True
        self.edit_article_window.update()

    def close_edit_article_window(self, e):
        self.m_ref2.disabled = False
        self.m_des2.disabled = False
        self.confirm.visible = False
        for widget in (self.m_ref2, self.m_des2, self.confirm):
            widget.update()
        self.edit_article_window.open = False
        self.edit_article_window.update()

    def update_article(self, e):
        ref_id = int(self.ref_id.value)
        if ref_id == 0:
            self.confirm.value = "opération impossible"
            self.confirm.visible = True
            self.confirm.update()
        else:
            backend.update_ref_by_name(self.m_des2.value, ref_id)
            self.confirm.visible = True
            self.confirm.update()
            self.m_ref2.disabled = True
            self.m_des2.disabled = True
            for widget in (self.m_ref2, self.m_des2, self.m_nat2,
                           self.m_qte2, self.m_prix2, self.m_unit2, self.ref_id):
                widget.value = ""
                widget.update()
            self.fill_table()
            self.table_stocks.update()

    def load_refs(self):
        for article in backend.all_references_stock():
            self.a_ref.options.append(
                ft.dropdown.Option(article)
            )

    def open_achat_window(self, e):
        self.achat_window.open = True
        self.achat_window.update()

    def close_achat_window(self, e):
        self.achat_window.open = False
        self.achat_window.update()

    def on_change_achat_ref(self, e):
        self.a_des.value = backend.search_designation(self.a_ref.value)[0]
        self.stock_actuel.value = backend.find_stock_ref(self.a_ref.value)
        self.a_des.update()
        self.stock_actuel.update()

    def on_change_achat_qte(self, e):
        self.stock_apres.value = str(int(self.a_qte.value) + int(self.stock_actuel.value))
        self.stock_apres.update()

    def add_achat(self, e):
        null_counter = 0
        for widget in (self.a_ref, self.a_qte, self.a_prix):
            if widget.value == "":
                null_counter += 1

        if null_counter > 0:
            self.a_error.value = "les champs reference, qte et prix ne doivent pas être vides"
            self.a_error.visible = True
            self.a_error.update()

        else:
            qte = int(self.a_qte.value)
            prix = int(self.a_prix.value)
            st_av = int(self.stock_actuel.value)
            st_ap = int(self.stock_apres.value)
            numero = backend.generate_achat_num()
            ancien_prix = backend.find_prix_ref(self.a_ref.value)
            nouveau_prix = ((st_av * ancien_prix) + (qte * prix)) // (st_av + qte)

            # ajouter à la table achat
            backend.add_achat(numero, self.a_ref.value, self.a_des.value, qte, prix, self.a_com.value)

            # ajouter à la table historique
            backend.add_historique(self.a_ref.value, "AD", numero, st_av, qte, st_ap)

            # update stock and prix
            backend.update_stock(st_ap, self.a_ref.value)
            backend.maj_prix_ref(nouveau_prix, self.a_ref.value)

            for widget in (self.a_ref, self.a_des, self.a_prix, self.stock_actuel, self.stock_apres):
                widget.value = ""
                widget.update()

            self.a_error.value = "opératioins effectuée avec succès"
            self.a_error.visible = True
            self.a_error.update()
            self.fill_table()

    def close_dialog_box(self, e):
        self.dialog_box.open = False
        self.dialog_box.update()

    def delete_reference(self, e):
        historic = backend.all_historique_by_ref(self.m_ref.value)
        if historic is None or historic == []:
            backend.delete_ref(self.m_ref.value)
            self.title_text.value = "confirmation"
            self.content_text.value = "Reference  supprimée"
            self.dialog_box.open = True
            self.title_text.update()
            self.content_text.update()
            self.dialog_box.update()
        else:
            self.title_text.value = "Erreur"
            self.content_text.value = f"Vous ne pouvez pas supprimer cette référence\nson historique n'est pas nulle"
            self.dialog_box.open = True
            self.title_text.update()
            self.content_text.update()
            self.dialog_box.update()
            self.fill_table()

    @staticmethod
    def extraire_stock(e: ft.FilePickerResultEvent):
        refs = []
        des = []
        types = []
        qtes = []
        prix = []
        unites = []
        stock = backend.all_articles()
        for row in stock:
            refs.append(row[1])
            des.append(row[2])
            types.append(row[3])
            qtes.append(row[4])
            prix.append(row[5])
            unites.append(row[6])

        data_set = {
            "reference": refs, "designation": des, "type": types,
            "qté": qtes, "prix": prix, "unité": unites
        }
        df = pandas.DataFrame(data_set)

        save_location = e.path
        if save_location:
            excel = pandas.ExcelWriter(save_location)
            df.to_excel(excel, sheet_name="Feuil 1")
            excel.close()

    @staticmethod
    def extraire_historique(e: ft.FilePickerResultEvent):
        refs = []
        dates = []
        mvts = []
        numeros = []
        qte_avts = []
        qtes = []
        qte_apres = []
        historiques = backend.all_historique()
        for row in historiques:
            refs.append(row[1])
            dates.append(row[2])
            mvts.append(row[3])
            numeros.append(row[4])
            qte_avts.append(row[5])
            qtes.append(row[6])
            qte_apres.append(row[7])

        data_set= {
            "reference": refs, "date": dates, "mouvement": mvts,
            "numero": numeros, "qté avant": qte_avts,
            "qté": qtes, "qté après": qte_apres
        }
        df = pandas.DataFrame(data_set)
        save_location = e.path
        if save_location:
            excel = pandas.ExcelWriter(save_location)
            df.to_excel(excel, sheet_name="Feuil 1")
            excel.close()

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
                        height=768,
                        alignment=ft.alignment.center,
                        spacing=10,
                        controls=[
                            ft.Container(**title_container_style, content=self.title_page),
                            self.filter_container,
                            ft.Row(
                                [
                                    ft.Column([self.table_container, self.info_histo, self.histo_container], height=550),
                                    self.edit_container,
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        "Extractions",
                                        style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb")
                                    ),
                                    self.stock_bt, self.save_me, self.histo_bt, self.save_histo
                                ], alignment="starf"),

                            self.new_article_window,
                            self.edit_article_window,
                            self.achat_window,
                            self.dialog_box
                        ]
                    )
                ]
            )
        )
