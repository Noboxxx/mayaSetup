import json
from maya import cmds

MAYA_MENU_BAR = 'MayaWindow'


def createMenu(name):
    print('# Creating \'{}\' menu'.format(name))

    if cmds.menu(name, exists=True, q=True):
        print('# Deleting \'{}\' menu'.format(name))
        cmds.deleteUI(name, menu=True)

    menu = cmds.menu(name, tearOff=True, parent=MAYA_MENU_BAR)
    return menu


def fillUpMenu(menu, data):

    for item in data:
        if isinstance(item, dict):
            label = item.get('label', 'untitled#')
            path = item.get('path')

            if path:
                parent = menu
                for folderName in path.split('|'):
                    folderPath = '{}|{}'.format(parent, folderName)
                    if not cmds.menuItem(folderPath, exists=True, q=True):
                        cmds.menuItem(
                            folderName,
                            subMenu=True,
                            tearOff=True,
                            parent=parent,
                        )
                    parent = folderPath
                fullPath = '{}|{}'.format(menu, path)
            else:
                fullPath = menu

            cmds.menuItem(
                label,
                command=item.get('command', ''),
                image=item.get('icon', ''),
                annotation=item.get('annotation', ''),
                parent=fullPath,
            )


def createMenuFromData(name, data):
    menu = createMenu(name)
    fillUpMenu(menu, data)
    return menu


def createMenuFromJson(name, file):

    with open(file, 'r') as f:
        data = json.load(f)

    return createMenuFromData(name, data)