#-*- coding: utf-8 -*-
# Copyright: Simone Gaiarin <simgunz@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Name: Minimize to Tray
# Version: 0.1
# Description: Minimize anki to tray when the X button is pressed
# Homepage: https://github.com/simgunz/anki-plugins
# Report any problem in the github issues section

from anki.hooks import addHook, wrap
from ankiqt import mw, ui

from PyQt4 import QtGui, QtCore


def init_hook():
    mw.mainWin.actionExit.triggered.disconnect(mw.close)
    mw.mainWin.actionExit.triggered.connect(mw.quit)
    trayMenu = QtGui.QMenu(mw)
    trayMenu.addAction(mw.mainWin.actionExit)
    mw.trayIcon.ti.setContextMenu(trayMenu)

def quit():
    if mw.state == "editCurrentFact":
        mw.moveToState("saveEdit")
        return
    if mw.saveAndClose(hideWelcome=True):
        if mw.config['syncOnProgramOpen']:
            mw.hideWelcome = True
            mw.syncDeck(interactive=False)
        mw.prepareForExit()
        mw.app.quit()

def myCloseEvent(event):
    "User hit the X button"
    if mw.trayIcon.ti.isVisible():
        mw.trayIcon.hideAll();
        event.ignore();

def myTrayActivated(reason):
    if reason != QtGui.QSystemTrayIcon.Context:
        if mw.trayIcon.anki_visible:
            mw.trayIcon.hideAll()
        else:
            mw.trayIcon.showAll()

if __name__ == "__main__":
    print "Don't run me. I'm a plugin."

else:
    mw.registerPlugin("Minimize to Tray", 1)
    if not mw.config['showTrayIcon']:
        ans = ui.utils.askUser("Minimize to tray plugin needs tray icon option "
                               "enabled.\nWould you like to enable it?")
        if ans:
            mw.config['showTrayIcon'] = True
            mw.config.save()
            mw.setupTray()

    if mw.config['showTrayIcon']:
        mw.quit = quit
        mw.closeEvent = myCloseEvent
        mw.trayIcon.activated = myTrayActivated
        mw.addHook('init', init_hook)
        print 'Minimize to tray plugin loaded'
    else:
        print 'Failed to load minimize to tray plugin. Tray not enabled.'
