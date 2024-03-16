import json
from maya import cmds, mel

MAYA_SHELF_LAYOUT = 'Shelf|MainShelfLayout|formLayout17|ShelfLayout'
SHELF_SUFFIX = '_'


def clearShelves():
    for shelf in cmds.lsUI(type='shelfLayout'):
        if shelf.endswith(SHELF_SUFFIX):
            print('# Deleting \'{}\' shelf'.format(shelf))
            cmds.deleteUI(shelf)


def createShelf(name):
    print('# Creating \'{}\' shelf'.format(name))

    formattedName = '{}{}'.format(name, SHELF_SUFFIX)
    if cmds.shelfLayout(formattedName, exists=True, q=True):
        print('# Deleting \'{}\' shelf'.format(formattedName))
        cmds.deleteUI(formattedName)

    shelf = cmds.shelfLayout(formattedName, parent=MAYA_SHELF_LAYOUT)

    return shelf


def fillUpShelf(shelf, data):
    for item in data:

        if isinstance(item, dict):
            cmds.shelfButton(
                annotation=item.get('annotation', ''),
                image=item.get('icon', 'pythonFamily.png'),
                command=item.get('command', ''),
                imageOverlayLabel=item.get('overlayLabel', ''),
                parent=shelf,
            )

        elif item is None:
            mel.eval('addShelfSeparator()')


def createShelfFromData(name, data):
    shelf = createShelf(name)
    fillUpShelf(shelf, data)
    return shelf


def createShelfFromJson(name, file):

    with open(file, 'r') as f:
        data = json.load(f)

    return createShelfFromData(name, data)