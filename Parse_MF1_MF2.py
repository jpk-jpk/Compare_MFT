import glob, os
#from tkinter import filedialog
import pandas as pd
#import matplotlib.pyplot as plt
#import numpy as np
import re
import argparse


parser=argparse.ArgumentParser(description="This Program is written for comparison of MF1 files with given tolerance for Vapor Fraction, Liquid Fraction, Liquid2 Fraction, Temperature, Pressure, Speed")
parser.add_argument("-f1","--Folder1", default="F1",required=True,help="Folder one with MF1 files")
parser.add_argument("-f2","--Folder2", default="F2",required=True, help="Folder two with MF1 files")
parser.add_argument("-f3","--Folder3", default="D:/Output",required=False, help="Folder three for output")
parser.add_argument("-o","--CSV_fn", default="Test.csv",required=False, help="CSV Filename for the Output")
parser.add_argument('-t','--tolerances',default=['0.0001', '0.0001', '0.0001', '0.001', '0.001','0.01']  , nargs='+',required=False, help='Input Tolerances for V,L1,L2,T,P,S with spaces default tolerances for V=0.0001 L1=0.0001 L2=0.0001 T=0.001 P=0.001 S=0.01')
args = parser.parse_args()

print("Folder1:",args.Folder1)
f1=args.Folder1
print("Folder2:",args.Folder2)
f2=args.Folder2
print("Folder3:",args.Folder3)
f3=args.Folder3
print("CSV File Name:",args.CSV_fn)
CSV_Name=args.CSV_fn
toler=args.tolerances
print("The Tolerances are V={},L1={},L2={},T={},P={},S={}".format(*toler))


#This function returns a list of filenames with MF1 extension in the directory chosen
def files(path):
    fpf_names = glob.glob(path+"/*.MF1", recursive = True)
    #filenames=(os.path.basename(x) for x in glob.glob(path+"/*.csv", recursive = True))
    return fpf_names

#This function returns a pandas dataframe with parsed information (matrix) data of MF1  
def MF1_Parse(FN):
    z=pd.DataFrame((j.strip().split() for j in open(FN).readlines() if len(j.strip().split())>=18 and not j.startswith('-')))
    for i in [1,2,3,5,7,8,9,10,11,12,13,15,16,17]:
        z[i]=z[i].apply(pd.to_numeric, errors='ignore')
    z=z.rename(columns=z.iloc[0]).drop(z.index[0])
    return z

#with the given params the function creates a output text file and
def c_new(str_iso,fname,_filepath,slb,file_path_string3):
    with open(file_path_string3.replace("/","\\")+'\\'+os.path.basename(fname)[:-4]+"_iso.txt","w") as iso_newfile:
        iso_newfile.write(str_iso)
        print("\tTest sweeps are isolated")
    if not slb==" ":
        ss='copy  '+"\""+_filepath.replace("/","\\")+'\\'+slb+"\""+'  '+"\""+file_path_string3.replace("/","\\")+'\\'+slb+"\""
        print("\t",ss)
        try:
            if os.popen(ss):
                print("\tCopied")
        except:
            print("\tNo slb file was found")

