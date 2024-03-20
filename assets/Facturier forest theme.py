import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
import datetime
import os
import openpyxl
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
import BE_facturier
from useful_fonctions import *


# """fonctions pour supprimer les widgets"""![](Forest-dark screenshot.png)
def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def clear_frames():
    for element in frame_list:
        clear_widgets(element)


# infos de l'entreprise
ENTITE_NOM = "Fomiderc SARL"
ENTITE_TEL = "+237 690063525 / 654991819"
ENTITE_MAIL = "fomiderc.services@gmail.com"
ENTITE_WEB = "fomidercgroupeservices.com"
ENTITE_ADRESSE_1 = "Carrefour equinoxe Akwa-Douala"
ENTITE_ADRESSE_2 = "Face agence BENEFICIAL assurance"
ENTITE_RC = "RC/DLA/2018/B/510"
ENTITE_NUI = "M021812677041N"
ENTITE_BANQUE = "AFRILAND FIRST BANK"
ENTITE_IBAN = "CM21 10005 - 00022 - 08174701001 - 58"
ENTITE_SWIFT = "CCEICMCX"


def load_mod_devis_frame():
    """this function is to create and edit a devis"""

    global details_facture_liste, details_devis_liste
    details_facture_liste, details_devis_liste = [], []
    clear_frames()
    mod_devis_frame.tkraise()

    def activer_remise(*args):
        if var_activer.get() == 1:
            remise.config(state="enabled")
        else:
            remise.config(state="disabled")

    def mod_desig(*args):
        var_desig.set(BE_facturier.search_designation(var_reference.get()))

    def remplir_infos():
        details1 = BE_facturier.search_devis_details(num_devis_temp.get())
        for row in details1:
            tree.insert(parent='', index="end", text='', values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        details = BE_facturier.show_info_devis(num_devis_temp.get())
        var_montant.set(details[3])
        var_remise.set(details[4])
        var_lettres.set(details[5])

    def select_ligne(e):
        selected = tree.focus()
        valeurs = tree.item(selected, 'values')
        var_id.set(valeurs[0])
        var_reference.set(valeurs[1])
        var_desig.set(valeurs[2])
        var_qte.set(valeurs[3])
        var_prix.set(valeurs[4])

    def modifier_ligne():
        BE_facturier.update_devis_details(var_reference.get(), var_qte.get(), var_prix.get(), var_id.get())
        for child in tree.get_children():
            tree.delete(child)

        details = BE_facturier.search_devis_details(num_devis_temp.get())

        for row in details:
            tree.insert(parent='', index="end", text='',
                        values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=('oddrow',))

        total = 0
        for row in details:
            total += (row[3] * row[4])

        total = total - (total * var_remise.get() / 100)

        var_montant.set(total)
        var_lettres.set(ecrire_en_lettres(var_montant.get()))

    def ajouter_ligne():
        new_ligne = tk.Toplevel()
        new_ligne.title("Nouvelle ligne")

        def remplir_desig(*args):
            if var_ref.get() == "":
                var_des.set("")
            else:
                var_des.set(BE_facturier.search_designation(var_ref.get()))

        def valider():
            if var_ref.get() != "" and qte1.get() != "" and prix1.get() != "":
                BE_facturier.add_devis_details(num_devis_temp.get(), var_ref.get(), qte1.get(), prix1.get())
                var_ref.set("")
                qte1.delete(0, tk.END)
                prix1.delete(0, tk.END)
                lab.configure(text="Ligne joutée")

                for child in tree.get_children():
                    tree.delete(child)

                details = BE_facturier.search_devis_details(num_devis_temp.get())

                for row in details:
                    tree.insert(parent='', index="end", text='',
                                values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=('oddrow',))

                total = 0
                for row in details:
                    total += (row[3] * row[4])

                total = total - (total * var_remise.get() / 100)

                var_montant.set(total)
                var_lettres.set(ecrire_en_lettres(var_montant.get()))

            else:
                lab.configure(text="tous les champs sont obligatoires")

        var_ref = tk.StringVar()
        var_ref.trace("w", remplir_desig)
        var_des = tk.StringVar()

        infos_frame = ttk.LabelFrame(new_ligne, text="Infos ligne")
        infos_frame.grid(row=0, column=0, padx=10, pady=10)

        ref_lb = tk.Label(infos_frame, text="reference", font=font, fg="#8C8C8C")
        ref_lb.grid(row=0, column=0, sticky="e")
        ref = ttk.Combobox(infos_frame, width=20, textvariable=var_ref, font=font, values=BE_facturier.all_references(),
                           state="readonly")
        ref.grid(row=0, column=1, sticky="w")

        desig_lb = tk.Label(infos_frame, text="designation", font=font, fg="#8C8C8C")
        desig_lb.grid(row=1, column=0, sticky="e")
        desig = ttk.Entry(infos_frame, width=30, textvariable=var_des, font=font, state="disabled")
        desig.grid(row=1, column=1)

        qte1_lb = tk.Label(infos_frame, text="qte", font=font, fg="#8C8C8C")
        qte1_lb.grid(row=2, column=0, sticky="e")
        qte1 = ttk.Entry(infos_frame, width=5, font=font)
        qte1.grid(row=2, column=1, sticky="w")

        prix1_lb = tk.Label(infos_frame, text="prix", font=font, fg="#8C8C8C")
        prix1_lb.grid(row=3, column=0, sticky="e")
        prix1 = ttk.Entry(infos_frame, width=12, font=font)
        prix1.grid(row=3, column=1, sticky="w")

        for widget in infos_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)

        valider_bt = ttk.Button(new_ligne, text="valider", command=valider, style="Accent.TButton")
        valider_bt.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        lab = tk.Label(new_ligne, text="Ajouter nouvelle ligne")
        lab.grid(row=2, column=0, padx=10, pady=10)

    def valider_modifs():
        BE_facturier.update_devis(var_montant.get(), var_remise.get(), var_lettres.get(), num_devis_temp.get())
        showinfo("", "Devis modifié avec succès")
        load_all_devis_frame()

    var_reference = tk.StringVar()
    var_reference.trace("w", mod_desig)
    var_id = tk.StringVar()
    var_desig = tk.StringVar()
    var_qte = tk.IntVar()
    var_prix = tk.IntVar()
    var_remise = tk.IntVar()
    var_lettres = tk.StringVar()
    var_montant = tk.DoubleVar()
    var_activer = tk.IntVar()
    var_activer.trace("w", activer_remise)

    ifr = ttk.LabelFrame(mod_devis_frame, text="N° devis")
    ifr.grid(row=0, column=0, sticky="ew")

    tfr = tk.Frame(mod_devis_frame)
    tfr.grid(row=1, column=0, sticky="ew")

    dfr = ttk.LabelFrame(mod_devis_frame, text="Details devis")
    dfr.grid(row=2, column=0, sticky="ew")

    bfr = ttk.LabelFrame(mod_devis_frame, text="Commandes")
    bfr.grid(row=3, column=0, sticky="ew")

    tbfr = ttk.LabelFrame(mod_devis_frame, text="Infos devis")
    tbfr.grid(row=4, column=0, sticky="ew")

    bfr2 = ttk.LabelFrame(mod_devis_frame, text="Valider modifications")
    bfr2.grid(row=5, column=0, sticky="ew")

    # ifr
    devis_lb = tk.Label(ifr, text="N° Devis", font=font, fg="#8C8C8C")
    devis_lb.grid(row=0, column=0, sticky="e")
    devis = ttk.Entry(ifr, width=20, textvariable=num_devis_temp, font=font, state="disabled")
    devis.grid(row=0, column=1)

    afficher_bt = ttk.Button(ifr, text="afficher infos", style="Accent.TButton", command=remplir_infos)
    afficher_bt.grid(row=0, column=2)

    # tfr
    scrolly = ttk.Scrollbar(tfr, orient=tk.VERTICAL)
    scrolly.pack(fill='y', side=tk.LEFT)

    tree = ttk.Treeview(tfr, columns=(1, 2, 3, 4, 5, 6), show="headings", height=5, yscrollcommand=scrolly.set,
                        selectmode="extended")
    scrolly.configure(command=tree.yview)

    tree.pack(fill=tk.BOTH, pady=10, padx=2)
    tree.heading(1, text="id")
    tree.heading(2, text="reference")
    tree.heading(3, text="designation")
    tree.heading(4, text="qte")
    tree.heading(5, text="prix")
    tree.heading(6, text="total")
    tree.column(1, width=70, anchor="center")
    tree.column(2, width=100, anchor="center")
    tree.column(3, width=200, anchor="center")
    tree.column(4, width=70, anchor="center")
    tree.column(5, width=100, anchor="center")
    tree.column(6, width=100, anchor="center")
    tree.bind('<ButtonRelease-1>', select_ligne)

    # dfr
    ref_lb = tk.Label(dfr, text="reference", font=font, fg="#8C8C8C")
    ref_lb.grid(row=0, column=0, sticky="e")
    ref = ttk.Combobox(dfr, width=20, textvariable=var_reference, font=font, values=BE_facturier.all_references())
    ref.grid(row=0, column=1)

    desig_lb = tk.Label(dfr, text="designation", font=font, fg="#8C8C8C")
    desig_lb.grid(row=0, column=2, sticky="e")
    desig = ttk.Entry(dfr, width=30, textvariable=var_desig, font=font, state="disabled")
    desig.grid(row=0, column=3)

    qte_lb = tk.Label(dfr, text="qte", font=font, fg="#8C8C8C")
    qte_lb.grid(row=0, column=4, sticky="e")
    qte = ttk.Entry(dfr, width=5, textvariable=var_qte, font=font)
    qte.grid(row=0, column=5)

    prix_lb = tk.Label(dfr, text="prix", font=font, fg="#8C8C8C")
    prix_lb.grid(row=0, column=6, sticky="e")
    prix = ttk.Entry(dfr, width=12, textvariable=var_prix, font=font)
    prix.grid(row=0, column=7)

    # bfr
    maj_ligne_bt = ttk.Button(bfr, text="Modifier ligne", style="Accent.TButton", command=modifier_ligne)
    maj_ligne_bt.grid(row=0, column=0)

    ajouter_bt = ttk.Button(bfr, text="Ajouter ligne", style="Accent.TButton", command=ajouter_ligne)
    ajouter_bt.grid(row=0, column=1)

    # tbfr
    activer = ttk.Checkbutton(tbfr, variable=var_activer, onvalue=1, offvalue=0, style="Switch")
    activer.grid(row=0, column=0)

    remise_lb = tk.Label(tbfr, text="remise (%)", font=font, fg="#8C8C8C")
    remise_lb.grid(row=0, column=1, stick="n")
    remise = ttk.Entry(tbfr, textvariable=var_remise, width=5, font=font, state="disabled")
    remise.grid(row=0, column=2, sticky="w")

    montant_lb = tk.Label(tbfr, text="montant", font=font, fg="#8C8C8C")
    montant_lb.grid(row=0, column=3, sticky="e")
    montant = ttk.Entry(tbfr, width=15, textvariable=var_montant, font=font, state="disabled")
    montant.grid(row=0, column=4)

    lettres_lb = tk.Label(tbfr, text="lettres", font=font, fg="#8C8C8C")
    lettres_lb.grid(row=0, column=5, sticky="e")
    lettres = ttk.Entry(tbfr, width=30, textvariable=var_lettres, font=font, state="disabled")
    lettres.grid(row=0, column=6)

    # bfr2
    retour_bt = ttk.Button(bfr2, text="Mettre à jour", style="Accent.TButton", command=modifier_ligne)
    retour_bt.grid(row=0, column=0)

    valider_bt = ttk.Button(bfr2, text="Valider modifs", style="Accent.TButton", command=valider_modifs)
    valider_bt.grid(row=0, column=1)

    for widget in mod_devis_frame.winfo_children():
        widget.grid_configure(padx=10, pady=10)

    for widget in ifr.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in dfr.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in bfr.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in tbfr.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in bfr2.winfo_children():
        widget.grid_configure(padx=10, pady=6)


