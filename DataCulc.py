import configparser
    
def DataJudge(specnumber,Numberfmt,Dat):
    global errflag
    ThreshDat = []

    errtimevalue = ''
    errflag = 0
    inifile = configparser.ConfigParser()
    inifile.read(R'ThreshSettings.ini',encoding="utf-8_sig")                     #iniファイル読み込み

    #SPEC = inifile['ThreshSettings'][str(specnumber)]
    ThresholdCondition = inifile['ThreshSettings'][str(specnumber)]
    ThreshDat = ThresholdCondition.split(',')
    SPEC = ThreshDat[0]
    type = int(ThreshDat[1])

    strvalue = Dat
    
    
    if Numberfmt == 0:                  #0なら16進数,1なら10進数浮動小数点あり
        try:
            intvalue = int(Dat,16)
        except:
            intvalue = int(Dat)
    else:
        intvalue = float(Dat)
            
    if intvalue > int('ffff',16):
        errtimevalue = '-'
        color = '#ffFFFF'
        errflag += 1
    elif type == 0:
        if intvalue < float(SPEC):    #以下でNG
            color = '#ff0000'
            errflag += 1
        else:
            color = '#ffffff'
    elif type == 1:
        if intvalue > float(SPEC):    #以上でNG
            color = '#ff0000'
            errflag += 1
        else:
            color = '#ffffff'
    elif type == 2:
        color = '#ffffff'
        
    return color,errflag,errtimevalue


def DatChange_Stroke(DatRow):
    colors = []
    errtimevalue = ''
    errflag = 0
    ERROR=0
    OD_I = 0
    
    inifile = configparser.ConfigParser()
    inifile.read(R'InspectionDataOrder.ini',encoding="utf-8_sig")                     #iniファイル読み込み
    
    OD_I = inifile['InspectionOrder']['OD_STROKE_ERRCODE']
    ERRCODE_MR_0_ADJ = DatRow[int(OD_I)] 
    OD_I = inifile['InspectionOrder']['OD_STROKE_MR_PULSE']
    MR_PULSE = DatRow[int(OD_I)]

    mr_pulse = int(MR_PULSE,16)
    color,errflag,errtimevalue = DataJudge(0,0,MR_PULSE)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        mr_pulse = '-'
        
    errcode = ERRCODE_MR_0_ADJ
    if int(errcode,16) != 0 and int(errcode,16) < 256:
        color = '#ff0000'
        colors.append(color)
    elif errcode == 'ffffffff' :    
        errcode = '-'
        color = '#ffffff'
        colors.append(color)
    else:
        color = '#ffffff'
        colors.append(color)

    return mr_pulse,errcode,colors,ERROR

