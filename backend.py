import sqlite3 as sql
import datetime

today = datetime.date.today()
my_base = "facturier.db"
initiales_entreprise = "FMD"


def connexion_base():
    conn = sql.connect(my_base)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS devis (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero          TEXT UNIQUE,
                    date            DATE,
                    client          INTEGER REFERENCES "clients"("id"),
                    montant         NUMERIC,
                    objet           TEXT,
                    remise          INTEGER,
                    montant_lettres TEXT,
                    statut          TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS devis_details (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero    TEXT,
                    reference TEXT,
                    qte       INTEGER,
                    prix      NUMERIC)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS articles (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    reference   TEXT,
                    designation TEXT,
                    nature      TEXT,
                    qté         INTEGER,
                    prix        NUMERIC,
                    unite       TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS clients (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom       TEXT,
                    initiales TEXT,
                    contact   TEXT,
                    NUI       TEXT,
                    RC        TEXT,
                    courriel  TEXT,
                    commercial TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS factures (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero          TEXT UNIQUE,
                    date            DATE,
                    client          INTEGER REFERENCES "clients"("id"),
                    montant         NUMERIC,
                    objet           TEXT,
                    remise          INTEGER,
                    montant_lettres TEXT,
                    devis           TEXT,
                    bc_client       TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS facture_details (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero    TEXT,
                    reference TEXT,
                    qte       INTEGER,
                    prix      NUMERIC)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS reglement (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    facture TEXT,
                    montant TEXT,
                    type    TEXT,
                    date    DATE)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS utilisateurs (
                    login     TEXT,
                    pass      TEXT,
                    nom       TEXT,
                    fonction  TEXT,
                    groupe    TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS bordereau_details (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero    TEXT,
                    reference TEXT,
                    qte       INTEGER,
                    prix      NUMERIC)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS bordereau (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero     TEXT,
                    devis      TEXT,
                    bc_client  TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS historique (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    reference TEXT,
                    date      DATE,
                    mouvement TEXT,
                    num_mvt   TEXT,
                    qte_avant INTEGER,
                    qte_mvt   INTEGER,
                    qte_apres INTEGER)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS achats (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    reference   TEXT,
                    designation TEXT,
                    qte         INTEGER,
                    prix        INTEGER,
                    commentaire  TEXT,
                    date         DATETIME)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS fournisseurs (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom        TEXT,
                    initiales  TEXT,
                    contact    TEXT,
                    NUI        TEXT,
                    RC         TEXT,
                    courriel   TEXT,
                    commercial TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS commandes (
                    id              INTEGER  PRIMARY KEY AUTOINCREMENT,
                    numero          TEXT     UNIQUE,
                    date            DATETIME,
                    fournisseur     INTEGER     REFERENCES fournisseurs (id),
                    montant         NUMERIC,
                    montant_lettres TEXT,
                    statut          TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS commande_details (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero    TEXT,
                    reference TEXT,
                    qte       INTEGER,
                    prix      NUMERIC)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS receptions (
                    id        INTEGER  PRIMARY KEY AUTOINCREMENT,
                    numero    TEXT,
                    bl_client TEXT,
                    commande  TEXT,
                    date      DATETIME )""")

    cur.execute("""CREATE TABLE reception_details (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero    TEXT,
                    reference TEXT,
                    qte       INTEGER,
                    prix      NUMERIC)""")

    conn.commit()
    conn.close()


# fonctions de la table devis et devis_details ___________________________________________________________
def add_devis(numero, date, client, montant, objet, remise, montant_lettres):
    """Cete fonction génère un nouveau devis
        numero, date, client, montant, objet, remise, montant_lettres sont les paramètres de base"""

    statut = "Non facturé"
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO devis values 
                    (?,?,?,?,?,?,?,?,?)""",
                (cur.lastrowid, numero, date, client, montant, objet, remise, montant_lettres, statut))
    conn.commit()
    conn.close()


def update_devis_details(ref, qte, prix, id_det):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""UPDATE devis_details SET 
                                        reference = ?,
                                        qte = ?,
                                        prix = ?
                                        WHERE id = ?""", (ref, qte, prix, id_det))
    conn.commit()
    conn.close()


def update_devis(montant, remise, montant_lettres, numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""UPDATE devis SET 
                    montant = ?,
                    remise = ?,
                    montant_lettres = ?
                    WHERE numero = ?""", (montant, remise, montant_lettres, numero))
    conn.commit()
    conn.close()


def delete_devis_details(id_detail):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""DELETE FROM devis_details WHERE id = ?""", (id_detail, ))
    con.commit()
    con.close()


def delete_devis_details_by_numero(numero):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""DELETE FROM devis_details WHERE numero = ?""", (numero, ))
    con.commit()
    con.close()


def delete_devis(numero):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""DELETE FROM devis WHERE numero = ?""", (numero, ))
    con.commit()
    con.close()


def find_devis_num(id_client):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT count(id) FROM devis WHERE client=?""", (id_client,))
    resultat = cur.fetchone()
    r_final = ""

    ini_cli = search_initiales(id_client)

    if resultat[0] is None or resultat[0] == 0:
        r_final = initiales_entreprise + "/DV/" + ini_cli + "001"
    else:
        if int(resultat[0]) < 10:
            r_final = initiales_entreprise + "/DV/" + ini_cli + "00" + str(resultat[0] + 1)

        elif 10 < int(resultat[0]) < 100:
            r_final = initiales_entreprise + "/DV/" + ini_cli + "0" + str(resultat[0] + 1)

        else:
            r_final = initiales_entreprise + "/DV/" + ini_cli + str(resultat[0] + 1)

    conn.commit()
    conn.close()
    return r_final


def search_devis_details(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT id, reference, 

                    (SELECT designation FROM articles WHERE articles.reference = devis_details.reference) as designation,

                    qte, prix FROM devis_details WHERE numero =?""", (numero,))

    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        total = row[3] * row[4]
        row = row + (total,)
        r_final.append(row)

    conn.commit()
    conn.close()
    return r_final


def add_devis_details(numero, reference, qte, prix):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(""" INSERT INTO devis_details values (?,?,?,?,?)""", (cur.lastrowid, numero, reference, qte, prix))
    conn.commit()
    conn.close()


def show_info_devis(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(""" SELECT client, date, objet, montant, remise, montant_lettres, statut FROM devis WHERE numero = ? """,
                (numero,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat


def find_devis_details(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM devis_details WHERE numero=?""", (numero,))
    resultat = cur.fetchall()
    conn.commit()
    conn.close()
    return resultat


def all_devis():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT numero from devis""")
    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        r_final.append(row[0])

    conn.commit()
    conn.close()
    return r_final


def all_devis_rech(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    num = "%" + numero + "%"
    cur.execute("""SELECT numero from devis WHERE numero LIKE ?""", (num,))
    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        r_final.append(row[0])

    conn.commit()
    conn.close()
    return r_final


def search_statut_devis(devis_num):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT statut FROM devis WHERE numero = ?""", (devis_num,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def maj_statut_devis(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""UPDATE devis set statut=? WHERE numero=?""", ("Facturé", numero))
    conn.commit()
    conn.close()


# table clients _____________________________________________________________________________________
def search_initiales(id_client: int):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT initiales FROM clients WHERE id = ?""", (id_client,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def search_initiales_nom(nom: int):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT initiales FROM clients WHERE nom = ?""", (nom,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def all_initiales():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT initiales FROM clients""")
    resultat = cur.fetchall()
    final = []
    for row in resultat:
        final.append(row[0])
    conn.commit()
    conn.close()
    return final


def id_client_by_name(nom):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT id FROM clients WHERE nom = ?""", (nom,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def add_client(nom, ini, cont, nui, rc, mail, comm):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO clients values (?,?,?,?,?,?,?,?)""",
                (cur.lastrowid, nom, ini, cont, nui, rc, mail, comm))
    conn.commit()
    conn.close()


def all_clients():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT nom FROM clients ORDER BY nom""")
    resultat = cur.fetchall()
    r_final = []
    for row in resultat:
        r_final.append(row[0])
    conn.commit()
    conn.close()
    return r_final


def recherche_initiales():
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT initiales FROM clients""")
    resultat = cur.fetchall()
    r_final = []
    for row in resultat:
        r_final.append(row[0])
    con.commit()
    con.close()
    return r_final


def liste_clients():
    """all clients name"""
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT nom FROM clients""")
    resultat = cur.fetchall()
    r_final = []
    for row in resultat:
        r_final.append(row[0])
    conn.commit()
    conn.close()
    return r_final


def infos_clients(id_client):
    """search infos client by id"""
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM clients WHERE id = ?""", (id_client,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat


def update_client(nom, ini, cont, nui, rc, mail, comm, id_client):
    """update a client"""
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""UPDATE clients SET 
                    nom = ?,
                    initiales = ?,
                    contact = ?,
                    NUI = ?,
                    RC = ?,
                    courriel = ?,
                    commercial = ?
                    WHERE id = ?""", (nom, ini, cont, nui, rc, mail, comm, id_client))
    conn.commit()
    conn.close()


def id_client_par_nom(nom_client):
    """ search id client by name"""
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT id FROM clients WHERE nom = ?""", (nom_client,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def infos_clients_par_id(id_client):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM clients WHERE id = ?""", (id_client,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res


# table factures _____________________________________________________________________
def add_facture(numero, client, montant, objet, remise, montant_lettres, devis, bc_client):
    global today
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO factures values 
                    (?,?,?,?,?,?,?,?,?,?)""",
                (cur.lastrowid, numero, today, client, montant, objet, remise, montant_lettres, devis, bc_client))
    conn.commit()
    conn.close()


def add_details_facture(numero, ref, qte, prix):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO facture_details values (?,?,?,?,?)""", (cur.lastrowid, numero, ref, qte, prix))
    conn.commit()
    conn.close()


def nb_factures():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT id FROm factures ORDER BY id DESC""")
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def find_facture_num(id_client):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT count(id) FROM factures WHERE client=?""", (id_client,))
    resultat = cur.fetchone()
    ini_cli = search_initiales(id_client)

    if resultat[0] == 0:
        r_final = initiales_entreprise + "/FA/" + ini_cli + "001"
    else:
        if resultat[0] < 10:
            r_final = initiales_entreprise + "/FA/" + ini_cli + "00" + str(resultat[0] + 1)

        elif 10 < resultat[0] < 100:
            r_final = initiales_entreprise + "/FA/" + ini_cli + "0" + str(resultat[0] + 1)

        else:
            r_final = initiales_entreprise + "/FA/" + ini_cli + str(resultat[0] + 1)
    conn.commit()
    conn.close()
    return r_final


def all_factures_rech(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    num = "%" + numero + "%"
    cur.execute("""SELECT numero from factures WHERE numero LIKE ?""", (num,))
    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        r_final.append(row[0])

    conn.commit()
    conn.close()
    return r_final


def show_info_factures(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """ SELECT client, date, objet, montant, remise, montant_lettres, bc_client, devis FROM factures WHERE numero = ? """,
        (numero,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat


def search_factures_details(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT id, reference, 

                    (SELECT designation FROM articles WHERE articles.reference = facture_details.reference) as designation,

                    qte, prix FROM facture_details WHERE numero =?""", (numero,))

    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        total = row[3] * row[4]
        row = row + (total,)
        r_final.append(row)

    conn.commit()
    conn.close()
    return r_final


def find_montant_facture(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT montant FROM factures WHERE numero =?""", (numero,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def mt_deja_paye(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT sum(montant) FROM reglement WHERE facture = ?""", (numero,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def add_reglement(facture, montant, type, date):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO reglement values (?,?,?,?,?)""", (cur.lastrowid, facture, montant, type, date))
    conn.commit()
    conn.close()


def all_factures():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT numero FROM factures""")
    resultat = cur.fetchall()

    r_final = []

    for row in resultat:
        r_final.append(row[0])

    conn.commit()
    conn.close()
    return r_final


def factures_client(id_client):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT id, numero, montant, 

                    (select sum(montant) FROM reglement WHERE reglement.facture = factures.numero) as percu

                    FROM factures WHERE client =?""", (id_client,))

    resultat = cur.fetchall()

    r_final = []

    for row in resultat:
        if row[3] is not None:
            reste = int(row[2]) - int(row[3])
            if reste == 0:
                statut = "réglée"
            else:
                statut = "en cours"
            row = row + (reste, statut)
            r_final.append(row)
        else:
            reste = row[2]
            statut = "en cours"
            row2 = (row[0], row[1], row[2], 0, reste, statut)
            r_final.append(row2)

    conn.commit()
    conn.close()
    return r_final


def search_factures_details(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT id, reference, 

                    (SELECT designation FROM articles WHERE articles.reference = facture_details.reference) as designation,

                    qte, prix FROM facture_details WHERE numero =?""", (numero,))

    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        total = row[3] * row[4]
        row = row + (total,)
        r_final.append(row)

    conn.commit()
    conn.close()
    return r_final


# table articles
def search_designation(reference):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT designation, prix FROM articles WHERE reference = ?""", (reference,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat


def search_infos_desig(designation):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM articles WHERE designation = ?""", (designation,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat


def all_references():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT reference FROM articles ORDER BY reference""")
    resultat = cur.fetchall()
    r_final = []
    for row in resultat:
        r_final.append(row[0])
    conn.commit()
    conn.close()
    return r_final


def all_references_stock():
    nature = "stock"
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT reference FROM articles WHERE nature = ? """, (nature, ))
    resultat = cur.fetchall()
    r_final = []
    for row in resultat:
        r_final.append(row[0])
    conn.commit()
    conn.close()
    return r_final


def all_articles():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM articles""")
    resultat = cur.fetchall()
    conn.commit()
    conn.close()
    return resultat


def find_stock_ref(ref):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT qté FROM articles WHERE reference =?""", (ref,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def find_prix_ref(ref):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT prix FROM articles WHERE reference =?""", (ref,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def find_nature_ref(ref):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT nature FROM articles WHERE reference =?""", (ref,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def filtrer_articles(designation, nature):
    des = "%" + designation + "%"
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM articles WHERE designation LIKE ? AND nature=?""", (des, nature))
    resultat = cur.fetchall()
    conn.commit()
    conn.close()
    return resultat


def add_ref(ref, des, nat, qte, prix, unite):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO articles values (?,?,?,?,?,?,?)""", (cur.lastrowid, ref, des, nat, qte, prix, unite))
    conn.commit()
    conn.close()


def update_stock(qte, ref):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""UPDATE articles SET qté = ? WHERE reference = ?""", (qte, ref))
    conn.commit()
    conn.close()


def all_infos_ref(reference):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT designation, nature, qté FROM articles WHERE reference =? """, (reference,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat


def look_unit(ref):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT unite FROM articles WHERE reference=?""", (ref,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def search_ref_id(reference):
    """chercher l'id d'une référence à partir de la référence"""
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT id FROM articles WHERE reference = ?""", (reference, ))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def find_unique_ref():
    """ verifier l'unicité d'une référence"""
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT reference FROM articles""")
    result = cur.fetchall()
    final = []
    for row in result:
        final.append(row[0])
    conn.commit()
    conn.close()
    return final


def update_ref_by_name(designation, ref_id):
    """ update reference and designation by id ref"""
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("UPDATE articles SET designation = ? WHERE id = ?", (designation, ref_id))
    conn.commit()
    conn.close()


# tables utilisateurs
def all_users():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT login, pass from utilisateurs""")
    resultat = cur.fetchall()
    conn.commit()
    conn.close()
    return resultat


def check_user(login: str):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT login FROM utilisateurs""")
    resultat = cur.fetchall()
    conn.commit()
    conn.close()
    counter = 0

    for item in resultat:
        if item[0] == login:
            counter += 1

    if counter > 0:
        return True
    else:
        return False


def find_user_password(login):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT pass from utilisateurs WHERE login = ?""", (login,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


# table bordereau details
def add_bordereau(numero, devis, bc_client):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO bordereau values (?,?,?,?)""", (cur.lastrowid, numero, devis, bc_client))
    conn.commit()
    conn.close()


def add_bordereau_details(numero, ref, qte, prix):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO bordereau_details values (?,?,?,?,?)""", (cur.lastrowid, numero, ref, qte, prix))
    conn.commit()
    conn.close()


def all_bordereaux():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT numero FROM bordereau""")
    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        r_final.append(row[0])

    conn.commit()
    conn.close()
    return r_final


def find_bordereau_num(client):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT id FROM bordereau ORDER BY id DESC""")
    resultat = cur.fetchone()

    r_final = ""

    if resultat == None:
        r_final = initiales_entreprise + "/BL/" + str(client) + "001"
    else:
        if resultat[0] < 10:
            r_final = initiales_entreprise + "/BL/" + str(client) + "00" + str(resultat[0])

        elif resultat[0] > 10 and resultat[0] < 100:
            r_final = initiales_entreprise + "/BL/" + str(client) + "0" + str(resultat[0])

        else:
            r_final = initiales_entreprise + "/BL/" + str(client) + str(resultat[0])

    conn.commit()
    conn.close()
    return r_final


def search_bordereau(devis):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM bordereau WHERE devis = ?""", (devis,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat


def verif_bordereau(devis):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT numero FROM bordereau WHERE devis =?""", (devis,))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


# table historique
def add_historique(ref, typp, num, qte_av, qte, qte_ap):
    global today
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO historique values (?,?,?,?,?,?,?,?)""",
                (cur.lastrowid, ref, today, typp, num, qte_av, qte, qte_ap))
    conn.commit()
    conn.close()


def find_histo_num():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT id FROM historique ORDER by id  DESC""")
    resultat = cur.fetchone()

    if resultat is None:
        numero = initiales_entreprise + "/EN/1"

    else:
        numero = initiales_entreprise + "/EN/" + str(resultat[0] + 1)

    conn.commit()
    conn.close()
    return numero


