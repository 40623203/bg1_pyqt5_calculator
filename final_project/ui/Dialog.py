# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_Dialog import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        
        self.waitingForOperand = True
        
        self.display.setText('0')
       
        digits = [self.one,  self.two,  self.three, \
            self.four,  self.five,  self.six, \
            self.seven,  self.eight,  self.nine,  self.zero]
        
        for i in digits:
            i.clicked.connect(self.digitClicked)
            
        plus_minus = [self.plusButton,  self.minusButton]
        
        for i in plus_minus:
            i.clicked.connect(self.additiveOperatorClicked)
            
        multiply_divide = [self.timesButton,  self.divisionButton]
        
        for i in multiply_divide:
            i.clicked.connect(self.multiplicativeOperatorClicked)
        
        self.equalButton.clicked.connect(self.equalClicked)
        
        self.clearButton.clicked.connect(self.clear)
        
        self.clearAllButton.clicked.connect(self.clearAll)
        
        self.readMemoryButton.clicked.connect(self.readMemory)
        
        self.clearMemoryButton.clicked.connect(self.clearMemory)
        
        self.setMemoryButton.clicked.connect(self.setMemory)
        
        self.addToMemoryButton.clicked.connect(self.addToMemory)
        
        self.pointButton.clicked.connect(self.pointClicked)
        
        self.changeSignButton.clicked.connect(self.changeSignClicked)
        
        self.backspaceButton.clicked.connect(self.backspaceClicked)
        
        unaryOperator = [self.squareRootButton, self.powerButton,  self.reciprocalButton ]
        for i in unaryOperator:
            i.clicked.connect(self.unaryOperatorClicked)
    def digitClicked(self):
        clickedButton = self.sender()
        digitValue = int(clickedButton.text())
        
        if self.display.text() == '0' and digitValue == 0.0:
            return
            
        if self.waitingForOperand:
            self.display.clear()
            self.waitingForOperand = False
            
        self.display.setText(self.display.text() + str(digitValue))
        
    def unaryOperatorClicked(self):
        '''單一運算元按下後處理方法'''
        pass
        
    def additiveOperatorClicked(self):
        '''加或減按下後進行的處理方法'''
        pass
        
    def multiplicativeOperatorClicked(self):
        '''乘或除按下後進行的處理方法'''
        pass
        
    def equalClicked(self):
        '''等號按下後的處理方法'''
        pass
        
    def pointClicked(self):
        pass

    def changeSignClicked(self):
        '''變號鍵按下後的處理方法'''
        pass
            
    def backspaceClicked(self):
        '''回復鍵按下的處理方法'''
        pass
        
    def clear(self):
        self.display.setText('0')
        self.waitingForOperand = True
        
    def clearAll(self):
        '''全部清除鍵按下後的處理方法'''
        self.sumSoFar =0.0
        self.factorSoFar =0.0
        self.pendingAdditiveOperator=''
        self.pendingMultiplicativeOperator=''
        self.display.setText('0')
        self.waitingForOperand = True
        
    def clearMemory(self):
        '''清除記憶體鍵按下後的處理方法'''
        pass
        
    def readMemory(self):
        '''讀取記憶體鍵按下後的處理方法'''
        pass
        
    def setMemory(self):
        '''設定記憶體鍵按下後的處理方法'''
        pass
        
    def addToMemory(self):
        '''放到記憶體鍵按下後的處理方法'''
        pass
        
    def createButton(self):
        ''' 建立按鍵處理方法, 以 Qt Designer 建立對話框時, 不需要此方法'''
        pass
        
    def abortOperation(self):
        '''中斷運算'''
        pass
        
    def calculate(self):
        '''計算'''
        pass