def load_all_devis_frame():
    global details_facture_liste, details_devis_liste
    details_facture_liste, details_devis_liste = [], []
    clear_frames()
    all_devis_frame.tkraise()

    def remplir_infos(*args):
        if var_devis_numero.get() == "":
            var_client.set("")
            var_date.set("")
            var_objet.set("")
            var_montant.set("")
            var_remise.set("")
            var_lettres.set("")
            for child in tree.get_children():
                tree.delete(child)
        else:
            all_infos = BE_facturier.show_info_devis(var_devis_numero.get())
            if all_infos != None:
                var_client.set(all_infos[0])
                var_date.set(all_infos[1])
                var_objet.set(all_infos[2])
                var_montant.set(all_infos[3])
                var_remise.set(all_infos[4])
                var_lettres.set(all_infos[5])
                num_devis_temp.set(var_devis_numero.get())

                for child in tree.get_children():
                    tree.delete(child)

                count = 0
                for row in BE_facturier.search_devis_details(var_devis_numero.get()):
                    if count % 2 == 0:
                        tree.insert(parent='', index="end", iid=count, text='',
                                    values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=('oddrow',))
                    else:
                        tree.insert(parent='', index="end", iid=count, text='',
                                    values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=('evenrow',))

                    count += 1

            else:
                var_client.set("")
                var_date.set("")
                var_objet.set("")
                var_montant.set("")
                var_remise.set("")
                var_lettres.set("")
                for child in tree.get_children():
                    tree.delete(child)

    def imprimer_personnel():
        global ENTITE_NOM, ENTITE_TEL, ENTITE_MAIL, ENTITE_ADRESSE_1, ENTITE_ADRESSE_2, ENTITE_RC, ENTITE_NUI, ENTITE_WEB, ENTITE_BANQUE, ENTITE_IBAN, ENTITE_SWIFT
        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)  # 1) Choix d'un nom de fichier pour le document à produire :
        can = Canvas("{0}".format(fichier),
                     pagesize=A4)  # 2) Instanciation d'un "objet canevas" Reportlab lié à ce fichier :

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
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {var_devis_numero.get()}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(var_date.get())}")

            # infos du client
            infos_client = BE_facturier.infos_clients(var_client.get())
            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{var_client.get()}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[3] != None:
                can.drawString(11 * cm, 23.4 * cm, f"Contact: {infos_client[3]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[4] != None:
                can.drawString(11 * cm, 22.7 * cm, f"NUI: {infos_client[4]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[5] != None:
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

        for row in tree.get_children():
            ref_list.append(tree.item(row)['values'])

        for row in ref_list:
            total_devis += row[5]
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[3]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{BE_facturier.look_unit(row[1])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[5])}")
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

        if var_remise.get() != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - 1.5) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2) * cm, "Après remise:")
            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - 1.5) * cm, f"{var_remise.get()}%")
            can.drawCentredString(18.5 * cm, (y - 2) * cm, f"{milSep(var_montant.get())}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 3) * cm, f"arrêtée à la somme de: {var_lettres.get()}")
            can.drawCentredString(10.5 * cm, (y - 3.5) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        else:
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 2) * cm, f"arrêtée à la somme de: {var_lettres.get()}")
            can.drawCentredString(10.5 * cm, (y - 2.5) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")
        can.save()

    def imprimer_etat():
        global ENTITE_NOM, ENTITE_TEL, ENTITE_MAIL, ENTITE_ADRESSE_1, ENTITE_ADRESSE_2, ENTITE_RC, ENTITE_NUI, ENTITE_WEB, ENTITE_BANQUE, ENTITE_IBAN, ENTITE_SWIFT
        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)  # 1) Choix d'un nom de fichier pour le document à produire :
        can = Canvas("{0}".format(fichier),
                     pagesize=A4)  # 2) Instanciation d'un "objet canevas" Reportlab lié à ce fichier :

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
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {var_devis_numero.get()}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(var_date.get())}")
            # infos du client
            infos_client = BE_facturier.infos_clients(var_client.get())
            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{var_client.get()}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[3] != None:
                can.drawString(11 * cm, 23.4 * cm, f"Contact: {infos_client[3]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[4] != None:
                can.drawString(11 * cm, 22.7 * cm, f"NUI: {infos_client[4]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[5] != None:
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

        for row in tree.get_children():
            ref_list.append(tree.item(row)['values'])

        for row in ref_list:
            total_devis += row[5]
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[3]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{BE_facturier.look_unit(row[1])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[5])}")
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

        if var_remise.get() != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Après remise:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "NAP:")
            can.drawCentredString(15.5 * cm, (y - 5 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 6 * pas) * cm, "Total TTC:")
            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{var_remise.get()}%")
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(var_montant.get())}")

            if var_montant.get() < 5000000:
                mt_ir = var_montant.get() * 5.5 / 100
            else:
                mt_ir = var_montant.get() * 2.2 / 100

            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_ir))}")
            mt_nap = var_montant.get() - mt_ir
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_nap))}")
            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 5 * pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 6 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 8 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")
            can.drawCentredString(10.5 * cm, (y - 9 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        else:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "NAP:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "Total TTC:")
            can.setFont("Helvetica", 11)

            if var_montant.get() < 5000000:
                mt_ir = var_montant.get() * 5.5 / 100
            else:
                mt_ir = var_montant.get() * 2.2 / 100

            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{milSep(int(mt_ir))}")
            mt_nap = var_montant.get() - mt_ir
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(mt_nap))}")
            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 6 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")
            can.drawCentredString(10.5 * cm, (y - 7 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")
        can.save()

    def imprimer_seul_TVA():
        global ENTITE_NOM, ENTITE_TEL, ENTITE_MAIL, ENTITE_ADRESSE_1, ENTITE_ADRESSE_2, ENTITE_RC, ENTITE_NUI, ENTITE_WEB, ENTITE_BANQUE, ENTITE_IBAN, ENTITE_SWIFT
        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)  # 1) Choix d'un nom de fichier pour le document à produire :
        can = Canvas("{0}".format(fichier),
                     pagesize=A4)  # 2) Instanciation d'un "objet canevas" Reportlab lié à ce fichier :

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
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {var_devis_numero.get()}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(var_date.get())}")
            # infos du client
            infos_client = BE_facturier.infos_clients(var_client.get())
            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{var_client.get()}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[3] != None:
                can.drawString(11 * cm, 23.4 * cm, f"Contact: {infos_client[3]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[4] != None:
                can.drawString(11 * cm, 22.7 * cm, f"NUI: {infos_client[4]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[5] != None:
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
        for row in tree.get_children():
            ref_list.append(tree.item(row)['values'])

        for row in ref_list:
            total_devis += row[5]
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[3]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{BE_facturier.look_unit(row[1])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[5])}")
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

        if var_remise.get() != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Montant après remise:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "Total TTC:")
            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{var_remise.get()}%")
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(var_montant.get())}")
            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 6 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")
            can.drawCentredString(10.5 * cm, (y - 7 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        else:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Total TTC:")
            can.setFont("Helvetica", 11)
            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 4 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")
            can.drawCentredString(10.5 * cm, (y - 5 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")
        can.save()

    def imprimer_IR_sans_NAP():
        global ENTITE_NOM, ENTITE_TEL, ENTITE_MAIL, ENTITE_ADRESSE_1, ENTITE_ADRESSE_2, ENTITE_RC, ENTITE_NUI, ENTITE_WEB, ENTITE_BANQUE, ENTITE_IBAN, ENTITE_SWIFT
        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)  # 1) Choix d'un nom de fichier pour le document à produire :
        can = Canvas("{0}".format(fichier),
                     pagesize=A4)  # 2) Instanciation d'un "objet canevas" Reportlab lié à ce fichier :

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
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {var_devis_numero.get()}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(var_date.get())}")
            # infos du client
            infos_client = BE_facturier.infos_clients(var_client.get())
            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{var_client.get()}")
            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[3] != None:
                can.drawString(11 * cm, 23.4 * cm, f"Contact: {infos_client[3]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[4] != None:
                can.drawString(11 * cm, 22.7 * cm, f"NUI: {infos_client[4]}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if infos_client[5] != None:
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

        for row in tree.get_children():
            ref_list.append(tree.item(row)['values'])

        for row in ref_list:
            total_devis += row[5]
            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[3]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{BE_facturier.look_unit(row[1])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[5])}")
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

        if var_remise.get() != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Après remise:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 5 * pas) * cm, "Total TTC:")

            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{var_remise.get()}%")
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(var_montant.get())}")

            if var_montant.get() < 5000000:
                mt_ir = var_montant.get() * 5.5 / 100
            else:
                mt_ir = var_montant.get() * 2.2 / 100
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_ir))}")

            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 5 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 7 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")
            can.drawCentredString(10.5 * cm, (y - 8 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        else:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "Total TTC:")
            can.setFont("Helvetica", 11)

            if var_montant.get() < 5000000:
                mt_ir = var_montant.get() * 5.5 / 100
            else:
                mt_ir = var_montant.get() * 2.2 / 100

            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{milSep(int(mt_ir))}")
            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(mt_tva))}")
            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_ttc))}")
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 5 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")
            can.drawCentredString(10.5 * cm, (y - 6 * pas) * cm,
                                  "Disponibilité: produits disponibles en stock sauf vente entretemps")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")
        can.save()

    def imprimer():
        if var_code.get() == 1:
            imprimer_etat()
            showinfo("", "Devis imprimé")

        elif var_code.get() == 2:
            imprimer_personnel()
            showinfo("", "Devis imprimé")

        elif var_code.get() == 3:
            imprimer_seul_TVA()
            showinfo("", "Devis imprimé")

        elif var_code.get() == 4:
            imprimer_IR_sans_NAP()
            showinfo("", "Devis imprimé")

        else:
            showerror("", "Veuillez choisir au moins une option")

    def facturer():
        if var_devis_numero.get() == "":
            showerror("", "Vous devez sélectionner un devis")
        else:
            if BE_facturier.search_statut_devis(var_devis_numero.get()) == "Facturé":
                showerror("", "ce devis est déja associé à une facture")

            else:
                info_facture = BE_facturier.show_info_devis(var_devis_numero.get())
                initiales_client = BE_facturier.search_initiales(info_facture[0])
                numero_facture = BE_facturier.find_facture_num(info_facture[0])
                details_factures = BE_facturier.find_devis_details(var_devis_numero.get())

                count_nc = 0
                for row in details_factures:

                    # vérifie les stocks
                    if BE_facturier.find_nature_ref(row[2]) == "stock":
                        ancien_stock = BE_facturier.find_stock_ref(row[2])

                        if ancien_stock < row[3]:
                            count_nc += 1

                if count_nc > 0:
                    showerror("",
                              f"la facturation ne peut s'effectuer!!! \n veuillez vérifier les quantités sorties par rapport au stock")

                else:
                    fen = tk.Toplevel()
                    fen.title("BC")

                    def make_facture():
                        BE_facturier.add_facture(numero_facture, info_facture[0], info_facture[3], info_facture[2],
                                                 info_facture[4], info_facture[5], var_devis_numero.get(), var_bc.get())
                        # creer details factures
                        for row in details_factures:
                            BE_facturier.add_details_facture(numero_facture, row[2], row[3], row[4])
                            # Mise à jour du stock
                            if BE_facturier.find_nature_ref(row[2]) == "stock":
                                ancien_stock = BE_facturier.find_stock_ref(row[2])
                                nouveau_stock = ancien_stock - row[3]
                                BE_facturier.update_stock(nouveau_stock, row[2])
                                BE_facturier.add_historique(row[2], "S", var_devis_numero.get(), ancien_stock, row[3],
                                                            nouveau_stock)

                        BE_facturier.maj_statut_devis(var_devis_numero.get())

                        # remplir les bordereaux de livraison
                        numero_bordereau = BE_facturier.find_bordereau_num(initiales_client)
                        BE_facturier.add_bordereau(numero_bordereau, var_devis_numero.get(), var_bc.get())

                        for row in details_factures:
                            BE_facturier.add_bordereau_details(numero_bordereau, row[2], row[3], row[4])

                        fen.destroy()
                        showinfo("", f"Facture N° {numero_facture} \n générée avec succès")

                    var_bc = tk.StringVar()
                    bclab = tk.Label(fen, text="Bon de commande client")
                    bclab.pack(padx=10, pady=10)

                    bcnum = ttk.Entry(fen, textvariable=var_bc, width=20)
                    bcnum.pack(padx=10, pady=10)

                    bt = ttk.Button(fen, style="Accent.TButton", command=make_facture, width=15, text="Valider")
                    bt.pack(padx=10, pady=10)
                    # creer facture

    def imprimer_bordereau():
        global ENTITE_NOM, ENTITE_TEL, ENTITE_MAIL, ENTITE_ADRESSE_1, ENTITE_ADRESSE_2, ENTITE_RC, ENTITE_NUI, ENTITE_WEB, ENTITE_BANQUE, ENTITE_IBAN, ENTITE_SWIFT

        if not BE_facturier.verif_bordereau(var_devis_numero.get()):
            showerror(f"Ce devis n'a pas été facturé!\n Vous devez facturer le devis au préalable")

        else:
            global ENTITE_NOM, ENTITE_TEL, ENTITE_MAIL, ENTITE_ADRESSE_1, ENTITE_ADRESSE_2, ENTITE_RC, ENTITE_NUI, ENTITE_WEB, ENTITE_BANQUE, ENTITE_IBAN, ENTITE_SWIFT

            chemin = asksaveasfilename(title='save as', defaultextension="pdf")
            fichier = os.path.abspath(chemin)  # 1) Choix d'un nom de fichier pour le document à produire :
            can = Canvas("{0}".format(fichier), pagesize=A4)  # 2) Instanciation d'un "objet canevas" Reportlab lié à ce fichier :

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
                num_bex = BE_facturier.search_bordereau(var_devis_numero.get())[1]
                bc = BE_facturier.search_bordereau(var_devis_numero.get())[3]
                can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {num_bex}")
                can.setFont("Helvetica", 12)
                can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(var_date.get())}")
                # infos du client
                infos_client = BE_facturier.infos_clients(var_client.get())
                # cadre des infos du client
                can.setStrokeColorRGB(0, 0, 0)
                can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)
                can.setFont("Helvetica-Bold", 12)
                can.setFillColorRGB(0, 0, 0)
                can.drawString(11 * cm, 24.1 * cm, f"{var_client.get()}")
                can.setFont("Helvetica", 12)
                can.setFillColorRGB(0, 0, 0)
                can.drawString(11 * cm, 23.6 * cm, f"BC client: {bc}")

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

            for row in tree.get_children():
                ref_list.append(tree.item(row)['values'])

            for row in ref_list:
                total_devis += row[5]
                can.setFillColorRGB(0, 0, 0)
                can.setFont("Helvetica", 10)
                can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[2]}")
                can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[3]}")
                can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{BE_facturier.look_unit(row[1])}")
                can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
                can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[5])}")

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
            showinfo("", "Bordereau généré avec succès")

    var_devis_numero = tk.StringVar()
    var_devis_numero.trace("w", remplir_infos)
    var_client = tk.StringVar()
    var_date = tk.StringVar()
    var_objet = tk.StringVar()
    var_montant = tk.IntVar()
    var_remise = tk.IntVar()
    var_lettres = tk.StringVar()
    var_code = tk.IntVar()

    select_devis = ttk.LabelFrame(all_devis_frame, text="Sélectionner le devis")
    select_devis.grid(row=0, column=0, sticky="ew")

    infos_devis = ttk.LabelFrame(all_devis_frame, text="Infos devis")
    infos_devis.grid(row=1, column=0, sticky="ew")

    details_devis = ttk.Frame(all_devis_frame)
    details_devis.grid(row=2, column=0, sticky="ew")

    bouton_frame = ttk.LabelFrame(all_devis_frame, text="Commandes")
    bouton_frame.grid(row=3, column=0, sticky="ew")

    bt_frame = ttk.LabelFrame(all_devis_frame, text="Options impression")
    bt_frame.grid(row=4, column=0, sticky="ew")

    # widgets select_devis
    devis_lb = tk.Label(select_devis, text="N° Devis", font=font, fg="#8C8C8C")
    devis_lb.grid(row=0, column=0, sticky="e")
    devis = ttk.Combobox(select_devis, values=BE_facturier.all_devis(), width=20, textvariable=var_devis_numero,
                         font=font, state="readonly")
    devis.grid(row=0, column=1)

    # widgets info_devis
    client_lb = tk.Label(infos_devis, text="client", font=font, fg="#8C8C8C")
    client_lb.grid(row=0, column=0, sticky="n")
    client = ttk.Entry(infos_devis, textvariable=var_client, width=70, font=font, state="disabled")
    client.grid(row=0, column=1, sticky="w", columnspan=6)

    date_lb = tk.Label(infos_devis, text="date", font=font, fg="#8C8C8C")
    date_lb.grid(row=1, column=0, sticky="n")
    date = ttk.Entry(infos_devis, textvariable=var_date, width=10, font=font, state="disabled")
    date.grid(row=1, column=1, sticky="w")

    montant_lb = tk.Label(infos_devis, text="montant", font=font, fg="#8C8C8C")
    montant_lb.grid(row=1, column=2, sticky="n")
    montant = ttk.Entry(infos_devis, textvariable=var_montant, width=12, font=font, state="disabled")
    montant.grid(row=1, column=3, sticky="w")

    remise_lb = tk.Label(infos_devis, text="remise", font=font, fg="#8C8C8C")
    remise_lb.grid(row=1, column=4, sticky="n")
    remise = ttk.Entry(infos_devis, textvariable=var_remise, width=8, font=font, state="disabled")
    remise.grid(row=1, column=5, sticky="w")

    lettres_lb = tk.Label(infos_devis, text="Montant lettres", font=font, fg="#8C8C8C")
    lettres_lb.grid(row=2, column=0, sticky="n")
    lettres = ttk.Entry(infos_devis, textvariable=var_lettres, width=70, font=font, state="disabled")
    lettres.grid(row=2, column=1, sticky="w", columnspan=6)

    # widget details_devis
    scrolly = ttk.Scrollbar(details_devis, orient=tk.VERTICAL)
    scrolly.pack(fill='y', side=tk.LEFT)

    tree = ttk.Treeview(details_devis, columns=(1, 2, 3, 4, 5, 6), show="headings", height=5,
                        yscrollcommand=scrolly.set, selectmode="extended")
    scrolly.configure(command=tree.yview)

    tree.pack(fill=tk.BOTH, pady=10, padx=2)
    tree.heading(1, text="id")
    tree.heading(2, text="reference")
    tree.heading(3, text="designation")
    tree.heading(4, text="qte")
    tree.heading(5, text="prix")
    tree.heading(6, text="total")
    tree.column(1, width=70, anchor="center")
    tree.column(2, width=100, anchor="center")
    tree.column(3, width=250, anchor="center")
    tree.column(4, width=70, anchor="center")
    tree.column(5, width=100, anchor="center")
    tree.column(6, width=100, anchor="center")

    # widget bouton_frame
    modifier_bt = ttk.Button(bouton_frame, text="Modifier", style="Accent.TButton", command=load_mod_devis_frame)
    modifier_bt.grid(row=0, column=0)

    facturer_bt = ttk.Button(bouton_frame, text="Facturer", style="Accent.TButton", command=facturer)
    facturer_bt.grid(row=0, column=2)

    bordereau_bt = ttk.Button(bouton_frame, text="bordereau livraison", style="Accent.TButton",
                              command=imprimer_bordereau)
    bordereau_bt.grid(row=0, column=3)

    etat = ttk.Radiobutton(bt_frame, text="Etat (TVA, IR, NAP)", variable=var_code, value=1)
    etat.grid(row=0, column=0)
    partic = ttk.Radiobutton(bt_frame, text="Particulier (sans TVA, IR, NAP)", variable=var_code, value=2)
    partic.grid(row=0, column=1)
    pme1 = ttk.Radiobutton(bt_frame, text="avec TVA (seule)", variable=var_code, value=3)
    pme1.grid(row=0, column=2)
    pme2 = ttk.Radiobutton(bt_frame, text="Avec IR sans NAP", variable=var_code, value=4)
    pme2.grid(row=0, column=3)

    imprimer_bt = ttk.Button(bt_frame, text="imprimer", style="Accent.TButton", command=imprimer)
    imprimer_bt.grid(row=0, column=4)

    for widget in all_devis_frame.winfo_children():
        widget.grid_configure(padx=10, pady=10)

    for widget in select_devis.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in infos_devis.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in bouton_frame.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in bt_frame.winfo_children():
        widget.grid_configure(padx=10, pady=6)