def DatChange_MRSensor(DatRow):
    colors=[]
    errtimevalue = ''
    errflag = 0
    ERROR = 0
    OD_I = 0
    
    inifile = configparser.ConfigParser()
    inifile.read(R'InspectionDataOrder.ini',encoding="utf-8_sig")                     #iniファイル読み込み
    
    OD_I = inifile['InspectionOrder']['OD_MR0_PHASEA_AMPMAX']
    MR0_AMP_MAX_A = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_MR0_PHASEA_AMPMIN']
    MR0_AMP_MIN_A = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_MR0_PHASEA_FLUCTRETIO']
    MR0_AMPFLUC_A = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_MR0_PHASEB_AMPMAX']
    MR0_AMP_MAX_B = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_MR0_PHASEB_AMPMIN']
    MR0_AMP_MIN_B = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_MR0_PHASEB_FLUCTRETIO']
    MR0_AMPFLUC_B = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_MR0_DISTORTION_FAR']
    MR_DIST_FAR = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_MR0_DISTORTION_MID']
    MR_DIST_MID = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_MR0_DISTORTION_NEAR']
    MR_DIST_NEAR = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_MR0_ERRCODE']
    ERRCODE_MR0 = DatRow[int(OD_I)]

    mr_max_a = int(MR0_AMP_MAX_A,16)
    color,errflag,errtimevalue= DataJudge(1,0,MR0_AMP_MAX_A)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        mr_max_a = '-'

    mr_min_a = int(MR0_AMP_MIN_A,16)
    color,errflag,errtimevalue= DataJudge(2,0,MR0_AMP_MIN_A)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        mr_min_a = '-'

    int_mr_fluct_a = int(MR0_AMPFLUC_A,16)
    mr_fluct_a = float(int_mr_fluct_a / 2**8)
    mr_fluct_a = round(mr_fluct_a,3)
    color,errflag,errtimevalue= DataJudge(3,1,str(mr_fluct_a))
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        mr_fluct_a = '-'

    mr_max_b = int(MR0_AMP_MAX_B,16)
    color,errflag,errtimevalue= DataJudge(1,0,MR0_AMP_MAX_B)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        mr_fluct_b = '-'

    mr_min_b = int(MR0_AMP_MIN_B,16)
    color,errflag,errtimevalue= DataJudge(2,0,MR0_AMP_MIN_B)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        mr_min_b = '-'

    int_mr_fluct_b = int(MR0_AMPFLUC_B,16)
    mr_fluct_b = float(int_mr_fluct_b / 2**8)
    mr_fluct_b = round(mr_fluct_b,3)
    color,errflag,errtimevalue= DataJudge(3,1,str(mr_fluct_b))
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        mr_fluct_b = '-'

    int_mr_dist_far = int(MR_DIST_FAR,16)
    mr_dist_far = float(int_mr_dist_far / 1000)
    color,errflag,errtimevalue= DataJudge(4,1,str(mr_dist_far))
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        mr_dist_far = '-'

    int_mr_dist_mid = int(MR_DIST_MID,16)
    mr_dist_mid = float(int_mr_dist_mid / 1000)
    color,errflag,errtimevalue= DataJudge(4,1,str(mr_dist_mid))
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        mr_dist_mid = '-'

    int_mr_dist_near = int(MR_DIST_NEAR,16)
    mr_dist_near = float(int_mr_dist_near / 1000)
    color,errflag,errtimevalue= DataJudge(4,1,str(mr_dist_near))
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        mr_dist_near = '-'

    errcode = ERRCODE_MR0
    if int(errcode,16) != 0 and int(errcode,16) < 256:
        color = '#ff0000'
        colors.append(color)
    elif errcode == 'ffffffff' :    
        errcode = '-'
        color = '#ffffff'
        colors.append(color)
    else:
        color = '#ffffff'
        colors.append(color)
    
    return mr_max_a,mr_min_a,mr_fluct_a,mr_max_b,mr_min_b,mr_fluct_b,mr_dist_far,mr_dist_mid,mr_dist_near,errcode,colors,ERROR

def DatChange_PiStroke(DatRow):
    colors=[]
    errtimevalue = ''
    errflag = 0    
    ERROR=0
    OD_I = 0
    
    inifile = configparser.ConfigParser()
    inifile.read(R'InspectionDataOrder.ini',encoding="utf-8_sig")                     #iniファイル読み込み
    
    OD_I = inifile['InspectionOrder']['OD_STROKEPI_MECHASTRK_FAR']
    RST_TO_FARMECH = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_STROKEPI_MECHASTRK_NEAR']
    RST_TO_NEARMECH = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_STROKEPI_MECHASTRK_FULL']
    FULLMECH = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_STROKEPI_PIOUT_FAR']
    PI_AD_FAR = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_STROKEPI_PIOUT_NEAR']
    PI_AD_NEAR = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_STROKEPI_ERRCODE']
    ERRCODE_PI = DatRow[int(OD_I)]
    
    intrsttofar = int(RST_TO_FARMECH,16)
    rsttofar = float(intrsttofar * 264/256)
    rsttofar = round(rsttofar)
    color,errflag,errtimevalue= DataJudge(5,1,rsttofar)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        rsttofar = '-'

    intrsttonear = int(RST_TO_NEARMECH,16)
    rsttonear = float(intrsttonear * 264/256)
    rsttonear = round(rsttonear)
    color,errflag,errtimevalue= DataJudge(6,1,rsttonear)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        rsttonear = '-'

    intfullmecha = int(FULLMECH,16)
    fullmecha = float(intfullmecha * 264/256)
    fullmecha = round(fullmecha)
    color,errflag,errtimevalue= DataJudge(7,1,fullmecha)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        fullmecha = '-'

    intpifar = int(PI_AD_FAR,16)
    pifar = float(intpifar * 3/4095)
    pifar = round(pifar,2)
    color,errflag,errtimevalue= DataJudge(8,1,pifar)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        pifar = '-'

    intpinear = int(PI_AD_NEAR,16)
    pinear = float(intpinear * 3/4095)
    pinear = round(pinear,2)
    color,errflag,errtimevalue= DataJudge(9,1,pinear)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        pinear = '-'

    errcode = ERRCODE_PI
    if int(errcode,16) != 0 and int(errcode,16) < 256:
        color = '#ff0000'
        colors.append(color)
    elif errcode == 'ffffffff' :    
        errcode = '-'
        color = '#ffffff'
        colors.append(color)
    else:
        color = '#ffffff'
        colors.append(color)
    
    return rsttofar,rsttonear,fullmecha,pifar,pinear,errcode,colors,ERROR

