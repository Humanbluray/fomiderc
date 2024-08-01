def imprimer_devis(self, e: ft.FilePickerResultEvent):
        if self.search_devis.value is None or self.search_devis.value == "":
            self.bad_impression.open = True
            self.bad_impression.update()

        else:
            if self.ir_inactive.value is False:
                save_location = e.path
                fichier = f"{os.path.abspath(save_location)}.pdf"
                can = Canvas("{0}".format(fichier), pagesize=A4)

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
                can.drawCentredString(16.5 * cm, (y - 1) * cm, "Total:")
                can.setFont("Helvetica", 11)
                can.drawCentredString(18.75 * cm, (y - 1) * cm, f"{milSep(total_devis)}")

                if int(self.remise.value) == 0:
                    ir = int(total_devis * 5.5 // 100)
                    nap = int(total_devis - ir)
                    can.setFont("Helvetica-Bold", 10)
                    can.drawCentredString(16.5 * cm, (y - 1.5) * cm, "IR:")
                    can.drawCentredString(16.5 * cm, (y - 2) * cm, "NAP:")

                    can.setFont("Helvetica", 11)
                    can.drawCentredString(18.75 * cm, (y - 1.5) * cm, f"{milSep(ir)} ")
                    can.drawCentredString(18.75 * cm, (y - 2) * cm, f"{milSep(nap)} FCFA")

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
                        can.drawString(1 * cm, (y - 1) * cm, f"Point de livraison: {infos[9]}")

                    if infos[11] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 1.5) * cm, f"Paiement: {infos[11]} jours après dépôt de facture")

                    if infos[10] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 2) * cm, f"validité de l'offre: {infos[10]} mois")

                    can.setFont("Helvetica", 10)
                    can.drawString(1 * cm, (y - 3) * cm, "INFORMATION BANCAIRES")
                    can.setFont("Helvetica", 11)
                    can.drawString(1 * cm, (y - 3.5) * cm, f"par virement à: {ENTITE_BANQUE},   IBAN {ENTITE_IBAN}")
                    can.drawString(1 * cm, (y - 4) * cm, f"Code swift: {ENTITE_SWIFT},  Titualire: {ENTITE_NOM}")

                else:
                    rem = int(self.remise.value)
                    mt_rem = int(total_devis * rem // 100)
                    net = int(total_devis - mt_rem)
                    ir = int(net * 5.5 // 100)
                    nap = int(net - ir)
                    can.setFont("Helvetica-Bold", 10)
                    can.drawCentredString(16.5 * cm, (y - 1.5) * cm, "Remise:")
                    can.drawCentredString(16.5 * cm, (y - 2) * cm, "net:")
                    can.drawCentredString(16.5 * cm, (y - 2.5) * cm, "IR:")
                    can.drawCentredString(16.5 * cm, (y - 3) * cm, "NAP:")

                    can.setFont("Helvetica", 11)
                    can.drawCentredString(18.75 * cm, (y - 1.5) * cm, f"{milSep(mt_rem)}")
                    can.drawCentredString(18.75 * cm, (y - 2) * cm, f"{milSep(net)}")
                    can.drawCentredString(18.75 * cm, (y - 2.5) * cm, f"{milSep(ir)}")
                    can.drawCentredString(18.75 * cm, (y - 3) * cm, f"{milSep(nap)} FCFA")
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
                        can.drawString(1 * cm, (y - 1) * cm, f"Point de livraison: {infos[9]}")

                    if infos[11] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 1.5) * cm, f"Paiement: {infos[11]} jours après dépôt de facture")

                    if infos[10] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 2) * cm, f"validité de l'offre: {infos[10]} mois")

                    can.setFont("Helvetica", 10)
                    can.drawString(1 * cm, (y - 3) * cm, "INFORMATIONS BANCAIRES")
                    can.setFont("Helvetica", 11)
                    can.drawString(1 * cm, (y - 3.5) * cm, f"par virement à: {ENTITE_BANQUE},   IBAN {ENTITE_IBAN}")
                    can.drawString(1 * cm, (y - 4) * cm, f"Code swift: {ENTITE_SWIFT},  Titualire: {ENTITE_NOM}")

                can.save()
                self.good_impression.open = True
                self.good_impression.update()

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
                can.drawCentredString(16.5 * cm, (y - 1) * cm, "Total:")
                can.setFont("Helvetica", 11)
                can.drawCentredString(18.75 * cm, (y - 1) * cm, f"{milSep(total_devis)}")

                if int(self.remise.value) == 0:
                    can.setFont("Helvetica-Bold", 11)
                    can.drawString(1 * cm, (y - 2) * cm, f"Montant total: {ecrire_en_lettres(total_devis)}")

                    infos = backend.show_info_devis(self.search_devis.value)

                    can.setFont("Helvetica", 11)
                    can.drawString(1 * cm, (y - 3) * cm, "NB:")
                    nb_list = infos[7].split(";")
                    if infos[7] is not None:
                        for i in range(0, len(nb_list) - 1):
                            can.setFont("Helvetica-Bold", 12)
                            can.drawString(1 * cm, ((y - 2.5) - i * 0.5) * cm, f"{nb_list[i].lower()}")

                    y = y - 3 - len(nb_list) * 0.5

                    if infos[8] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 0.5) * cm, f"Délai de livraison: {infos[8]}")

                    if infos[9] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 1) * cm, f"Point de livraison: {infos[9]}")

                    if infos[11] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 1.5) * cm, f"Paiement: {infos[11]} jours après dépôt de facture")

                    if infos[10] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 2) * cm, f"validité de l'offre: {infos[10]} mois")

                    can.setFont("Helvetica", 10)
                    can.drawString(1 * cm, (y - 3) * cm, "INFORMATION BANCAIRES")
                    can.setFont("Helvetica", 11)
                    can.drawString(1 * cm, (y - 3.5) * cm, f"par virement à: {ENTITE_BANQUE},   IBAN {ENTITE_IBAN}")
                    can.drawString(1 * cm, (y - 4) * cm, f"Code swift: {ENTITE_SWIFT},  Titualire: {ENTITE_NOM}")

                else:
                    rem = int(self.remise.value)
                    mt_rem = int(total_devis * rem // 100)
                    montant_ap_remise = total_devis - mt_rem
                    can.setFont("Helvetica-Bold", 10)
                    can.drawCentredString(16.5 * cm, (y - 1.5) * cm, "Remise:")
                    can.drawCentredString(16.5 * cm, (y - 2) * cm, "Montant Total:")

                    can.setFont("Helvetica", 11)
                    can.drawCentredString(18.75 * cm, (y - 1.5) * cm, f"{milSep(mt_rem)}")
                    can.drawCentredString(18.75 * cm, (y - 2) * cm, f"{milSep(montant_ap_remise)}")

                    can.setFont("Helvetica-Bold", 11)
                    can.drawString(1 * cm, (y - 3) * cm, f"Montant total: {ecrire_en_lettres(montant_ap_remise)}")
                    infos = backend.show_info_devis(self.search_devis.value)

                    can.setFont("Helvetica", 11)
                    can.drawString(1 * cm, (y - 4) * cm, "NB:")
                    nb_list = infos[7].split(";")
                    if infos[7] is not None:
                        for i in range(len(nb_list) - 1):
                            can.setFont("Helvetica-Bold", 12)
                            can.drawString(1 * cm, ((y - 4.5) - i * 0.5) * cm, f"{nb_list[i].lower()}")

                    y = y - 4 - len(nb_list) * 0.5

                    if infos[8] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 0.5) * cm, f"Délai de livraison: {infos[8]}")

                    if infos[9] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 1) * cm, f"Point de livraison: {infos[9]}")

                    if infos[11] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 1.5) * cm, f"Paiement: {infos[11]} jours après dépôt de facture")

                    if infos[10] is not None:
                        can.setFont("Helvetica-Bold", 12)
                        can.drawString(1 * cm, (y - 2) * cm, f"validité de l'offre: {infos[10]} mois")

                    can.setFont("Helvetica", 10)
                    can.drawString(1 * cm, (y - 3) * cm, "INFORMATIONS BANCAIRES")
                    can.setFont("Helvetica", 11)
                    can.drawString(1 * cm, (y - 3.5) * cm, f"par virement à: {ENTITE_BANQUE},   IBAN {ENTITE_IBAN}")
                    can.drawString(1 * cm, (y - 4) * cm, f"Code swift: {ENTITE_SWIFT},  Titualire: {ENTITE_NOM}")

                can.save()
                self.good_impression.open = True
                self.good_impression.update()
