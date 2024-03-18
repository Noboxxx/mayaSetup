import json
from functools import partial

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QAction, QMenu
from maya import cmds, OpenMayaUI
from shiboken2 import wrapInstance

MAYA_MAIN_WINDOW = 'MayaWindow'


def execCommand(command):
    exec(command)


def getMenu(name):
    pointer = OpenMayaUI.MQtUtil.findControl(name)
    return wrapInstance(int(pointer), QMenu)


def createMenu(name):
    print('# Creating \'{}\' menu'.format(name))

    if cmds.menu(name, exists=True, q=True):
        print('# Deleting \'{}\' menu'.format(name))
        cmds.deleteUI(name, menu=True)

    menu = cmds.menu(name, tearOff=True, parent=MAYA_MAIN_WINDOW)
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

            parentMenu = getMenu(fullPath)

            action = QAction(label, parentMenu)

            command = item.get('command')
            if command:
                action.triggered.connect(partial(execCommand, command))

            icon = item.get('icon')
            if icon:
                action.setIcon(QIcon(icon))

            shortcut = item.get('shortcut')
            if shortcut:
                action.setShortcut(shortcut)

            parentMenu.addAction(action)


def createMenuFromData(name, data):
    menu = createMenu(name)
    fillUpMenu(menu, data)
    return menu


def createMenuFromJson(name, file):

    with open(file, 'r') as f:
        data = json.load(f)

    return createMenuFromData(name, data)