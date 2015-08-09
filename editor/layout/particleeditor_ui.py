# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'particleeditor.ui'
#
# Created: Sun Aug  9 13:31:51 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_particleEditor(object):
    def setupUi(self, particleEditor):
        particleEditor.setObjectName("particleEditor")
        particleEditor.resize(364, 796)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName("formLayout")
        self.lblMaxParticles = QtGui.QLabel(self.groupBox_3)
        self.lblMaxParticles.setObjectName("lblMaxParticles")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblMaxParticles)
        self.editParticleLimit = QtGui.QLineEdit(self.groupBox_3)
        self.editParticleLimit.setObjectName("editParticleLimit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.editParticleLimit)
        self.lblMaxSprites = QtGui.QLabel(self.groupBox_3)
        self.lblMaxSprites.setObjectName("lblMaxSprites")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblMaxSprites)
        self.editSpriteLimit = QtGui.QLineEdit(self.groupBox_3)
        self.editSpriteLimit.setObjectName("editSpriteLimit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.editSpriteLimit)
        self.chkWrapParticles = QtGui.QCheckBox(self.groupBox_3)
        self.chkWrapParticles.setObjectName("chkWrapParticles")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.chkWrapParticles)
        self.chkWrapSprites = QtGui.QCheckBox(self.groupBox_3)
        self.chkWrapSprites.setObjectName("chkWrapSprites")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.chkWrapSprites)
        self.chkReverseDraw = QtGui.QCheckBox(self.groupBox_3)
        self.chkReverseDraw.setObjectName("chkReverseDraw")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.chkReverseDraw)
        self.btnTexture = QtGui.QPushButton(self.groupBox_3)
        self.btnTexture.setObjectName("btnTexture")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.btnTexture)
        self.btnBgColor = QtGui.QToolButton(self.groupBox_3)
        self.btnBgColor.setText("")
        self.btnBgColor.setObjectName("btnBgColor")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.btnBgColor)
        self.lblColor = QtGui.QLabel(self.groupBox_3)
        self.lblColor.setObjectName("lblColor")
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.lblColor)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.btnAddEmitter = QtGui.QPushButton(self.groupBox)
        self.btnAddEmitter.setObjectName("btnAddEmitter")
        self.gridLayout.addWidget(self.btnAddEmitter, 1, 0, 1, 1)
        self.btnDeleteEmitter = QtGui.QPushButton(self.groupBox)
        self.btnDeleteEmitter.setObjectName("btnDeleteEmitter")
        self.gridLayout.addWidget(self.btnDeleteEmitter, 1, 1, 1, 1)
        self.listEmitter = QtGui.QListWidget(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listEmitter.sizePolicy().hasHeightForWidth())
        self.listEmitter.setSizePolicy(sizePolicy)
        self.listEmitter.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listEmitter.setProperty("showDropIndicator", False)
        self.listEmitter.setResizeMode(QtGui.QListView.Adjust)
        self.listEmitter.setSelectionRectVisible(True)
        self.listEmitter.setObjectName("listEmitter")
        self.gridLayout.addWidget(self.listEmitter, 0, 0, 1, 2)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnAddState = QtGui.QPushButton(self.groupBox_2)
        self.btnAddState.setObjectName("btnAddState")
        self.gridLayout_2.addWidget(self.btnAddState, 1, 0, 1, 1)
        self.cmbComponent = QtGui.QComboBox(self.groupBox_2)
        self.cmbComponent.setObjectName("cmbComponent")
        self.gridLayout_2.addWidget(self.cmbComponent, 2, 0, 1, 1)
        self.btnAddComponent = QtGui.QPushButton(self.groupBox_2)
        self.btnAddComponent.setObjectName("btnAddComponent")
        self.gridLayout_2.addWidget(self.btnAddComponent, 2, 1, 1, 1)
        self.btnDeleteState = QtGui.QPushButton(self.groupBox_2)
        self.btnDeleteState.setObjectName("btnDeleteState")
        self.gridLayout_2.addWidget(self.btnDeleteState, 1, 1, 1, 1)
        self.listState = QtGui.QListWidget(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listState.sizePolicy().hasHeightForWidth())
        self.listState.setSizePolicy(sizePolicy)
        self.listState.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listState.setProperty("showDropIndicator", False)
        self.listState.setResizeMode(QtGui.QListView.Adjust)
        self.listState.setSelectionRectVisible(True)
        self.listState.setObjectName("listState")
        self.gridLayout_2.addWidget(self.listState, 0, 0, 1, 2)
        self.btnRemoveComponent = QtGui.QPushButton(self.groupBox_2)
        self.btnRemoveComponent.setObjectName("btnRemoveComponent")
        self.gridLayout_2.addWidget(self.btnRemoveComponent, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        particleEditor.setWidget(self.dockWidgetContents)

        self.retranslateUi(particleEditor)
        QtCore.QObject.connect(self.btnAddComponent, QtCore.SIGNAL("clicked()"), particleEditor.onNewComponent)
        QtCore.QObject.connect(self.btnAddEmitter, QtCore.SIGNAL("clicked()"), particleEditor.onNewEmitter)
        QtCore.QObject.connect(self.btnAddState, QtCore.SIGNAL("clicked()"), particleEditor.onNewState)
        QtCore.QObject.connect(self.btnDeleteEmitter, QtCore.SIGNAL("clicked()"), particleEditor.onDeleteEmitter)
        QtCore.QObject.connect(self.btnDeleteState, QtCore.SIGNAL("clicked()"), particleEditor.onDeleteState)
        QtCore.QObject.connect(self.btnTexture, QtCore.SIGNAL("clicked()"), particleEditor.onLoadTexture)
        QtCore.QObject.connect(self.chkReverseDraw, QtCore.SIGNAL("toggled(bool)"), particleEditor.onReverseDraw)
        QtCore.QObject.connect(self.chkWrapParticles, QtCore.SIGNAL("toggled(bool)"), particleEditor.onWrapParticles)
        QtCore.QObject.connect(self.chkWrapSprites, QtCore.SIGNAL("toggled(bool)"), particleEditor.onWrapSprites)
        QtCore.QObject.connect(self.editParticleLimit, QtCore.SIGNAL("textChanged(QString)"), particleEditor.onEditParticleLimit)
        QtCore.QObject.connect(self.editSpriteLimit, QtCore.SIGNAL("textChanged(QString)"), particleEditor.onEditSpriteLimit)
        QtCore.QObject.connect(self.listEmitter, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), particleEditor.onEmitterClick)
        QtCore.QObject.connect(self.listState, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), particleEditor.onStateClick)
        QtCore.QObject.connect(self.btnBgColor, QtCore.SIGNAL("clicked()"), particleEditor.onBgColorClick)
        QtCore.QObject.connect(self.btnRemoveComponent, QtCore.SIGNAL("clicked()"), particleEditor.onDeleteComponent)
        QtCore.QMetaObject.connectSlotsByName(particleEditor)

    def retranslateUi(self, particleEditor):
        particleEditor.setWindowTitle(QtGui.QApplication.translate("particleEditor", "Particle Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("particleEditor", "Particle System", None, QtGui.QApplication.UnicodeUTF8))
        self.lblMaxParticles.setText(QtGui.QApplication.translate("particleEditor", "Particle limit", None, QtGui.QApplication.UnicodeUTF8))
        self.lblMaxSprites.setText(QtGui.QApplication.translate("particleEditor", "Sprite limit", None, QtGui.QApplication.UnicodeUTF8))
        self.chkWrapParticles.setText(QtGui.QApplication.translate("particleEditor", "Wrap particles", None, QtGui.QApplication.UnicodeUTF8))
        self.chkWrapSprites.setText(QtGui.QApplication.translate("particleEditor", "Wrap sprites", None, QtGui.QApplication.UnicodeUTF8))
        self.chkReverseDraw.setText(QtGui.QApplication.translate("particleEditor", "Reverse draw order", None, QtGui.QApplication.UnicodeUTF8))
        self.btnTexture.setText(QtGui.QApplication.translate("particleEditor", "Load texture atlas", None, QtGui.QApplication.UnicodeUTF8))
        self.lblColor.setText(QtGui.QApplication.translate("particleEditor", "Background color", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("particleEditor", "Emitters", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddEmitter.setText(QtGui.QApplication.translate("particleEditor", "Add emitter", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDeleteEmitter.setText(QtGui.QApplication.translate("particleEditor", "Remove emitter", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("particleEditor", "Particle States", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddState.setText(QtGui.QApplication.translate("particleEditor", "Add state", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddComponent.setText(QtGui.QApplication.translate("particleEditor", "Add component", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDeleteState.setText(QtGui.QApplication.translate("particleEditor", "Remove state", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRemoveComponent.setText(QtGui.QApplication.translate("particleEditor", "Remove component", None, QtGui.QApplication.UnicodeUTF8))

