'''
    Category Annotate with GUI.
'''

import os
import sys
import shutil
import html
import numpy as np
import pandas as pd
try:
    import PyQt5
except:
    os.system('pip install PyQt5')
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui  import QFont
from PyQt5.QtCore import Qt

# global path.
rootPath = './'
candiPath = rootPath + '/candidates/'
tempPath = rootPath + '/temp_judged/'
judFile = tempPath + '/judge.csv'
judPosPath = tempPath + '/positives/'
judNegPath = tempPath + '/negatives/'
# global size
ScrW, ScrH = 2560, 1440
WinW, WinH = 2200, 1200 # WinW=TxtInt+TxtW+2*BtnInt+BtnW
TxtInt = 25
BoxW, BoxH = 5 * TxtInt, 35
TxtFont = 22
TxtW, TxtH = 1600, (WinH - 3 * TxtInt - BoxH)
BtnInt = 50
BtnGap = 40
BtnW, BtnH = 200, 40
WinW = TxtInt + TxtW + 2 * BtnInt + BtnW
EyeCare = 0
DiffColor = 0

# class Example
class Annotation(QWidget):
    def __init__(self):
        super(Annotation, self).__init__()
        # variable.
        self.df = PreProcess()
        self.filename = ''
        self.index = 0
        # main window.
        self.setWindowTitle("Security Patch Annotation GUI Version 1.0")
        self.move(int((ScrW-WinW)/2), int((ScrH-WinH)/2))
        self.setFixedSize(WinW, WinH)
        self.InitUI()

    def InitUI(self):
        # Text Box
        self.textbox = QTextBrowser(self)
        self.textbox.move(TxtInt, TxtInt)
        self.textbox.resize(TxtW, TxtH)
        self.textbox.setFont(QFont("Consolas", TxtFont))
        self.index, self.filename = self.FindNext()
        # index box
        self.indexbox = QTextBrowser(self)
        self.indexbox.move(TxtInt, WinH - TxtInt - BoxH)
        self.indexbox.resize(BoxW, BoxH)
        self.indexbox.setFont(QFont("Consolas", 14))
        # filename box
        self.fnamebox = QTextBrowser(self)
        self.fnamebox.move(2 * TxtInt + BoxW, WinH - TxtInt - BoxH)
        self.fnamebox.resize(TxtW - TxtInt - BoxW, BoxH)
        self.fnamebox.setFont(QFont("Consolas", 14))
        self.UpdateScreen()

        # SP-NSP Labeling
        self.lb2 = QLabel(self)
        self.lb2.move(TxtInt + TxtW + BtnInt, TxtInt)
        self.lb2.resize(BtnW, BtnH)
        self.lb2.setText("Select Patch Annotation")
        self.lb2.setStyleSheet("font: 14pt;")
        self.lb2.setAlignment(Qt.AlignCenter)
        # Button-Security Patch
        self.btn1 = QPushButton("Security Patch", self)
        self.btn1.move(TxtInt + TxtW + BtnInt, 2 * TxtInt + BtnH)
        self.btn1.resize(BtnW, BtnH)
        self.btn1.setStyleSheet("font: 14pt; color: rgb(204, 51, 0);")
        self.btn1.clicked.connect(self.SecPatchButton)
        # Button-Non-Security Patch
        self.btn0 = QPushButton("Non-Security Patch", self)
        self.btn0.move(TxtInt + TxtW + BtnInt, 2 * TxtInt + 2 * BtnH + BtnGap)
        self.btn0.resize(BtnW, BtnH)
        self.btn0.setStyleSheet("font: 14pt; color: rgb(51, 150, 0);")
        self.btn0.clicked.connect(self.NonSecPatchButton)

        # Important Operation
        self.lb3 = QLabel(self)
        self.lb3.move(TxtInt + TxtW + BtnInt, 7 * TxtInt + 3 * BtnH + BtnGap)
        self.lb3.resize(BtnW, BtnH)
        self.lb3.setText("Auxiliary Operation")
        self.lb3.setStyleSheet("font: 14pt;")
        self.lb3.setAlignment(Qt.AlignCenter)
        # Button-Find a Patch
        self.btnP1 = QPushButton("Re-label A Patch", self)
        self.btnP1.move(TxtInt + TxtW + BtnInt, 8 * TxtInt + 4 * BtnH + BtnGap)
        self.btnP1.resize(BtnW, BtnH)
        self.btnP1.setStyleSheet("font: 14pt;")
        self.btnP1.clicked.connect(self.SkipToPatch)
        # Button-Auto File
        self.btnP1 = QPushButton("Auto File Storage", self)
        self.btnP1.move(TxtInt + TxtW + BtnInt, 8 * TxtInt + 5 * BtnH + 2 * BtnGap)
        self.btnP1.resize(BtnW, BtnH)
        self.btnP1.setStyleSheet("font: 14pt;")
        self.btnP1.clicked.connect(self.FileStorage)

        # Setting
        self.lb3 = QLabel(self)
        self.lb3.move(TxtInt + TxtW + BtnInt, WinH - 4 * TxtInt - 5 * BtnH)
        self.lb3.resize(BtnW, BtnH)
        self.lb3.setText("Setting Preferences")
        self.lb3.setStyleSheet("font: 14pt;")
        self.lb3.setAlignment(Qt.AlignCenter)
        # Button-
        self.btnS1 = QPushButton("Change Font Size", self)
        self.btnS1.move(TxtInt + TxtW + BtnInt, WinH - 3 * TxtInt - 4 * BtnH)
        self.btnS1.resize(BtnW, BtnH)
        self.btnS1.setStyleSheet("font: 14pt;")
        self.btnS1.clicked.connect(self.ChangeFontSize)
        # Button
        self.btnS2 = QPushButton("Eye-Care Mode", self)
        self.btnS2.move(TxtInt + TxtW + BtnInt, WinH - 2 * TxtInt - 3 * BtnH)
        self.btnS2.resize(BtnW, BtnH)
        self.btnS2.setStyleSheet("font: 14pt;")
        self.btnS2.clicked.connect(self.EyeCareMode)
        # self.EyeCareMode() # default for eye-care
        # Button
        self.btnS3 = QPushButton("Show Diff Color", self)
        self.btnS3.move(TxtInt + TxtW + BtnInt, WinH - TxtInt - 2 * BtnH)
        self.btnS3.resize(BtnW, BtnH)
        self.btnS3.setStyleSheet("font: 14pt;")
        self.btnS3.clicked.connect(self.DiffColor)
        # show
        self.show()

    def FindNext(self):
        for ind in range(len(self.df)):
            if -1 == self.df.loc[ind, 'label']:
                return ind, self.df.loc[ind, 'filename']
        return -1, 'none'

    def UpdateScreen(self):
        if -1 == self.index:
            text = 'All data has been labeled.\n\n[Developed by Shu W.]'
            self.textbox.setText(text)
            self.indexbox.setText('N/A')
            self.fnamebox.setText(str(self.filename))
        else:
            # update textbox
            self.textbox.clear()
            fp = open(os.path.join(candiPath, self.filename), errors='ignore')
            lines = fp.readlines()
            if 0 == DiffColor:  # close all diff color.
                for line in lines:  # for each line.
                    line = html.escape(line)
                    line = line.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
                    line = line.replace(" ", "&nbsp;")
                    self.textbox.append('<html style="color:black;">{}<\html>'.format(line))
            elif 1 == DiffColor:  # open all diff color.
                for line in lines:  # for each line.
                    line = html.escape(line)
                    line = line.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
                    line = line.replace(" ", "&nbsp;")
                    if '+' == line[0]:
                        self.textbox.append('<html style="color:rgb(0,100,0);background-color:rgb(172,242,189);font-weight:bold;">{}<\html>'.format(line))
                        #self.textbox.append('<html style="color:rgb(0,153,0);">{}<\html>'.format(line))
                    elif '-' == line[0]:
                        self.textbox.append('<html style="color:rgb(150,0,0);background-color:rgb(253,184,192);font-weight:bold;">{}<\html>'.format(line))
                        #self.textbox.append('<html style="color:rgb(204,0,0);">{}<\html>'.format(line))
                    elif '@@' == line[0:2]:
                        self.textbox.append('<html style="color:rgb(200,0,220);font-weight:bold;">{}<\html>'.format(line))
                    else:
                        self.textbox.append('<html style="color:black;">{}<\html>'.format(line))
            self.textbox.moveCursor(1)
            # update index and filename.
            self.indexbox.setText(str(self.index) + '/' + str(len(self.df)))
            self.fnamebox.setText(str(self.filename))
        return

    def SecPatchButton(self):
        # change label and save to csv.
        if self.index >= 0:
            self.df.loc[self.index, 'label'] = 1
            self.df.to_csv(judFile)
        # change variable status.
        self.index, self.filename = self.FindNext()
        # change screen status,
        self.UpdateScreen()
        return

    def NonSecPatchButton(self):
        # change label and save to csv.
        if self.index >= 0:
            self.df.loc[self.index, 'label'] = 0
            self.df.to_csv(judFile)
        # change variable status.
        self.index, self.filename = self.FindNext()
        # change screen status,
        self.UpdateScreen()
        return

    def SkipToPatch(self):
        initValue = (len(self.df) - 1) if self.index < 0 else self.index
        item, ok = QInputDialog.getInt(self, 'Skip to a patch', '<html style="font-size:10pt;">Select Patch Number:<\html>',
                                         value = initValue, min = 0, max = len(self.df) - 1, step = 1)
        if ok:
            self.df.loc[item, 'label'] = -1
            self.df.to_csv(judFile)
            self.index = item
            self.filename = self.df.loc[self.index, 'filename']
            self.UpdateScreen()
        return

    def FileStorage(self):
        if os.path.exists(judPosPath):
            shutil.rmtree(judPosPath)
        os.mkdir(judPosPath)
        if os.path.exists(judNegPath):
            shutil.rmtree(judNegPath)
        os.mkdir(judNegPath)
        # find files.
        for ind in range(len(self.df)):
            label = self.df.loc[ind, 'label']
            if label >= 0:
                fname = self.df.loc[ind, 'filename']
                fpath = os.path.join(candiPath, fname)
                dest = judPosPath if 1 == label else judNegPath
                if os.path.exists(fpath):
                    shutil.copy(fpath, dest)
        QMessageBox.information(self, 'Info', 'Successfully Store All Patch Files!', QMessageBox.Yes)
        return

    def ChangeFontSize(self):
        global TxtFont
        item, ok = QInputDialog().getInt(self, 'Font Setting', '<html style="font-size:10pt;">Font Size:<\html>',
                                         value = TxtFont, min = 8, max = 30, step = 1)
        if ok:
            TxtFont = int(item)
            self.textbox.setFont(QFont("Consolas", TxtFont))
            self.UpdateScreen()
        return

    def EyeCareMode(self):
        global EyeCare
        if 0 == EyeCare:
            self.textbox.setStyleSheet("background-color: rgb(227, 237, 205);")
            self.indexbox.setStyleSheet("background-color: rgb(227, 237, 205);")
            self.fnamebox.setStyleSheet("background-color: rgb(227, 237, 205);")
            self.btnS2.setText('Nomarl Mode')
            EyeCare = 1
        elif 1 == EyeCare:
            self.textbox.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.indexbox.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.fnamebox.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.btnS2.setText('Eye-Care Mode')
            EyeCare = 0
        return

    def DiffColor(self):
        global DiffColor
        if 0 == DiffColor:
            self.btnS3.setText('Close Diff Color')
            DiffColor = 1
        elif 1 == DiffColor:
            self.btnS3.setText('Show Diff Color')
            DiffColor = 0
        self.UpdateScreen()
        return

