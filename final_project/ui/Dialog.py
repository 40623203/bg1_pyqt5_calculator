# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_Dialog import Ui_Dialog

import math

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
        
        self.display.setText('0')
       
        digits = [self.one,  self.two,  self.three, \
            self.four,  self.five,  self.six, \
            self.seven,  self.eight,  self.nine,  self.zero]
        
        for i in digits:
            i.clicked.connect(self.digitClicked)
            '''
            0 ~9 數字按建, 點按後由 digitClicked() 方法槽承接處理
            '''
            
        plus_minus = [self.plusButton,  self.minusButton]
        
        for i in plus_minus:
            i.clicked.connect(self.additiveOperatorClicked)
            '''
            加或減運算元, 包括 + 與 - 運算, 點按後由 additiveOperatorClicked() 方法槽承接處理
            '''
            
        multiply_divide = [self.timesButton,  self.divisionButton]
        
        for i in multiply_divide:
            i.clicked.connect(self.multiplicativeOperatorClicked)
            '''
            乘或除運算元, 包括 * 與 / 運算, 點按後由 multiplicativeOperatorClicked() 方法槽承接處理
            '''
        
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
        
        unaryOperator = [self.squareRootButton, self.powerButton,  self.reciprocalButton]
        '''
        其餘按鍵則各自以特定的方法槽承接處理
        '''
        
        for i in unaryOperator:
            i.clicked.connect(self.unaryOperatorClicked)
            '''
            直接運算元, 包括 Sqrt, x^2 與 1/x, 點按後由 unaryOperatorClicked() 方法槽承接處理
            '''
        
        self.pendingAdditiveOperator = ''
        '''
        儲存使用者最後點按的加或減運算子字串
        '''
        self.sumSoFar = 0.0
        '''
        儲存累計數值, 使用者按下等號後, sumSoFar 重新計算結果, 並顯示在 display 幕, Clear All 按鍵則重置 sumSoFar 為 0
        '''
        self.waitingForOperand = True
        '''
        界定使用者是否處理運算數輸入階段, 若 waitingForOperand 為 True, 表示計算機正在等待使用者"開始"輸入運算數
        '''
        self.sumInMemory = 0.0
        '''
        與 MS, M+, 或 MC 按鍵相關的計算機記憶體數值, 存入 sumInMemory 變數對應的記憶空間
        '''
        self.factorSoFar = 0.0
        '''
        儲存乘或除運算子運算過程所得的暫存數值
        '''
        self.pendingMultiplicativeOperator = ''
        '''
        儲存使用者最後點按的乘或除運算子字串
        '''
        
    def digitClicked(self):
        '''
        使用者按下數字鍵, 必須能夠累積顯示該數字
        當顯示幕已經為 0, 再按零不會顯示 00, 而仍顯示 0 或 0.0
        
        '''
        #pass
        '''
        按數字按鍵, 將會送出該按鍵的 clicked() 訊號
        按鍵的 clicked() 訊號將會根據設定, 觸發 digitClicked() 方法槽
        PyQt5 的 Push Button 以 Qt5 中的 QObject::sender() 送出訊號, 此函式會傳回 sender 作為 QObject 的指標
        此一與 Push Button 配合的 sender 為 Button 物件, 因此可以在 digitClicked() 函式中, 利用 sender().text() 取得按鍵的 text 字串
        假如使用者點按 0, display 顯示字串 0, 但是若一開始輸入兩個以上的 0, digitClicked() 應該仍只顯示 0 字串
        若計算機處於等待新運算數輸入時 (以 waitingForOperand 判定), 新數字在顯示前, display 應該要清除先前所顯示的數字
        除了在顯示幕為 0 之後的 0 按鍵輸入, digitClicked() 方法槽不會繼續判定是否清除顯示幕或堆疊數字字串外, 所按的數字將會堆疊顯示
        '''
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
        #pass
        '''
        Sqrt, x^2 與 1/x 等按鍵的處理方法為 unaryOperatorClicked(), 與數字按鍵的點按回應相同, 透過 sender().text() 取得按鍵上的 text 字串
        unaryOperatorClicked() 方法隨後根據 text 判定運算子後, 利用 display 上的運算數進行運算後, 再將結果顯示在 display 顯示幕
        若進行運算 Sqrt 求數值的平方根時, 顯示幕中為負值, 或 1/x 運算時, x 為 0, 都視為無法處理的情況, 以呼叫 abortOperation() 處理
        直接運算子處理結束前, 運算結果會顯示在 display 中, 而且運算至此告一段落, 計算機狀態應該要回復到等待新運算數的階段, 因此 waitingForOperand 要重置為 True
        '''
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
        
        if clickedOperator  == "Sqrt":
            if operand < 0.0:
                self.abortOperation()
                return
                
            result = math.sqrt(operand)
        elif clickedOperator == "X^2":
            result = math.pow(operand,  2.0)
        elif clickedOperator == "1/x":
            if operand == 0.0:
                self.abortOperation()
                return
            result = 1.0 / operand
 
        self.display.setText(str(result))
        self.waitingForOperand = True
        
    def additiveOperatorClicked(self):
        '''加或減按下後進行的處理方法'''
        #pass
        '''
        按下加或減運算子按鍵時, 程式設定以 additiveOperatorClicked() 處理
        進入 additiveOperatorClicked() 後, 必須先查是否有尚未運算的乘或除運算子, 因為必須先乘除後才能加減
        先處理乘與除運算後, 再處理加或減運算後, 將 sumSoFar 顯示在 display 後, 必須重置 sumSoFar 為 0, 表示運算告一段落
        '''
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            self.display.setText(str(self.factorSoFar))
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''

        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return

            self.display.setText(str(self.sumSoFar))
        else:
            self.sumSoFar = operand

        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True
        
    def multiplicativeOperatorClicked(self):
        '''乘或除按下後進行的處理方法'''
        #pass
        '''
        按下乘或除運算子按鍵時, 程式設定以 multiplicativeOperatorClicked() 處理
        進入 multiplicativeOperatorClicked() 後, 無需檢查是否有尚未運算的加或減運算子, 因為乘除運算有優先權
        先處理乘與除運算後, 再處理加或減運算, 將 sumSoFar 顯示在 display 後, 必須重置 sumSoFar 為 0, 表示運算告一段落
        '''
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
 
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
 
            self.display.setText(str(self.factorSoFar))
        else:
            self.factorSoFar = operand
 
        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True
        
    def equalClicked(self):
        '''等號按下後的處理方法'''
        #pass
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''

        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return

            self.pendingAdditiveOperator = ''
        else:
            self.sumSoFar = operand

        self.display.setText(str(self.sumSoFar))
        self.sumSoFar = 0.0
        self.waitingForOperand = True
        
    def pointClicked(self):
        '''小數點按下後的處理方法'''
        #pass
        '''
        按下小數點按鍵後, 以 pointClicked() 方法處理, 直接在 display 字串中加上 "." 字串
        '''
        if self.waitingForOperand:
            self.display.setText('0')
 
        if "." not in self.display.text():
            self.display.setText(self.display.text() + ".")
 
        self.waitingForOperand = False

    def changeSignClicked(self):
        '''變號鍵按下後的處理方法'''
        #pass
        '''
        按下變號按鍵後, 由 changeSignClicked() 處理, 若顯示幕上為正值, 則在 display 字串最前面, 疊上 "-" 字串
        假如顯示幕上為負值, 則設法移除 display 上字串最前方的 "-" 字元
        '''
        text = self.display.text()
        value = float(text)
 
        if value > 0.0:
            text = "-" + text
        elif value < 0.0:
            text = text[1:]
 
        self.display.setText(text)
            
    def backspaceClicked(self):
        '''回復鍵按下的處理方法'''
        #pass
        '''
        按下退格按鍵後, 由 backspaceClicked() 處理, 這時可以利用 Python 字串數列中的 [:-1], 保留除了最後一個字元的字串
        離開 backspaceClicked() 前 ,將顯示幕中原有字串的 [:-1] 字串, 顯示在 display 上
        若退格後 display 上為空字串, 則顯示 0, 並且將 waitingForOperand 起始設為 True, 表示等待新運算數中
        '''
        if self.waitingForOperand:
            return
     
        text = self.display.text()[:-1]
        if not text:
            text = '0'
            self.waitingForOperand = True
        
        self.display.setText(text)
        
    def clear(self):
        '''清除鍵按下後的處理方法'''
        #pass
        '''
        按下 Clear 按鍵後, 以 clear() 方法處理, 進入函式後, 將現有的運算數重置為 0
        離開 clear() 前, 將 waitingForOperand 起始設為 True, 表示等待新運算數中
        '''
        self.display.setText('0')
        self.waitingForOperand = True
        
    def clearAll(self):
        '''全部清除鍵按下後的處理方法'''
        #pass
        '''
        將所有變數全部重置為起始狀態
        '''
        self.sumSoFar =0.0
        self.factorSoFar =0.0
        self.pendingAdditiveOperator=''
        self.pendingMultiplicativeOperator=''
        self.display.setText('0')
        self.waitingForOperand = True
        
    def clearMemory(self):
        '''清除記憶體鍵按下後的處理方法'''
        #pass
        '''
        與 "MC" 按鍵對應, 清除記憶體中所存 sumInMemory 設為 0
        '''
        self.sumInMemory = 0.0
        
    def readMemory(self):
        '''讀取記憶體鍵按下後的處理方法'''
        #pass
        '''
        與 "MR" 按鍵對應, 功能為讀取記憶體中的數值, 將 sumInMemory 顯示在 display, 作為運算數
        '''
        self.display.setText(str(self.sumInMemory))
        self.waitingForOperand = True
        
    def setMemory(self):
        '''設定記憶體鍵按下後的處理方法'''
        #pass
        '''
        與 "MS" 按鍵對應, 功能為設定記憶體中的數值，取 display 中的數字, 存入 sumInMemory
        setMemory() 與 addToMemory() 方法, 都需要取用 display 上的數值, 必須先呼叫 equalClicked(), 以更新 sumSoFar 與 display 上的數值
        '''
        self.equalClicked()
        self.sumInMemory = float(self.display.text())
        
    def addToMemory(self):
        '''放到記憶體鍵按下後的處理方法'''
       # pass
        '''
        與 "M+" 按鍵對應, 功能為加上記憶體中的數值, 將 sumInMemory 加上 display 中的數值
        setMemory() 與 addToMemory() 方法, 都需要取用 display 上的數值, 必須先呼叫 equalClicked(), 以更新 sumSoFar 與 display 上的數值
        '''
        self.equalClicked()
        self.sumInMemory += float(self.display.text())
        
    def createButton(self):
        ''' 建立按鍵處理方法, 以 Qt Designer 建立對話框時, 不需要此方法'''
        pass
        
    def abortOperation(self):
        '''中斷運算'''
        #pass
        '''
        重置所有起始變數, 並在 display 中顯示 "####"
        '''
        self.clearAll()
        self.display.setText("####")
        
    def calculate(self, rightOperand, pendingOperator):
        '''計算'''
        #pass
        '''
        運算以 rightOperand 為右運算數
        當執行加或減運算時, 左運算數為 sumSoFar
        當執行乘或除運算時, 左運算數為 factorSoFar
        若運算過程出現除與 0 時, 將會回傳 False
        '''
        if pendingOperator == "+":
            self.sumSoFar += rightOperand
        elif pendingOperator == "-":
            self.sumSoFar -= rightOperand
        elif pendingOperator == "*":
            self.factorSoFar *= rightOperand
        elif pendingOperator == "/":
            if rightOperand == 0.0:
                return False

            self.factorSoFar /= rightOperand

        return True