def load_devis_frame():
    global details_facture_liste, details_devis_liste
    details_facture_liste, details_devis_liste = [], []
    clear_frames()
    devis_frame.tkraise()

    def activer_remise(*args):
        if var_activer.get() == 1:
            remise.config(state="enabled")
        else:
            remise.config(state="disabled")
            var_remise.set(0)

    def mettre_numero_devis(*args):
        if var_client.get() == "":
            var_num_devis.set("")
        else:
            var_num_devis.set(BE_facturier.find_devis_num(var_client.get()))

    def mettre_designation(*args):
        if var_reference.get() == "":
            var_desig.set("")
        else:
            var_desig.set(BE_facturier.search_designation(var_reference.get()))

    def ajouter_details():
        global details_devis_liste

        details_devis_liste.append((var_reference.get(), var_desig.get(), var_qte.get(), var_prix.get()))

        for child in tree.get_children():
            tree.delete(child)

        for row in details_devis_liste:
            tree.insert(parent='', index="end", text='', values=(row[0], row[1], row[2], row[3]), tags=('oddrow',))

        var_reference.set("")
        var_qte.set("")
        var_prix.set("")

        valeurs = []
        total = 0

        for row in tree.get_children():
            valeurs.append(tree.item(row)['values'])

        for row in valeurs:
            total += (row[3] * row[2])

        total_remise = total - (total * (var_remise.get() / 100))

        var_montant.set(total)
        var_montant_lettres.set(ecrire_en_lettres(var_montant.get()))

    def creer_nouveau_devis():
        global details_devis_liste

        if var_client.get() == "" or var_objet.get() == "":
            showerror("les champs sont obligatoires")
        else:
            for row in tree.get_children():
                valeurs = tree.item(row)['values']
                BE_facturier.add_devis_details(var_num_devis.get(), valeurs[0], valeurs[2], valeurs[3])

            BE_facturier.add_devis(var_num_devis.get(), today, var_client.get(), var_montant.get(), var_objet.get(),
                                   var_remise.get(), var_montant_lettres.get())
            showinfo("", "devis généré avec succès")
            var_client.set("")
            var_objet.set("")
            var_montant.set(0)
            var_activer.set(0)
            var_montant_lettres.set("")

            for child in tree.get_children():
                tree.delete(child)

            details_devis_liste = []

    var_num_devis = tk.StringVar()
    var_client = tk.StringVar()
    var_client.trace("w", mettre_numero_devis)
    var_objet = tk.StringVar()
    var_reference = tk.StringVar()
    var_reference.trace("w", mettre_designation)
    var_desig = tk.StringVar()
    var_qte = tk.IntVar()
    var_prix = tk.IntVar()
    var_remise = tk.IntVar()
    var_montant = tk.DoubleVar()
    var_montant_lettres = tk.StringVar()
    var_activer = tk.IntVar()
    var_activer.trace("w", activer_remise)

    info_devis = ttk.LabelFrame(devis_frame, text="info devis")
    info_devis.grid(row=0, column=0, sticky="ew")

    details = ttk.LabelFrame(devis_frame, text="détails devis")
    details.grid(row=1, column=0, sticky="ew")

    bt_add_frame = ttk.LabelFrame(devis_frame, text="Ajouter")
    bt_add_frame.grid(row=2, column=0, sticky="ew")

    arbre_frame = ttk.Frame(devis_frame)
    arbre_frame.grid(row=3, column=0, sticky="ew")

    bt_valid_frame = ttk.LabelFrame(devis_frame, text="Valider devis")
    bt_valid_frame.grid(row=4, column=0, sticky="ew")

    # widgts info_devis
    num_devis_lb = tk.Label(info_devis, text="N° devis", font=font, fg="#8C8C8C")
    num_devis_lb.grid(row=0, column=0, stick="n")
    num_devis = ttk.Entry(info_devis, textvariable=var_num_devis, state="disabled", width=20, font=font)
    num_devis.grid(row=0, column=1, sticky="w")

    client_lb = tk.Label(info_devis, text="client", font=font, fg="#8C8C8C")
    client_lb.grid(row=0, column=2, stick="n")
    client = ttk.Combobox(info_devis, textvariable=var_client, values=BE_facturier.all_clients(), width=30, font=font,
                          state="readonly")
    client.grid(row=0, column=3, sticky="w")

    objet_lb = tk.Label(info_devis, text="objet", font=font, fg="#8C8C8C")
    objet_lb.grid(row=1, column=0, stick="n")
    objet = ttk.Entry(info_devis, textvariable=var_objet, width=75, font=font)
    objet.grid(row=1, column=1, sticky="w", columnspan=4)

    activer = ttk.Checkbutton(info_devis, variable=var_activer, onvalue=1, offvalue=0, style="Switch")
    activer.grid(row=2, column=0)

    remise_lb = tk.Label(info_devis, text="remise (%)", font=font, fg="#8C8C8C")
    remise_lb.grid(row=2, column=1, stick="n")
    remise = ttk.Spinbox(info_devis, textvariable=var_remise, from_=0, to=15, width=5, font=font, state="disabled")
    remise.grid(row=2, column=2, sticky="w")

    # widgts details
    reference_lb = tk.Label(details, text="reference", font=font, fg="#8C8C8C")
    reference_lb.grid(row=0, column=0, stick="n")
    reference = ttk.Combobox(details, textvariable=var_reference, width=15, values=BE_facturier.all_references(),
                             font=font)
    reference.grid(row=0, column=1, sticky="w", columnspan=3)

    desig = ttk.Entry(details, textvariable=var_desig, state="disabled", width=40, font=font)
    desig.grid(row=0, column=2, stick="w")

    qte_lb = tk.Label(details, text="qté", font=font, fg="#8C8C8C")
    qte_lb.grid(row=0, column=3, stick="n")
    qte = ttk.Entry(details, textvariable=var_qte, width=5, font=font)
    qte.grid(row=0, column=4, sticky="w")

    prix_lb = tk.Label(details, text="prix", font=font, fg="#8C8C8C")
    prix_lb.grid(row=1, column=0, stick="n")
    prix = ttk.Entry(details, textvariable=var_prix, width=15, font=font)
    prix.grid(row=1, column=1, sticky="w")

    prix_unit = tk.Label(details, text="prix", font=font, fg="#8C8C8C")
    prix_unit.grid(row=1, column=0, stick="n")
    prix_uni = ttk.Entry(details, textvariable=var_prix, width=15, font=font)
    prix_uni.grid(row=1, column=1, sticky="w")

    montant_lb = tk.Label(details, text="total devis", font=font, fg="#8C8C8C")
    montant_lb.grid(row=2, column=0, stick="n")
    montant = ttk.Entry(details, textvariable=var_montant, width=15, state="disabled", font=font)
    montant.grid(row=2, column=1, sticky="w")

    montant_lettres = ttk.Entry(details, textvariable=var_montant_lettres, width=50, state="disabled", font=font)
    montant_lettres.grid(row=2, column=2, sticky="w", columnspan=4)

    # bt_add_frame
    ajouter_bt = ttk.Button(bt_add_frame, text="Ajouter", style="Accent.TButton", command=ajouter_details)
    ajouter_bt.grid(row=0, column=0)

    # arbre_drame
    scrolly = ttk.Scrollbar(arbre_frame, orient=tk.VERTICAL)
    scrolly.pack(fill='y', side=tk.LEFT)

    tree = ttk.Treeview(arbre_frame, columns=(1, 2, 3, 4), show="headings", height=3, yscrollcommand=scrolly.set,
                        selectmode="extended")
    scrolly.configure(command=tree.yview)

    tree.pack(fill=tk.BOTH, pady=10, padx=2)
    tree.heading(1, text="reference")
    tree.heading(2, text="designation")
    tree.heading(3, text="Qte")
    tree.heading(4, text="Prix")
    tree.column(1, width=150, anchor="center")
    tree.column(2, width=250, anchor="center")
    tree.column(3, width=70, anchor="center")
    tree.column(4, width=100, anchor="center")

    # bt_valid_frame
    valider_bt = ttk.Button(bt_valid_frame, text="valider", style="Accent.TButton", command=creer_nouveau_devis)
    valider_bt.grid(row=0, column=0)

    for widget in devis_frame.winfo_children():
        widget.grid_configure(padx=10, pady=7)

    for widget in info_devis.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in details.winfo_children():
        widget.grid_configure(padx=14, pady=6)

    for widget in bt_add_frame.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in bt_valid_frame.winfo_children():
        widget.grid_configure(padx=10, pady=6)