def DatChange_StartingLoad(DatRow):
    colors = []
    errtimevalue = ''
    errflag = 0    
    ERROR=0
    OD_I = 0
    
    inifile = configparser.ConfigParser()
    inifile.read(R'InspectionDataOrder.ini',encoding="utf-8_sig")                     #iniファイル読み込み
    
    OD_I = inifile['InspectionOrder']['OD_STARTINGLOAD_COEF']
    SL_TARGETAMP = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_STARTINGLOAD_ACTAMP']
    SL_ACTUALAMP = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_STARTINGLOAD_ERRCODE']
    ERRCODE_STARTINGLOAD = DatRow[int(OD_I)]

    inifile = configparser.ConfigParser()
    inifile.read(R'ThreshSettings.ini',encoding="utf-8_sig")                     #iniファイル読み込み
    THRUSTCONSTANT = float(inifile['ThreshSettings'][str(27)])
    COILRESISTANCE = float(inifile['ThreshSettings'][str(28)])
    MOVINGPARTSWEIGHT = float(inifile['ThreshSettings'][str(29)])
    
    inttagetamp = int(SL_TARGETAMP,16)
    targetamp = float(inttagetamp*THRUSTCONSTANT*(768/128*4.8/2048/COILRESISTANCE/9.81/(MOVINGPARTSWEIGHT/1000)))
    targetamp = round(targetamp,3)
    color,errflag,errtimevalue= DataJudge(10,1,targetamp)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        targetamp = '-'

    actualamp = int(SL_ACTUALAMP,16)
    color,errflag,errtimevalue= DataJudge(11,0,SL_ACTUALAMP)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        actualamp = '-'

    errcode = ERRCODE_STARTINGLOAD
    if int(errcode,16) != 0 and int(errcode,16) < 256:
        color = '#ff0000'
        colors.append(color)
    elif errcode == 'ffffffff' :    
        errcode = '-'
        color = '#ffffff'
        colors.append(color)
    else:
        color = '#ffffff'
        colors.append(color)

    return targetamp,actualamp,errcode,colors,ERROR    

