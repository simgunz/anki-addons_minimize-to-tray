#-*- coding: utf-8 -*-
# Copyright: Simone Gaiarin <simgunz@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Name: Minimize to Tray 2
# Version: 0.1
# Description: Minimize anki to tray when the X button is pressed
# Homepage: https://github.com/simgunz/anki-plugins
# Report any problem in the github issues section

from PyQt4.QtGui import *
from PyQt4 import QtCore
import aqt
from anki.hooks import addHook

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

def focusChanged(old, now):
    if now == None:
        self.last_focus = old

def showAll():
    for w in self.tray_hidden:
        if w.isWindow() and w.isHidden():
            w.showNormal()
    active = self.last_focus
    active.raise_()
    active.activateWindow()
    self.anki_visible = True
    self.tray_hidden = []

def hideAll():
    self.tray_hidden = []
    activeWindow = QApplication.activeModalWidget()
    for w in QApplication.topLevelWidgets():
        if w.isWindow() and not w.isHidden():
            if not w.children():
                continue
            w.hide()
            self.tray_hidden.append(w)
    self.anki_visible = False

def trayActivated(reason):
    if reason == QSystemTrayIcon.Trigger:
        if self.anki_visible:
            hideAll()
        else:
            showAll()

def createSysTray():
    self.anki_visible = True
    self.last_focus = self
    self.trayIcon = QSystemTrayIcon(self)
    ankiLogo = QIcon()
    ankiLogo.addPixmap(QPixmap(_fromUtf8(":/icons/anki.png")), QIcon.Normal, QIcon.Off)
    self.trayIcon.setIcon(ankiLogo)
    trayMenu = QMenu(self)
    self.trayIcon.setContextMenu(trayMenu)
    trayMenu.addAction(self.form.actionExit)
    self.connect(self.trayIcon, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), trayActivated)
    self.connect(self.app, QtCore.SIGNAL("focusChanged(QWidget*,QWidget*)"), focusChanged)
    self.trayIcon.show()

def myOnClose():
    "Called from a shortcut key. Close current active window."
    aw = self.app.activeWindow()
    if not aw or aw == self:
        self.unloadProfile(browser=False)
        self.app.quit()
    else:
        aw.close()

def myCloseEvent(event):
    "User hit the X button"
    trayActivated(QSystemTrayIcon.Trigger)
    event.ignore();

def setCloseEventAction():
    self.disconnect(self.form.actionExit, QtCore.SIGNAL("triggered()"), self, QtCore.SLOT("close()"))
    self.connect(self.form.actionExit, QtCore.SIGNAL("triggered()"), self.onClose)

if __name__ == "__main__":
    print "Don't run me. I'm a plugin."
else:
    self = aqt.mw
    addHook("profileLoaded", setCloseEventAction)
    addHook("profileLoaded", createSysTray)
    self.closeEvent = myCloseEvent
    self.onClose = myOnClose