# """Fonctions pour le chargement des sous-menus du menu factures"""
def load_facture_frame():
    global details_facture_liste, details_devis_liste
    details_facture_liste, details_devis_liste = [], []
    clear_frames()
    facture_frame.tkraise()

    def activer_remise(*args):
        if var_activer.get() == 1:
            remise.config(state="enabled")
        else:
            remise.config(state="disabled")
            var_remise.set(0)

    def mettre_numero_devis(*args):
        if var_client.get() == "":
            var_num_fact.set("")
        else:
            var_num_fact.set(BE_facturier.find_facture_num(BE_facturier.search_initiales(var_client.get())))

    def mettre_designation(*args):
        if var_reference.get() == "":
            var_desig.set("")
        else:
            var_desig.set(BE_facturier.search_designation(var_reference.get()))

    def ajouter_details():
        global details_facture_liste
        details_facture_liste.append((var_reference.get(), var_desig.get(), var_qte.get(), var_prix.get()))

        for child in tree.get_children():
            tree.delete(child)

        count = 0
        for row in details_facture_liste:
            if count % 2 == 0:
                tree.insert(parent='', index="end", iid=count, text='', values=(row[0], row[1], row[2], row[3]),
                            tags=('oddrow',))
            else:
                tree.insert(parent='', index="end", iid=count, text='', values=(row[0], row[1], row[2], row[3]),
                            tags=('evenrow',))
            count += 1

        var_reference.set("")
        var_qte.set("")
        var_prix.set("")

        valeurs = []
        total = 0

        for row in tree.get_children():
            valeurs.append(tree.item(row)['values'])

        for row in valeurs:
            total += (row[3] * row[2])

        total_remise = total - (total * (var_remise.get() / 100))

        var_montant.set(total)
        var_montant_lettres.set(ecrire_en_lettres(var_montant.get()))

    def creer_nouvelle_facture():
        global details_facture_liste

        if var_client.get() == "" or var_objet.get() == "":
            showerror("les champs sont obligatoires")

        else:
            for row in tree.get_children():
                valeurs = tree.item(row)['values']
                BE_facturier.add_details_facture(var_num_fact.get(), valeurs[0], valeurs[2], valeurs[3])

            num_devis = ""
            BE_facturier.add_facture(var_num_fact.get(), var_client.get(), var_montant.get(), var_objet.get(),
                                     var_remise.get(), var_montant_lettres.get(), num_devis)
            showinfo("facture générée avec succès")

            var_client.set("")
            var_objet.set("")
            var_montant.set(0)
            var_activer.set(0)
            var_montant_lettres.set("")

            for child in tree.get_children():
                tree.delete(child)

            details_facture_liste = []

    var_num_fact = tk.StringVar()
    var_client = tk.StringVar()
    var_client.trace("w", mettre_numero_devis)
    var_objet = tk.StringVar()
    var_reference = tk.StringVar()
    var_reference.trace("w", mettre_designation)
    var_desig = tk.StringVar()
    var_qte = tk.IntVar()
    var_prix = tk.IntVar()
    var_remise = tk.IntVar()
    var_montant = tk.DoubleVar()
    var_montant_lettres = tk.StringVar()
    var_activer = tk.IntVar()
    var_activer.trace("w", activer_remise)

    infos_fact = ttk.LabelFrame(facture_frame, text="   info facture   ")
    infos_fact.grid(row=0, column=0, sticky="ew")

    details = ttk.LabelFrame(facture_frame, text="   détails facture   ")
    details.grid(row=1, column=0, sticky="ew")

    bt_add_frame = ttk.LabelFrame(facture_frame, text="   Ajouter   ")
    bt_add_frame.grid(row=2, column=0, sticky="ew")

    arbre_frame = tk.Frame(facture_frame)
    arbre_frame.grid(row=3, column=0, sticky="ew")

    bt_valid_frame = ttk.LabelFrame(facture_frame, text="   Valider facture   ")
    bt_valid_frame.grid(row=4, column=0, sticky="ew")

    # widgts infos_fact
    num_fact_lb = tk.Label(infos_fact, text="N° facture", font=font)
    num_fact_lb.grid(row=0, column=0, stick="n")
    num_fact = ttk.Entry(infos_fact, textvariable=var_num_fact, state="disabled", width=20, font=font)
    num_fact.grid(row=0, column=1, sticky="w")

    client_lb = tk.Label(infos_fact, text="client", font=font)
    client_lb.grid(row=0, column=2, stick="n")
    client = ttk.Combobox(infos_fact, textvariable=var_client, values=BE_facturier.all_clients(), width=30, font=font,
                          state="readonly")
    client.grid(row=0, column=3, sticky="w")

    objet_lb = tk.Label(infos_fact, text="objet", font=font)
    objet_lb.grid(row=1, column=0, stick="n")
    objet = ttk.Entry(infos_fact, textvariable=var_objet, width=75, font=font)
    objet.grid(row=1, column=1, sticky="w", columnspan=4)

    activer = ttk.Checkbutton(infos_fact, variable=var_activer, onvalue=1, offvalue=0, style="Switch")
    activer.grid(row=2, column=0)

    remise_lb = tk.Label(infos_fact, text="remise(%)", font=font)
    remise_lb.grid(row=2, column=1, stick="n")
    remise = ttk.Spinbox(infos_fact, textvariable=var_remise, from_=0, to=15, width=5, font=font, state="disabled")
    remise.grid(row=2, column=2, sticky="w")

    # widgts details
    reference_lb = tk.Label(details, text="reference", font=font)
    reference_lb.grid(row=0, column=0, stick="n")
    reference = ttk.Combobox(details, textvariable=var_reference, width=15, values=BE_facturier.all_references(),
                             font=font, state="readonly")
    reference.grid(row=0, column=1, sticky="w", columnspan=3)

    desig = ttk.Entry(details, textvariable=var_desig, state="disabled", width=40, font=font)
    desig.grid(row=0, column=2, stick="w")

    qte_lb = tk.Label(details, text="qté", font=font)
    qte_lb.grid(row=0, column=3, stick="n")
    qte = ttk.Entry(details, textvariable=var_qte, width=5, font=font)
    qte.grid(row=0, column=4, sticky="w")

    prix_lb = tk.Label(details, text="prix", font=font)
    prix_lb.grid(row=1, column=0, stick="n")
    prix = ttk.Entry(details, textvariable=var_prix, width=15, font=font)
    prix.grid(row=1, column=1, sticky="w")

    montant_lb = tk.Label(details, text="total devis", font=font)
    montant_lb.grid(row=2, column=0, stick="n")
    montant = ttk.Entry(details, textvariable=var_montant, width=15, state="disabled", font=font)
    montant.grid(row=2, column=1, sticky="w")

    montant_lettres = ttk.Entry(details, textvariable=var_montant_lettres, width=50, state="disabled", font=font)
    montant_lettres.grid(row=2, column=2, sticky="w", columnspan=4)

    # bt_add_frame
    ajouter_bt = ttk.Button(bt_add_frame, text="Ajouter", style="Accent.TButton", command=ajouter_details)
    ajouter_bt.grid(row=0, column=0)

    # arbre_drame
    scrolly = ttk.Scrollbar(arbre_frame, orient="vertical")
    scrolly.pack(fill='y', side="left")

    tree = ttk.Treeview(arbre_frame, columns=(1, 2, 3, 4), show="headings", height=3, yscrollcommand=scrolly.set,
                        selectmode="extended")
    scrolly.configure(command=tree.yview)

    tree.pack(fill="both", pady=10, padx=2)
    tree.heading(1, text="reference")
    tree.heading(2, text="designation")
    tree.heading(3, text="Qte")
    tree.heading(4, text="Prix")
    tree.column(1, width=150, anchor="center")
    tree.column(2, width=250, anchor="center")
    tree.column(3, width=70, anchor="center")
    tree.column(4, width=100, anchor="center")

    tree.tag_configure('oddrow', background='#F9F9F9')
    tree.tag_configure('evenrow', background='white')

    # bt_valid_frame
    valider_bt = ttk.Button(bt_valid_frame, text="valider", style="Accent.TButton", command=creer_nouvelle_facture)
    valider_bt.grid(row=0, column=0)

    for widget in facture_frame.winfo_children():
        widget.grid_configure(padx=10, pady=7)

    for widget in infos_fact.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in details.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in bt_add_frame.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in bt_valid_frame.winfo_children():
        widget.grid_configure(padx=10, pady=6)