def DatChange_Settling1(DatRow):
    colors = []
    errtimevalue = ''
    errflag = 0    
    ERROR=0
    OD_I = 0
    
    inifile = configparser.ConfigParser()
    inifile.read(R'InspectionDataOrder.ini',encoding="utf-8_sig")                     #iniファイル読み込み
    
    OD_I = inifile['InspectionOrder']['OD_SETTLING1_START']
    SETTLING1_STARTPOS = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING1_END']
    SETTLING1_ENDPOS = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING1_MOVE']
    SETTLING1_POS_025VD = DatRow[int(OD_I)]    
    OD_I = inifile['InspectionOrder']['OD_SETTLING1_DELAY']
    SETTLING1_POS_100VD = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING1_ERROR']
    SETTLING1_POS_150VD = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING1_MAX']
    SETTLING1_MAX = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING1_MIN']
    SETTLING1_MIN = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING1_ERRCODE']
    ERRCODE_SETTLING1 = DatRow[int(OD_I)]
    CulcMeth = int(inifile['InspectionOrder']['SETTLING_CULC'])

    startpos1 = int(SETTLING1_STARTPOS,16)
    color,errflag,errtimevalue= DataJudge(12,0,SETTLING1_STARTPOS)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        startpos1 = '-'

    endpos1 = int(SETTLING1_ENDPOS,16)
    color,errflag,errtimevalue= DataJudge(13,0,SETTLING1_ENDPOS)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        endpos1 = '-'
    
    
    if startpos1 == '-':
        pos025vd1 = '-'
        color = '#ffffff'
        errflag = 1
    else:
        intpos025vd1 = int(SETTLING1_POS_025VD,16)
        pos025vd1 = float(intpos025vd1 / 2**16) - startpos1
        pos025vd1 = round(pos025vd1,3)
        color,errflag,errtimevalue= DataJudge(14,1,pos025vd1)
        colors.append(color)
    ERROR += errflag     
    
    if endpos1 == '-':
        pos100vd1 = '-'
        color = '#ffffff'
        errflag = 1
    else:
        intpos100vd1 = int(SETTLING1_POS_100VD,16)
        pos100vd1 = float(endpos1 - intpos100vd1 / 2**16) 
        pos100vd1 = round(pos100vd1,3)
        color,errflag,errtimevalue= DataJudge(15,1,pos100vd1)
        colors.append(color)
    ERROR += errflag     
    
    if endpos1 == '-':
        pos150vd1 = '-'
        color = '#ffffff'
        errflag = 1
    else:
        intpos150vd1 = int(SETTLING1_POS_150VD,16)
        if CulcMeth == 0:
            if intpos150vd1 < 2**31 :
                pos150vd1 = intpos150vd1 / 2**16 - endpos1
            else:
                pos150vd1 = (intpos150vd1-2**32) / 2**16 - endpos1
        elif CulcMeth == 1:
                pos150vd1 = endpos1 - intpos150vd1 / 2**16
        pos150vd1 = round(pos150vd1,3)
        color,errflag,errtimevalue= DataJudge(16,1,pos150vd1)
            
    colors.append(color)
    ERROR += errflag     

    intsettlingmax1 = int(SETTLING1_MAX,16)
    if intsettlingmax1 < 2**31:
        settlingmax1 = intsettlingmax1 / 2**16
    else :
        settlingmax1 = (2**32 - intsettlingmax1) / 2**16
    settlingmax1 = round(settlingmax1,3)    
    color,errflag,errtimevalue= DataJudge(17,1,settlingmax1)
    colors.append(color)
    ERROR += errflag     
    if SETTLING1_MAX == 'ffffffff':
        settlingmax1 = '-'
        
    intsettlingmin1 = int(SETTLING1_MIN,16)
    if intsettlingmin1 < 2**31:
        settlingmin1 = intsettlingmin1 / 2**16
    else :
        settlingmin1 = (intsettlingmin1 - 2**32) / 2**16
    settlingmin1 = round(settlingmin1,3)
    color,errflag,errtimevalue= DataJudge(18,1,settlingmin1)
    colors.append(color)
    ERROR += errflag     
    if SETTLING1_MIN == 'ffffffff':
        settlingmin1 = '-'

    if settlingmax1 == '-' or settlingmin1 == '-':
        settling1 = '-'
        colors.append('#ffffff')
        errflag = 1
    else:
        if abs(settlingmax1) > abs(settlingmin1):
            settling1 = settlingmax1
            settling1 = round(settling1,3)
            color,errflag,errtimevalue= DataJudge(17,1,settling1)
            colors.append(color)
        else:
            settling1 = settlingmin1
            settling1 = round(settling1,3)
            color,errflag,errtimevalue= DataJudge(18,1,settling1)
            colors.append(color)
    ERROR += errflag     
        
    errcode = ERRCODE_SETTLING1
    if int(errcode,16) != 0 and int(errcode,16) < 65535:
        color = '#ff0000'
        colors.append(color)
    elif errcode == 'ffffffff' :    
        errcode = '-'
        color = '#ffffff'
        colors.append(color)
    else:
        color = '#ffffff'
        colors.append(color)
    
    return startpos1,endpos1,pos025vd1,pos100vd1,pos150vd1,settlingmax1,settlingmin1,settling1,errcode,colors,ERROR