def PreProcess():
    # path validation.
    if not os.path.exists(candiPath):
        print('[Error] Cannot find candidate path: ' + candiPath)
        return
    if not os.path.exists(tempPath):
        os.mkdir(tempPath)
    if not os.path.exists(judPosPath):
        os.mkdir(judPosPath)
    if not os.path.exists(judNegPath):
        os.mkdir(judNegPath)
    # file validation.
    df = pd.DataFrame()
    if not os.path.exists(judFile):
        # get file name.
        filename = [file for root, dirs, files in os.walk(candiPath) for file in files]
        df['filename'] = filename
        # get init label.
        numFile = len(df)
        label = -1 * np.ones(numFile)
        df['label'] = label.astype(int)
        # save to csv file.
        df.to_csv(judFile)
        print('[Info] Create data file to ' + judFile)
    else:
        # get hist file.
        df = pd.read_csv(judFile, usecols=['filename', 'label'])
        origLen = len(df)
        # get file name.
        filename = [file for root, dirs, files in os.walk(candiPath) for file in files]
        for file in filename:
            if file not in df['filename'].tolist():
                df.loc[len(df)] = {'filename': file, 'label': -1}
        # save to csv file.
        if origLen != len(df):
            df.to_csv(judFile)
            print('[Info] Update data file to ' + judFile)
    return df

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Annotation()
    sys.exit(app.exec_())