def load_all_facture_frame():
    global details_facture_liste, details_devis_liste
    details_facture_liste, details_devis_liste = [], []
    clear_frames()
    all_facture_frame.tkraise()

    def remplir_infos(*args):
        if var_fact_num.get() == "":
            var_client.set("")
            var_date.set("")
            var_objet.set("")
            var_montant.set("")
            var_remise.set("")
            var_lettres.set("")

            for child in tree.get_children():
                tree.delete(child)
        else:
            all_infos = BE_facturier.show_info_factures(var_fact_num.get())
            if all_infos == None:
                var_client.set("")
                var_date.set("")
                var_objet.set("")
                var_montant.set("")
                var_remise.set("")
                var_lettres.set("")
                for child in tree.get_children():
                    tree.delete(child)
            else:
                var_client.set(all_infos[0])
                var_date.set(all_infos[1])
                var_objet.set(all_infos[2])
                var_montant.set(all_infos[3])
                var_remise.set(all_infos[4])
                var_lettres.set(all_infos[5])
                num_devis_temp.set(var_fact_num.get())

                for child in tree.get_children():
                    tree.delete(child)

                count = 0
                for row in BE_facturier.search_factures_details(var_fact_num.get()):
                    if count % 2 == 0:
                        tree.insert(parent='', index="end", iid=count, text='',
                                    values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=('oddrow',))
                    else:
                        tree.insert(parent='', index="end", iid=count, text='',
                                    values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=('evenrow',))
                    count += 1
                var_num_fac_paie.set(var_fact_num.get())

    def imprimer_personnel():

        global ENTITE_NOM, ENTITE_TEL, ENTITE_MAIL, ENTITE_ADRESSE_1, ENTITE_ADRESSE_2, ENTITE_RC, ENTITE_NUI, ENTITE_WEB, ENTITE_BANQUE, ENTITE_IBAN, ENTITE_SWIFT

        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)  # 1) Choix d'un nom de fichier pour le document à produire :
        can = Canvas("{0}".format(fichier),
                     pagesize=A4)  # 2) Instanciation d'un "objet canevas" Reportlab lié à ce fichier :

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
            can.drawCentredString(15 * cm, 27.5 * cm, "Facture")

            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {var_fact_num.get()}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(var_date.get())}")

            # infos du client
            infos_client = BE_facturier.infos_clients(var_client.get())
            bc = BE_facturier.show_info_factures(var_fact_num.get())[6]
            devis = BE_facturier.show_info_factures(var_fact_num.get())[5]

            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)

            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{var_client.get()}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)

            if bc != None:
                can.drawString(11 * cm, 23.4 * cm, f"BC client: {bc}")
            else:
                can.drawString(11 * cm, 23.4 * cm, f"Suivant proforma N°: {bc}")

        draw_headers()

        y = 21.5

        can.setFillColorRGB(0.9, 0.9, 0.9)
        can.rect(1 * cm, (y - 2) * cm, 19 * cm, 1 * cm, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)

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

        for row in tree.get_children():
            ref_list.append(tree.item(row)['values'])

        for row in ref_list:
            total_devis += row[5]

            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[3]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{BE_facturier.look_unit(row[1])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[5])}")

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

        if var_remise.get() != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - 1.5) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2) * cm, "Après remise:")
            can.setFont("Helvetica-Oblique", 10)
            can.drawCentredString(18.5 * cm, (y - 1.5) * cm, f"{var_remise.get()}%")
            can.drawCentredString(18.5 * cm, (y - 2) * cm, f"{milSep(var_montant.get())}")

            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 3) * cm, f"arrêtée à la somme de: {var_lettres.get()}")

            can.setFont("Helvetica", 10)
            can.drawString(1 * cm, (y - 4) * cm, f"par virement à: {ENTITE_BANQUE}")
            can.drawString(1 * cm, (y - 4.5) * cm, f"IBAN: {ENTITE_IBAN}")
            can.drawString(1 * cm, (y - 5) * cm, f"Code swift: {ENTITE_SWIFT}")
            can.drawString(1 * cm, (y - 4.5) * cm, f"Titulaire: {ENTITE_NOM}")


        else:
            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 2) * cm, f"arrêtée à la somme de: {var_lettres.get()}")

            can.setFont("Helvetica", 10)
            can.drawString(1 * cm, (y - 3) * cm, f"par virement à: {ENTITE_BANQUE}")
            can.drawString(1 * cm, (y - 3.5) * cm, f"IBAN: {ENTITE_IBAN}")
            can.drawString(1 * cm, (y - 4) * cm, f"Code swift: {ENTITE_SWIFT}")
            can.drawString(1 * cm, (y - 4.5) * cm, f"Titulaire: {ENTITE_NOM}")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")

        can.save()
        showinfo("", "Facture générée avec succès")

    def imprimer_etat():

        global ENTITE_NOM, ENTITE_TEL, ENTITE_MAIL, ENTITE_ADRESSE_1, ENTITE_ADRESSE_2, ENTITE_RC, ENTITE_NUI, ENTITE_WEB, ENTITE_BANQUE, ENTITE_IBAN, ENTITE_SWIFT

        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)  # 1) Choix d'un nom de fichier pour le document à produire :
        can = Canvas("{0}".format(fichier),
                     pagesize=A4)  # 2) Instanciation d'un "objet canevas" Reportlab lié à ce fichier :

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
            can.drawCentredString(15 * cm, 27.5 * cm, "Facture")

            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {var_fact_num.get()}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(var_date.get())}")

            # infos du client
            infos_client = BE_facturier.infos_clients(var_client.get())
            bc = BE_facturier.show_info_factures(var_fact_num.get())[6]
            devis = BE_facturier.show_info_factures(var_fact_num.get())[5]

            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)

            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{var_client.get()}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)
            if bc != None:
                can.drawString(11 * cm, 23.4 * cm, f"BC client: {bc}")
            else:
                can.drawString(11 * cm, 23.4 * cm, f"Suivant proforma N°: {bc}")

        draw_headers()

        y = 21.5

        can.setFillColorRGB(0.9, 0.9, 0.9)
        can.rect(1 * cm, (y - 2) * cm, 19 * cm, 1 * cm, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)

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

        for row in tree.get_children():
            ref_list.append(tree.item(row)['values'])

        for row in ref_list:
            total_devis += row[5]

            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[3]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{BE_facturier.look_unit(row[1])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[5])}")

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
        can.drawCentredString(14.5 * cm, (y - 1) * cm, "Total:")
        can.setFont("Helvetica", 11)
        can.drawCentredString(18 * cm, (y - 1) * cm, f"{milSep(total_devis)}")

        y = y - 1

        pas = 0.5

        if var_remise.get() != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Après remise:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "NAP:")
            can.drawCentredString(15.5 * cm, (y - 5 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 6 * pas) * cm, "Total TTC:")

            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{var_remise.get()}%")
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(var_montant.get())}")

            if var_montant.get() < 5000000:
                mt_ir = var_montant.get() * 5.5 / 100
            else:
                mt_ir = var_montant.get() * 2.2 / 100
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_ir))}")

            mt_nap = var_montant.get() - mt_ir
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_nap))}")

            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 5 * pas) * cm, f"{milSep(int(mt_tva))}")

            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 6 * pas) * cm, f"{milSep(int(mt_ttc))}")

            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 8 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")

            can.setFont("Helvetica", 10)
            can.drawString(1 * cm, (y - 10 * pas) * cm, f"par virement à: {ENTITE_BANQUE}")
            can.drawString(1 * cm, (y - 11 * pas) * cm, f"IBAN: {ENTITE_IBAN}")
            can.drawString(1 * cm, (y - 12 * pas) * cm, f"Code swift: {ENTITE_SWIFT}")
            can.drawString(1 * cm, (y - 13 * pas) * cm, f"Code swift: {ENTITE_NOM}")

        else:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "NAP:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "Total TTC:")

            can.setFont("Helvetica", 11)
            if var_montant.get() < 5000000:
                mt_ir = var_montant.get() * 5.5 / 100
            else:
                mt_ir = var_montant.get() * 2.2 / 100
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{milSep(int(mt_ir))}")

            mt_nap = var_montant.get() - mt_ir
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(mt_nap))}")

            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_tva))}")

            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_ttc))}")

            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 6 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")

            can.setFont("Helvetica", 9)
            can.drawString(1 * cm, (y - 8 * pas) * cm, f"par virement à: {ENTITE_BANQUE}")
            can.drawString(1 * cm, (y - 9 * pas) * cm, f"IBAN: {ENTITE_IBAN}")
            can.drawString(1 * cm, (y - 10 * pas) * cm, f"Code swift: {ENTITE_SWIFT}")
            can.drawString(1 * cm, (y - 11 * pas) * cm, f"Code swift: {ENTITE_NOM}")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")

        can.save()
        showinfo("", "Facture générée avec succès")

    def imprimer_seul_TVA():

        global ENTITE_NOM, ENTITE_TEL, ENTITE_MAIL, ENTITE_ADRESSE_1, ENTITE_ADRESSE_2, ENTITE_RC, ENTITE_NUI, ENTITE_WEB, ENTITE_BANQUE, ENTITE_IBAN, ENTITE_SWIFT

        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)  # 1) Choix d'un nom de fichier pour le document à produire :
        can = Canvas("{0}".format(fichier),
                     pagesize=A4)  # 2) Instanciation d'un "objet canevas" Reportlab lié à ce fichier :

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
            can.drawCentredString(15 * cm, 27.5 * cm, "Facture")

            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {var_fact_num.get()}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(var_date.get())}")

            # infos du client
            infos_client = BE_facturier.infos_clients(var_client.get())
            bc = BE_facturier.show_info_factures(var_fact_num.get())[6]
            devis = BE_facturier.show_info_factures(var_fact_num.get())[5]

            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)

            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{var_client.get()}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)
            if bc != None:
                can.drawString(11 * cm, 23.4 * cm, f"BC client: {bc}")
            else:
                can.drawString(11 * cm, 23.4 * cm, f"Suivant proforma N°: {bc}")

        draw_headers()

        y = 21.5

        can.setFillColorRGB(0.9, 0.9, 0.9)
        can.rect(1 * cm, (y - 2) * cm, 19 * cm, 1 * cm, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)

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

        for row in tree.get_children():
            ref_list.append(tree.item(row)['values'])

        for row in ref_list:
            total_devis += row[5]

            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[3]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{BE_facturier.look_unit(row[1])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[5])}")

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

        if var_remise.get() != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Montant après remise:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "Total TTC:")

            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{var_remise.get()}%")
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(var_montant.get())}")

            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_tva))}")

            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_ttc))}")

            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 6 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")

            can.setFont("Helvetica", 10)
            can.drawString(1 * cm, (y - 8 * pas) * cm, f"par virement à: {ENTITE_BANQUE}")
            can.drawString(1 * cm, (y - 9 * pas) * cm, f"IBAN: {ENTITE_IBAN}")
            can.drawString(1 * cm, (y - 10 * pas) * cm, f"Code swift: {ENTITE_SWIFT}")
            can.drawString(1 * cm, (y - 11 * pas) * cm, f"Code swift: {ENTITE_NOM}")

        else:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Total TTC:")

            can.setFont("Helvetica", 11)
            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{milSep(int(mt_tva))}")

            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(mt_ttc))}")

            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 4 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")

            can.setFont("Helvetica", 10)
            can.drawString(1 * cm, (y - 6 * pas) * cm, f"par virement à: {ENTITE_BANQUE}")
            can.drawString(1 * cm, (y - 7 * pas) * cm, f"IBAN: {ENTITE_IBAN}")
            can.drawString(1 * cm, (y - 8 * pas) * cm, f"Code swift: {ENTITE_SWIFT}")
            can.drawString(1 * cm, (y - 9 * pas) * cm, f"Code swift: {ENTITE_NOM}")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")

        can.save()
        showinfo("", "Facture générée avec succès")

    def imprimer_IR_sans_NAP():

        global ENTITE_NOM, ENTITE_TEL, ENTITE_MAIL, ENTITE_ADRESSE_1, ENTITE_ADRESSE_2, ENTITE_RC, ENTITE_NUI, ENTITE_WEB, ENTITE_BANQUE, ENTITE_IBAN, ENTITE_SWIFT

        chemin = asksaveasfilename(title='save as', defaultextension="pdf")
        fichier = os.path.abspath(chemin)  # 1) Choix d'un nom de fichier pour le document à produire :
        can = Canvas("{0}".format(fichier),
                     pagesize=A4)  # 2) Instanciation d'un "objet canevas" Reportlab lié à ce fichier :

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
            can.drawCentredString(15 * cm, 27.5 * cm, "Facture")

            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.8 * cm, f"N°: {var_fact_num.get()}")
            can.setFont("Helvetica", 12)
            can.drawCentredString(15 * cm, 26.3 * cm, f"date: {ecrire_date(var_date.get())}")

            # infos du client
            infos_client = BE_facturier.infos_clients(var_client.get())
            bc = BE_facturier.show_info_factures(var_fact_num.get())[6]
            devis = BE_facturier.show_info_factures(var_fact_num.get())[5]

            # cadre des infos du client
            can.setStrokeColorRGB(0, 0, 0)
            can.rect(10.5 * cm, 21.6 * cm, 9.5 * cm, 3 * cm, fill=0, stroke=1)

            can.setFont("Helvetica-Bold", 12)
            can.setFillColorRGB(0, 0, 0)
            can.drawString(11 * cm, 24.1 * cm, f"{var_client.get()}")

            can.setFont("Helvetica", 11)
            can.setFillColorRGB(0, 0, 0)
            if bc != None:
                can.drawString(11 * cm, 23.4 * cm, f"BC client: {bc}")
            else:
                can.drawString(11 * cm, 23.4 * cm, f"Suivant proforma N°: {bc}")

        draw_headers()

        y = 21.5

        can.setFillColorRGB(0.9, 0.9, 0.9)
        can.rect(1 * cm, (y - 2) * cm, 19 * cm, 1 * cm, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)

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

        for row in tree.get_children():
            ref_list.append(tree.item(row)['values'])

        for row in ref_list:
            total_devis += row[5]

            can.setFillColorRGB(0, 0, 0)
            can.setFont("Helvetica", 10)
            can.drawCentredString(6 * cm, (y - 2.6) * cm, f"{row[2]}")
            can.drawCentredString(11.75 * cm, (y - 2.6) * cm, f"{row[3]}")
            can.drawCentredString(13.25 * cm, (y - 2.6) * cm, f"{BE_facturier.look_unit(row[1])}")
            can.drawCentredString(15.5 * cm, (y - 2.6) * cm, f"{milSep(row[4])}")
            can.drawCentredString(18.5 * cm, (y - 2.6) * cm, f"{milSep(row[5])}")

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

        if var_remise.get() != 0:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "Remise:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "Après remise:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 4 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 5 * pas) * cm, "Total TTC:")

            can.setFont("Helvetica", 11)
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{var_remise.get()}%")
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(var_montant.get())}")

            if var_montant.get() < 5000000:
                mt_ir = var_montant.get() * 5.5 / 100
            else:
                mt_ir = var_montant.get() * 2.2 / 100
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_ir))}")

            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 4 * pas) * cm, f"{milSep(int(mt_tva))}")

            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 5 * pas) * cm, f"{milSep(int(mt_ttc))}")

            can.setFont("Helvetica", 11)
            can.drawCentredString(10.5 * cm, (y - 7 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")

            can.setFont("Helvetica", 10)
            can.drawString(1 * cm, (y - 9 * pas) * cm, f"par virement à: {ENTITE_BANQUE}")
            can.drawString(1 * cm, (y - 10 * pas) * cm, f"IBAN: {ENTITE_IBAN}")
            can.drawString(1 * cm, (y - 11 * pas) * cm, f"Code swift: {ENTITE_SWIFT}")
            can.drawString(1 * cm, (y - 12 * pas) * cm, f"Code swift: {ENTITE_NOM}")

        else:
            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(15.5 * cm, (y - pas) * cm, "IR:")
            can.drawCentredString(15.5 * cm, (y - 2 * pas) * cm, "TVA:")
            can.drawCentredString(15.5 * cm, (y - 3 * pas) * cm, "Total TTC:")

            can.setFont("Helvetica", 11)

            if var_montant.get() < 5000000:
                mt_ir = var_montant.get() * 5.5 / 100
            else:
                mt_ir = var_montant.get() * 2.2 / 100
            can.drawCentredString(18.5 * cm, (y - pas) * cm, f"{milSep(int(mt_ir))}")

            mt_tva = var_montant.get() * 19.25 / 100
            can.drawCentredString(18.5 * cm, (y - 2 * pas) * cm, f"{milSep(int(mt_tva))}")

            mt_ttc = var_montant.get() + mt_tva
            can.drawCentredString(18.5 * cm, (y - 3 * pas) * cm, f"{milSep(int(mt_ttc))}")

            can.setFont("Helvetica-Bold", 10)
            can.drawCentredString(10.5 * cm, (y - 5 * pas) * cm, f"arrêtée à la somme de: {ecrire_en_lettres(mt_ttc)}")

            can.setFont("Helvetica", 10)
            can.drawString(1 * cm, (y - 7 * pas) * cm, f"par virement à: {ENTITE_BANQUE}")
            can.drawString(1 * cm, (y - 8 * pas) * cm, f"IBAN: {ENTITE_IBAN}")
            can.drawString(1 * cm, (y - 9 * pas) * cm, f"Code swift: {ENTITE_SWIFT}")
            can.drawString(1 * cm, (y - 10 * pas) * cm, f"Code swift: {ENTITE_NOM}")

        # pied de page
        can.setFont("Helvetica", 8)
        can.setFillColorRGB(0.25, 0.25, 0.25)
        can.drawCentredString(10.5 * cm, 1.3 * cm, "FOMIDERC SARL")
        can.drawCentredString(10.5 * cm, 0.9 * cm, f"{ENTITE_ADRESSE_1} {ENTITE_ADRESSE_2}")
        can.drawCentredString(10.5 * cm, 0.5 * cm, f"contact: {ENTITE_TEL}, courriel: {ENTITE_MAIL}")

        can.save()
        showinfo("", "Facture générée avec succès")

    def imprimer():
        if var_code.get() == 1:
            imprimer_etat()
        elif var_code.get() == 2:
            imprimer_personnel()
        elif var_code.get() == 3:
            imprimer_seul_TVA()
        elif var_code.get() == 4:
            imprimer_IR_sans_NAP()
        else:
            Messagebox().show_error("Veuillez choisir au moins une option")

    def paiement():
        fen_paie = tk.Toplevel()
        fen_paie.title("paiement")

        def remplir_montant(*args):
            if var_solde.get() == 0:
                verse.config(state="enabled")
                var_reglement.set(0)

            else:
                verse.config(state="disabled")
                var_reglement.set(var_mt.get())

        def remplir(*args):
            if BE_facturier.find_montant_facture(var_fac.get()) == None or var_fac.get() == "":
                var_mt.set(0)
            else:
                var_mt.set(BE_facturier.find_montant_facture(var_fac.get()))
                if BE_facturier.mt_deja_paye(var_fac.get()) == None:
                    var_deja.set(0)
                else:
                    var_deja.set(BE_facturier.mt_deja_paye(var_fac.get()))

        def valider_paiement():
            if var_reglement.get() == 0 or var_moyen.get() == "":
                verif.config(text="tous les champs sont obligatoires")

            else:
                reste = int(var_mt.get()) - int(var_deja.get())
                if var_reglement.get() > reste:
                    verif.config(text="Le total de reglèment sera supérieur au montant de la facture")

                else:
                    BE_facturier.add_reglement(var_fac.get(), var_reglement.get(), var_moyen.get())
                    verif.config(text="Règlement enregistré")
                    var_num_fac_paie.set("")
                    var_fac.set("")
                    var_mt.set(0)
                    var_deja.set(0)
                    var_reglement.set(0)
                    var_moyen.set("")

        var_fac = tk.StringVar()
        var_fac.trace("w", remplir)
        var_mt = tk.IntVar()
        var_reglement = tk.IntVar()
        var_solde = tk.IntVar()
        var_solde.trace("w", remplir_montant)
        var_moyen = tk.StringVar()
        var_deja = tk.IntVar()

        infos_fact = ttk.LabelFrame(fen_paie, text="   infos facture   ")
        infos_fact.grid(row=0, column=0, padx=10, pady=10)

        fact_lb = tk.Label(infos_fact, text="facture N°", font=font)
        fact_lb.grid(row=0, column=0)
        fact = ttk.Entry(infos_fact, textvariable=var_num_fac_paie, width=20, state="disabled", font=font)
        fact.grid(row=0, column=1)

        montant_lb = tk.Label(infos_fact, text="Total facture", font=font)
        montant_lb.grid(row=1, column=0)
        montant = ttk.Entry(infos_fact, textvariable=var_mt, width=15, state="disabled", font=font)
        montant.grid(row=1, column=1)

        deja_lb = tk.Label(infos_fact, text="Déja reglé", font=font)
        deja_lb.grid(row=2, column=0)
        deja = ttk.Entry(infos_fact, textvariable=var_deja, width=15, font=font, state="disabled")
        deja.grid(row=2, column=1)

        solde_lb = tk.Label(infos_fact, text="Solde", font=font)
        solde_lb.grid(row=3, column=0)
        solde = ttk.Checkbutton(infos_fact, variable=var_solde, offvalue=0, onvalue=1, style="Switch")
        solde.grid(row=3, column=1)

        verse_lb = tk.Label(infos_fact, text="Montant réglement", font=font)
        verse_lb.grid(row=4, column=0)
        verse = ttk.Entry(infos_fact, textvariable=var_reglement, width=15, font=font)
        verse.grid(row=4, column=1)

        moyen_lb = tk.Label(infos_fact, text="Moyen paiement", font=font)
        moyen_lb.grid(row=5, column=0)
        moyen = ttk.Combobox(infos_fact, values=["cash", "virement", "Mobile"], textvariable=var_moyen, width=15,
                             font=font, state="readonly")
        moyen.grid(row=5, column=1)

        valid_bt = ttk.Button(fen_paie, text="Valider", style="Accent.TButton", command=valider_paiement)
        valid_bt.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        verif = tk.Label(fen_paie, text="Valider paiement")
        verif.grid(row=2, column=0, padx=10, pady=10, sticky="n")

        var_fac.set(var_num_fac_paie.get())

        for widget in infos_fact.winfo_children():
            widget.grid_configure(padx=10, pady=10)

    var_fact_num = tk.StringVar()
    # var_fact_num.trace("w", filtre_dynamique)
    var_fact_num.trace("w", remplir_infos)
    var_client = tk.StringVar()
    var_date = tk.StringVar()
    var_objet = tk.StringVar()
    var_montant = tk.IntVar()
    var_remise = tk.IntVar()
    var_lettres = tk.StringVar()
    var_percu = tk.StringVar()
    var_statut = tk.StringVar()
    var_code = tk.IntVar()

    select_fact = ttk.LabelFrame(all_facture_frame, text="   Sélectionner le facture   ")
    select_fact.grid(row=0, column=0, sticky="ew")

    infos_fac = ttk.LabelFrame(all_facture_frame, text="   Infos facture  ")
    infos_fac.grid(row=1, column=0, sticky="ew")

    details_fact = tk.Frame(all_facture_frame)
    details_fact.grid(row=2, column=0, sticky="ew")

    bouton_frame = ttk.LabelFrame(all_facture_frame, text="   Boutons de commandes  ")
    bouton_frame.grid(row=3, column=0, sticky="ew")

    # widgets select_fact
    facture_lb = tk.Label(select_fact, text="N° facture", font=font)
    facture_lb.grid(row=0, column=0, sticky="e")
    facture = ttk.Combobox(select_fact, values=BE_facturier.all_factures(), width=20, textvariable=var_fact_num,
                           font=font, state="readonly")
    facture.grid(row=0, column=1)

    # widgets info_facture
    client_lb = tk.Label(infos_fac, text="client", font=font)
    client_lb.grid(row=0, column=0, sticky="n")
    client = ttk.Entry(infos_fac, textvariable=var_client, width=70, font=font, state="disabled")
    client.grid(row=0, column=1, sticky="w", columnspan=6)

    date_lb = tk.Label(infos_fac, text="date", font=font)
    date_lb.grid(row=1, column=0, sticky="n")
    date = ttk.Entry(infos_fac, textvariable=var_date, width=10, font=font, state="disabled")
    date.grid(row=1, column=1, sticky="w")

    montant_lb = tk.Label(infos_fac, text="montant", font=font)
    montant_lb.grid(row=1, column=2, sticky="n")
    montant = ttk.Entry(infos_fac, textvariable=var_montant, width=12, font=font, state="disabled")
    montant.grid(row=1, column=3, sticky="w")

    remise_lb = tk.Label(infos_fac, text="remise", font=font)
    remise_lb.grid(row=1, column=4, sticky="n")
    remise = ttk.Entry(infos_fac, textvariable=var_remise, width=8, font=font, state="disabled")
    remise.grid(row=1, column=5, sticky="w")

    percu_lb = tk.Label(infos_fac, text="montant percu", font=font)
    percu_lb.grid(row=2, column=0, sticky="n")
    percu = ttk.Entry(infos_fac, textvariable=var_percu, width=17, font=font, state="disabled")
    percu.grid(row=2, column=1, sticky="w")

    statut_lb = tk.Label(infos_fac, text="statut", font=font)
    statut_lb.grid(row=2, column=2, sticky="n")
    statut = ttk.Entry(infos_fac, textvariable=var_statut, width=8, font=font, state="disabled")
    statut.grid(row=2, column=3, sticky="w")

    lettres_lb = tk.Label(infos_fac, text="Montant lettres", font=font)
    lettres_lb.grid(row=3, column=0, sticky="n")
    lettres = ttk.Entry(infos_fac, textvariable=var_lettres, width=70, font=font, state="disabled")
    lettres.grid(row=3, column=1, sticky="w", columnspan=6)

    # widget details_fact
    scrolly = ttk.Scrollbar(details_fact, orient="vertical")
    scrolly.pack(fill='y', side="left")

    tree = ttk.Treeview(details_fact, columns=(1, 2, 3, 4, 5, 6), show="headings", height=5, yscrollcommand=scrolly.set,
                        selectmode="extended")
    scrolly.configure(command=tree.yview)

    tree.pack(fill="both", pady=10, padx=2)
    tree.heading(1, text="id")
    tree.heading(2, text="reference")
    tree.heading(3, text="designation")
    tree.heading(4, text="qte")
    tree.heading(5, text="prix")
    tree.heading(6, text="total")
    tree.column(1, width=70, anchor="center")
    tree.column(2, width=100, anchor="center")
    tree.column(3, width=250, anchor="center")
    tree.column(4, width=70, anchor="center")
    tree.column(5, width=100, anchor="center")
    tree.column(6, width=100, anchor="center")
    tree.tag_configure('oddrow', background='#F9F9F9')
    tree.tag_configure('evenrow', background='white')

    # widget bouton_frame
    etat = ttk.Radiobutton(bouton_frame, text="Etat (TVA, IR, NAP)", variable=var_code, value=1)
    etat.grid(row=0, column=0)
    partic = ttk.Radiobutton(bouton_frame, text="Particulier (sans TVA, IR, NAP)", variable=var_code, value=2)
    partic.grid(row=0, column=1)
    pme1 = ttk.Radiobutton(bouton_frame, text="avec TVA (seule)", variable=var_code, value=3)
    pme1.grid(row=0, column=2)
    pme2 = ttk.Radiobutton(bouton_frame, text="Avec IR sans NAP", variable=var_code, value=4)
    pme2.grid(row=0, column=3)

    imprimer_bt = ttk.Button(bouton_frame, text="imprimer", style="Accent.TButton", command=imprimer)
    imprimer_bt.grid(row=0, column=4)

    paiment_bt = ttk.Button(select_fact, text="paiment", style="Accent.TButton", command=paiement)
    paiment_bt.grid(row=0, column=3)

    for widget in all_facture_frame.winfo_children():
        widget.grid_configure(padx=10, pady=7)

    for widget in select_fact.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in infos_fac.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in bouton_frame.winfo_children():
        widget.grid_configure(padx=10, pady=6)


# fenetre des clients
def load_all_clients_frame():
    global details_facture_liste, details_devis_liste
    details_facture_liste, details_devis_liste = [], []
    clear_frames()
    all_clients_frame.tkraise()

    def remplir_infos(*args):

        if var_cli.get() == "":
            var_nui.set("NUI")
            var_registre.set("RCMM")
            var_contact.set("TEL")

        else:
            infos_clients = BE_facturier.infos_clients(var_cli.get())

            if infos_clients == None:
                var_nui.set("NUI")
                var_registre.set("RCMM")
                var_contact.set("TEL")

            else:
                var_nui.set(infos_clients[4])
                var_registre.set(infos_clients[5])
                var_contact.set(infos_clients[3])

                all_fac = BE_facturier.factures_client(var_cli.get())

                for child in tree.get_children():
                    tree.delete(child)

                for row in all_fac:
                    tree.insert(parent='', index="end", text='',
                                values=(row[1], milSep(row[2]), milSep(row[3]), row[5]), tags=('oddrow',))

    def remplir_details_facture(e):
        selected = tree.focus()
        valeurs = tree.item(selected, 'values')
        num_facture = valeurs[0]

        all_details = BE_facturier.search_factures_details(num_facture)

        for child in d_tree.get_children():
            d_tree.delete(child)

        count = 0
        for row in all_details:
            d_tree.insert(parent='', index="end", text='',
                          values=(row[1], row[2], row[3], milSep(row[4]), milSep(row[5])), tags=('oddrow',))

    def ajouter_client():
        fen_new_cli = tk.Toplevel()
        fen_new_cli.title("Nouveau client")

        def new_client():

            count = 0
            for variable in (var_nom, var_initiales):
                if variable.get() == "":
                    count += 1

            if count == 0:
                if var_initiales.get() in BE_facturier.recherche_initiales():
                    verif.config(text=f"Les initiales {var_initiales.get()} existent déja\n veuillez choisir un autre")

                else:
                    BE_facturier.add_client(var_nom.get(), var_initiales.get(), var_contact.get(), var_cli_nui.get(),
                                            var_cli_RC.get(), var_mail.get(), var_comm.get())
                    for variable in (var_nom, var_initiales, var_contact, var_cli_nui, var_cli_RC, var_mail):
                        variable.set("")

                    verif.config(text="client créé")

            else:
                verif.config(text="les champs nom et initiales sont obligatoires")

        var_nom = tk.StringVar()
        var_initiales = tk.StringVar()
        var_contact = tk.StringVar()
        var_cli_nui = tk.StringVar()
        var_cli_RC = tk.StringVar()
        var_mail = tk.StringVar()
        var_comm = tk.StringVar()

        info_frame = ttk.LabelFrame(fen_new_cli, text="Infos clients")
        info_frame.grid(row=0, column=0, padx=10, pady=10)

        # info_frame
        nom_lb = tk.Label(info_frame, text="  Nom client  ", font=font)
        nom_lb.grid(row=0, column=0)
        nom = ttk.Entry(info_frame, width=30, textvariable=var_nom, font=font)
        nom.grid(row=0, column=1, sticky="w")

        initiales_lb = tk.Label(info_frame, text="initiales client", font=font)
        initiales_lb.grid(row=1, column=0)
        initiales = ttk.Entry(info_frame, width=10, textvariable=var_initiales, font=font)
        initiales.grid(row=1, column=1, sticky="w")

        contact_lb = tk.Label(info_frame, text="contact client", font=font)
        contact_lb.grid(row=2, column=0)
        contact = ttk.Entry(info_frame, width=25, textvariable=var_contact, font=font)
        contact.grid(row=2, column=1, sticky="w")

        cli_nui_lb = tk.Label(info_frame, text="NUI client", font=font)
        cli_nui_lb.grid(row=3, column=0)
        cli_nui = ttk.Entry(info_frame, width=30, textvariable=var_cli_nui, font=font)
        cli_nui.grid(row=3, column=1, sticky="w")

        cli_RC_lb = tk.Label(info_frame, text="RC client", font=font)
        cli_RC_lb.grid(row=4, column=0)
        cli_RC = ttk.Entry(info_frame, width=30, textvariable=var_cli_RC, font=font)
        cli_RC.grid(row=4, column=1, sticky="w")

        mail_lb = tk.Label(info_frame, text="e-mail client", font=font)
        mail_lb.grid(row=5, column=0)
        mail = ttk.Entry(info_frame, width=30, textvariable=var_mail, font=font)
        mail.grid(row=5, column=1, sticky="w")

        comm_lb = tk.Label(info_frame, text="Commercial", font=font)
        comm_lb.grid(row=6, column=0)
        comm = ttk.Entry(info_frame, width=30, textvariable=var_comm, font=font)
        comm.grid(row=6, column=1, sticky="w")

        bt_valid = ttk.Button(fen_new_cli, text="Valider", style="Accent.TButton", command=new_client)
        bt_valid.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        verif = tk.Label(fen_new_cli, text="Créer client")
        verif.grid(row=2, column=0, padx=10, pady=10, sticky="n")

        for widget in info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=6)

    def importer_client():
        file = askopenfilename(initialdir='/', title='selectionner un fichier',
                               filetype=(("xlsx files", "*.xlsx"), ("xls files", "*.xls")))
        absolute_path = os.path.abspath(file)
        workbook = openpyxl.load_workboshowinfo(absolute_path)
        sheet = workbook.active
        list_values = list(sheet.values)

        for data in list_values:
            BE_facturier.add_client(data[0], data[1], data[2], data[3], data[4], data[5], data[6])

        Messagebox().showinfo("Importation du fichier clients réussie")

    def maj_client():
        fen_upd_cli = tk.Toplevel()
        fen_upd_cli.title("modifier client")

        def update_client():
            BE_facturier.update_client(var_nom.get(), var_initiales.get(), var_contact.get(), var_cli_nui.get(),
                                       var_cli_RC.get(), var_mail.get(), var_comm.get(), var_id_client.get())

            for variable in (var_nom, var_initiales, var_contact, var_cli_nui, var_cli_RC, var_mail):
                variable.set("")

            verif.config(text="client créé")

        var_nom = tk.StringVar()
        var_initiales = tk.StringVar()
        var_contact = tk.StringVar()
        var_cli_nui = tk.StringVar()
        var_cli_RC = tk.StringVar()
        var_mail = tk.StringVar()
        var_comm = tk.StringVar()

        infos_client = BE_facturier.infos_clients_par_id(var_id_client.get())
        var_nom.set(infos_client[1])
        var_initiales.set(infos_client[2])

        if infos_client[3] != None:
            var_contact.set(infos_client[3])
        else:
            var_contact.set("")

        if infos_client[4] != None:
            var_cli_nui.set(infos_client[4])
        else:
            var_cli_nui.set("")

        if infos_client[5] != None:
            var_cli_RC.set(infos_client[5])
        else:
            var_cli_RC.set("")

        if infos_client[6] != None:
            var_mail.set(infos_client[6])
        else:
            var_mail.set("")

        if infos_client[7] != None:
            var_comm.set(infos_client[7])
        else:
            var_comm.set("")

        info_frame = ttk.LabelFrame(fen_upd_cli, text="Infos clients")
        info_frame.grid(row=0, column=0, padx=10, pady=10)

        # info_frame
        nom_lb = tk.Label(info_frame, text="  Nom client  ", font=font)
        nom_lb.grid(row=0, column=0)
        nom = ttk.Entry(info_frame, width=30, textvariable=var_nom, font=font)
        nom.grid(row=0, column=1, sticky="w")

        initiales_lb = tk.Label(info_frame, text="initiales client", font=font)
        initiales_lb.grid(row=1, column=0)
        initiales = ttk.Entry(info_frame, width=10, textvariable=var_initiales, font=font)
        initiales.grid(row=1, column=1, sticky="w")

        contact_lb = tk.Label(info_frame, text="contact client", font=font)
        contact_lb.grid(row=2, column=0)
        contact = ttk.Entry(info_frame, width=25, textvariable=var_contact, font=font)
        contact.grid(row=2, column=1, sticky="w")

        cli_nui_lb = tk.Label(info_frame, text="NUI client", font=font)
        cli_nui_lb.grid(row=3, column=0)
        cli_nui = ttk.Entry(info_frame, width=30, textvariable=var_cli_nui, font=font)
        cli_nui.grid(row=3, column=1, sticky="w")

        cli_RC_lb = tk.Label(info_frame, text="RC client", font=font)
        cli_RC_lb.grid(row=4, column=0)
        cli_RC = ttk.Entry(info_frame, width=30, textvariable=var_cli_RC, font=font)
        cli_RC.grid(row=4, column=1, sticky="w")

        mail_lb = tk.Label(info_frame, text="e-mail client", font=font)
        mail_lb.grid(row=5, column=0)
        mail = ttk.Entry(info_frame, width=30, textvariable=var_mail, font=font)
        mail.grid(row=5, column=1, sticky="w")

        comm_lb = tk.Label(info_frame, text="Commercial", font=font)
        comm_lb.grid(row=6, column=0)
        comm = ttk.Entry(info_frame, width=30, textvariable=var_comm, font=font)
        comm.grid(row=6, column=1, sticky="w")

        bt_valid = ttk.Button(fen_upd_cli, text="Valider", style="Accent.TButton", command=update_client)
        bt_valid.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        verif = tk.Label(fen_upd_cli, text="Créer client")
        verif.grid(row=2, column=0, padx=10, pady=10, sticky="n")

        for widget in info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=6)

    def remplir_id_client(*args):
        if var_cli.get() == "" or var_cli.get() == "Selectionner client":
            var_id_client.set(0)
        else:
            var_id_client.set(BE_facturier.id_client_par_nom(var_cli.get()))

    var_id_client = tk.IntVar()
    var_cli = tk.StringVar()
    var_cli.trace("w", remplir_infos)
    var_cli.trace("w", remplir_id_client)
    var_nui = tk.StringVar()
    var_contact = tk.StringVar()
    var_registre = tk.StringVar()

    ffr = ttk.LabelFrame(all_clients_frame, text="Selection client")
    ffr.grid(row=0, column=0, sticky="w")

    tfr = ttk.Frame(all_clients_frame)
    tfr.grid(row=0, column=1, sticky="nesw")

    dfr = ttk.Frame(all_clients_frame)
    dfr.grid(row=1, column=0, sticky="ew", columnspan=2)

    cfr = ttk.LabelFrame(all_clients_frame, text="Commandes")
    cfr.grid(row=3, column=0, sticky="w")

    # ffr
    client = ttk.Combobox(ffr, values=BE_facturier.liste_clients(), textvariable=var_cli, width=30, font=font,
                          state="readonly")
    var_cli.set("Selectionner client")
    client.grid(row=1, column=0, sticky="w")

    # ifr
    registre = ttk.Entry(ffr, state="disabled", textvariable=var_registre, font=font)
    var_registre.set("RCMM")
    registre.grid(row=2, column=0, sticky="ew")

    unique = ttk.Entry(ffr, state="disabled", textvariable=var_nui, font=font)
    var_nui.set("NUI")
    unique.grid(row=3, column=0, sticky="ew")

    contact = ttk.Entry(ffr, state="disabled", textvariable=var_contact, font=font)
    var_contact.set("TEL")
    contact.grid(row=4, column=0, sticky="ew")

    # widget of tfr
    scrolly = ttk.Scrollbar(tfr, orient=tk.VERTICAL)
    scrolly.pack(fill='y', side=tk.RIGHT)

    tree = ttk.Treeview(tfr, columns=(1, 2, 3, 4), show="headings", height=5, yscrollcommand=scrolly.set,
                        selectmode="extended", )
    scrolly.configure(command=tree.yview)

    tree.pack(fill=tk.BOTH, pady=5, padx=5, expand=True)

    tree.heading(1, text="Facture")
    tree.heading(2, text="Total")
    tree.heading(3, text="Perçu")
    tree.heading(4, text="Statut")
    tree.column(1, width=100, anchor="center")
    tree.column(2, width=100, anchor="center")
    tree.column(3, width=100, anchor="center")
    tree.column(4, width=100, anchor="center")
    tree.bind("<ButtonRelease-1>", remplir_details_facture)

    # dfr
    d_scrolly = ttk.Scrollbar(dfr, orient=tk.VERTICAL)
    d_scrolly.pack(fill='y', side=tk.RIGHT)

    d_tree = ttk.Treeview(dfr, columns=(1, 2, 3, 4, 5), show="headings", height=5, yscrollcommand=d_scrolly.set,
                          selectmode="extended")
    d_scrolly.configure(command=tree.yview)

    d_tree.pack(fill=tk.BOTH, pady=10, padx=2)
    d_tree.heading(1, text="reference")
    d_tree.heading(2, text="Designation")
    d_tree.heading(3, text="Qté")
    d_tree.heading(4, text="Prix")
    d_tree.heading(5, text="Total")
    d_tree.column(1, width=150, anchor="center")
    d_tree.column(2, width=200, anchor="center")
    d_tree.column(3, width=70, anchor="center")
    d_tree.column(4, width=150, anchor="center")
    d_tree.column(5, width=150, anchor="center")

    # Commandes
    new_cli_bt = ttk.Button(cfr, text="Nouveau client", style="Accent.TButton", command=ajouter_client)
    new_cli_bt.grid(row=0, column=0)

    maj_cli_bt = ttk.Button(cfr, text="Modifier client", style="Accent.TButton", command=maj_client)
    maj_cli_bt.grid(row=0, column=1)

    importer_bt = ttk.Button(cfr, text="Import excel", style="Accent.TButton", command=importer_client)
    importer_bt.grid(row=0, column=2)

    for widget in all_clients_frame.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    for widget in ffr.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in cfr.winfo_children():
        widget.grid_configure(padx=10, pady=6)