def DatChange_Settling2(DatRow):
    colors = []
    errtimevalue = ''
    errflag = 0    
    ERROR=0
    OD_I = 0
    
    inifile = configparser.ConfigParser()
    inifile.read(R'InspectionDataOrder.ini',encoding="utf-8_sig")                     #iniファイル読み込み
    
    OD_I = inifile['InspectionOrder']['OD_SETTLING2_START']
    SETTLING2_STARTPOS = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING2_END']
    SETTLING2_ENDPOS = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING2_MOVE']
    SETTLING2_POS_025VD = DatRow[int(OD_I)]    
    OD_I = inifile['InspectionOrder']['OD_SETTLING2_DELAY']
    SETTLING2_POS_100VD = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING2_ERROR']
    SETTLING2_POS_150VD = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING2_MAX']
    SETTLING2_MAX = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING2_MIN']
    SETTLING2_MIN = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_SETTLING2_ERRCODE']
    ERRCODE_SETTLING2 = DatRow[int(OD_I)]
    CulcMeth = int(inifile['InspectionOrder']['SETTLING_CULC'])

    startpos2 = int(SETTLING2_STARTPOS,16)
    color,errflag,errtimevalue= DataJudge(12,0,SETTLING2_STARTPOS)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        startpos2 = '-'

    endpos2 = int(SETTLING2_ENDPOS,16)
    color,errflag,errtimevalue= DataJudge(13,0,SETTLING2_ENDPOS)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        endpos2 = '-'

    if startpos2 == '-':
        pos025vd2 = '-'
        color = '#ffffff'
        errflag = 1
    else:
        intpos025vd2 = int(SETTLING2_POS_025VD,16)
        if CulcMeth == 0:
            pos025vd2 = float(intpos025vd2 / 2**16) - startpos2
        elif CulcMeth == 1:
            pos025vd2 = float(intpos025vd2 / 2**32)
        pos025vd2 = round(pos025vd2,3)
        color,errflag,errtimevalue= DataJudge(14,1,pos025vd2)

    colors.append(color)
    ERROR += errflag     

    if endpos2 == '-':
        pos100vd2 = '-'
        color = '#ffffff'
        errflag = 1
    else:
        intpos100vd2 = int(SETTLING2_POS_100VD,16)
        if CulcMeth == 0:
            pos100vd2 = float(endpos2 - intpos100vd2 / 2**16)
        elif CulcMeth == 1:
            pos100vd2 = float(intpos100vd2 / 2**32)
        pos100vd2 = round(pos100vd2,3)
        color,errflag,errtimevalue= DataJudge(15,1,pos100vd2)
    colors.append(color)
    ERROR += errflag     

    if endpos2 == '-':
        pos150vd2 = '-'
        color = '#ffffff'
        errflag = 1
    else:
        intpos150vd2 = int(SETTLING2_POS_150VD,16)
        if CulcMeth == 0:
            if intpos150vd2 < 2**31 :
                pos150vd2 = intpos150vd2 / 2**16 - endpos2
            else:
                pos150vd2 = (intpos150vd2-2**32) / 2**16 - endpos2
        elif CulcMeth == 1:
            if intpos150vd2 < 2**31 :
                pos150vd2 = intpos150vd2 / 2**16
            else:
                pos150vd2 = (intpos150vd2-2**32) / 2**16
        pos150vd2 = round(pos150vd2,3)
        color,errflag,errtimevalue= DataJudge(16,1,pos150vd2)
    colors.append(color)
    ERROR += errflag     

    intsettlingmax2 = int(SETTLING2_MAX,16)
    if CulcMeth == 0:
        if intsettlingmax2 < 2**31:
            settlingmax2 = intsettlingmax2 / 2**16
        else :
            settlingmax2 = (2**32 - intsettlingmax2) / 2**16
    elif CulcMeth == 1:
        if intsettlingmax2 < 2**31:
            settlingmax2 = intsettlingmax2 / 2**16
        else :
            settlingmax2 = (intsettlingmax2 - 2**32) / 2**16
    settlingmax2 = round(settlingmax2,3)
    color,errflag,errtimevalue= DataJudge(17,1,settlingmax2)
    colors.append(color)
    ERROR += errflag     
    if SETTLING2_MAX == 'ffffffff':
        settlingmax2 = '-'

    intsettlingmin2 = int(SETTLING2_MIN,16)
    if intsettlingmin2 < 2**31:
        settlingmin2 = intsettlingmin2 / 2**16
    else :
        settlingmin2 = (intsettlingmin2 - 2**32) / 2**16
    settlingmin2 = round(settlingmin2,3)
    color,errflag,errtimevalue= DataJudge(18,1,settlingmin2)
    colors.append(color)
    ERROR += errflag     
    if SETTLING2_MIN == 'ffffffff':
        settlingmin2 = '-'

    if settlingmax2 == '-' or settlingmin2 == '-':
        settling2 = '-'
        colors.append('#ffffff')
        errflag = 1
    else:
        if abs(settlingmax2) > abs(settlingmin2):
            settling2 = settlingmax2
            settling2 = round(settling2,3)
            color,errflag,errtimevalue= DataJudge(17,1,settling2)
            colors.append(color)
        else:
            settling2 = settlingmin2
            settling2 = round(settling2,3)
            color,errflag,errtimevalue= DataJudge(18,1,settling2)
            colors.append(color)
    ERROR += errflag     

    errcode = ERRCODE_SETTLING2
    if int(errcode,16) != 0 and int(errcode,16) < 65535:
        color = '#ff0000'
        colors.append(color)
    elif errcode == 'ffffffff' :    
        errcode = '-'
        color = '#ffffff'
        colors.append(color)
    else:
        color = '#ffffff'
        colors.append(color)
    
    return startpos2,endpos2,pos025vd2,pos100vd2,pos150vd2,settlingmax2,settlingmin2,settling2,errcode,colors,ERROR

