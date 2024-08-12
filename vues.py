from flet import View
from stocks import Stocks
from accueil import Accueil
from clients import Clients
from fournisseurs import Fournisseurs
from commandes import Commandes
from devis import Devis
from factures import Factures


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