# Fonctions pour le chargement des sous-menus du menu données bases
def load_all_articles_frame():
    clear_frames()
    all_articles_frame.tkraise()

    def afficher_all_ref():
        for child in tree.get_children():
            tree.delete(child)

        for row in BE_facturier.all_articles():
            tree.insert(parent='', index="end", text='', values=(row[2], row[4], milSep(row[5])))

    def filtrer(*args):

        for child in tree.get_children():
            tree.delete(child)

        if var_naturex.get() == 1:

            for row in BE_facturier.filtrer_articles(var_designation.get(), "stock"):
                tree.insert(parent='', index="end", text='', values=(row[2], row[4], milSep(row[5])))

        elif var_naturex.get() == 2:

            for row in BE_facturier.filtrer_articles(var_designation.get(), "non-stock"):
                tree.insert(parent='', index="end", text='', values=(row[2], row[4], milSep(row[5])))

        else:
            for row in BE_facturier.all_articles():
                tree.insert(parent='', index="end", text='', values=(row[2], row[4], milSep(row[5])))

    def suppr_filtres():
        var_designation.set("")
        for child in tree.get_children():
            tree.delete(child)

        afficher_all_ref()

    def select_article(e):
        selected = tree.focus()
        valeurs = tree.item(selected, 'values')
        var_des.set(valeurs[0])
        infos = BE_facturier.search_infos_desig(var_des.get())
        var_id.set(infos[0])
        var_ref.set(infos[1])
        var_nat.set(infos[3])
        var_qte.set(infos[4])
        var_price.set(infos[5])
        var_unit.set(infos[6])

    def ajouter_ref():

        fen_new = tk.Toplevel()
        fen_new.title("Modifier référence")

        def deblock_qte(*args):
            if var_nat2.get() == "stock":
                qrte.config(state="enabled")
            else:
                qrte.config(state="disabled")
                var_qte2.set(1)

        def valider():
            if var_des2.get() == "" or var_ref2.get() == "" or var_nat2.get() == "" or var_qte2.get() == "" or var_price2.get() == "":
                verif_lb.config(text="Tous les champs sont obligatoires")

            else:
                BE_facturier.add_ref(var_ref2.get(), var_des2.get(), var_nat2.get(), var_qte2.get(), var_price2.get(),
                                     var_unit2.get())
                verif_lb.config(text="Référence ajoutée")
                var_ref2.set("")
                var_des2.set("")
                var_nat2.set("")
                var_qte2.set("")
                var_price2.set("")
                var_unit2.set("")
                afficher_all_ref()

        var_ref2 = tk.StringVar()
        var_des2 = tk.StringVar()
        var_nat2 = tk.StringVar()
        var_nat2.trace("w", deblock_qte)
        var_qte2 = tk.StringVar()
        var_price2 = tk.StringVar()
        var_unit2 = tk.StringVar()

        info_frame = ttk.LabelFrame(fen_new, text="infos article")
        info_frame.grid(row=0, column=0)

        refer_lb = tk.Label(info_frame, text="référence", font=font, fg="#8C8C8C")
        refer_lb.grid(row=1, column=0)
        refer = ttk.Entry(info_frame, textvariable=var_ref2, width=15, font=font)
        refer.grid(row=1, column=1, sticky="w")
        var_ref2.set("Référence")
        refer.bind("<ButtonRelease-1>", lambda event: refer.delete(0, "end"))

        desig_lb = tk.Label(info_frame, text="désignation", font=font, fg="#8C8C8C")
        desig_lb.grid(row=2, column=0)
        desig = ttk.Entry(info_frame, textvariable=var_des2, width=30, font=font)
        desig.grid(row=2, column=1, sticky="w")
        var_des2.set("désignation")
        desig.bind("<ButtonRelease-1>", lambda event: desig.delete(0, "end"))

        natur_lb = tk.Label(info_frame, text="nature", font=font, fg="#8C8C8C")
        natur_lb.grid(row=3, column=0)
        natur = ttk.Combobox(info_frame, textvariable=var_nat2, width=12, font=font, values=["non-stock", "stock"],
                             state="readonly")
        natur.grid(row=3, column=1, sticky="w")
        natur.current(0)

        qrte_lb = tk.Label(info_frame, text="Qté", font=font, fg="#8C8C8C")
        qrte_lb.grid(row=4, column=0)
        qrte = ttk.Spinbox(info_frame, textvariable=var_qte2, width=5, font=font, from_=1, to=10, state="disabled")
        qrte.grid(row=4, column=1, sticky="w")
        var_qte2.set(1)

        price_lb = tk.Label(info_frame, text="prix", font=font, fg="#8C8C8C")
        price_lb.grid(row=5, column=0)
        price = ttk.Entry(info_frame, textvariable=var_price2, width=12, font=font)
        price.grid(row=5, column=1, sticky="w")
        var_price2.set("Prix")
        price.bind("<ButtonRelease-1>", lambda event: price.delete(0, "end"))

        unite_lb = tk.Label(info_frame, text="unité", font=font, fg="#8C8C8C")
        unite_lb.grid(row=6, column=0)
        unite = ttk.Combobox(info_frame, values=["u", "ml", "t", "kg", "g", "l" "m²", ], textvariable=var_unit2,
                             width=4, font=font, state="readonly")
        unite.grid(row=6, column=1, sticky="w")
        unite.current(0)

        valider_bt = ttk.Button(fen_new, text="Valider", command=valider, style="Accent.TButton")
        valider_bt.grid(row=1, column=0, stick="ew")

        verif_lb = tk.Label(fen_new, text="Créer Article")
        verif_lb.grid(row=2, column=0, stick="n")

        for widget in fen_new.winfo_children():
            widget.grid_configure(padx=10, pady=7)

        for widget in info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)

    def new_entree_ref():

        fen_new = tk.Toplevel()
        fen_new.title("Nouvelle entrée")

        def remplir_infos(*args):
            if var_ref.get() == "" or BE_facturier.all_infos_ref(var_ref.get()) == None:
                var_des.set("")
                var_nat.set("")
                var_qte.set(0)

            else:
                infos = BE_facturier.all_infos_ref(var_ref.get())
                var_des.set(infos[0])
                var_nat.set(infos[1])
                var_qte.set(infos[2])

        def new_stock(*args):
            var_qte_new.set(var_qte.get() + var_qte_ent.get())

        def valider():
            if var_des.get() == "" or var_qte_ent.get() == "":
                verif_lb.config(text="Veuillez remplir les champs référence et quantité ")

            else:
                BE_facturier.add_historique(var_ref.get(), "R", BE_facturier.find_histo_num(), var_qte.get(),
                                            var_qte_ent.get(), var_qte_new.get())
                BE_facturier.update_stock(var_qte_new.get(), var_ref.get())
                verif_lb.config(text="Nouvelle entrée enregistrée")
                var_ref.set("")
                var_qte_ent.set(0)
                afficher_all_ref()

        var_ref = tk.StringVar()
        var_ref.trace("w", remplir_infos)
        var_des = tk.StringVar()
        var_nat = tk.StringVar()

        var_qte = tk.IntVar()
        var_qte_ent = tk.IntVar()
        var_qte_ent.trace("w", new_stock)
        var_qte_new = tk.IntVar()

        info_frame = ttk.LabelFrame(fen_new, text="infos article")
        info_frame.grid(row=0, column=0)

        ref_lb = tk.Label(info_frame, text="référence", font=font)
        ref_lb.grid(row=1, column=0)
        ref = ttk.Combobox(info_frame, textvariable=var_ref, width=15, font=font,
                           values=BE_facturier.all_references_stock(), state="readonly")
        ref.grid(row=1, column=1, sticky="w")

        des_lb = tk.Label(info_frame, text="désignation", font=font)
        des_lb.grid(row=2, column=0)
        des = ttk.Entry(info_frame, textvariable=var_des, width=30, font=font, state="disabled")
        des.grid(row=2, column=1, sticky="w")

        nat_lb = tk.Label(info_frame, text="nature", font=font)
        nat_lb.grid(row=3, column=0)
        nat = ttk.Entry(info_frame, textvariable=var_nat, width=12, font=font, state="disabled")
        nat.grid(row=3, column=1, sticky="w")

        qte_lb = tk.Label(info_frame, text="Qté en stock", font=font)
        qte_lb.grid(row=4, column=0)
        qte = ttk.Entry(info_frame, textvariable=var_qte, width=5, font=font, state="disabled")
        qte.grid(row=4, column=1, sticky="w")

        qte_ent_lb = tk.Label(info_frame, text="Qté entré", font=font)
        qte_ent_lb.grid(row=5, column=0)
        qte_ent = ttk.Spinbox(info_frame, textvariable=var_qte_ent, width=5, font=font, from_=0, to=10)
        qte_ent.grid(row=5, column=1, sticky="w")

        qte_new_lb = tk.Label(info_frame, text="nouveau stock", font=font)
        qte_new_lb.grid(row=6, column=0)
        qte_new = ttk.Entry(info_frame, textvariable=var_qte_new, width=5, font=font, state="disabled")
        qte_new.grid(row=6, column=1, sticky="w")

        valider_bt = ttk.Button(fen_new, text="Valider", command=valider, style="Accent.TButton")
        valider_bt.grid(row=1, column=0, stick="ew")

        verif_lb = tk.Label(fen_new, text="Nouvelle entrée")
        verif_lb.grid(row=2, column=0, stick="n")

        for widget in fen_new.winfo_children():
            widget.grid_configure(padx=10, pady=7)

        for widget in info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)

    def importer_articles():
        file = askopenfilename(initialdir='/', title='selectionner un fichier',
                               filetype=(("xlsx files", "*.xlsx"), ("xls files", "*.xls")))
        absolute_path = os.path.abspath(file)
        workbook = openpyxl.load_workboshowinfo(absolute_path)
        sheet = workbook.active
        list_values = list(sheet.values)

        for data in list_values:
            BE_facturier.add_ref(data[0], data[1], data[2], data[3], data[4], data[5])

        Messagebox().showinfo("Importation du fichier clients réussie")

    ffr = ttk.LabelFrame(all_articles_frame, text="Filtres")
    ffr.grid(row=0, column=0, sticky="ew")

    tfr = tk.Frame(all_articles_frame)
    tfr.grid(row=1, column=0, sticky="w")

    ifr = ttk.LabelFrame(all_articles_frame, text="Infos référence")
    ifr.grid(row=2, column=0, sticky="news")

    cfr = ttk.LabelFrame(all_articles_frame, text="Commandes")
    cfr.grid(row=3, column=0, sticky="ew")

    # rechfr
    var_designation = tk.StringVar()
    var_naturex = tk.IntVar()
    var_designation.trace("w", filtrer)
    var_naturex.trace("w", filtrer)

    designation_lb = tk.Label(ffr, text="designation", font=font, fg="#8C8C8C")
    designation_lb.grid(row=0, column=0)
    designation = ttk.Entry(ffr, textvariable=var_designation, width=20, font=font)
    designation.grid(row=0, column=1)

    nature_1 = ttk.Radiobutton(ffr, text="Stock", variable=var_naturex, value=1)
    nature_1.grid(row=0, column=2)
    nature_1 = ttk.Radiobutton(ffr, text="Non-stock", variable=var_naturex, value=2)
    nature_1.grid(row=0, column=3)
    # var_naturex.set(1)

    # widget of tfr
    scrolly = ttk.Scrollbar(tfr, orient=tk.VERTICAL)
    scrolly.pack(fill='y', side=tk.LEFT)

    tree = ttk.Treeview(tfr, columns=(1, 2, 3,), show="headings", height=8, yscrollcommand=scrolly.set,
                        selectmode="extended")
    scrolly.configure(command=tree.yview)
    tree.pack(fill=tk.BOTH, pady=10, padx=2)

    tree.heading(1, text="designation")
    tree.heading(2, text="Qté")
    tree.heading(3, text="prix")
    tree.column(1, width=300, anchor="center")
    tree.column(2, width=70, anchor="center")
    tree.column(3, width=100, anchor="center")

    afficher_all_ref()
    tree.bind("<ButtonRelease-1>", select_article)

    # ifr widgets
    var_id = tk.StringVar()
    var_ref = tk.StringVar()
    var_des = tk.StringVar()
    var_nat = tk.StringVar()
    var_qte = tk.StringVar()
    var_price = tk.StringVar()
    var_unit = tk.StringVar()

    id_lb = tk.Label(ifr, text="Id", fg="#8C8C8C")
    id_lb.grid(row=0, column=0)
    id_ent = ttk.Entry(ifr, textvariable=var_id, state="disabled", width=5)
    id_ent.grid(row=0, column=1, sticky="w")
    var_id.set("Id")

    ref_lb = tk.Label(ifr, text="référence", font=font, fg="#8C8C8C")
    ref_lb.grid(row=0, column=2)
    ref = ttk.Entry(ifr, textvariable=var_ref, width=20, font=font, state="disabled")
    ref.grid(row=0, column=3, sticky="w", columnspan=4)
    var_ref.set("Référence")

    des_lb = tk.Label(ifr, text="désignation", font=font, fg="#8C8C8C")
    des_lb.grid(row=1, column=0)
    des = ttk.Entry(ifr, textvariable=var_des, width=50, font=font, state="disabled")
    des.grid(row=1, column=1, sticky="w", columnspan=4)
    var_des.set("désignation")

    nat_lb = tk.Label(ifr, text="nature", font=font, fg="#8C8C8C")
    nat_lb.grid(row=2, column=0)
    nat = ttk.Entry(ifr, textvariable=var_nat, width=12, font=font, state="disabled")
    nat.grid(row=2, column=1, sticky="w")
    var_nat.set("Nature")

    qte_lb = tk.Label(ifr, text="Qté", font=font, fg="#8C8C8C")
    qte_lb.grid(row=2, column=2)
    qte = ttk.Entry(ifr, textvariable=var_qte, width=5, font=font, state="disabled")
    qte.grid(row=2, column=3, sticky="w")
    var_qte.set("Qté")

    prix_lb = tk.Label(ifr, text="prix", font=font, fg="#8C8C8C")
    prix_lb.grid(row=2, column=4)
    prix = ttk.Entry(ifr, textvariable=var_price, width=12, font=font, state="disabled")
    prix.grid(row=2, column=5, sticky="w")
    var_price.set("Prix")

    unit_lb = tk.Label(ifr, text="unité", font=font, fg="#8C8C8C")
    unit_lb.grid(row=2, column=6)
    unit = ttk.Entry(ifr, textvariable=var_unit, width=5, font=font, state="disabled")
    unit.grid(row=2, column=7, sticky="w")
    var_unit.set("Unité")

    # Commandes
    suppr_filtrer_bt = ttk.Button(ffr, text="Supprimer", command=suppr_filtres, style="Accent.TButton")
    suppr_filtrer_bt.grid(row=0, column=4)

    new_ref_bt = ttk.Button(cfr, text="Nouveau", style="Accent.TButton", command=ajouter_ref)
    new_ref_bt.grid(row=0, column=0)

    new_ent_bt = ttk.Button(cfr, text="Entrée", style="Accent.TButton", command=new_entree_ref)
    new_ent_bt.grid(row=0, column=1)

    import_bt = ttk.Button(cfr, text="import excel", style="Accent.TButton", command=importer_articles)
    import_bt.grid(row=0, column=2)

    for widget in all_articles_frame.winfo_children():
        widget.grid_configure(padx=10, pady=7)

    for widget in ffr.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in ifr.winfo_children():
        widget.grid_configure(padx=10, pady=6)

    for widget in cfr.winfo_children():
        widget.grid_configure(padx=10, pady=6)


