from Sicapp.models import Compra


def iniciarCompra():
    compra=Compra()
    compra.precio=0
    compra.total=0
    compra.save()

    return compra.idCompra