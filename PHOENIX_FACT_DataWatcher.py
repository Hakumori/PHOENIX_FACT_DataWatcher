#pyinstaller DriectoryObserver.py --onefile --noconsole
#pyinstaller --exclude-module numpy --exclude-module pandas --exclude-module altgraph --exclude-module matplotlib --onefile --noconsole PHOENIX_FACT_DataWatcher.py
#pyinstaller --exclude-module altgraph --onefile --noconsole DriectoryObserver.py
import DataCulc
import tkinter #GUIライブラリ
from tkinter import messagebox
import threading
import time
import os
import csv
import datetime
import configparser
import logging
from logging import INFO,DEBUG,NOTSET
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


DIR_WATCH = str()
PATTERNS = str()

class fileObserve:
    def file_check(self):   #ファイルパスおよびファイル格納先のフォルダパスチェック iniファイルを参照
        global DIR_WATCH
        global PATTERNS
        global FILENAME
        
        inifile = configparser.ConfigParser()
        inifile.read(R'DatSavePath.ini',encoding="utf-8_sig")                     #iniファイル読み込み
        FILEPATH = inifile['SAVEDATImfo'][str(0)]
        MODELNAME = inifile['SAVEDATImfo'][str(1)]
        COMMONFILENAME = inifile['SAVEDATImfo'][str(2)]
        
        dt_now = datetime.datetime.now()
        YEAR = str(dt_now.year)
        MONTH = str(dt_now.month)
        if dt_now.month < 10:
            MONTH = '0' + MONTH
        DATE = str(dt_now.day)
        if dt_now.day < 10:
            DATE = '0' + DATE
        DIR_WATCH = FILEPATH + '\\' + MODELNAME
        FULLPATH =  FILEPATH + '\\' + MODELNAME + '\\' + YEAR + '\\' + MONTH + '\\' + DATE
        PATTERNS = ['*.csv']
        FILENAME = YEAR+MONTH+DATE+'_'+MODELNAME+'_'+COMMONFILENAME
        a=os.path.exists(os.path.join(FULLPATH,FILENAME))
        #print(a)
        os.makedirs(DIR_WATCH,exist_ok=True)
        
    def LogChecker(self):          #ファイル/フォルダの更新を監視
        global observer

        FileCheck.file_check()

        logging.basicConfig(level=logging.INFO,format='%(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        event_handler = LoggingEventHandler()
        observer = Observer()
        #observer.stop()
        observer.schedule(event_handler,DIR_WATCH,recursive=True)
        observer.start()

        time.sleep(2)

    def LoggingStop(self):
        observer.stop()


FileCheck = fileObserve()

def Data_Sampling(path,n):  #csvファイルの最終行データを抜き取り
    with open(path) as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        
        return [list(map(str,row)) for row in rows[-n:]]
    
class LoggingEventHandler(LoggingEventHandler):     #ファイル/フォルダの更新で得られたlogより、ファイルパスを得る
    def on_modified(self,event):
        global FILEMODEL
        filepath = event.src_path
        filename = os.path.basename(filepath)
        u=filename.find('VX')
        FILEMODEL=filename[u:u+6]
        #print(FILEMODEL)
        
        if filename[len(filename) - 4:] == '.csv':
            #print(filename)
            SamplingDat = Data_Sampling(filepath,1)
            #print(SamplingDat[0])
            DataDisp(SamplingDat)

    def on_created(self,event):
        filepath = event.src_path
        filename = os.path.basename(filepath)    
        #print('%s created' % filename)

def DataDisp(Data):         #各種データをテキストボックスに表示
    global Date
    global Serial

    errflag = 0
    OKNG=0
    colors=[]
    EntryDelete()
    
    AllData = str()
    AllData = Data[00]
    for i in range(len(AllData)):
        if AllData[i] == '':
            AllData[i] = 'ffffffff'
            
        
    #print("GUIData : " + AllData[0])

    Model['text'] = FILEMODEL
    Date['text'] = AllData[0]
    Serial['text'] = AllData[1]
    
    colors = []
    stroke,errcode,colors,OKNG = DataCulc.DatChange_Stroke(AllData)
    Mrpulasedat.insert(tkinter.END,stroke)
    Mrpulasedat['bg'] = colors[0]
    ErrCodeStrdat.insert(tkinter.END,errcode)
    ErrCodeStrdat['bg'] = colors[1]
    errflag += OKNG 
    
    colors = []
    mr_max_a,mr_min_a,mr_fluct_a,mr_max_b,mr_min_b,mr_fluct_b,mr_dist_far,mr_dist_mid,mr_dist_near,errcode,colors,OKNG = DataCulc.DatChange_MRSensor(AllData)
    MrampmaxdatA.insert(tkinter.END,mr_max_a)
    MrampmaxdatA['bg'] = colors[0]
    MrampmindatA.insert(tkinter.END,mr_min_a)
    MrampmindatA['bg'] = colors[1]
    MrfluctratiodatA.insert(tkinter.END,mr_fluct_a)
    MrfluctratiodatA['bg'] = colors[2]
    MrampmaxdatB.insert(tkinter.END,mr_max_b)
    MrampmaxdatB['bg'] = colors[3]
    MrampmindatB.insert(tkinter.END,mr_min_b)
    MrampmindatB['bg'] = colors[4]
    MrfluctratiodatB.insert(tkinter.END,mr_fluct_b)
    MrfluctratiodatB['bg'] = colors[5]
    MrDistFardat.insert(tkinter.END,mr_dist_far)
    MrDistFardat['bg'] = colors[6]
    MrDistMiddat.insert(tkinter.END,mr_dist_mid)
    MrDistMiddat['bg'] = colors[7]
    MrDistNeardat.insert(tkinter.END,mr_dist_near)
    MrDistNeardat['bg'] = colors[8]
    ErrCodeMRdat.insert(tkinter.END,errcode)
    ErrCodeMRdat['bg'] = colors[9]
    errflag += OKNG 
    
    colors = []
    rst_to_far,rst_to_near,full_strk,pi_out_far,pi_out_near,errcode,colors,OKNG = DataCulc.DatChange_PiStroke(AllData)
    StrkRstFardat.insert(tkinter.END,rst_to_far)
    StrkRstFardat['bg'] = colors[0]
    StrkRstNeardat.insert(tkinter.END,rst_to_near)
    StrkRstNeardat['bg'] = colors[1]
    StrkRstFulldat.insert(tkinter.END,full_strk)
    StrkRstFulldat['bg'] = colors[2]
    PiOutFardat.insert(tkinter.END,pi_out_far)
    PiOutFardat['bg'] = colors[3]
    PiOutNeardat.insert(tkinter.END,pi_out_near)
    PiOutNeardat['bg'] = colors[4]
    ErrCodePidat.insert(tkinter.END,errcode)
    ErrCodePidat['bg'] = colors[5]
    errflag += OKNG 
    
    colors = []
    startingload_coef,startingload_amp,errcode,colors,OKNG = DataCulc.DatChange_StartingLoad(AllData)
    SlCoefdat.insert(tkinter.END,startingload_coef)
    SlCoefdat['bg'] = colors[0]
    SlAmpdat.insert(tkinter.END,startingload_amp)
    SlAmpdat['bg'] = colors[1]
    ErrCodeSldat.insert(tkinter.END,errcode)
    ErrCodeSldat['bg'] = colors[2]
    errflag += OKNG 

    colors = []
    inststart1,instend1,mv0251,delay1001,err1501,settmax1,settmin1,settling1,errcode,colors,OKNG = DataCulc.DatChange_Settling1(AllData)
    Set1InstStartdat.insert(tkinter.END,inststart1)
    Set1InstStartdat['bg'] = colors[0]
    Set1InstEnddat.insert(tkinter.END,instend1)
    Set1InstEnddat['bg'] = colors[1]
    Set1ActMv025dat.insert(tkinter.END,mv0251)
    Set1ActMv025dat['bg'] = colors[2]
    Set1ActDelay100dat.insert(tkinter.END,delay1001)
    Set1ActDelay100dat['bg'] = colors[3]
    Set1ActErr150dat.insert(tkinter.END,err1501)
    Set1ActErr150dat['bg'] = colors[4]
    Set1ActSettlingMaxdat.insert(tkinter.END,settmax1)
    Set1ActSettlingMaxdat['bg'] = colors[5]
    Set1ActSettlingMindat.insert(tkinter.END,settmin1)
    Set1ActSettlingMindat['bg'] = colors[6]
    Set1ActSettlingdat.insert(tkinter.END,settling1)
    Set1ActSettlingdat['bg'] = colors[7]
    ErrCodeSettling1dat.insert(tkinter.END,errcode)
    ErrCodeSettling1dat['bg'] = colors[8]
    errflag += OKNG 

    colors = []
    inststart2,instend2,mv0252,delay1002,err1502,settmax2,settmin2,settling2,errcode,colors,OKNG = DataCulc.DatChange_Settling2(AllData)
    Set2InstStartdat.insert(tkinter.END,inststart2)
    Set2InstStartdat['bg'] = colors[0]
    Set2InstEnddat.insert(tkinter.END,instend2)
    Set2InstEnddat['bg'] = colors[1]
    Set2ActMv025dat.insert(tkinter.END,mv0252)
    Set2ActMv025dat['bg'] = colors[2]
    Set2ActDelay100dat.insert(tkinter.END,delay1002)
    Set2ActDelay100dat['bg'] = colors[3]
    Set2ActErr150dat.insert(tkinter.END,err1502)
    Set2ActErr150dat['bg'] = colors[4]
    Set2ActSettlingMaxdat.insert(tkinter.END,settmax2)
    Set2ActSettlingMaxdat['bg'] = colors[5]
    Set2ActSettlingMindat.insert(tkinter.END,settmin2)
    Set2ActSettlingMindat['bg'] = colors[6]
    Set2ActSettlingdat.insert(tkinter.END,settling2)
    Set2ActSettlingdat['bg'] = colors[7]
    ErrCodeSettling2dat.insert(tkinter.END,errcode)
    ErrCodeSettling2dat['bg'] = colors[8]
    errflag += OKNG 

    colors = []
    startupA,startupB,overshootA,overshootB,ampmidA,ampmidB,ampend,rate1,rate2,rate3,rate4,rate5,rate6,errcode,colors,OKNG = DataCulc.DatChange_Wobbling(AllData)
    WobStartUpAdat.insert(tkinter.END,startupA)
    WobStartUpAdat['bg'] = colors[0]
    WobStartUpBdat.insert(tkinter.END,startupB)
    WobStartUpBdat['bg'] = colors[1]
    WobOverShootAdat.insert(tkinter.END,overshootA)
    WobOverShootAdat['bg'] = colors[2]
    WobOverShootBdat.insert(tkinter.END,overshootB)
    WobOverShootBdat['bg'] = colors[3]
    WobAmpMidAdat.insert(tkinter.END,ampmidA)
    WobAmpMidAdat['bg'] = colors[4]
    WobAmpMidBdat.insert(tkinter.END,ampmidB)
    WobAmpMidBdat['bg'] = colors[5]
    WobAmpEnddat.insert(tkinter.END,ampend)
    WobAmpEnddat['bg'] = colors[6]
    WobRate1dat.insert(tkinter.END,rate1)
    WobRate1dat['bg'] = colors[8]
    WobRate2dat.insert(tkinter.END,rate2)
    WobRate2dat['bg'] = colors[9]
    WobRate3dat.insert(tkinter.END,rate3)
    WobRate3dat['bg'] = colors[10]
    WobRate4dat.insert(tkinter.END,rate4)
    WobRate4dat['bg'] = colors[11]
    WobRate5dat.insert(tkinter.END,rate5)
    WobRate5dat['bg'] = colors[12]
    WobRate6dat.insert(tkinter.END,rate6)
    WobRate6dat['bg'] = colors[13]
    ErrCodeWobblingdat.insert(tkinter.END,errcode)
    ErrCodeWobblingdat['bg'] = colors[7]
    errflag += OKNG 

    delay,advance,errcode,colors,OKNG = DataCulc.DatChange_Delay(AllData)
    DelayDelaydat.insert(tkinter.END,delay)
    DelayDelaydat['bg'] = colors[0]
    DelayAdvancedat.insert(tkinter.END,advance)
    DelayAdvancedat['bg'] = colors[1]
    ErrCodeDelaydat.insert(tkinter.END,errcode)
    ErrCodeDelaydat['bg'] = colors[2]
    errflag += OKNG 
    
    if errflag ==0:
        AllDataChk.insert(tkinter.END,'OK')
        AllDataChk['bg'] = '#ffffff'
    else:
        AllDataChk.insert(tkinter.END,'NG')
        AllDataChk['bg'] = '#ff0000'

def EntryDelete():
    Date['text'] = ""
    Serial['text'] = ""
    AllDataChk.delete(0,tkinter.END)
    AllDataChk['bg'] = '#ffffff'
    Mrpulasedat.delete(0,tkinter.END)
    Mrpulasedat['bg'] = '#ffffff'
    ErrCodeStrdat.delete(0,tkinter.END)
    ErrCodeStrdat['bg'] = '#ffffff'
    MrampmaxdatA.delete(0,tkinter.END)
    MrampmaxdatA['bg'] = '#ffffff'
    MrampmindatA.delete(0,tkinter.END)
    MrampmindatA['bg'] = '#ffffff'
    MrfluctratiodatA.delete(0,tkinter.END)
    MrfluctratiodatA['bg'] = '#ffffff'
    MrampmaxdatB.delete(0,tkinter.END)
    MrampmaxdatB['bg'] = '#ffffff'
    MrampmindatB.delete(0,tkinter.END)
    MrampmindatB['bg'] = '#ffffff'
    MrfluctratiodatB.delete(0,tkinter.END)
    MrfluctratiodatB['bg'] = '#ffffff'
    MrDistFardat.delete(0,tkinter.END)
    MrDistFardat['bg'] = '#ffffff'
    MrDistMiddat.delete(0,tkinter.END)
    MrDistMiddat['bg'] = '#ffffff'    
    MrDistNeardat.delete(0,tkinter.END)
    MrDistNeardat['bg'] = '#ffffff'
    ErrCodeMRdat.delete(0,tkinter.END)
    ErrCodeMRdat['bg'] = '#ffffff'
    StrkRstFardat.delete(0,tkinter.END)
    StrkRstFardat['bg'] = '#ffffff'
    StrkRstNeardat.delete(0,tkinter.END)
    StrkRstNeardat['bg'] = '#ffffff'
    StrkRstFulldat.delete(0,tkinter.END)
    StrkRstFulldat['bg'] = '#ffffff'
    PiOutFardat.delete(0,tkinter.END)
    PiOutFardat['bg'] = '#ffffff'
    PiOutNeardat.delete(0,tkinter.END)
    PiOutNeardat['bg'] = '#ffffff'
    ErrCodePidat.delete(0,tkinter.END)
    ErrCodePidat['bg'] = '#ffffff'
    SlCoefdat.delete(0,tkinter.END)
    SlCoefdat['bg'] = '#ffffff'
    SlAmpdat.delete(0,tkinter.END)
    SlAmpdat['bg'] = '#ffffff'
    ErrCodeSldat.delete(0,tkinter.END)
    ErrCodeSldat['bg'] = '#ffffff'
    Set1InstStartdat.delete(0,tkinter.END)
    Set1InstStartdat['bg'] = '#ffffff'
    Set1InstEnddat.delete(0,tkinter.END)
    Set1InstEnddat['bg'] = '#ffffff'
    Set1ActMv025dat.delete(0,tkinter.END)
    Set1ActMv025dat['bg'] = '#ffffff'
    Set1ActDelay100dat.delete(0,tkinter.END)
    Set1ActDelay100dat['bg'] = '#ffffff'
    Set1ActErr150dat.delete(0,tkinter.END)
    Set1ActErr150dat['bg'] = '#ffffff'
    Set1ActSettlingMaxdat.delete(0,tkinter.END)
    Set1ActSettlingMaxdat['bg'] = '#ffffff'
    Set1ActSettlingMindat.delete(0,tkinter.END)
    Set1ActSettlingMindat['bg'] = '#ffffff'
    Set1ActSettlingdat.delete(0,tkinter.END)
    Set1ActSettlingdat['bg'] = '#ffffff'
    ErrCodeSettling1dat.delete(0,tkinter.END)
    ErrCodeSettling1dat['bg'] = '#ffffff'
    Set2InstStartdat.delete(0,tkinter.END)
    Set2InstStartdat['bg'] = '#ffffff'
    Set2InstEnddat.delete(0,tkinter.END)
    Set2InstEnddat['bg'] = '#ffffff'
    Set2ActMv025dat.delete(0,tkinter.END)
    Set2ActMv025dat['bg'] = '#ffffff'
    Set2ActDelay100dat.delete(0,tkinter.END)
    Set2ActDelay100dat['bg'] = '#ffffff'
    Set2ActErr150dat.delete(0,tkinter.END)
    Set2ActErr150dat['bg'] = '#ffffff'
    Set2ActSettlingMaxdat.delete(0,tkinter.END)
    Set2ActSettlingMaxdat['bg'] = '#ffffff'
    Set2ActSettlingMindat.delete(0,tkinter.END)
    Set2ActSettlingMindat['bg'] = '#ffffff'
    Set2ActSettlingdat.delete(0,tkinter.END)
    Set2ActSettlingdat['bg'] = '#ffffff'
    ErrCodeSettling2dat.delete(0,tkinter.END)
    ErrCodeSettling2dat['bg'] = '#ffffff'
    WobStartUpAdat.delete(0,tkinter.END)
    WobStartUpAdat['bg'] = '#ffffff'
    WobStartUpBdat.delete(0,tkinter.END)
    WobStartUpBdat['bg'] = '#ffffff'
    WobOverShootAdat.delete(0,tkinter.END)
    WobOverShootAdat['bg'] = '#ffffff'
    WobOverShootBdat.delete(0,tkinter.END)
    WobOverShootBdat['bg'] = '#ffffff'
    WobAmpMidAdat.delete(0,tkinter.END)
    WobAmpMidAdat['bg'] = '#ffffff'
    WobAmpMidBdat.delete(0,tkinter.END)
    WobAmpMidBdat['bg'] = '#ffffff'
    WobAmpEnddat.delete(0,tkinter.END)
    WobAmpEnddat['bg'] = '#ffffff'
    ErrCodeWobblingdat.delete(0,tkinter.END)
    ErrCodeWobblingdat['bg'] = '#ffffff'
    WobRate1dat.delete(0,tkinter.END)
    WobRate1dat['bg'] = '#ffffff'
    WobRate2dat.delete(0,tkinter.END)
    WobRate2dat['bg'] = '#ffffff'
    WobRate3dat.delete(0,tkinter.END)
    WobRate3dat['bg'] = '#ffffff'
    WobRate4dat.delete(0,tkinter.END)
    WobRate4dat['bg'] = '#ffffff'
    WobRate5dat.delete(0,tkinter.END)
    WobRate5dat['bg'] = '#ffffff'
    WobRate6dat.delete(0,tkinter.END)
    WobRate6dat['bg'] = '#ffffff'
    DelayDelaydat.delete(0,tkinter.END)
    DelayDelaydat['bg'] = '#ffffff'
    DelayAdvancedat.delete(0,tkinter.END)
    DelayAdvancedat['bg'] = '#ffffff'
    ErrCodeDelaydat.delete(0,tkinter.END)
    ErrCodeDelaydat['bg'] = '#ffffff'    

def main(): #スレッド
    thread1 = threading.Thread(target=FileCheck.LogChecker())
    thread1.start()
        
def click_close():
    if messagebox.askokcancel("","Quit the application."):
        root.destroy()
    
if __name__ == "__main__":
    print('GUI Start Up')
    main()

    try:
        root = tkinter.Tk()
        root.title("PHOENIX_FACT_DataWatcher") #GUIタイトル
        root.geometry("1500x680")        
        
        #ラベル
        Model = tkinter.Label(None,text = '',font=('Meiryo UI',20))
        Model.pack()
        Model.place(x=15,y=5)
        Date = tkinter.Label(None,text = '',font=('Meiryo UI',12))                                  #検査日時
        Date.pack()
        Date.place(x=135,y=15)
        Serial = tkinter.Label(None,text = '',font=('Meiryo UI',12))                                #シリアル
        Serial.pack()
        Serial.place(x=330,y=15)

        strk_y = 50
        Stroke = tkinter.Label(None,text = 'STROKE',font=('Meiryo UI',12))                          #メカストローク検査
        Stroke.pack()
        Stroke.place(x=10,y=strk_y+25)
        Mrpulase = tkinter.Label(None,text = 'MR_PULSE',font=('Meiryo UI',10))
        Mrpulase.pack()
        Mrpulase.place(x=150,y=strk_y)
        ErrCodeStr = tkinter.Label(None,text = 'ERR CODE',font=('Meiryo UI',10))
        ErrCodeStr.pack()
        ErrCodeStr.place(x=300,y=strk_y)

        mr_y = 110
        mr_y2 = 170
        MrSensor = tkinter.Label(None,text = 'MR0',font=('Meiryo UI',12))                           #MR検査
        MrSensor.pack()
        MrSensor.place(x=10,y=mr_y+25)
        MrAmpMaxA = tkinter.Label(None,text = 'AMP_MAX_A',font=('Meiryo UI',10))
        MrAmpMaxA.pack()
        MrAmpMaxA.place(x=150,y=mr_y)
        MrAmpMinA = tkinter.Label(None,text = 'AMP_MIN_A',font=('Meiryo UI',10))
        MrAmpMinA.pack()
        MrAmpMinA.place(x=300,y=mr_y)
        FlucratioA = tkinter.Label(None,text = 'FLUCT_RATIO_A',font=('Meiryo UI',10))
        FlucratioA.pack()
        FlucratioA.place(x=450,y=mr_y)
        MrAmpMaxB = tkinter.Label(None,text = 'AMP_MAX_B',font=('Meiryo UI',10))
        MrAmpMaxB.pack()
        MrAmpMaxB.place(x=600,y=mr_y)
        MrAmpMinB = tkinter.Label(None,text = 'AMP_MIN_B',font=('Meiryo UI',10))
        MrAmpMinB.pack()
        MrAmpMinB.place(x=750,y=mr_y)
        FlucratioB = tkinter.Label(None,text = 'FLUCT_RATIO_B',font=('Meiryo UI',10))
        FlucratioB.pack()
        FlucratioB.place(x=900,y=mr_y)
        MrDistFar = tkinter.Label(None,text = 'DIST_FAR',font=('Meiryo UI',10))
        MrDistFar.pack()
        MrDistFar.place(x=150,y=mr_y2)
        MrDistMid = tkinter.Label(None,text = 'DIST_MID',font=('Meiryo UI',10))
        MrDistMid.pack()
        MrDistMid.place(x=300,y=mr_y2)
        MrDistNear = tkinter.Label(None,text = 'DIST_NEAR',font=('Meiryo UI',10))
        MrDistNear.pack()
        MrDistNear.place(x=450,y=mr_y2)
        ErrCodeMR = tkinter.Label(None,text = 'ERR CODE',font=('Meiryo UI',10))
        ErrCodeMR.pack()
        ErrCodeMR.place(x=1050,y=mr_y)

        pi_y = 230
        StrokePI = tkinter.Label(None,text = 'STROKE/PI',font=('Meiryo UI',12))                     #PI検査
        StrokePI.pack()
        StrokePI.place(x=10,y=pi_y+25)
        StrokePiFar = tkinter.Label(None,text = 'STRK_RST-FAR',font=('Meiryo UI',10))
        StrokePiFar.pack()
        StrokePiFar.place(x=150,y=pi_y)
        StrokePiNear = tkinter.Label(None,text = 'STRK_RST-NEAR',font=('Meiryo UI',10))
        StrokePiNear.pack()
        StrokePiNear.place(x=300,y=pi_y)
        StrokePiFull = tkinter.Label(None,text = 'STRK_FULL',font=('Meiryo UI',10))
        StrokePiFull.pack()
        StrokePiFull.place(x=450,y=pi_y)
        PiOutFar = tkinter.Label(None,text = 'PI_OUT_FAR',font=('Meiryo UI',10))
        PiOutFar.pack()
        PiOutFar.place(x=600,y=pi_y)
        PiOutNear = tkinter.Label(None,text = 'PI_OUT_NEAR',font=('Meiryo UI',10))
        PiOutNear.pack()
        PiOutNear.place(x=750,y=pi_y)
        ErrCodePI = tkinter.Label(None,text = 'ERR CODE',font=('Meiryo UI',10))
        ErrCodePI.pack()
        ErrCodePI.place(x=900,y=pi_y)

        sl_y = 290
        StartlingLoad = tkinter.Label(None,text = 'STARTING LOAD',font=('Meiryo UI',11))            #起動負荷
        StartlingLoad.pack()
        StartlingLoad.place(x=10,y=sl_y+25)
        StatingLoadCoef = tkinter.Label(None,text = 'COEF',font=('Meiryo UI',10))
        StatingLoadCoef.pack()
        StatingLoadCoef.place(x=150,y=sl_y)
        StatingLoadActAmp = tkinter.Label(None,text = 'ACTUAL_AMP',font=('Meiryo UI',10))
        StatingLoadActAmp.pack()
        StatingLoadActAmp.place(x=300,y=sl_y)
        ErrCodeSL = tkinter.Label(None,text = 'ERR CODE',font=('Meiryo UI',10))
        ErrCodeSL.pack()
        ErrCodeSL.place(x=450,y=sl_y)
        
        sett1_y = 350
        Settling1 = tkinter.Label(None,text = 'SETTLING1',font=('Meiryo UI',12))                    #制定性1
        Settling1.pack()
        Settling1.place(x=10,y=sett1_y+25)
        Pos1_Inst_Start = tkinter.Label(None,text = 'INST_START',font=('Meiryo UI',10))
        Pos1_Inst_Start.pack()
        Pos1_Inst_Start.place(x=150,y=sett1_y)
        Pos1_Inst_End = tkinter.Label(None,text = 'INST_END',font=('Meiryo UI',10))
        Pos1_Inst_End.pack()
        Pos1_Inst_End.place(x=300,y=sett1_y)
        Pos1_Act_MV_025 = tkinter.Label(None,text = 'MOVE 1/4VD',font=('Meiryo UI',10))
        Pos1_Act_MV_025.pack()
        Pos1_Act_MV_025.place(x=450,y=sett1_y)
        Pos1_Act_Delay_100 = tkinter.Label(None,text = 'DELAY 1.0VD',font=('Meiryo UI',10))
        Pos1_Act_Delay_100.pack()
        Pos1_Act_Delay_100.place(x=600,y=sett1_y)
        Pos1_Act_Err_150 = tkinter.Label(None,text = 'ERROR 1.5VD',font=('Meiryo UI',10))
        Pos1_Act_Err_150.pack()
        Pos1_Act_Err_150.place(x=750,y=sett1_y)
        Pos1_Act_SETTLING_MAX = tkinter.Label(None,text = 'SETTLING_MAX',font=('Meiryo UI',9))
        Pos1_Act_SETTLING_MAX.pack()
        Pos1_Act_SETTLING_MAX.place(x=900,y=sett1_y)
        Pos1_Act_SETTLING_MIN = tkinter.Label(None,text = 'SETTLING_MIN',font=('Meiryo UI',9))
        Pos1_Act_SETTLING_MIN.pack()
        Pos1_Act_SETTLING_MIN.place(x=1050,y=sett1_y)
        Pos1_Act_SETTLING = tkinter.Label(None,text = 'SETTLING',font=('Meiryo UI',10))
        Pos1_Act_SETTLING.pack()
        Pos1_Act_SETTLING.place(x=1200,y=sett1_y)
        ErrCodeSettring1 = tkinter.Label(None,text = 'ERR CODE',font=('Meiryo UI',10))
        ErrCodeSettring1.pack()
        ErrCodeSettring1.place(x=1350,y=sett1_y)

        sett2_y = 410
        Settling2 = tkinter.Label(None,text = 'SETTLING2',font=('Meiryo UI',12))                    #制定性2
        Settling2.pack()
        Settling2.place(x=10,y=sett2_y+25)
        Pos2_Inst_Start = tkinter.Label(None,text = 'INST_START',font=('Meiryo UI',10))
        Pos2_Inst_Start.pack()
        Pos2_Inst_Start.place(x=150,y=sett2_y)
        Pos2_Inst_End = tkinter.Label(None,text = 'INST_END',font=('Meiryo UI',10))
        Pos2_Inst_End.pack()
        Pos2_Inst_End.place(x=300,y=sett2_y)
        Pos2_Act_MV_025 = tkinter.Label(None,text = 'MOVE 1/4VD',font=('Meiryo UI',10))
        Pos2_Act_MV_025.pack()
        Pos2_Act_MV_025.place(x=450,y=sett2_y)
        Pos2_Act_Delay_100 = tkinter.Label(None,text = 'DELAY 1.0VD',font=('Meiryo UI',10))
        Pos2_Act_Delay_100.pack()
        Pos2_Act_Delay_100.place(x=600,y=sett2_y)
        Pos2_Act_Err_150 = tkinter.Label(None,text = 'ERROR 1.5VD',font=('Meiryo UI',10))
        Pos2_Act_Err_150.pack()
        Pos2_Act_Err_150.place(x=750,y=sett2_y)
        Pos2_Act_SETTLING_MAX = tkinter.Label(None,text = 'SETTLING_MAX',font=('Meiryo UI',9))
        Pos2_Act_SETTLING_MAX.pack()
        Pos2_Act_SETTLING_MAX.place(x=900,y=sett2_y)
        Pos2_Act_SETTLING_MIN = tkinter.Label(None,text = 'SETTLING_MIN',font=('Meiryo UI',9))
        Pos2_Act_SETTLING_MIN.pack()
        Pos2_Act_SETTLING_MIN.place(x=1050,y=sett2_y)
        Pos2_Act_SETTLING = tkinter.Label(None,text = 'SETTLING',font=('Meiryo UI',10))
        Pos2_Act_SETTLING.pack()
        Pos2_Act_SETTLING.place(x=1200,y=sett2_y)
        ErrCodeSettring2 = tkinter.Label(None,text = 'ERR CODE',font=('Meiryo UI',10))
        ErrCodeSettring2.pack()
        ErrCodeSettring2.place(x=1350,y=sett2_y)

        wobb_y1 = 470
        wobb_y2 = 530
        Wobbling = tkinter.Label(None,text = 'WOBBLING',font=('Meiryo UI',12))                      #Wobbling
        Wobbling.pack()
        Wobbling.place(x=10,y=wobb_y1+25)
        WobStartUpA = tkinter.Label(None,text = 'START_UP A',font=('Meiryo UI',10))
        WobStartUpA.pack()
        WobStartUpA.place(x=150,y=wobb_y1)
        WobStartUpB = tkinter.Label(None,text = 'START_UP B',font=('Meiryo UI',10))
        WobStartUpB.pack()
        WobStartUpB.place(x=300,y=wobb_y1)
        WobOverShootA = tkinter.Label(None,text = 'OVER_SHOOT A',font=('Meiryo UI',10))
        WobOverShootA.pack()
        WobOverShootA.place(x=450,y=wobb_y1)
        WobOverShootB = tkinter.Label(None,text = 'OVER_SHOOT B',font=('Meiryo UI',10))
        WobOverShootB.pack()
        WobOverShootB.place(x=600,y=wobb_y1)
        WobAmpMidA = tkinter.Label(None,text = 'AMP_MID A',font=('Meiryo UI',10))
        WobAmpMidA.pack()
        WobAmpMidA.place(x=750,y=wobb_y1)
        WobAmpMidB = tkinter.Label(None,text = 'AMP_MID B',font=('Meiryo UI',9))
        WobAmpMidB.pack()
        WobAmpMidB.place(x=900,y=wobb_y1)
        WobAmpEnd = tkinter.Label(None,text = 'AMP_END',font=('Meiryo UI',9))
        WobAmpEnd.pack()
        WobAmpEnd.place(x=1050,y=wobb_y1)
        WobRate1 = tkinter.Label(None,text = 'RATE1',font=('Meiryo UI',10))
        WobRate1.pack()
        WobRate1.place(x=150,y=wobb_y2)
        WobRate2 = tkinter.Label(None,text = 'RATE2',font=('Meiryo UI',10))
        WobRate2.pack()
        WobRate2.place(x=300,y=wobb_y2)
        WobRate3 = tkinter.Label(None,text = 'RATE3',font=('Meiryo UI',10))
        WobRate3.pack()
        WobRate3.place(x=450,y=wobb_y2)
        WobRate4 = tkinter.Label(None,text = 'RATE4',font=('Meiryo UI',10))
        WobRate4.pack()
        WobRate4.place(x=600,y=wobb_y2)
        WobRate5 = tkinter.Label(None,text = 'RATE5',font=('Meiryo UI',10))
        WobRate5.pack()
        WobRate5.place(x=750,y=wobb_y2)
        WobRate6 = tkinter.Label(None,text = 'RATE6',font=('Meiryo UI',9))
        WobRate6.pack()
        WobRate6.place(x=900,y=wobb_y2)
        ErrCodeWobb = tkinter.Label(None,text = 'ERR CODE',font=('Meiryo UI',10))
        ErrCodeWobb.pack()
        ErrCodeWobb.place(x=1200,y=wobb_y1)

        delay_y = 590
        Delay = tkinter.Label(None,text = 'DELAY',font=('Meiryo UI',12))                            #遅れ,追従性
        Delay.pack()
        Delay.place(x=10,y=delay_y+25)
        DelayDelay = tkinter.Label(None,text = 'DELAY',font=('Meiryo UI',10))
        DelayDelay.pack()
        DelayDelay.place(x=150,y=delay_y)
        DelayAdvance = tkinter.Label(None,text = 'ADVANCE',font=('Meiryo UI',10))
        DelayAdvance.pack()
        DelayAdvance.place(x=300,y=delay_y)
        ErrCodeDelay = tkinter.Label(None,text = 'ERR CODE',font=('Meiryo UI',10))
        ErrCodeDelay.pack()
        ErrCodeDelay.place(x=450,y=delay_y)

        AllDataChk = tkinter.Entry(width=5,font=('Meiryo UI',24),justify="center")                                  #最終判定
        AllDataChk.pack()
        AllDataChk.place(x=1350,y=15,width=100,height=60)

        #データ表示用テキストボックス
        fonts = ('Meiryo UI',18)
        #メカストローク
        Mrpulasedat = tkinter.Entry(width=18,font=fonts,justify="center")
        Mrpulasedat.pack()
        Mrpulasedat.place(x=150,y=strk_y+25,width=100,height=30)
        ErrCodeStrdat = tkinter.Entry(width=18,font=fonts,justify="center")
        ErrCodeStrdat.pack()
        ErrCodeStrdat.place(x=300,y=strk_y+25,width=100,height=30)
        #MR出力
        MrampmaxdatA = tkinter.Entry(width=18,font=fonts,justify="center")
        MrampmaxdatA.pack()
        MrampmaxdatA.place(x=150,y=mr_y+25,width=100,height=30)
        MrampmindatA = tkinter.Entry(width=18,font=fonts,justify="center")
        MrampmindatA.pack()
        MrampmindatA.place(x=300,y=mr_y+25,width=100,height=30)
        MrfluctratiodatA = tkinter.Entry(width=18,font=fonts,justify="center")
        MrfluctratiodatA.pack()
        MrfluctratiodatA.place(x=450,y=mr_y+25,width=100,height=30)
        MrampmaxdatB = tkinter.Entry(width=18,font=fonts,justify="center")
        MrampmaxdatB.pack()
        MrampmaxdatB.place(x=600,y=mr_y+25,width=100,height=30)
        MrampmindatB = tkinter.Entry(width=18,font=fonts,justify="center")
        MrampmindatB.pack()
        MrampmindatB.place(x=750,y=mr_y+25,width=100,height=30)
        MrfluctratiodatB = tkinter.Entry(width=18,font=fonts,justify="center")
        MrfluctratiodatB.pack()
        MrfluctratiodatB.place(x=900,y=mr_y+25,width=100,height=30)
        MrDistFardat = tkinter.Entry(width=18,font=fonts,justify="center")
        MrDistFardat.pack()
        MrDistFardat.place(x=150,y=mr_y2+25,width=100,height=30)
        MrDistMiddat = tkinter.Entry(width=18,font=fonts,justify="center")
        MrDistMiddat.pack()
        MrDistMiddat.place(x=300,y=mr_y2+25,width=100,height=30)
        MrDistNeardat = tkinter.Entry(width=18,font=fonts,justify="center")
        MrDistNeardat.pack()
        MrDistNeardat.place(x=450,y=mr_y2+25,width=100,height=30)
        ErrCodeMRdat = tkinter.Entry(width=18,font=fonts,justify="center")
        ErrCodeMRdat.pack()
        ErrCodeMRdat.place(x=1050,y=mr_y+25,width=100,height=30)
        #PI/ストローク
        StrkRstFardat = tkinter.Entry(width=18,font=fonts,justify="center")
        StrkRstFardat.pack()
        StrkRstFardat.place(x=150,y=pi_y+25,width=100,height=30)
        StrkRstNeardat = tkinter.Entry(width=18,font=fonts,justify="center")
        StrkRstNeardat.pack()
        StrkRstNeardat.place(x=300,y=pi_y+25,width=100,height=30)
        StrkRstFulldat = tkinter.Entry(width=18,font=fonts,justify="center")
        StrkRstFulldat.pack()
        StrkRstFulldat.place(x=450,y=pi_y+25,width=100,height=30)
        PiOutFardat = tkinter.Entry(width=18,font=fonts,justify="center")
        PiOutFardat.pack()
        PiOutFardat.place(x=600,y=pi_y+25,width=100,height=30)
        PiOutNeardat = tkinter.Entry(width=18,font=fonts,justify="center")
        PiOutNeardat.pack()
        PiOutNeardat.place(x=750,y=pi_y+25,width=100,height=30)
        ErrCodePidat = tkinter.Entry(width=18,font=fonts,justify="center")
        ErrCodePidat.pack()
        ErrCodePidat.place(x=900,y=pi_y+25,width=100,height=30)
        #起動負荷
        SlCoefdat = tkinter.Entry(width=18,font=fonts,justify="center")
        SlCoefdat.pack()
        SlCoefdat.place(x=150,y=sl_y+25,width=100,height=30)
        SlAmpdat = tkinter.Entry(width=18,font=fonts,justify="center")
        SlAmpdat.pack()
        SlAmpdat.place(x=300,y=sl_y+25,width=100,height=30)
        ErrCodeSldat = tkinter.Entry(width=18,font=fonts,justify="center")
        ErrCodeSldat.pack()
        ErrCodeSldat.place(x=450,y=sl_y+25,width=100,height=30)
        #制定性1
        Set1InstStartdat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set1InstStartdat.pack()
        Set1InstStartdat.place(x=150,y=sett1_y+25,width=100,height=30)
        Set1InstEnddat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set1InstEnddat.pack()
        Set1InstEnddat.place(x=300,y=sett1_y+25,width=100,height=30)
        Set1ActMv025dat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set1ActMv025dat.pack()
        Set1ActMv025dat.place(x=450,y=sett1_y+25,width=100,height=30)
        Set1ActDelay100dat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set1ActDelay100dat.pack()
        Set1ActDelay100dat.place(x=600,y=sett1_y+25,width=100,height=30)
        Set1ActErr150dat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set1ActErr150dat.pack()
        Set1ActErr150dat.place(x=750,y=sett1_y+25,width=100,height=30)
        Set1ActSettlingMaxdat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set1ActSettlingMaxdat.pack()
        Set1ActSettlingMaxdat.place(x=900,y=sett1_y+25,width=100,height=30)
        Set1ActSettlingMindat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set1ActSettlingMindat.pack()
        Set1ActSettlingMindat.place(x=1050,y=sett1_y+25,width=100,height=30)
        Set1ActSettlingdat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set1ActSettlingdat.pack()
        Set1ActSettlingdat.place(x=1200,y=sett1_y+25,width=100,height=30)
        ErrCodeSettling1dat = tkinter.Entry(width=18,font=fonts,justify="center")
        ErrCodeSettling1dat.pack()
        ErrCodeSettling1dat.place(x=1350,y=sett1_y+25,width=100,height=30)
        #制定性2
        Set2InstStartdat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set2InstStartdat.pack()
        Set2InstStartdat.place(x=150,y=sett2_y+25,width=100,height=30)
        Set2InstEnddat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set2InstEnddat.pack()
        Set2InstEnddat.place(x=300,y=sett2_y+25,width=100,height=30)
        Set2ActMv025dat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set2ActMv025dat.pack()
        Set2ActMv025dat.place(x=450,y=sett2_y+25,width=100,height=30)
        Set2ActDelay100dat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set2ActDelay100dat.pack()
        Set2ActDelay100dat.place(x=600,y=sett2_y+25,width=100,height=30)
        Set2ActErr150dat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set2ActErr150dat.pack()
        Set2ActErr150dat.place(x=750,y=sett2_y+25,width=100,height=30)
        Set2ActSettlingMaxdat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set2ActSettlingMaxdat.pack()
        Set2ActSettlingMaxdat.place(x=900,y=sett2_y+25,width=100,height=30)
        Set2ActSettlingMindat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set2ActSettlingMindat.pack()
        Set2ActSettlingMindat.place(x=1050,y=sett2_y+25,width=100,height=30)
        Set2ActSettlingdat = tkinter.Entry(width=18,font=fonts,justify="center")
        Set2ActSettlingdat.pack()
        Set2ActSettlingdat.place(x=1200,y=sett2_y+25,width=100,height=30)
        ErrCodeSettling2dat = tkinter.Entry(width=18,font=fonts,justify="center")
        ErrCodeSettling2dat.pack()
        ErrCodeSettling2dat.place(x=1350,y=sett2_y+25,width=100,height=30)
        #Wobbling
        WobStartUpAdat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobStartUpAdat.pack()
        WobStartUpAdat.place(x=150,y=wobb_y1+25,width=100,height=30)
        WobStartUpBdat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobStartUpBdat.pack()
        WobStartUpBdat.place(x=300,y=wobb_y1+25,width=100,height=30)
        WobOverShootAdat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobOverShootAdat.pack()
        WobOverShootAdat.place(x=450,y=wobb_y1+25,width=100,height=30)
        WobOverShootBdat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobOverShootBdat.pack()
        WobOverShootBdat.place(x=600,y=wobb_y1+25,width=100,height=30)
        WobAmpMidAdat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobAmpMidAdat.pack()
        WobAmpMidAdat.place(x=750,y=wobb_y1+25,width=100,height=30)
        WobAmpMidBdat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobAmpMidBdat.pack()
        WobAmpMidBdat.place(x=900,y=wobb_y1+25,width=100,height=30)
        WobAmpEnddat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobAmpEnddat.pack()
        WobAmpEnddat.place(x=1050,y=wobb_y1+25,width=100,height=30)
        ErrCodeWobblingdat = tkinter.Entry(width=18,font=fonts,justify="center")
        ErrCodeWobblingdat.pack()
        ErrCodeWobblingdat.place(x=1200,y=wobb_y1+25,width=100,height=30)

        gray_color = '#ffffff'
        WobRate1dat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobRate1dat.pack()
        WobRate1dat.place(x=150,y=wobb_y2+25,width=100,height=30)
        WobRate1dat['bg'] = gray_color
        WobRate2dat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobRate2dat.pack()
        WobRate2dat.place(x=300,y=wobb_y2+25,width=100,height=30)
        WobRate2dat['bg'] = gray_color
        WobRate3dat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobRate3dat.pack()
        WobRate3dat.place(x=450,y=wobb_y2+25,width=100,height=30)
        WobRate3dat['bg'] = gray_color
        WobRate4dat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobRate4dat.pack()
        WobRate4dat.place(x=600,y=wobb_y2+25,width=100,height=30)
        WobRate4dat['bg'] = gray_color
        WobRate5dat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobRate5dat.pack()
        WobRate5dat.place(x=750,y=wobb_y2+25,width=100,height=30)
        WobRate5dat['bg'] = gray_color
        WobRate6dat = tkinter.Entry(width=18,font=fonts,justify="center")
        WobRate6dat.pack()
        WobRate6dat.place(x=900,y=wobb_y2+25,width=100,height=30)
        WobRate6dat['bg'] = gray_color
        #遅れ/追従性
        DelayDelaydat = tkinter.Entry(width=18,font=fonts,justify="center")
        DelayDelaydat.pack()
        DelayDelaydat.place(x=150,y=delay_y+25,width=100,height=30)
        DelayAdvancedat = tkinter.Entry(width=18,font=fonts,justify="center")
        DelayAdvancedat.pack()
        DelayAdvancedat.place(x=300,y=delay_y+25,width=100,height=30)
        ErrCodeDelaydat = tkinter.Entry(width=18,font=fonts,justify="center")
        ErrCodeDelaydat.pack()
        ErrCodeDelaydat.place(x=450,y=delay_y+25,width=100,height=30)
        
        def DirectryReload(self):
            FileCheck.LoggingStop()
            FileCheck.LogChecker()
            
        DirReload = tkinter.Button(root,text='Folder Reload',font=('Meiryo UI',10))
        DirReload.place(x=1350,y=90,width=100,height=40)
        DirReload.bind('<Button-1>',DirectryReload)
                
        #描画を継続
        root.protocol("WM_DELETE_WINDOW",click_close)
        root.mainloop()

    except:
        import traceback
        traceback.print_exc()        