# chargment du menu
def load_menu_frame():
    clear_frames()
    menu_frame.tkraise()

    infos_base_menu = ttk.Menubutton(menu_frame, text='données de base', width=15)
    infos_base_menu.grid(row=0, column=0, padx=2, pady=2)
    inside_infos_base_menu = tk.Menu(infos_base_menu)
    inside_infos_base_menu.add_radiobutton(label='Clients', command=load_all_clients_frame)
    inside_infos_base_menu.add_radiobutton(label='Articles', command=load_all_articles_frame)
    infos_base_menu['menu'] = inside_infos_base_menu

    devis_menu = ttk.Menubutton(menu_frame, text='devis', width=15)
    devis_menu.grid(row=0, column=1, padx=2, pady=2)
    inside_devis_menu = tk.Menu(devis_menu)
    inside_devis_menu.add_radiobutton(label='Nouveau devis', command=load_devis_frame)
    inside_devis_menu.add_radiobutton(label='Voir devis', command=load_all_devis_frame)
    devis_menu['menu'] = inside_devis_menu

    facture_menu = ttk.Menubutton(menu_frame, text='Factures', width=15)
    facture_menu.grid(row=0, column=2, padx=2, pady=2)
    inside_facture_menu = tk.Menu(facture_menu)
    inside_facture_menu.add_radiobutton(label='Nouvelle facture', command=load_facture_frame)
    inside_facture_menu.add_radiobutton(label='Voir factures', command=load_all_facture_frame)
    facture_menu['menu'] = inside_facture_menu

    # def change_style(*args):

    #     if var_style.get() == 1:
    #         # Set the theme with the theme_use method
    #         app.tk.call("set_theme", "dark")
    #         style.configure('Treeview', rowheight=24, font=font, foreground="#A6A6A6")
    #         style.configure('Treeview.Heading', font=font)
    #         style.configure("Accent.TButton", font=font)

    #     else:
    #         # Set the theme with the theme_use method
    #         app.tk.call("set_theme", "light")
    #         style.configure('Treeview', rowheight=24, font=font, foreground="black")
    #         style.configure('Treeview.Heading', font=font)
    #         style.configure("Accent.TButton", font=font)

    # var_style=tk.IntVar()
    # var_style.trace("w", change_style)

    # change_lb = tk.Label(menu_frame, text="changer le thème", fg="#8C8C8C")

 # change_lb.grid(row=0, column=3, padx=10, pady=10)
    # change = ttk.Checkbutton(menu_frame, variable=var_style, style="Switch", onvalue=1, offvalue=0)
    # change.grid(row=0, column=4, padx=10, pady=10)


