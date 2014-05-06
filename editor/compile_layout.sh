#!/bin/bash

cd layout

pyside-uic -o mainwindow_ui.py mainwindow.ui
pyside-uic -o debugdock_ui.py debugdock.ui
pyside-uic -o environmentdock_ui.py environmentdock.ui
pyside-uic -o propertyeditordock_ui.py propertyeditordock.ui
pyside-uic -o consoledock_ui.py consoledock.ui
pyside-uic -o outlinerdock_ui.py outlinerdock.ui
pyside-uic -o profilerdock_ui.py profilerdock.ui

cd ..