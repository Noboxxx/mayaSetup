import os
from .menu import createMenuFromJson
from .shelf import createShelfFromJson, clearShelves


def example():
    file = os.path.join(os.path.dirname(__file__), 'example.json')
    createMenuFromJson('Example', file)

    clearShelves()
    createShelfFromJson('Example', file)