def all_historique_by_ref(reference):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM historique WHERE reference = ?""", (reference,))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def nb_achats():
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT count(id) FROM achats""")
    resultat = cur.fetchone()
    con.commit()
    con.close()
    if resultat[0] is None:
        return 0
    else:
        return resultat[0]


def generate_achat_num():
    nb = nb_achats()
    return f"FMD/AD/{int(nb) + 1}"


def add_achat(numero, ref, des, qte, prix, comm):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""INSERT INTO achats values (?,?,?,?,?,?,?,?)""", (cur.lastrowid, numero, ref, des, qte, prix, comm, today))
    con.commit()
    con.close()


def maj_prix_ref(prix, reference):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""UPDATE articles SET prix = ? WHERE reference = ? """, (prix, reference))
    con.commit()
    con.close()


def delete_ref(reference):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""DELETE FROM articles WHERE reference = ? """, (reference,))
    con.commit()
    con.close()


# table fournisseurs __________________________________________________________________
def add_fournisseur(nom, initiales, contact, nui, rc, courriel, commercial):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO fournisseurs values (?,?,?,?,?,?,?,?)""", (cur.lastrowid, nom, initiales, contact, nui, rc, courriel, commercial))
    conn.commit()
    conn.close()


def infos_fournisseur_by_name(nom):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM fournisseurs WHERE nom = ?""", (nom,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def infos_fournisseur_by_id(id_fournisseur):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM fournisseurs WHERE id = ?""", (id_fournisseur,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def all_fournisseurs():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM fournisseurs""")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def all_fournisseur_name():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT nom FROM fournisseurs""")
    result = cur.fetchall()
    final = []
    for data in result:
        final.append(data[0])
    conn.commit()
    conn.close()
    return final