def DatChange_Wobbling(DatRow):
    colors=[]
    errtimevalue = ''
    errflag = 0    
    ERROR=0
    OD_I = 0
    
    inifile = configparser.ConfigParser()
    inifile.read(R'InspectionDataOrder.ini',encoding="utf-8_sig")                     #iniファイル読み込み
    
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_STARTUP_A']
    WOB_STARTUP_A =DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_STARTUP_B']
    WOB_STARTUP_B = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_OVERSHOOT_A']
    WOB_OVERSHOOT_A = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_OVERSHOOT_B']
    WOB_OVERSHOOT_B = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_AMPMID_A']
    WOB_MIDAMP_A = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_AMPMID_B']
    WOB_MIDAMP_B = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_AMPEND']
    WOB_ENDAMP = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_RATE1']
    WOB_RATE1 = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_RATE2']
    WOB_RATE2 = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_RATE3']
    WOB_RATE3 = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_RATE4']
    WOB_RATE4 = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_RATE5']
    WOB_RATE5 = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_RATE6']
    WOB_RATE6 = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_WOBBLING_ERRCODE']
    ERRCODE_WOB = DatRow[int(OD_I)]
    
    startupA = int(WOB_STARTUP_A,16)
    if startupA > 32768:
        startupA = startupA - 65536
    color,errflag,errtimevalue= DataJudge(19,1,startupA)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        startupA = '-'

    startupB = int(WOB_STARTUP_B,16)
    if startupB > 32768:
        startupB = startupB - 65536
    color,errflag,errtimevalue= DataJudge(19,1,startupB)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        startupB = '-'

    overshootA = int(WOB_OVERSHOOT_A,16)
    color,errflag,errtimevalue= DataJudge(20,1,overshootA)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        overshootA = '-'

    overshootB = int(WOB_OVERSHOOT_B,16)
    color,errflag,errtimevalue= DataJudge(20,1,overshootB)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        overshootB = '-'

    midampA = int(WOB_MIDAMP_A,16)
    color,errflag,errtimevalue= DataJudge(21,1,midampA)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        midampA = '-'

    midampB = int(WOB_MIDAMP_B,16)
    color,errflag,errtimevalue= DataJudge(21,1,midampB)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        midampB = '-'

    intampend = int(WOB_ENDAMP,16)
    ampend = float(intampend / 2**8)
    ampend = round(ampend,1)
    color,errflag,errtimevalue= DataJudge(22,1,ampend)
    colors.append(color)
    datng=0
    if errflag == 0:
        datng = 1
    if datng ==1:
        color,errflag,errtimevalue= DataJudge(23,1,ampend)
        colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        ampend = '-'

    intrate1 = int(WOB_RATE1,16)
    rate1 = round(intrate1,1) 
    color,errflag,errtimevalue= DataJudge(24,1,rate1)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        rate1 = '-'

    intrate2 = int(WOB_RATE2,16)
    rate2 = round(intrate2,1) 
    color,errflag,errtimevalue= DataJudge(24,1,rate2)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        rate2 = '-'

    intrate3 = int(WOB_RATE3,16)
    rate3 = round(intrate3,1) 
    color,errflag,errtimevalue= DataJudge(24,1,rate3)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        rate3 = '-'

    intrate4 = int(WOB_RATE4,16)
    rate4 = round(intrate4,1)
    color,errflag,errtimevalue= DataJudge(24,1,rate4)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        rate4 = '-'

    intrate5 = int(WOB_RATE5,16)
    rate5 = round(intrate5,1) 
    color,errflag,errtimevalue= DataJudge(24,1,rate5)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        rate5 = '-'

    intrate6 = int(WOB_RATE6,16)
    rate6 = round(intrate6,1)
    color,errflag,errtimevalue= DataJudge(24,1,rate6)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        rate6 = '-'

    errcode = ERRCODE_WOB 
    if int(errcode,16) != 0 and int(errcode,16) < 256:
        color = '#ff0000'
        colors.append(color)
    elif errcode == 'ffffffff' :    
        errcode = '-'
        color = '#ffffff'
        colors.append(color)
    else:
        color = '#ffffff'
        colors.append(color)
    
    return startupA,startupB,overshootA,overshootB,midampA,midampB,ampend,rate1,rate2,rate3,rate4,rate5,rate6,errcode,colors,ERROR
    
