from flet import View
from pages.stocks import Stocks
from pages.accueil import Accueil
from pages.clients import Clients
from pages.fournisseurs import Fournisseurs
from pages.commandes import Commandes
from pages.devis import Devis
from pages.factures import Factures


def view_handler(page):
    return {
        '/': View(
            route='/',
            controls=[
                Accueil(page)
            ]
        ),

        '/stocks': View(
            route='/stocks',
            controls=[
                Stocks(page)
            ]
        ),

        '/clients': View(
            route='/clients',
            controls=[
                Clients(page)
            ]
        ),

        '/fournisseurs': View(
            route='/fournisseurs',
            controls=[
                Fournisseurs(page)
            ]
        ),

        '/commandes': View(
            route='/commandes',
            controls=[
                Commandes(page)
            ]
        ),

        '/devis': View(
            route='/devis',
            controls=[
                Devis(page)
            ]
        ),

        '/factures': View(
            route='/factures',
            controls=[
                Factures(page)
            ]
        ),

    }