def all_initiales_fournisseurs():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT initiales FROM fournisseurs""")
    result = cur.fetchall()
    final = []
    for data in result:
        final.append(data[0])
    conn.commit()
    conn.close()
    return final


def update_fournisseur_by_id(nom, initiales, contact, nui, rc, courriel, comm, id_foun):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""UPDATE fournisseurs SET
                nom = ?,
                initiales = ?,
                contact = ?,
                NUI = ?,
                RC = ?,
                courriel = ?,
                commercial = ? WHERE id = ?""", (nom, initiales, contact, nui, rc, courriel, comm, id_foun))
    conn.commit()
    conn.close()


def delete_fournisseurs_by_id(id_fournisseur):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""DELETE FROM fournisseurs WHERE id = ?""", (id_fournisseur, ))
    conn.commit()
    conn.close()


# Table commandes t details commandes _____________________________________________________________________________________
def add_commande(numero, date, fournisseur_id, montant, montant_lettres):
    statut = "en cours"
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO commandes values (?,?,?,?,?,?,?)""", (cur.lastrowid, numero, date, fournisseur_id, montant, montant_lettres, statut))
    conn.commit()
    conn.close()


def add_commande_detail(numero, reference, qte, prix):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO commande_details values (?,?,?,?,?)""", (cur.lastrowid, numero, reference, qte, prix))
    conn.commit()
    conn.close()


def update_commande(montant, montant_lettres, statut, numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""UPDATE commande SET
                montant = ?,
                montant_lettres = ?,
                statut = ? WHERE numero = ?""", (montant, montant_lettres, statut, numero))
    conn.commit()
    conn.close()