def DatChange_Delay(DatRow):
    colors=[]
    errtimevalue = ''
    errflag = 0    
    ERROR=0
    OD_I = 0
    
    inifile = configparser.ConfigParser()
    inifile.read(R'InspectionDataOrder.ini',encoding="utf-8_sig")                     #iniファイル読み込み
    
    OD_I = inifile['InspectionOrder']['OD_DELAY_DELAY']
    DELAY_DELAY = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_DELAY_ADVANCE']
    DELAY_ADVANCE = DatRow[int(OD_I)]
    OD_I = inifile['InspectionOrder']['OD_DELAY_ERRODE']
    ERRCODE_DELAY = DatRow[int(OD_I)]
    
    delay = int(DELAY_DELAY,16)
    color,errflag,errtimevalue= DataJudge(25,1,delay)
    colors.append(color)
    ERROR += errflag     
    if errtimevalue == '-':
        delay = '-'

    advance = int(DELAY_ADVANCE,16)    
    color,errflag,errtimevalue= DataJudge(26,0,advance)
    colors.append(color)
    ERROR += errflag     
    if advance > 32768:
        advance = advance - 65536
    if errtimevalue == '-':
        advance = '-'
        
    errcode = ERRCODE_DELAY
    if int(errcode,16) != 0 and int(errcode,16) < 256:
        color = '#ff0000'
        colors.append(color)
    elif errcode == 'ffffffff' :    
        errcode = '-'
        color = '#ffffff'
        colors.append(color)
    else:
        color = '#ffffff'
        colors.append(color)
    
    return delay,advance,errcode,colors,ERROR