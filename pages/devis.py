import backend
from styles.devisStyleSheet import *
from others.useful_fonctions import *
from datetime import date
import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


class Devis(ft.UserControl):
    def __init__(self, page):
        super(Devis, self).__init__()

        # Menu ________________________________________________________________________
        self.page = page
        self.rail = ft.NavigationRail(
            selected_index=4,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            # min_extended_width=400,
            leading=ft.Text("MENU", style=ft.TextStyle(size=20, font_family="Poppins Bold",
                                                       decoration=ft.TextDecoration.UNDERLINE)),
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

        # filtres conteneur ____________________________________________________________________________________________________
        self.filtre = ft.Text("Filtre",
                              style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.client_id = ft.Text("", visible=False)
        self.filtre_clients = ft.TextField(**standard_tf_style, hint_text="rechercher client...", on_change=self.on_change_look_clients)
        self.choix = ft.Text("", visible=False)
        self.search_devis = ft.Text("", visible=False)
        self.aucun_devis = ft.Text("Aucun devis pour ce client", visible=False, size=12, color="red", font_family="Poppins Black")
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
                padding=20,
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
        self.list_devis_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("N° devis", size=12, font_family="Poppins Black"))],
            rows=[]
        )
        self.list_devis_container = ft.Container(
            **standard_ct_style,
            height=300, width=300,
            content=ft.Column(
                [self.list_devis_table, self.aucun_devis], expand=True,
                height=300,
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        # actions
        self.actions = ft.Text("actions",
                               style=ft.TextStyle(font_family="Poppins Medium", size=12, italic=True, color="#ebebeb"))
        self.add = ft.IconButton(icon=ft.icons.ADD_OUTLINED, tooltip="Créer devis",
                                 on_click=self.open_new_devis_window
                                 )
        self.edit = ft.IconButton(icon=ft.icons.EDIT_OUTLINED, tooltip="Modifier devis",
                                  on_click=self.open_edit_devis_window
                                  )
        self.fp = ft.FilePicker(on_result=self.imprimer_bordereau)
        self.delivery = ft.IconButton(icon=ft.icons.PRINT_OUTLINED, tooltip="imprimer bordereau livraison",
                                      on_click=lambda e: self.fp.save_file(allowed_extensions=["pdf"]))
        self.bill = ft.IconButton(icon=ft.icons.EURO_OUTLINED, tooltip="facturer", on_click=self.facturer_devis)
        self.delete = ft.IconButton(icon=ft.icons.DELETE_OUTLINED, tooltip="supprimer devis",
                                    on_click=self.delete_devis
                                    )

        self.filter_container = ft.Container(
            **filter_container_style,
            content=ft.Row(
                [
                    ft.Row(
                        [
                            self.search_nomclient, self.search_devis, self.client_id,
                            self.afficher_infos, self.stats
                        ]
                    ),
                    ft.Row([self.actions, self.add, self.edit, self.delivery, self.bill, self.delete, self.fp])
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
            height=300, width=800,
            content=ft.Column(
                [self.table_devis], expand=True,
                height=360,
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        # impressions options _____________________________________________________________________
        self.fp2 = ft.FilePicker(on_result=self.imprimer_devis)
        self.print_button = ft.ElevatedButton(
            text="Imprimer",
            height=50,
            color="white",
            bgcolor="red",
            icon=ft.icons.PRINT_OUTLINED,
            icon_color="white",
            tooltip="imprimer devis",
            on_click=lambda e: self.fp2.save_file(allowed_extensions=["pdf"])
        )
        self.options_container = ft.Container(
            **standard_ct_style,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[self.print_button, self.fp2]
            )
        )
        # # Stack ecran de creatiuon de devis****************************************************************************************************
        self.n_dev = ft.TextField(**devis_num_style, disabled=True)
        self.n_cliname = ft.Dropdown(**client_name_style, on_change=self.on_change_client)
        self.n_cli_id = ft.Text(visible=False)
        self.n_initiales = ft.Text(visible=False)
        self.object = ft.TextField(**standard_tf_style, label="objet")
        self.n_remise = ft.TextField(**new_remise_style, value="0")
        self.up = ft.IconButton(ft.icons.ADD_CIRCLE_OUTLINE, icon_size=24, on_click=self.add_remise)
        self.down = ft.IconButton(ft.icons.REMOVE_CIRCLE_OUTLINE, icon_size=24, on_click=self.remove_remise)
        self.delai = ft.TextField(**nb_style, label="délai livraison")
        self.ptliv = ft.TextField(**liv_style, label="point de livraison")
        self.paydelay = ft.TextField(**paydelay_style, label="paiement", input_filter=ft.NumbersOnlyInputFilter())
        self.validite = ft.TextField(**paydelay_style, label="validite", input_filter=ft.NumbersOnlyInputFilter())
        self.notabene = ft.TextField(**nb_style, label="NB")
        self.ct_first = ft.Container(
            **standard_ct_style,
            content=ft.Column(
                [
                    ft.Row([self.n_dev, self.object, self.n_cli_id, ft.Row([self.up, self.n_remise, self.down])]),
                    ft.Row([self.n_cliname, self.n_cli_id, self.n_initiales])
                ]
            )
        )
        self.reference = ft.TextField(**search_ref_style, on_change=self.changement_reference)
        self.show_list_ref = ft.IconButton(ft.icons.IMAGE_SEARCH_OUTLINED, tooltip="rechercher", on_click=self.open_select_n_ref_windows)
        self.designation = ft.TextField(**standard_tf_style, label="designation", disabled=True)
        self.prix_stock = ft.TextField(**new_prix_style, label="prix indiqué", disabled=True)
        self.qte = ft.TextField(**new_qte_style, input_filter=ft.NumbersOnlyInputFilter())
        self.prix = ft.TextField(**new_prix_style, label="prix", input_filter=ft.NumbersOnlyInputFilter())
        self.total = ft.TextField(**new_prix_style, label="total", disabled=True)
        self.total_lettres = ft.TextField(**mt_lettres_style, disabled=True)
        self.button_add = ft.ElevatedButton(
            icon=ft.icons.ADD, text="Ajouter",
            icon_color="white", color="white", height=50,
            bgcolor=ft.colors.BLACK87,
            on_click=self.add_table_line
        )
        self.filtre_n_ref = ft.TextField(**standard_tf_style, hint_text="rechercher client...", on_change=self.on_change_n_ref)
        self.choix_n_ref = ft.Text("", visible=False)
        self.n_table_ref = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("reference", style=ft.TextStyle(size=12, font_family="Poppins Black"))),
                ft.DataColumn(ft.Text("designation", style=ft.TextStyle(size=12, font_family="Poppins Black"))),
            ],
            rows=[]
        )
        self.select_n_ref_window = ft.Card(
            elevation=30, expand=True,
            top=5, left=300,
            height=700, width=800,
            scale=ft.transform.Scale(scale=0),
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN),
            content=ft.Container(
                padding=20,
                bgcolor="white",
                content=ft.Column(
                    expand=True, height=600,
                    controls=[
                        ft.Text("Selectionner reference", size=20, font_family="Poppins Regular"),
                        ft.Divider(height=20, color="transparent"),
                        self.filtre_n_ref,
                        self.choix_n_ref,
                        ft.Column([self.n_table_ref], scroll=ft.ScrollMode.ADAPTIVE, height=500),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
        self.ct_second = ft.Container(
            **standard_ct_style,
            content=ft.Column(
                [
                    ft.Row([self.reference, self.show_list_ref, self.designation]),
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
            top=2, left=100,
            scale=ft.transform.Scale(scale=0),
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN),
            content=ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=8,
                opacity=1,
                expand=True,
                height=750,
                padding=ft.padding.all(20),
                content=ft.Column(
                    controls=[
                        self.ct_first,
                        self.ct_second,
                        ft.Container(
                            **standard_ct_style,
                            content=ft.Column(
                                [
                                    self.table_new_devis,
                                ],
                                expand=True,
                                height=150, width=600,
                                scroll=ft.ScrollMode.ADAPTIVE
                            )
                        ),
                        ft.Row([self.notabene, self.paydelay, self.validite]),
                        ft.Row([self.ptliv, self.delai]),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Valider",
                                    icon=ft.icons.CHECK_OUTLINED,
                                    icon_color="white", color="white", bgcolor="red", height=50,
                                    on_click=self.add_new_devis
                                ),
                                ft.ElevatedButton(
                                    "Quitter",
                                    icon=ft.icons.ARROW_BACK_OUTLINED,
                                    icon_color="white", color="white", bgcolor=ft.colors.BLACK87, height=50,
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
            content=ft.Text("Veuillez choisir une option avant d'imprimer",
                            style=ft.TextStyle(size=16, font_family="Poppins Regular")),
            actions=[
                ft.FilledTonalButton(text="Fermer", on_click=self.close_bad_impression)
            ]
        )
        # fenetre de facturation de devis __________________________________________________________________________
        self.bc_client = ft.TextField(**bc_tf_style, label="bc client")
        self.ov = ft.TextField(**bc_tf_style, label="OV(CIMENCAM)")
        self.confirmation_facturation = ft.Text("devis facturé", visible=False,
                                                style=ft.TextStyle(size=16, font_family="Poppins Regular", color="red"))
        self.facturer_window = ft.AlertDialog(
            title=ft.Text("facturer devis"),
            content=ft.Column(
                [
                    ft.Text("Entrez le numéro de BC du client",
                            style=ft.TextStyle(size=12, font_family="Poppins Regular")),
                    self.bc_client,
                    self.ov,
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

        # fenetre de modification de devis ***************************************************************************************************
        self.table_edit_devis = ft.DataTable(**table_edit_devis_style)
        self.m_devis = ft.TextField(**devis_num_style, disabled=True)
        self.table_container_edit = ft.Container(
            **standard_ct_style, expand=True, height=100, width=600,
            content=ft.Column([self.table_edit_devis], expand=True, width=600, height=100,
                              scroll=ft.ScrollMode.ADAPTIVE)
        )
        self.m_reference = ft.TextField(**search_ref_style, on_change=self.changement_m_reference)
        self.show_list_m_ref = ft.IconButton(ft.icons.IMAGE_SEARCH_OUTLINED, tooltip="rechercher", on_click=self.open_select_m_ref_windows)
        self.id_ligne = ft.Text(visible=False)
        self.m_remise = ft.TextField(**new_remise_style)
        self.m_designation = ft.TextField(**standard_tf_style, label="designation", disabled=True)
        self.m_prix_stock = ft.TextField(**new_prix_style, label="prix indiqué", disabled=True)
        self.m_qte = ft.TextField(**new_qte_style, input_filter=ft.NumbersOnlyInputFilter())
        self.m_prix = ft.TextField(**new_prix_style, label="prix", input_filter=ft.NumbersOnlyInputFilter())
        self.m_total = ft.TextField(**new_prix_style, label="total", disabled=True)
        self.m_total_lettres = ft.TextField(**mt_lettres_style, disabled=True)
        self.m_delai = ft.TextField(**nb_style, label="délai livraison")
        self.m_ptliv = ft.TextField(**liv_style, label="point de livraison")
        self.m_paydelay = ft.TextField(**paydelay_style, label="paiement", input_filter=ft.NumbersOnlyInputFilter())
        self.m_validite = ft.TextField(**paydelay_style, label="validite", input_filter=ft.NumbersOnlyInputFilter())
        self.m_notabene = ft.TextField(**nb_style, label="NB")
        self.m_button_add = ft.ElevatedButton(
            icon=ft.icons.ADD, text="Ajouter",
            icon_color="white", color="white", height=40,
            bgcolor=ft.colors.BLACK87,
            on_click=self.add_table_line
        )

        self.filtre_m_ref = ft.TextField(**standard_tf_style, hint_text="rechercher client...", on_change=self.on_change_m_ref)
        self.choix_m_ref = ft.Text("", visible=False)
        self.m_table_ref = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("reference", style=ft.TextStyle(size=12, font_family="Poppins Black"))),
                ft.DataColumn(ft.Text("designation", style=ft.TextStyle(size=12, font_family="Poppins Black"))),
            ],
            rows=[]
        )
        self.select_m_ref_window = ft.Card(
            elevation=30, expand=True,
            top=5, left=300,
            height=700, width=800,
            scale=ft.transform.Scale(scale=0),
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN),
            content=ft.Container(
                padding=20,
                bgcolor="white",
                content=ft.Column(
                    expand=True, height=600,
                    controls=[
                        ft.Text("Selectionner reference", size=20, font_family="Poppins Regular"),
                        ft.Divider(height=20, color="transparent"),
                        self.filtre_m_ref,
                        self.choix_m_ref,
                        ft.Column([self.m_table_ref], scroll=ft.ScrollMode.ADAPTIVE, height=500),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
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
        self.valid_text = ft.Text("", size=14, font_family="Poppins Medium")
        self.valid_box = ft.AlertDialog(
            title=ft.Text("Confirmation"),
            content=self.valid_text,
            actions=[
                ft.FilledTonalButton("quitter", on_click=self.close_valid_box, height=50),
            ]
        )
        # edit devis card _________________________________________________________
        self.edit_devis_window = ft.Card(
            elevation=30, expand=True,
            top=0, left=100,
            scale=ft.transform.Scale(scale=0),
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN),
            content=ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=8,
                opacity=1,
                expand=True,
                height=750,
                padding=ft.padding.all(20),
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            **standard_ct_style,
                            content=ft.Row([self.m_devis, self.m_total_lettres])
                        ),
                        self.table_container_edit,
                        ft.Row([self.m_notabene, self.m_paydelay, self.m_validite]),
                        ft.Row([self.m_ptliv, self.m_delai]),
                        ft.Container(
                            **standard_ct_style,
                            content=ft.Row([self.id_ligne, self.m_reference, self.show_list_m_ref, self.m_designation, self.m_qte, self.m_prix])
                        ),
                        ft.Container(
                            **standard_ct_style,
                            content=ft.Row(
                                [
                                    ft.ElevatedButton("Modifier ligne", icon=ft.icons.EDIT, icon_color="white",
                                                      color="white", height=50, bgcolor=ft.colors.BLACK87,
                                                      on_click=self.update_ligne),
                                    ft.ElevatedButton("Ajouter ligne", icon=ft.icons.ADD, icon_color="white",
                                                      color="white",
                                                      height=50, bgcolor=ft.colors.BLACK87, on_click=self.open_new_ligne_window),
                                    ft.ElevatedButton("Supprimer ligne", icon=ft.icons.DELETE, icon_color="white",
                                                      color="white", height=50, bgcolor=ft.colors.BLACK87,
                                                      on_click=self.delete_detail_line)
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
                                            ft.IconButton(ft.icons.REMOVE_CIRCLE_OUTLINE, icon_size=24,
                                                          on_click=self.edit_remise_down),
                                            self.m_remise,
                                            ft.IconButton(ft.icons.ADD_CIRCLE_OUTLINE, icon_size=24,
                                                          on_click=self.edit_remise_up),
                                            self.m_total
                                        ]
                                    ),
                                    ft.ElevatedButton("valider remise", icon=ft.icons.EDIT, icon_color="white",
                                                      color="white", height=50, bgcolor=ft.colors.BLACK87,
                                                      on_click=self.on_change_edit_remise)
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
                                                      height=50, bgcolor="red", on_click=self.finish_edit_devis),
                                ]
                            )
                        )
                    ],
                )
            )
        )
        # fonctions à charger sans evenements ____________________________________________________________

        self.load_clients_list()
        self.load_n_ref()
        self.load_m_ref()
        self.load_edit_ref_list2()
        self.load_all_client_name()
        self.show_alertes()

    # functions ___________________________________________________________________________________________________
    def switch_page(self, e):
        pages = [
            "stocks", "clients", "fournisseurs", "commandes",
            "devis", "factures"
        ]
        self.page.go(f"/{pages[e.control.selected_index]}")

    def show_alertes(self):
        datas = backend.delais_by_numero()
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
        datas = backend.delais_by_numero()
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
                            ft.DataCell(ft.Text(ecrire_date(data[3]), size=12, font_family="Poppins Medium")),
                            ft.DataCell(ft.Text(data[4], size=12, font_family="Poppins Medium")),
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
        for row in self.list_devis_table.rows[:]:
            self.list_devis_table.rows.remove(row)

        if backend.id_client_by_name(self.search_nomclient.value) is None:
            self.aucun_devis.visible = True
            self.aucun_devis.update()

        else:
            self.client_id.value = backend.id_client_by_name(self.search_nomclient.value)[0]
            self.client_id.update()

            cli_id = int(self.client_id.value)
            datas = backend.all_devis_by_client_id(cli_id)

            if datas == [] or datas is None:
                self.aucun_devis.visible = True
                self.aucun_devis.update()
            else:
                for data in datas:
                    self.list_devis_table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(data, style=ft.TextStyle(font_family="poppins Medium", size=12)))
                            ],
                            on_select_changed=lambda e: self.on_change_devis(e.control.cells[0].content.value)
                        )
                    )
                self.aucun_devis.visible = False
                self.aucun_devis.update()

            self.list_devis_table.update()

    def changement_client_2(self):
        for row in self.list_devis_table.rows[:]:
            self.list_devis_table.rows.remove(row)

        if backend.id_client_by_name(self.search_nomclient.value) is None:
            self.aucun_devis.visible = True
            self.aucun_devis.update()

        else:
            self.client_id.value = backend.id_client_by_name(self.search_nomclient.value)[0]
            self.client_id.update()

            cli_id = int(self.client_id.value)
            datas = backend.all_devis_by_client_id(cli_id)

            if datas == [] or datas is None:
                self.aucun_devis.visible = True
                self.aucun_devis.update()
            else:
                for data in datas:
                    self.list_devis_table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(data, style=ft.TextStyle(font_family="poppins Medium", size=12)))
                            ],
                            on_select_changed=lambda e: self.on_change_devis(e.control.cells[0].content.value)
                        )
                    )
                self.aucun_devis.visible = False
                self.aucun_devis.update()

            self.list_devis_table.update()

    # changement des devis
    def on_change_devis(self, e):
        self.search_devis.value = e
        self.search_devis.update()
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
                                            style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["designation"].upper(),
                                            style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["qte"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["prix"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(data["total"], style=ft.TextStyle(font_family="poppins Medium", size=12))),
                    ]
                )
            )
        self.table_devis.update()

    def close_valid_box(self, e):
        self.valid_box.open = False
        self.valid_box.update()

    # second content stack nouveau devis _______________________________________________________________________________________

    def open_select_n_ref_windows(self, e):
        self.select_n_ref_window.scale = 1
        self.select_n_ref_window.update()

    def load_n_ref(self):
        for row in self.n_table_ref.rows[:]:
            self.n_table_ref.rows.remove(row)

        datas = backend.all_ref_and_desig()
        for data in datas:
            self.n_table_ref.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{data[0].upper()}", style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(f"{data[1].upper()}", style=ft.TextStyle(font_family="poppins Medium", size=12))),
                    ],
                    on_select_changed=lambda e: self.on_select_change_n_ref(e.control.cells[0].content.value)
                )
            )

    def on_change_n_ref(self, e):
        for row in self.n_table_ref.rows[:]:
            self.n_table_ref.rows.remove(row)

        datas = []
        for data in backend.all_ref_and_desig():
            dico = {"reference": data[0], "designation": data[1] }
            datas.append(dico)

        myfiler = list(filter(lambda x: self.filtre_n_ref.value.lower() in x['designation'].lower(), datas))

        for row in myfiler:
            self.n_table_ref.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(f"{row['reference']}", style=ft.TextStyle(font_family="Poppins Medium", size=12))),
                    ft.DataCell(ft.Text(f"{row['designation']}", style=ft.TextStyle(font_family="Poppins Medium", size=12)))
                    ],
                    on_select_changed=lambda e: self.on_select_change_n_ref(e.control.cells[0].content.value)
                )
            )
        self.n_table_ref.update()

    def on_select_change_n_ref(self, e):
        self.choix.value = e
        self.choix.update()
        self.reference.value = self.choix.value
        self.reference.update()
        self.select_n_ref_window.scale = 0
        self.select_n_ref_window.animate_scale = ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT)
        self.select_n_ref_window.update()
        self.changement_reference_2()

    def changement_reference(self, e):
        self.designation.value = backend.search_designation(self.reference.value)[0]
        self.prix_stock.value = backend.search_designation(self.reference.value)[1]
        self.designation.update()
        self.prix_stock.update()

    def changement_reference_2(self):
        self.designation.value = backend.search_designation(self.reference.value)[0]
        self.prix_stock.value = backend.search_designation(self.reference.value)[1]
        self.designation.update()
        self.prix_stock.update()

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

    def load_clients_list(self):
        for name in backend.all_clients():
            self.n_cliname.options.append(
                ft.dropdown.Option(name)
            )

    def add_remise(self, e):
        self.n_remise.value = str(int(self.n_remise.value) + 1)
        self.n_remise.update()

    def remove_remise(self, e):
        remise = int(self.n_remise.value)
        if remise > 0:
            self.n_remise.value = str(remise - 1)
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
                        ft.DataCell(ft.Text(self.reference.value.upper(),
                                            style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(self.designation.value.upper(),
                                            style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(ft.Text(self.qte.value, style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(
                            ft.Text(self.prix.value, style=ft.TextStyle(font_family="poppins Medium", size=12))),
                    ]
                )
            )
        else:
            pass

        # recuperer la liste des lignes dans un tableau
        grande_liste = []
        liste = self.table_new_devis.rows[:]  # liste de DataRow
        for i in range(len(liste)):
            sous_liste = []
            for j in range(len(liste[i].cells)):
                sous_liste.append(liste[i].cells[j].content.value)
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
        liste = self.table_new_devis.rows[:]  # liste de DataRow
        for i in range(len(liste)):
            sous_liste = []
            for j in range(len(liste[i].cells)):
                sous_liste.append(liste[i].cells[j].content.value)
            grande_liste.append(sous_liste)

        # add devis
        if self.n_cliname.value == "":
            self.msg_error.open = True
            self.msg_error.update()

        else:
            mt_remise = int(self.n_remise.value)
            montant = int(self.total.value)
            cli_id = int(self.n_cli_id.value)
            backend.add_devis(self.n_dev.value, date.today(), cli_id, montant, self.object.value, mt_remise,
                              self.total_lettres.value, self.notabene.value, self.delai.value, self.ptliv.value,
                              self.validite.value, self.paydelay.value)

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
            self.delai.value = ""
            self.notabene.value = ""
            self.ptliv.value = ""
            self.validite.value = ""
            self.paydelay.value = ""
            self.delai.update()
            self.notabene.update()
            self.ptliv.update()
            self.validite.update()
            self.paydelay.update()

            for row in self.table_new_devis.rows[:]:
                self.table_new_devis.rows.remove(row)

            self.table_new_devis.update()

    def close_confirm(self, e):
        self.msg_confirm.open = False
        self.msg_confirm.update()

    def close_error(self, e):
        self.msg_error.open = False
        self.msg_error.update()

    # # fonctions d'impression ______________________________________

    def imprimer_devis(self, e: ft.FilePickerResultEvent):

        save_location = e.path
        fichier = f"{os.path.abspath(save_location)}.pdf"
        can = Canvas("{0}".format(fichier), pagesize=A4)

        if self.search_devis.value is None:
            self.bad_impression.open = True
            self.bad_impression.update()

        else:

            # dessin des entêtes
            def draw_headers():
                entete = "assets/header.png"
                signature = "assets/signature.png"
                footer = "assets/footer.png"
                # dessin logo et dignature
                can.drawImage(entete, 0 * cm, 26.5 * cm)
                can.drawImage(footer, 0 * cm, 0 * cm)
                can.drawImage(signature, 12 * cm, 2 * cm)
                # infos de l'entreprise
                can.setFont("Helvetica-Bold", 24)
                can.setFillColorRGB(0, 0, 0)
                can.drawCentredString(5.5 * cm, 24.5 * cm, "PROFORMA")
                can.setFont("Helvetica", 13)
                can.drawCentredString(5.5 * cm, 23.8 * cm, f"N°: {self.search_devis.value}")
                can.setFont("Helvetica", 12)
                can.drawCentredString(5.5 * cm, 23.3 * cm, f"Suivant demande du {ecrire_date(self.date.value)}")

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
            can.line(2 * cm, (y - 1) * cm, 2 * cm, (y - 2) * cm)
            can.line(13.5 * cm, (y - 1) * cm, 13.5 * cm, (y - 2) * cm)
            can.line(14.5 * cm, (y - 1) * cm, 14.5 * cm, (y - 2) * cm)
            can.line(15.5 * cm, (y - 1) * cm, 15.5 * cm, (y - 2) * cm)
            can.line(17.5 * cm, (y - 1) * cm, 17.5 * cm, (y - 2) * cm)
            can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 2) * cm)
            # draw headers
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(1.5 * cm, (y - 1.6) * cm, "item")
            can.drawCentredString(7.75 * cm, (y - 1.6) * cm, "Désignation")
            can.drawCentredString(14 * cm, (y - 1.6) * cm, "Qté")
            can.drawCentredString(15 * cm, (y - 1.6) * cm, "U")
            can.drawCentredString(16.5 * cm, (y - 1.6) * cm, "P.U.")
            can.drawCentredString(18.75 * cm, (y - 1.6) * cm, "Montant")

            ref_list = []
            total_devis = 0
            liste = self.table_devis.rows[:]  # liste de DataRow
            for i in range(len(liste)):
                sous_liste = []
                for j in range(len(liste[i].cells)):
                    sous_liste.append(liste[i].cells[j].content.value)
                ref_list.append(sous_liste)

            item = 1
            for row in ref_list:
                total_devis += row[4]
                can.setFillColorRGB(0, 0, 0)
                can.setFont("Helvetica", 10)
                can.drawCentredString(1.5 * cm, (y - 2.6) * cm, f"{item}")
                can.drawCentredString(7.75 * cm, (y - 2.6) * cm, f"{row[1]}")
                can.drawCentredString(14 * cm, (y - 2.6) * cm, f"{row[2]}")
                can.drawCentredString(15 * cm, (y - 2.6) * cm, f"{backend.look_unit(row[0])}")
                can.drawCentredString(16.5 * cm, (y - 2.6) * cm, f"{milSep(row[3])}")
                can.drawCentredString(18.75 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
                # lignes verticales
                can.setStrokeColorRGB(0, 0, 0)
                can.line(1 * cm, (y - 1) * cm, 1 * cm, (y - 3) * cm)
                can.line(2 * cm, (y - 1) * cm, 2 * cm, (y - 3) * cm)
                can.line(13.5 * cm, (y - 1) * cm, 13.5 * cm, (y - 3) * cm)
                can.line(14.5 * cm, (y - 1) * cm, 14.5 * cm, (y - 3) * cm)
                can.line(15.5 * cm, (y - 1) * cm, 15.5 * cm, (y - 3) * cm)
                can.line(17.5 * cm, (y - 1) * cm, 17.5 * cm, (y - 3) * cm)
                can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 3) * cm)
                # lignes horizontales
                can.setStrokeColorRGB(0, 0, 0)
                can.line(1 * cm, (y - 3) * cm, 20 * cm, (y - 3) * cm)
                item += 1
                y -= 1

            y = y - 1.5

            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(16 * cm, (y - 1) * cm, "Total:")
            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - 1) * cm, f"{milSep(total_devis)}")

            if int(self.remise.value) != 0:
                rem = str(self.remise.value)
                mt_rem = int(total_devis * rem // 100)
                net = int(total_devis - mt_rem)
                ir = int(net * 5.5 // 100)
                nap = int(net - ir)
                can.setFont("Helvetica-Bold", 10)
                can.drawCentredString(16 * cm, (y - 1.5) * cm, "Remise:")
                can.drawCentredString(16 * cm, (y - 2) * cm, "net:")
                can.drawCentredString(16 * cm, (y - 2.5) * cm, "IR:")
                can.drawCentredString(16 * cm, (y - 3) * cm, "NAP:")

                can.setFont("Helvetica", 11)
                can.drawCentredString(18.5 * cm, (y - 1.5) * cm, f"{milSep(mt_rem)}")
                can.drawCentredString(18.5 * cm, (y - 2) * cm, f"{milSep(net)}")
                can.drawCentredString(15.5 * cm, (y - 2.5) * cm, f"{milSep(ir)}")
                can.drawCentredString(15.5 * cm, (y - 3) * cm, f"{milSep(nap)}")
                can.setFont("Helvetica-Bold", 11)
                can.drawString(1 * cm, (y - 4) * cm, f"Montant total: {ecrire_en_lettres(nap)}")
                infos = backend.show_info_devis(self.search_devis.value)

                can.setFont("Helvetica", 11)
                can.drawString(1 * cm, (y - 5) * cm, "NB:")
                nb_list = infos[7].split(";")
                if infos[7] is not None:
                    for i in range(len(nb_list) - 1):
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, ((y - 5.5) - i * 0.5) * cm, f"{nb_list[i].lower()}")

                y = y - 5 - len(nb_list) * 0.5

                if infos[8] is not None:
                    can.setFont("Helvetica-Bold", 12)
                    can.drawString(1 * cm, (y - 0.5) * cm, f"Délai de livraison: {infos[8]}")

                if infos[9] is not None:
                    can.setFont("Helvetica-Bold", 12)
                    can.drawString(1 * cm, (y - 1) * cm, f"Point de llivraison: {infos[9]}")

                if infos[11] is not None:
                    can.setFont("Helvetica-Bold", 12)
                    can.drawString(1 * cm, (y - 1.5) * cm, f"Paiement: {infos[11]} jours après dépôt de facture")

                if infos[10] is not None:
                    can.setFont("Helvetica-Bold", 12)
                    can.drawString(1 * cm, (y - 2) * cm, f"NB: validité de l'offre: {infos[10]} mois")

                can.setFont("Helvetica", 10)
                can.drawString(1 * cm, (y - 3) * cm, "INFORMATIONS BANCAIRES")
                can.setFont("Helvetica", 11)
                can.drawString(1 * cm, (y - 3.5) * cm, f"par virement à: {ENTITE_BANQUE},   IBAN {ENTITE_IBAN}")
                can.drawString(1 * cm, (y - 4) * cm, f"Code swift: {ENTITE_SWIFT},  Titualire: {ENTITE_NOM}")

            else:
                ir = int(total_devis * 5.5 // 100)
                nap = int(total_devis - ir)
                can.setFont("Helvetica-Bold", 10)
                can.drawCentredString(16 * cm, (y - 1.5) * cm, "IR:")
                can.drawCentredString(16 * cm, (y - 2) * cm, "NAP:")

                can.setFont("Helvetica", 11)
                can.drawCentredString(18.5 * cm, (y - 1.5) * cm, f"{milSep(ir)} ")
                can.drawCentredString(18.5 * cm, (y - 2) * cm, f"{milSep(nap)}")

                can.setFont("Helvetica-Bold", 11)
                can.drawString(1 * cm, (y - 3) * cm, f"Montant total: {ecrire_en_lettres(nap)}")

                infos = backend.show_info_devis(self.search_devis.value)

                can.setFont("Helvetica", 11)
                can.drawString(1 * cm, (y - 4) * cm, "NB:")
                nb_list = infos[7].split(";")
                if infos[7] is not None:
                    for i in range(0, len(nb_list) - 1):
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, ((y - 4.5) - i * 0.5) * cm, f"{nb_list[i].lower()}")

                y = y - 4 - len(nb_list) * 0.5

                if infos[8] is not None:
                    can.setFont("Helvetica-Bold", 12)
                    can.drawString(1 * cm, (y - 0.5) * cm, f"Délai de livraison: {infos[8]}")

                if infos[9] is not None:
                    can.setFont("Helvetica-Bold", 12)
                    can.drawString(1 * cm, (y - 1) * cm, f"Point de llivraison: {infos[9]}")

                if infos[11] is not None:
                    can.setFont("Helvetica-Bold", 12)
                    can.drawString(1 * cm, (y - 1.5) * cm, f"Paiement: {infos[11]} jours après dépôt de facture")

                if infos[10] is not None:
                    can.setFont("Helvetica-Bold", 12)
                    can.drawString(1 * cm, (y - 2) * cm, f"NB: validité de l'offre: {infos[10]} mois")

                can.setFont("Helvetica", 10)
                can.drawString(1 * cm, (y - 3) * cm, "INFORMATION BANCAIRES")
                can.setFont("Helvetica", 11)
                can.drawString(1 * cm, (y - 3.5) * cm, f"par virement à: {ENTITE_BANQUE},   IBAN {ENTITE_IBAN}")
                can.drawString(1 * cm, (y - 4) * cm, f"Code swift: {ENTITE_SWIFT},  Titualire: {ENTITE_NOM}")

            can.save()
            self.good_impression.open = True
            self.good_impression.update()

    def close_good_impression(self, e):
        self.good_impression.open = False
        self.good_impression.update()

    def close_bad_impression(self, e):
        self.bad_impression.open = False
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
            self.search_devis.value, self.bc_client.value, self.ov.value, info_facture[11])

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

        self.valid_text.value = f"facture N° {numero_facture} générée avec succés"
        self.valid_text.update()
        self.valid_box.open = True
        self.valid_box.update()

    def close_facturer_window(self, e):
        self.facturer_window.open = False
        self.facturer_window.update()

    def close_error_facture(self, e):
        self.error_facture.open = False
        self.error_facture.update()

    def close_error_stock(self, e):
        self.error_stock.open = False
        self.error_stock.update()

    def imprimer_bordereau(self, e: ft.FilePickerResultEvent):
        if self.statut.value.lower() == "non facturé":
            self.error_bordereau.open = True
            self.error_bordereau.update()

        else:
            save_location = e.path
            fichier = f"{os.path.abspath(save_location)}.pdf"
            can = Canvas("{0}".format(fichier), pagesize=A4)

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
                can.setFont("Helvetica-Bold", 16)
                can.setFillColorRGB(0, 0, 0)
                can.drawCentredString(5.5 * cm, 24.5 * cm, "BORDEREAU DE LIVRAISON")
                can.setFont("Helvetica", 12)
                num_bex = backend.search_bordereau(self.search_devis.value)[1]
                can.drawCentredString(5.5 * cm, 23.8 * cm, f"N°: {num_bex}")
                can.setFont("Helvetica", 11)
                can.drawCentredString(5.5 * cm, 23.3 * cm, f"date: {ecrire_date(self.date.value)}")
                bc_client = backend.find_bc_by_devis(self.search_devis.value)
                can.setFont("Helvetica", 10)
                can.drawCentredString(5.5 * cm, 22.8 * cm, f"BC: {bc_client}")

                # infos client"
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
            can.line(2 * cm, (y - 1) * cm, 2 * cm, (y - 2) * cm)
            can.line(13.5 * cm, (y - 1) * cm, 13.5 * cm, (y - 2) * cm)
            can.line(14.5 * cm, (y - 1) * cm, 14.5 * cm, (y - 2) * cm)
            can.line(15.5 * cm, (y - 1) * cm, 15.5 * cm, (y - 2) * cm)
            can.line(17.5 * cm, (y - 1) * cm, 17.5 * cm, (y - 2) * cm)
            can.line(20 * cm, (y - 1) * cm, 20 * cm, (y - 2) * cm)
            # draw headers
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(1.5 * cm, (y - 1.6) * cm, "item")
            can.drawCentredString(7.75 * cm, (y - 1.6) * cm, "Désignation")
            can.drawCentredString(14 * cm, (y - 1.6) * cm, "Qté")
            can.drawCentredString(15 * cm, (y - 1.6) * cm, "U")
            can.drawCentredString(16.5 * cm, (y - 1.6) * cm, "P.U.")
            can.drawCentredString(18.75 * cm, (y - 1.6) * cm, "Montant")

            ref_list = []
            total_devis = 0
            liste = self.table_devis.rows[:]  # liste de DataRow
            for i in range(len(liste)):
                sous_liste = []
                for j in range(len(liste[i].cells)):
                    sous_liste.append(liste[i].cells[j].content.value)
                ref_list.append(sous_liste)

            item = 1
            for row in ref_list:
                total_devis += row[4]
                can.setFillColorRGB(0, 0, 0)
                can.setFont("Helvetica", 10)
                can.drawCentredString(1.5* cm, (y - 2.6)*cm, f"{item}")
                can.drawCentredString(7.75* cm, (y - 2.6)*cm, f"{row[1]}")
                can.drawCentredString(14* cm, (y - 2.6)*cm, f"{row[2]}")
                can.drawCentredString(15* cm, (y - 2.6)*cm, f"{backend.look_unit(row[0])}")
                can.drawCentredString(16.5 * cm, (y - 2.6)*cm, f"{milSep(row[3])}")
                can.drawCentredString(18.75 * cm, (y - 2.6)*cm, f"{milSep(row[4])}")
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
                item += 1
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

    def open_select_m_ref_windows(self, e):
        self.select_m_ref_window.scale = 1
        self.select_m_ref_window.update()

    def load_m_ref(self):
        for row in self.m_table_ref.rows[:]:
            self.m_table_ref.rows.remove(row)

        datas = backend.all_ref_and_desig()
        for data in datas:
            self.m_table_ref.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(f"{data[0].upper()}", style=ft.TextStyle(font_family="poppins Medium", size=12))),
                        ft.DataCell(
                            ft.Text(f"{data[1].upper()}", style=ft.TextStyle(font_family="poppins Medium", size=12))),
                    ],
                    on_select_changed=lambda e: self.on_select_change_m_ref(e.control.cells[0].content.value)
                )
            )

    def on_change_m_ref(self, e):
        for row in self.m_table_ref.rows[:]:
            self.m_table_ref.rows.remove(row)

        datas = []
        for data in backend.all_ref_and_desig():
            dico = {"reference": data[0], "designation": data[1]}
            datas.append(dico)

        myfiler = list(filter(lambda x: self.filtre_m_ref.value.lower() in x['designation'].lower(), datas))

        for row in myfiler:
            self.m_table_ref.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(
                        ft.Text(f"{row['reference']}", style=ft.TextStyle(font_family="Poppins Medium", size=12))),
                    ft.DataCell(
                        ft.Text(f"{row['designation']}", style=ft.TextStyle(font_family="Poppins Medium", size=12)))
                ],
                    on_select_changed=lambda e: self.on_select_change_m_ref(e.control.cells[0].content.value)
                )
            )
        self.m_table_ref.update()

    def on_select_change_m_ref(self, e):
        self.choix.value = e
        self.choix.update()
        self.m_reference.value = self.choix.value
        self.m_reference.update()
        self.select_m_ref_window.scale = 0
        self.select_m_ref_window.animate_scale = ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT)
        self.select_m_ref_window.update()
        self.changement_m_reference_2()

    def changement_m_reference(self, e):
        self.m_designation.value = backend.search_designation(self.m_reference.value)[0]
        self.m_designation.update()

    def changement_m_reference_2(self):
        self.m_designation.value = backend.search_designation(self.m_reference.value)[0]
        self.m_designation.update()

    def load_edit_ref_list2(self):
        for name in backend.all_references():
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

            for row in self.table_edit_devis.rows[:]:
                self.table_edit_devis.rows.remove(row)

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
            self.table_edit_devis.update()

            infos_devis = backend.show_info_devis(self.m_devis.value)
            self.m_total.value = infos_devis[3]
            self.m_total_lettres.value = infos_devis[5]
            self.m_remise.value = str(infos_devis[4])
            self.m_notabene.value = infos_devis[7]
            self.m_delai.value = infos_devis[8]
            self.m_ptliv.value = infos_devis[9]
            self.m_validite.value = infos_devis[10]
            self.m_paydelay.value = infos_devis[11]

            for widget in (self.m_total, self.m_total_lettres, self.m_remise, self.m_notabene, self.m_delai, self.m_ptliv, self.m_validite, self.m_paydelay):
                widget.update()

            self.edit_devis_window.scale = 1
            self.edit_devis_window.update()

    def select_item(self, e, f, h, i):
        self.id_ligne.value = e
        self.m_reference.value = f
        self.m_designation.value = backend.search_designation(self.m_reference.value)[0]
        self.m_qte.value = h
        self.m_prix.value = i

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
        remise += 1
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
        if remise > 0:
            remise -= 1
            self.m_remise.value = remise
            self.m_remise.update()

    def finish_edit_devis(self, e):
        montant = int(self.m_total.value)
        remise = int(self.m_remise.value)
        lettres = self.m_total_lettres.value
        backend.update_devis(montant, remise, lettres, self.m_notabene.value, self.m_delai.value, self.m_ptliv.value, self.m_validite.value, self.m_paydelay.value, self.m_devis.value)
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
                                    spacing=10, scroll=ft.ScrollMode.ADAPTIVE,
                                    controls=[
                                        ft.Container(**title_container_style, content=ft.Row([self.title_page])),
                                        self.filter_container,
                                        ft.Row([self.list_devis_container, self.devis_container]),
                                        self.infos_container,
                                        self.options_container,
                                    ]
                                )
                            ]
                        )
                    ),
                    self.new_devis_window,
                    self.edit_devis_window,
                    self.select_cli_window,
                    self.ecran_notifs,
                    self.select_n_ref_window,
                    self.select_m_ref_window,
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
                    self.modal_box,
                    self.valid_box,
                ]
            )
        )