def update_commande_statut(statut, numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""UPDATE commandes SET statut = ? WHERE numero = ?""", (statut, numero))
    conn.commit()
    conn.close()


def update_commande_details(reference, qte, prix, numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""UPDATE commande_details SET
                reference = ?,
                qte = ?,
                prix = ? WHERE numero = ?""", (reference, qte, prix, numero))
    conn.commit()
    conn.close()


def delete_commade(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""DELETE FROM commandes WHERE numero = ?""", (numero,))
    conn.commit()
    conn.close()


def delete_commande_details(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""DELETE FROM commende_details WHERE numero = ?""", (numero,))
    conn.commit()
    conn.close()


def show_commande_details(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM commande_details WHERE numero = ?""", (numero,))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def all_commandes():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT numero,
                date,
                (SELECT nom FROM fournisseurs WHERE fournisseurs.id = commandes.fournisseur) as fournisseur,
                montant, statut FROM commandes""")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def list_commandes():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT numero FROM commandes""")
    result = cur.fetchall()
    final = []
    for row in result:
        final.append(row[0])
    conn.commit()
    conn.close()
    return final


def show_infos_commandes(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM commandes WHERE numero = ?""", (numero,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def nb_commandes_by_fournisseur(id_fournisseur):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT count(id) FROM commandes WHERE fournisseur =?""", (id_fournisseur, ))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def create_numero_commande(id_fournisseur):
    initiales = infos_fournisseur_by_id(id_fournisseur)[2]
    nombre = nb_commandes_by_fournisseur(id_fournisseur)
    if nombre == 0:
        numero = f"FMD/CMD/{initiales}001"
    elif nombre < 10:
        numero = f"FMD/CMD/{initiales}00{nombre + 1}"
    elif 10 < nombre < 99:
        numero = f"FMD/CMD/{initiales}0{nombre + 1}"
    else:
        numero = f"FMD/CMD/{initiales}{nombre + 1}"
    return numero


def update_state_command(statut, numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""UPDATE commandes SET statut = ? WHERE numero = ?""", (statut, numero))
    conn.commit()
    conn.close()


def commande_details_by_num(numero):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT reference, qte, prix FROM commande_details WHERE numero = ?""", (numero,))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


# table receptions ___________________________________________________________________________
def add_reception(numero, bl_client, commande, date):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO receptions values (?,?,?,?,?)""", (cur.lastrowid, numero, bl_client, commande, date))
    conn.commit()
    conn.close()


def add_reception_details(numero, ref, qte, prix):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""INSERT INTO reception_details values (?,?,?,?,?)""", (cur.lastrowid, numero, ref, qte, prix))
    conn.commit()
    conn.close()


def find_recept_num_by_command(command):
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT numero, date FROM receptions WHERE = ?""", (command, ))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def func():
    conn = sql.connect(my_base)
    cur = conn.cursor()
    cur.execute("""""")
    conn.commit()
    conn.close()