# Fonction de cghargement de la page de connexion et page d'accueil
def load_connexion_frame():
    clear_frames()
    connexion_frame.tkraise()

    def voir_mdp(*args):
        if var_voir.get() == 0:
            passw.config(show="*")
        else:
            passw.config(show="")

    def verifier_user():
        users_list = BE_facturier.all_users()
        count = 0

        for user in users_list:
            if user == (var_login.get(), var_passw.get()):
                count += 1

        if count == 0:
            showerror("", "Login ou mot de passe incorrect")
        else:
            load_menu_frame()

    var_login = tk.StringVar()
    var_passw = tk.StringVar()
    var_voir = tk.IntVar()
    var_voir.trace("w", voir_mdp)

    info_con = ttk.LabelFrame(connexion_frame, text="Login form")
    info_con.grid(row=0, column=0, padx=290, pady=120)

    login_lb = tk.Label(info_con, text="Login")
    login_lb.grid(row=0, column=0)
    login = ttk.Entry(info_con, textvariable=var_login, width=15)
    login.grid(row=0, column=1)

    passw_lb = ttk.Label(info_con, text="password")
    passw_lb.grid(row=1, column=0)
    passw = ttk.Entry(info_con, textvariable=var_passw, show="*", width=15)
    passw.grid(row=1, column=1)

    voir_lb = ttk.Label(info_con, text="voir mot de passe")
    voir_lb.grid(row=2, column=0)
    voir = ttk.Checkbutton(info_con, variable=var_voir, onvalue=1, offvalue=0, style="Switch")
    voir.grid(row=2, column=1)

    valider = ttk.Button(info_con, text="valider", style="Accent.TButton", command=verifier_user)
    valider.grid(row=3, column=0, sticky="ew", columnspan=2)
    quitter = ttk.Button(info_con, text="quitter", style="Accent.TButton", command=app.quit)
    quitter.grid(row=4, column=0, sticky="ew", columnspan=2)

    for widget in info_con.winfo_children():
        widget.grid_configure(padx=10, pady=10)


# Boucle principale
app = tk.Tk()
app.title("Facturier")
app.minsize(920, 730)
app.resizable(tk.NO, tk.NO)
app.option_add("*tearOff", False)  # This is always a good idea

app.update()
x_cordinate = int((app.winfo_screenwidth() / 2) - (app.winfo_width() / 2))
y_cordinate = int((app.winfo_screenheight() / 2) - (app.winfo_height() / 2))
app.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

# Create a style
style = ttk.Style(app)

# Import the tcl file

app.tk.call("source", "forest-light.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-light")

# Set the theme with the theme_use method
# style.theme_use("light")

font = ("gill sans MT", 10)
style.configure('Treeview.Heading', font=font)
style.configure("Accent.TButton", font=font)
style.configure("Treeview", rowheight=25, foreground="black", font=font)

connexion_frame = tk.Frame(app)
devis_frame = tk.Frame(app)
all_devis_frame = tk.Frame(app)
mod_devis_frame = tk.Frame(app)
facture_frame = tk.Frame(app)
all_facture_frame = tk.Frame(app)
all_articles_frame = tk.Frame(app)
all_clients_frame = tk.Frame(app)
all_bordereau_frame = tk.Frame(app)
splash = tk.Frame(app)

frame_list = [widget for widget in app.winfo_children()]

for frame in frame_list:
    frame.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

menu_frame = tk.Frame(app)
menu_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nw")

thfr = tk.Frame(app)
thfr.grid(row=2, column=0)

# variables globales
details_devis_liste = []
details_facture_liste = []
today = datetime.date.today()
num_devis_temp = tk.StringVar()
var_num_fac_paie = tk.StringVar()

# img_supp = tk.PhotoImage(file="croix.png")

BE_facturier.connexion_base()
load_connexion_frame()

app.mainloop()