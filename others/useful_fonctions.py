def ecrire_date(date):
    """This function writes the date of the day"""

    def find_mois(month):
        m: int = int(month)
        if m == 1:
            return "janvier"
        elif m == 2:
            return "février"
        elif m == 3:
            return "mars"
        elif m == 4:
            return "avril"
        elif m == 5:
            return "mai"
        elif m == 6:
            return "juin"
        elif m == 7:
            return "juillet"
        elif m == 8:
            return "août"
        elif m == 9:
            return "septembre"
        elif m == 10:
            return "octobre"
        elif m == 11:
            return "novembre"
        else:
            return "décembre"

    annee = date[0: 4]
    mois = date[5: 7]
    jour = date[8:]

    m = find_mois(mois)

    return str(jour) + " " + m + " " + str(annee)


def milSep(nombre):
    nombre = str(nombre)[::-1]
    resultat = ""
    for i, numero in enumerate(nombre, 1):
        numero_formatte = numero + " " if i % 3 == 0 and i != len(nombre) else numero
        resultat += numero_formatte

    return resultat[::-1]


def ecrire_en_lettres(nombre: int):
    carac = str(nombre)

    def nombre_unites(number):
        unite = ""
        if number == 1:
            unite = "un"

        elif number == 2:
            unite = "deux"

        elif number == 3:
            unite = "trois"

        elif number == 4:
            unite = "quatre"

        elif number == 5:
            unite = "cinq"

        elif number == 6:
            unite = "six"

        elif number == 7:
            unite = "sept"

        elif number == 8:
            unite = "huit"

        elif number == 9:
            unite = "neuf"

        elif number == 0:
            unite = "zéro"

        return unite

    def nombre_dizaines(number):  # if the value is more than 9 and under 99
        unite = ""
        dizaine = ""
        quotient = number // 10

        if quotient == 0:
            return nombre_unites(number)
        else:
            reste = number % (quotient * 10)

            if quotient == 1:
                if reste == 1:
                    dizaine = "onze"
                elif reste == 2:
                    dizaine = "douze"
                elif reste == 3:
                    dizaine = "treize"
                elif reste == 4:
                    dizaine = "quatorze"
                elif reste == 5:
                    dizaine = "quinze"
                elif reste == 6:
                    dizaine = "seize"
                elif reste == 7:
                    dizaine = "dix-sept"
                elif reste == 8:
                    dizaine = "dix-huit"
                elif reste == 9:
                    dizaine = "dix-neuf"
                elif reste == 0:
                    dizaine = "dix"
                unite = ""

            elif quotient == 2:
                dizaine = "vingt"
                if reste == 0:
                    unite = ""
                else:
                    unite = nombre_unites(reste)

            elif quotient == 3:
                dizaine = "trente"
                if reste == 0:
                    unite = ""
                else:
                    unite = nombre_unites(reste)

            elif quotient == 4:
                dizaine = "quarante"
                if reste == 0:
                    unite = ""
                else:
                    unite = nombre_unites(reste)

            elif quotient == 5:
                dizaine = "cinquante"
                if reste == 0:
                    unite = ""
                else:
                    unite = nombre_unites(reste)

            elif quotient == 6:
                dizaine = "soixante"
                if reste == 0:
                    unite = ""
                else:
                    unite = nombre_unites(reste)

            elif quotient == 7:
                dizaine = "soixante"
                if reste == 1:
                    unite = "onze"
                elif reste == 2:
                    unite = "douze"
                elif reste == 3:
                    unite = "treize"
                elif reste == 4:
                    unite = "quatorze"
                elif reste == 5:
                    unite = "quinze"
                elif reste == 6:
                    unite = "seize"
                elif reste == 7:
                    unite = "dix-sept"
                elif reste == 8:
                    unite = "dix-huit"
                elif reste == 9:
                    unite = "dix-neuf"
                elif reste == 0:
                    unite = "dix"

            elif quotient == 8:
                dizaine = "quatre vingt"
                if reste == 1:
                    unite = "et un"

                elif reste == 0:
                    unite = ""
                else:
                    unite = nombre_unites(reste)

            elif quotient == 9:
                dizaine = "quatre vingt"
                if reste == 1:
                    unite = "onze"
                elif reste == 2:
                    unite = "douze"
                elif reste == 3:
                    unite = "treize"
                elif reste == 4:
                    unite = "quatorze"
                elif reste == 5:
                    unite = "quinze"
                elif reste == 6:
                    unite = "seize"
                elif reste == 7:
                    unite = "dix-sept"
                elif reste == 8:
                    unite = "dix-huit"
                elif reste == 9:
                    unite = "dix-neuf"
                elif reste == 0:
                    unite = "dix"

            return dizaine + " " + unite

    def nombre_centaines(number):  # retourne un tuple
        dizaine = ""
        quotient = number // 100

        if quotient == 0:
            return nombre_dizaines(number)
        else:
            reste = number % (quotient * 100)

            if quotient == 1:
                centaine = "cent"
                if reste == 0:
                    dizaine = ""
                elif 0 < reste < 10:
                    dizaine = nombre_unites(reste)
                elif 10 < reste < 100:
                    dizaine = nombre_dizaines(reste)
                return centaine + " " + dizaine

            elif 1 < quotient < 10:
                centaine = nombre_unites(quotient) + " cent"
                if reste == 0:
                    dizaine = ""
                elif 0 < reste < 10:
                    dizaine = nombre_unites(reste)
                elif 10 < reste < 100:
                    dizaine = nombre_dizaines(reste)
                return centaine + " " + dizaine

    def nombre_milliers(number):
        centaine = ""
        quotient = number // 1000

        if quotient == 0:
            return nombre_centaines(number)
        else:
            reste = number % (quotient * 1000)

            if quotient == 1:
                milliers = "mille"
                if reste == 0:
                    centaine = ""
                elif 0 < reste < 10:
                    centaine = nombre_unites(reste)
                elif 10 <= reste < 100:
                    centaine = nombre_dizaines(reste)
                elif reste >= 100:
                    centaine = nombre_centaines(reste)
                return milliers + " " + centaine
            elif 1 < quotient < 10:
                milliers = nombre_unites(quotient) + " mille"
                if reste == 0:
                    centaine = ""
                elif 0 < reste < 10:
                    centaine = nombre_unites(reste)
                elif 10 <= reste < 100:
                    centaine = nombre_dizaines(reste)
                elif reste >= 100:
                    centaine = nombre_centaines(reste)
                return milliers + " " + centaine
            elif 10 <= quotient < 100:
                milliers = nombre_dizaines(quotient) + " mille"
                if reste == 0:
                    centaine = ""
                elif 0 < reste < 10:
                    centaine = nombre_unites(reste)
                elif 10 <= reste < 100:
                    centaine = nombre_dizaines(reste)
                elif reste >= 100:
                    centaine = nombre_centaines(reste)
                return milliers + " " + centaine
            elif 100 <= quotient < 1000:
                milliers = nombre_centaines(quotient) + " mille"
                if reste == 0:
                    centaine = ""
                elif 0 < reste < 10:
                    centaine = nombre_unites(reste)
                elif 10 <= reste < 100:
                    centaine = nombre_dizaines(reste)
                elif reste >= 100:
                    centaine = nombre_centaines(reste)
                return milliers + " " + centaine

    def nombre_millions(number):
        milliers = ""
        quotient = number // 1000000

        if quotient == 0:
            return nombre_milliers(number)
        else:
            reste = number % (quotient * 1000000)
            if quotient == 1:
                millions = "un million"
                if reste == 0:
                    milliers = ""
                elif 0 < reste < 10:
                    milliers = nombre_unites(reste)
                elif 10 <= reste < 100:
                    milliers = nombre_dizaines(reste)
                elif 100 <= reste < 1000:
                    milliers = nombre_centaines(reste)
                elif reste >= 1000:
                    milliers = nombre_milliers(reste)
                return millions + " " + milliers

            elif 1 < quotient < 10:
                millions = nombre_unites(quotient) + " millions"
                if reste == 0:
                    milliers = ""
                elif 0 < reste < 10:
                    milliers = nombre_unites(reste)
                elif 10 <= reste < 100:
                    milliers = nombre_dizaines(reste)
                elif 100 <= reste < 1000:
                    milliers = nombre_centaines(reste)
                elif reste >= 1000:
                    milliers = nombre_milliers(reste)
                return millions + " " + milliers
            elif 10 <= quotient < 100:
                millions = nombre_dizaines(quotient) + " millions"
                if reste == 0:
                    milliers = ""
                elif 0 < reste < 10:
                    milliers = nombre_unites(reste)
                elif 10 <= reste < 100:
                    milliers = nombre_dizaines(reste)
                elif 100 <= reste < 1000:
                    milliers = nombre_centaines(reste)
                elif reste >= 1000:
                    milliers = nombre_milliers(reste)
                return millions + " " + milliers
            elif 100 <= quotient < 1000:
                millions = nombre_centaines(quotient) + " millions"
                if reste == 0:
                    milliers = ""
                elif 0 < reste < 10:
                    milliers = nombre_unites(reste)
                elif 10 <= reste < 100:
                    milliers = nombre_dizaines(reste)
                elif 100 <= reste < 1000:
                    milliers = nombre_centaines(reste)
                elif reste >= 1000:
                    milliers = nombre_milliers(reste)
                return millions + " " + milliers

    def nombre_milliards(x):
        millions = ""
        y = x // 1000000000

        if y == 0:
            return nombre_millions(x)

        else:
            if 0 < y < 10:
                milliards = nombre_unites(y) + " milliards"
                reste = x % (y * 1000000000)

                if reste == 0:
                    millions = ""

                elif 0 < reste < 10:
                    millions = nombre_unites(reste)

                elif 10 <= reste < 100:
                    millions = nombre_dizaines(reste)

                elif 100 <= reste < 1000:
                    millions = nombre_centaines(reste)

                elif 1000 <= reste < 1000000:
                    millions = nombre_milliers(reste)

                elif reste >= 1000000:
                    millions = nombre_millions(reste)

                return milliards + " " + millions

            elif 10 <= y < 100:

                milliards = nombre_dizaines(y) + " milliards"
                reste = x % (y * 1000000000)

                if reste == 0:
                    millions = ""

                elif 0 < reste < 10:
                    millions = nombre_unites(reste)

                elif 10 <= reste < 100:
                    millions = nombre_dizaines(reste)

                elif 100 <= reste < 1000:
                    millions = nombre_centaines(reste)

                elif 1000 <= reste < 1000000:
                    millions = nombre_milliers(reste)

                elif reste >= 1000000:
                    millions = nombre_millions(reste)

                return milliards + " " + millions

            elif 100 <= y < 1000:

                reste = x % (y * 1000)
                milliards = nombre_centaines(y) + " milliards"

                if reste == 0:
                    millions = ""

                elif 0 < reste < 10:
                    millions = nombre_unites(reste)

                elif 10 <= reste < 100:
                    millions = nombre_dizaines(reste)

                elif 100 <= reste < 1000:
                    millions = nombre_centaines(reste)

                elif 1000 <= reste < 1000000:
                    millions = nombre_milliers(reste)

                elif reste >= 1000000:
                    millions = nombre_millions(reste)

                return milliards + " " + millions

    if len(carac) > 12:
        print("le nombre est trop long. entrez un nombre de moins de 13 chiffres")

    else:
        if 0 <= nombre < 10:
            lettres = nombre_unites(nombre)

        elif 10 <= nombre < 100:
            lettres = nombre_dizaines(nombre)

        elif 100 <= nombre < 1000:
            lettres = nombre_centaines(nombre)

        elif 1000 <= nombre < 1000000:
            lettres = nombre_milliers(nombre)

        elif 1000000 <= nombre < 1000000000:
            lettres = nombre_millions(nombre)

        else:
            lettres = nombre_milliards(nombre)

        return f"{lettres.upper()} FCFA"


# infos de l'entreprise
ENTITE_NOM = "Fomiderc SARL"
ENTITE_TEL = "+237 690063525 / 654991819"
ENTITE_MAIL = "fomiderc.services@gmail.com"
ENTITE_WEB = "fomidercgroupeservices.com"
ENTITE_ADRESSE_1 = "891 boulevard Ahmadou Ahidjo"
ENTITE_ADRESSE_2 = "Akwa, Douala Cameroun"
ENTITE_RC = "RC/DLA/2018/B/510"
ENTITE_NUI = "M021812677041N"
ENTITE_BANQUE = "AFRILAND FIRST BANK"
ENTITE_IBAN = "CM21 10005 - 00022 - 08174701001 - 58"
ENTITE_SWIFT = "CCEICMCX"
