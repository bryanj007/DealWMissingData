'''
Created on Aug 24, 2012

@author: sbyam
'''
Bad_Data_Value = 6999

def findandfillgaps(FileIn,FileOut,TimeDifference, Bad_Data_Value):
    #This function fills in missing data in FileIn with Bad_Data_Value
    #FileIn--- Directory and name of the inputfile with the missing dates
    #FileOut-- Dictory and name of the outputfile with the missing dates filled in with Bad_Data_Value
    #TimeDifference is in seconds.  This is the expected time difference between lines of data.
    #FileIn is assumed to be a *.csv file containing a time series of the format:
    #      header1
    #      header2
    #      header3
    #      header4
    #      "yyyy-mm-dd hh:mm:ss", floating point data value
    import time
    import datetime
    file_handle_in = open(FileIn,'r')
    data_in = file_handle_in.readlines()
    header1 = data_in[0]
    header2 = data_in[1]
    header3 = data_in[2]
    header4 = data_in[3]
    firstline_in = data_in[4]
    firstline_in = firstline_in.rstrip()
    firstline_array = firstline_in.split(',')
    YmdHms_firstline = time.strptime(firstline_array[0].strip('"'),'%Y-%m-%d %H:%M:%S')[0:6]
    Start_In = datetime.datetime(YmdHms_firstline[0],YmdHms_firstline[1],YmdHms_firstline[2],\
                              YmdHms_firstline[3],YmdHms_firstline[4],YmdHms_firstline[5])
    
    lastline_in = data_in[-1]
    lastline_in = lastline_in.rstrip()
    lastline_array = lastline_in.split(',')
    YmdHms_lastline = time.strptime(lastline_array[0].strip('"'),'%Y-%m-%d %H:%M:%S')[0:6]
    End_In = datetime.datetime(YmdHms_lastline[0],YmdHms_lastline[1],YmdHms_lastline[2],\
                              YmdHms_lastline[3],YmdHms_lastline[4],YmdHms_lastline[5])
    TimeDiffIn= End_In - Start_In
    TimeDiffInSeconds= TimeDiffIn.days*86400+TimeDiffIn.seconds
    NumberOfLinesToProcess = int(TimeDiffInSeconds/TimeDifference)+1
    print "NumberOfLinesToProcess", NumberOfLinesToProcess
    ActualNumOfLines = 0
    for line in data_in[4:]:
        ActualNumOfLines += 1
    print "ActualNumOfLines", ActualNumOfLines
    file_handle_out = open(FileOut,'w')
    file_handle_out.writelines(header1)
    file_handle_out.writelines(header2)
    file_handle_out.writelines(header3)
    file_handle_out.writelines(header4)
    if (NumberOfLinesToProcess == ActualNumOfLines):
        print "no missing dates\n"
        file_handle_out.writelines(data_in)
    else:
        Line_in =0
        PrevTime = Start_In
        ExpectedCurrTime = PrevTime 
        for line in data_in[4:]:
            CurrLine = line.rstrip()
            CurrLine_array = CurrLine.split(',')
            YmdHms_CurrLine = time.strptime(CurrLine_array[0].strip('"'),'%Y-%m-%d %H:%M:%S')[0:6]
            CurrTime = datetime.datetime(YmdHms_CurrLine[0],YmdHms_CurrLine[1],YmdHms_CurrLine[2],\
                         YmdHms_CurrLine[3],YmdHms_CurrLine[4],YmdHms_CurrLine[5])   
            while (ExpectedCurrTime<= CurrTime ):
                if(ExpectedCurrTime ==CurrTime):
                    stringout =   CurrLine_array[0] + ',' + CurrLine_array[1] +'\n'
                else:
                    stringout = str(ExpectedCurrTime) +','+ str(Bad_Data_Value) + '\n'
                ExpectedCurrTime = ExpectedCurrTime + datetime.timedelta(seconds = TimeDifference)
                file_handle_out.writelines(stringout)
            Line_in += 1
            PrevTime = CurrTime
    file_handle_out.close()
    file_handle_in.close()
    return

print "joe"    
FileWMissingDates = "C:\\bryan\\playdata\\netrad_short.csv"
FileWOMissingDates = "C:\\bryan\\playdata\\no_missing_dates.csv"
findandfillgaps(FileWMissingDates,FileWOMissingDates,3600,6999)
    