#
def MFT_Comparsion(f1,f2,f3,toler):
    #print("This Program will Parse and compare  the MF1 files in the given folder")
    #print("Select the folders that contains MF1 files Gold and New Build")
    #temp=input("Proceed: ")
    #del temp
    file_path_string = f1
    file_path_string2 = f2
    #file_path_string = filedialog.askdirectory(title='Please select MF1 reference folder1 (GOLD/RTRF)')
    #file_path_string2 = filedialog.askdirectory(title='Please select MF1 folder2')
    #tol=re.split('\s+',input("Give the Tolerance of Vapor,Liquid,Liquid2,Temperature,Pressure: "))
    file_path_string3 = f3
    #file_path_string3 = filedialog.askdirectory(title='Please select Output Text folder3')
    #tol = ['0.0001','0.0001','0.0001','0.0001','0.0001','0.0001'] #Tolerances
    tol = toler
    #print(file_path_string,file_path_string2)
    #FracList=['VAPOR','LIQUID','LIQUID2','TEMP','PRES','ITER','SPEED']
    FracList=['VAPOR','LIQUID','LIQUID2']
    PropList=['TEMP','PRES','SPEED']
    #writer = pd.ExcelWriter(str(input("Enter the Output Excel Name"))+'.xlsx', engine='xlsxwriter')
    F6=pd.DataFrame()
    count=0
    for i in files(file_path_string):
        if os.path.isfile(file_path_string2+"/"+os.path.basename(i)):
            count+=1
            try:
                #F3=pd.merge(MF1_Parse(i), MF1_Parse(file_path_string2+"/"+os.path.basename(i)), right_index=True, left_index=True)
                F1=MF1_Parse(i)
                F2=MF1_Parse(file_path_string2+"/"+os.path.basename(i))
                F5 = pd.DataFrame()
                F4 = pd.DataFrame()
                #creating the Relative Deviation  
                for item in FracList:
                    adev=item+"_atol"
                    item_x=item+"_1"
                    item_y=item+"_2"
                    F4[['SCENARIO','CASE','FLASH','SOLVED']] = F1[['SCENARIO','CASE','FLASH','SOLVED']]
                    F4[item_x]=F1[item]
                    F4[item_y]=F2[item]
                    F4[adev] = F4[item_x]-F4[item_y]
                for item in (PropList):
                    rdev=item+"_rtol"
                    item_1=item+"_1"
                    item_2=item+"_2"
                    F4[item_1]=F1[item]
                    F4[item_2]=F2[item]
                    F4[rdev] = 2*(((F4[item_1]-F4[item_2])/(F4[item_1]+F4[item_2])).abs())
                    
                print("\n",count,":", i)
                #Defining the conditions for filtering rows based on tolerances  
                F4.insert(0,"FileName",os.path.basename(i)[:-4])
                tol_s='VAPOR_atol.abs()>='+tol[0]+'or LIQUID_atol.abs()>='+tol[1]+'or LIQUID2_atol.abs()>='+tol[2]+'or TEMP_rtol.abs()>='+tol[3]+'or PRES_rtol.abs()>='+tol[4]+'or SPEED_rtol.abs()>='+tol[5]                        
                F5=F4.query(tol_s)
                F6=F6.append(F5)
                if not F5.empty:
                    print("\t--------FAIL---------\n")
                    F5=F5.drop_duplicates(['SCENARIO', 'CASE'])
                    F5['CASE']=F5['CASE'].astype(str)
                    iso_rows = F5[['SCENARIO', 'CASE']].values.tolist()
                    if iso_rows:
                        try:
                            with open(i[:-3]+"txt") as isotxt:
                                newf=""
                                c=0
                                for x, y in enumerate(isotxt):
                                    if x==0:
                                        newf+=y
                                        if re.match('\S+\.slb',re.split('\s+',y)[4]):
                                            slbname=re.split('\s+',y)[4]
                                        else:    
                                            print("\tNo SLB Name was found")
                                            slbname=" "
                                    elif c==0:
                                        newf+=y
                                        if y.upper().strip().startswith('SCENARIO'):
                                            c=x
                                            #print("Scenario line: ",c)
                                    elif re.split('\s+',y.lstrip())[:2] in iso_rows:
                                        newf+=y
                                    else:
                                        newf+=";"+y
                                        #print("ISO_Row: ",x+1)
                            c_new(newf,i,file_path_string,slbname,file_path_string3)
                        except:
                            print("\tNo text file was found in 2nd folder")
                    #print(iso_rows)
                    #print(F5)
                # F4[labels].plot(use_index=True, style=['+','o','x','s'],subplots=True,title=os.path.basename(i))
                # plt.legend(loc='best')
                else:
                    print("\t--------PASS---------\n")
            except:
                print("\tSome Error Occured opening ")
    if not F6.empty:
        with open(f3+"\\"+CSV_Name, 'w') as f:
            f.write("Input Folder1:,"+f1+"\n")
            f.write("Input Folder2:,"+f2+"\n")
            f.write("Output Folder:,"+f3+"\n")
            f.write("The Tolerances are, V={},L1={},L2={},T={},P={},S={}".format(*toler))
            f.write("\n\n\n")
        F6.to_csv(f3+"\\"+CSV_Name, mode='a')
        print("\n\n------------------------------------------------------------------")
        print("Mismatch Sweeps CSV is created at ",f3+"/"+CSV_Name)
        print("------------------------------------------------------------------")
        
    #plt.show()
    
    del F2,F4,F6,file_path_string,file_path_string2
	

MFT_Comparsion(f1,f2,f3,toler)  
