import time
import pandas as pd
import numpy as np
import random

import threading

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from CAPTCHA_object_detection_String import *


from tkinter import *
from tkinter import messagebox

import argparse

##from pynput.keyboard import Key, Controller
##keyboard = Controller()

global Check_Args_Mode
ProgramRunning = None
LoginCredentials = None

SmartLogin = True
MultipleChecks = True
AutoCaptcha = 1



Web = 'https://clickpayearn.com/login'
Dashboard_Url = 'https://clickpayearn.com/user/dashboard'

#Throughout the Program,Speed of delay is dependent on this
delay = int(2)
# numberofTotalAds=40
BrowserLimit = 2
universal_y_paddin=10




class Checking_Processed_ID():
    def datetime_now(self):
        self.WeekDayName = time.strftime('%a', time.localtime())
        self.DayofMonth  = time.strftime('%d', time.localtime())
        self.MonthName   = time.strftime('%m', time.localtime())
        self.Year        = time.strftime('%Y', time.localtime())
        self.Time        = time.strftime('%H:%M:%S:%p', time.localtime())
        
    def saving(self,email,balance):
        self.datetime_now()
        self.email=email
        self.balance = balance
        self.savingstring = '{},{},{},{},{},Account,{},Balance,{}'.format(self.WeekDayName,self.DayofMonth,self.MonthName,self.Year,self.Time,self.email,self.balance)
        
        if self.checking(email) == 0:
            return
        else:
            print(self.savingstring)

            file = open("RunHistoryLog.txt","a")
            file.write(self.savingstring)
            file.write('\n')
            file.close()
            print('close')

    def opening(self):
        self.datetime_now()
        self.data = pd.read_csv('RunHistoryLog.txt', header = None)
        # print(self.data)

    def checking(self,email):
        self.opening()
        self.email=email
        
        c=0
        # print(self.data)
        for i in self.data[6]:
            if (self.email==i):
                # print('{}'.format(self.DayofMonth))
                # print('{}'.format(self.data[1][c]))

                if self.WeekDayName == 'Sun':
                    # print('Today is Sun!!')
                    return 2

                if ( int(self.DayofMonth) == int(self.data[1][c]) and int(self.MonthName) == int(self.data[2][c]) and int(self.Year) == int(self.data[3][c] )):
                    print ('Email ID {} is Done for Today'.format(self.email))
                    return 0
            c+=1
        
class BOT_GUI():
    def __init__(self):
    # def GUI(self):
        self.root = Tk()
        self.root.title('Click Pay Earn Bot by Syed Qasim')
        # root.iconbitmap('c:/app/icon.ico')

        frame0=LabelFrame(self.root)
        frame0.pack(padx=20,pady=universal_y_paddin)
        WelcomeText= Label(frame0,text="Welcome to CPE Automated Bot by Syed Qasim")
        WelcomeText.grid    (row=0,column=0 )

        
        frame=LabelFrame(self.root)
        frame.pack(padx=20,pady=universal_y_paddin)
        
        

        EnterEmail  = Label(frame,text="Enter Email")
        Email       = Entry(frame, width=30,borderwidth=5)
        EnterPassword= Label(frame,text="Enter Password")
        Password    = Entry(frame, width=30,borderwidth=5)
        SaveButton = Button(frame, text="Save Credentials", command = lambda: self.SaveLoginCredentials(Email,Password))

        
        EnterEmail.grid     (row=1,column=0, pady=5)
        Email.grid          (row=1,column=1,columnspan=2, padx=10,pady=5)
        EnterPassword.grid  (row=2,column=0, pady=5)
        Password.grid       (row=2,column=1,columnspan=2, padx=10,pady=5)
        
        SaveButton.grid     (row=3,column=1, padx=10,pady=3)

        ##Loading Crdentials
        CredFrame=LabelFrame(self.root)
        CredFrame.pack(padx=10,pady=universal_y_paddin)

        
        LoadButton = Button(CredFrame, text="Load Credentials", command = LoadLoginCredentials)
        # NewButton = Button(CredFrame, text="Clear Credentials"  , command = lambda: self.NewLoginCredentials(Email,Password))

        LoadButton.grid     (row=0,column=1, padx=20,pady=3)
        # NewButton.grid      (row=0,column=2, padx=20,pady=3)
        

        ##Setting the Delay
        
        frameDelay=LabelFrame(self.root)
        frameDelay.pack(padx=10,pady=universal_y_paddin)
        r=IntVar()
        r.set("2") 
        DelayText= Label(frameDelay,text="Select Speed")
        DelayFast=Radiobutton   (frameDelay,text="Fast-2s", variable=r,value=2,command=lambda:self.SetDelay(r.get()))
        DelayMedium=Radiobutton (frameDelay,text="Medium-3s", variable=r,value=3,command=lambda:self.SetDelay(r.get()))
        DelaySlow=Radiobutton   (frameDelay,text="Slow-5s", variable=r,value=5,command=lambda:self.SetDelay(r.get()))
        
        
        
        DelayText.grid      (row=0,column=0 , padx=30,pady=3)
        DelayFast.grid      (row=0,column=1 , padx=5,pady=3)
        DelayMedium.grid    (row=0,column=2 , padx=5,pady=3)
        DelaySlow.grid      (row=0,column=3 , padx=5,pady=3)


        #Simultaneous Browsers
        framebrowsercount=LabelFrame(self.root)
        framebrowsercount.pack(padx=20,pady=universal_y_paddin)

        global BrowserLimit
        BrowserNumberText   = Label(framebrowsercount,text="Enter Browsers - Default={}".format(BrowserLimit))
        InputBrowserVariable     = Entry(framebrowsercount, width=30,borderwidth=5)
        SaveBrowserNumber   = Button(framebrowsercount, text="Save",command = lambda: self.SetBrowserLimit(InputBrowserVariable.get()))

        BrowserNumberText.grid  (row=1,column=0, pady=5)
        InputBrowserVariable.grid    (row=1,column=1,columnspan=2, padx=10,pady=5)
        SaveBrowserNumber.grid  (row=2,column=1, padx=30,pady=3)


        ########### Auto Captcha
        CaptchaFrame=LabelFrame(self.root)
        CaptchaFrame.pack(padx=10, pady=universal_y_paddin)

        
        
        global AutoCaptchatk
        AutoCaptchatk = IntVar()
        AutoCaptchatk.set("1")
        CaptchaaStatus   = Label(CaptchaFrame,text="Auto Captcha - Default={}".format(AutoCaptcha))
        CaptchaaStatusOn=Radiobutton (CaptchaFrame,text="On", variable=AutoCaptchatk,value='1',command=lambda:self.SetAutoCaptcha(AutoCaptchatk.get()))
        CaptchaaStatusOff=Radiobutton(CaptchaFrame,text="Off", variable=AutoCaptchatk,value='0',command=lambda:self.SetAutoCaptcha(AutoCaptchatk.get()))

        ##CaptchaaStatus.grid  (row=1,column=0, pady=5)
        ##CaptchaaStatusOn.grid    (row=1,column=1,columnspan=3, padx=10,pady=5)
        ##CaptchaaStatusOff.grid  (row=1,column=2, padx=10,pady=3)

        CaptchaaStatus.grid      (row=0,column=0 , padx=30,pady=3)
        CaptchaaStatusOn.grid      (row=0,column=1 , padx=5,pady=3)
        CaptchaaStatusOff.grid    (row=0,column=2 , padx=5,pady=3)
        
        
        ##Starting the Bot
        frameStartBot=LabelFrame(self.root)
        frameStartBot.pack(padx=20,pady=universal_y_paddin)
        
        
        StartText= Label(frameStartBot,text="To Start the Bot")
        ButtonBotStart = Button(frameStartBot,text="Click Here",command=StartBot,width = 20)

        StartText.grid      (row=0,column=0 , padx=30,pady=3)
        ButtonBotStart.grid      (row=0,column=1 , padx=5,pady=3)
        return
    
    def destroy(self):
        self.root.destroy()

    def SetDelay(self,value):
        global delay
        delay=value
        print(delay)

    def SetAutoCaptcha(self,value):
        global AutoCaptcha
        AutoCaptcha=value
        print(AutoCaptcha)
        
    def SetBrowserLimit(self,value):
        
        global BrowserLimit
        BrowserLimit=int(value)
        print(BrowserLimit)

    def SaveLoginCredentials(self,Email,Password):
        
        try:
            if Email.get() == "":
                messagebox.showerror("Error","Email not Found")
                return
            if Password.get()  == "":
                messagebox.showerror("Error","Password not Found")
                return
            
            file = open("Credentials.txt","a")
            file.write(str(Email.get()))
            file.write(",")
            file.write(str(Password.get()))
            file.write("\n")
            file.close()
            Email.delete(0,END)
            Password.delete(0,END)
            messagebox.showinfo("Success","Saved the Credentials")
            
        except:
            messagebox.showerror("Error","Can't save the Credentials")    

    def NewLoginCredentials(self,Email,Password):
        Email.delete(0,END)
        Password.delete(0,END)
        

def StartBot():    
    global file
    file = open("Ads-Running-Log.txt","w")
    try:
        if (LoginCredentials is None):
            LoadLoginCredentials()
            if len(LoginCredentials)==0:
                # print('Please Add Credentials by clicking the button above')
                messagebox.showerror("Error","Credentials not Found , Please Add New Accounts")
    except:
        print('Error while loading Credentials in StartBot Functions')

    global Check_Args_Mode
    if Check_Args_Mode==0:
        global app
        app.destroy()
        
    TotalAccounts=len(LoginCredentials['Email'])

    Total_Ad_Accounts_Remaining = TotalAccounts
    
    To_Run_Add = None

    browsers= []
    running_Emails = []
    Expired_IDs= []
    Invalid_Login_IDs = []

    i=0


    # while (i != TotalAccounts - 1 ):
    while ( Total_Ad_Accounts_Remaining > 0 ):
        
        if (Total_Ad_Accounts_Remaining > BrowserLimit):
            To_Run_Add = BrowserLimit
            Total_Ad_Accounts_Remaining = Total_Ad_Accounts_Remaining - BrowserLimit
        else:
            To_Run_Add = Total_Ad_Accounts_Remaining
            Total_Ad_Accounts_Remaining=0
        print("To_Run_Add : "+str(To_Run_Add))
        

    
        alternatepos= True
        while To_Run_Add >0:
            LoginDetails = [
                LoginCredentials['Email'][i],
                LoginCredentials['Password'][i]
            ]


            # print ('checking IDs')
            #Check if Ads had been watched already
            Check_P_IDs = Checking_Processed_ID()

            if SmartLogin == True:
                if Check_P_IDs.checking(LoginCredentials['Email'][i]) == 0:
                    # print('ID already done')
                    if Total_Ad_Accounts_Remaining >0:
                        Total_Ad_Accounts_Remaining-=1
                        print(str(Total_Ad_Accounts_Remaining) + ' Total Pending IDs Remaining')
                        # To_Run_Add-=1
                    else:
                        To_Run_Add-=1

                    i+=1
                    continue
                
                if Check_P_IDs.checking(LoginCredentials['Email'][i]) == 2:
                    print('Today is Sundayy - Holiday!!')
                    return
            
            print ('checking IDs Done')
            
            browser = webdriver.Chrome()
            browser.set_window_size(400,700)

            if alternatepos == True:
                browser.set_window_position(10,10)
                alternatepos=False
            else:
                browser.set_window_position(510,10)
                alternatepos=True

              
            LoadLoginPage(browser)
            LoginEntry(browser,LoginDetails)
            # time.sleep(delay)

            ############################################################################
            if MultipleChecks == True:
                if Check_Correct_Login(browser)==1 or Check_ID_Expired(browser)==1:
                    if Check_Correct_Login(browser)==1:
                        Invalid_Login_IDs.append(LoginCredentials['Email'][i])
                        print("Invalid Login ID Credentials")

                    else:

                        Expired_IDs.append(LoginCredentials['Email'][i])
                        print("Expired ID")

                    if Total_Ad_Accounts_Remaining >0:
                        Total_Ad_Accounts_Remaining-=1
                        print(str(Total_Ad_Accounts_Remaining) + ' Total IDs Remaining')
                    else:
                        To_Run_Add-=1
                    browser.quit()

                else:
                    if (CheckRemainingAds(browser,LoginCredentials['Email'][i])>0):
                        # print('Browser Added into the List')
                        browsers.append(browser)
                        print('this ID is saved to watch ad - {}'.format(LoginCredentials['Email'][i]))
                        running_Emails.append(LoginCredentials['Email'][i])
                        To_Run_Add-=1
                    else:
                        print('Ads already Completed for '+str(LoginCredentials['Email'][i]))
                        bal = CheckBalance(browser)
                        Check_P_IDs.saving(LoginCredentials['Email'][i],bal)
                        if Total_Ad_Accounts_Remaining > 0:
                            Total_Ad_Accounts_Remaining-=1
                            print(str(Total_Ad_Accounts_Remaining) + ' Total IDs Remaining')
                        else:
                            To_Run_Add-=1
                        browser.quit()
            ############################################################################
            
            if (i<TotalAccounts):
                print(str(i)+'=i and TotalAccounts'+ str(TotalAccounts))
                i+=1
            else:
                break

            
            # if (To_Run_Add < TotalAccounts):
            #     To_Run_Add = TotalAccounts

            
            print(str(To_Run_Add) + ' browsers to create')


        j=0
        # print('2- i={} , j={} and k={}'.format(i,j,k))
        alternate = False 
        brow1= None
        browsercount=int(len(browsers))
        # print(browsercount)
        for browser in browsers:
            #print(browsercount)
            if  browsercount==1:
                
                browser2 = webdriver.Chrome()
                browser2.set_window_size(400,700)
                browser2.set_window_position(510,10)
                LoadLoginPage(browser2)
                LoginEntry(browser2,LoginDetails)
                
                WatchMix(browser,browser2)
                browsercount-=1
                # BalanceSavingText(browser,(LoginCredentials['Email'][i]))
                bal = CheckBalance(browser)
                Check_P_IDs.saving(running_Emails[j],bal)
                j += 1

                
            elif alternate == False:
                brow1 = browser
                alternate = True
                
                j += 1
                print('1st browser j incremented = {}'.format(j))
                # print('3- i={} , j={} and k={}'.format(i,j,k))
                continue

            elif alternate == True:
                alternate=False
                WatchMix(brow1,browser)
                browsercount-=2

                print('initaing save')
                bal = CheckBalance(brow1)
                # running_Emails[j]
                Check_P_IDs.saving(running_Emails[j-1],bal)

                bal = CheckBalance(browser)
                Check_P_IDs.saving(running_Emails[j],bal)
                print('ending save')
                # BalanceSavingText(brow1,(LoginCredentials['Email'][i]))
                # BalanceSavingText(browser,(LoginCredentials['Email'][i+1]))
                # print('4- i={} , j={} and k={}'.format(i,j,k))
                # i+=2
                j += 1

                
            
        
        if len(Invalid_Login_IDs) >0 :
            print('{} IDs have Invalid Credentials '.format(len(Invalid_Login_IDs)))
            print('printing Invalid IDs')
            for id in Invalid_Login_IDs:
                print(id)

        if len(Expired_IDs) > 0 :
            print('{} were expired '.format(len(Expired_IDs)))
            print('printing exipred IDs')
            for id in Expired_IDs:
                print(id)
                    
        print('Quiting old IDs')
        for browser in browsers:
            browser.quit()
        browsers= []
        running_Emails = []

        #print('Enter 1 to continue')
        if AutoCaptcha ==0:
            sinnnput = input('Press Enter to continue')

    file.close()
    time.sleep(2)
    print("Quiting Now")
       

def LoadLoginCredentials():
    try:
        global LoginCredentials
        data = pd.read_csv('Credentials.txt', sep=",", header = None ,names=["Email", "Password"] )

        LoginCredentials=data.to_dict()

    #    for cred in LoginCredentials:
    #        print(cred)
    #        print (cred['Email'])
    #        print (cred['Password'])
    #        print('\n')
    #    print("printing login ids count"+str(len(LoginCredentials['Email'])))
    #    print(LoginCredentials['Email'])

        count = str(len(LoginCredentials['Email']))        
        global Check_Args_Mode
        if Check_Args_Mode==0:
            messagebox.showinfo("Success","Loaded {} Accounts Credentials".format(count))
        else:
            print("Success","Loaded {} Accounts Credentials".format(count))
    except:
        print("fail")
        messagebox.showerror("Error","Can't load the Credentials")

def CredentialsDefiner(login):
    text=str(login)
    text=text.split(',')
    email = login[0]
    password = login[1]
    
    return email,password


def LoadLoginPage(browser):
    try:
        browser.get(Web)
        print('Website loaded')
    except:
        print('Website Not Loaded')

def LoginEntry(browser,login):
    log_user,log_pass = CredentialsDefiner(login)
    
    user = browser.find_element_by_xpath("//input[@id    ='sender-email']")
    user.send_keys(log_user)   
    passs = browser.find_element_by_xpath("//input[@type ='password']")
    passs.send_keys(log_pass)


    if AutoCaptcha==1:
        SolveCaptcha(browser)
    else:
        CapEnter = browser.find_element_by_xpath("//input[@class ='captcha-base__input']")
        CapEnter.click()  
        

    print('Please Enter the captacha')

    CheckDashboardLoaded(browser,25) 
    
    # time.sleep(1)
    print('Hope So!! Captacha Done')

def SolveCaptcha(browser):
    global delay
    while True:
        CapEnter = browser.find_element_by_xpath("//input[@class ='captcha-base__input']")
        CapEnter.click()
        
        with open('cap_image.png', 'wb') as file:
            file.write(browser.find_element_by_xpath('//*[@class="captcha-base"]').screenshot_as_png)

        print("cracking captcha")
        start= time.time()
        cap_text = Captcha_detection("cap_image.png")
        end=time.time()
        time_taken = end -start
        time_taken = round(time_taken,1)
        print('cracked captcha is {} in {} seconds '.format(cap_text,time_taken))
        CapEnter.send_keys(cap_text)
        
        login_btn= browser.find_element_by_xpath('//*[@name="lg_btn"]').click()
        time.sleep(delay)
        if  Check_Correct_Login(browser)==1:
            reset= browser.find_element_by_xpath('//*[@class="captcha-base__reset"]').click()
        else:
            return

def WatchAdd(browser):
    x=2
    counter=0
    BrowserChangeInstruction()

    if Check_ID_Expired(browser)==1:
        return
    if Check_Correct_Login(browser)==1:
        return
    
    while x>1:
        try:
            # print('step 1')
            x=int(CheckRemainingAds(browser,1))
        #    print('x=',x)
            if (x!=0):
            #    print('x!=0')
                # print('step 2')
                WatchAddBtnClick(browser)
            # print('Max : ',x)
            
            if(x==1):
                file.write('Website Adds Completed.\n')
                print("Website  Adds Completed.")
                # print('step 3')
            CheckDashboardLoaded(browser,50)
            # print('step 4')
        except:
            
            print("Fault Occured in Watch Add Button - Watch Mix button")
            file.write('Fault Occured in Watch Add Button - Watch Mix button\n')
            

            counter+=1
            if(counter == 3):
                LoadDashboard(browser)
                counter=0

            time.sleep(3)
     
def WatchMix(browser,browser2):
    x=2
    counter=0
    BrowserChangeInstruction()


    if Check_ID_Expired(browser)==1 or Check_ID_Expired(browser2)==1:
        return
    if Check_Correct_Login(browser)==1 or Check_Correct_Login(browser2)==1 :
        return

    while x>1:
        try:
            x=int(CheckRemainingAds(browser,1))
            y=int(CheckRemainingAds(browser2,2))
        #    print('x=',x)
        #    print('y=',y)
            if (x!=0):
            #    print('x!=0')
                WatchAddBtnClick(browser)
            if (y>x):
                x=y
            #    print('Max : ',x)
            #    print('Printing Second Website : ',y)
            
            if (y!=0):
            #    print('y!=0')
                WatchAddBtnClick(browser2)
            if(x==1):
                file.write('Website 1 Adds Completed.\n')
                print("Website 1 Adds Completed.")
                
            if (y==1):
                file.write('Website 2 Adds Completed.\n')
                print("Website 2 Adds Completed.")
                            
                
            CheckDashboardLoaded(browser,50)
            CheckDashboardLoaded(browser2,50)
            
        except:
            
            print("Fault Occured in Watch Add Button - Watch Mix button")
            file.write('Fault Occured in Watch Add Button - Watch Mix button\n')

            counter+=1
            if(counter == 3):
                LoadDashboard(browser)
                LoadDashboard(browser2)
                counter=0

            time.sleep(3)


def WatchAddBtnClick(browser):
    # WatchAddBtn = browser.find_element_by_xpath("//div[@id ='watch-ads']")
    WatchAddBtn = browser.find_element(By.XPATH, '//*[text()="Watch Ads"]')
    WatchAddBtn.click()
 

def LoadDashboard(browser):
    try:
        browser.get(Dashboard_Url)
        print('Dashboard loaded')
    except:
        print('Dashboard Not Loaded')

   
def BalanceSavingText(browser,id):
    try:
        x = CheckRemainingAds(browser)
        CurrentTime=time.strftime('%c', time.localtime())
        # print(CurrentTime)
        file = open("AdWebsiteLogFile.txt","a")
        file.write(CurrentTime)
        file.write('- Balance for id -')
        file.write(str(id))
        file.write('-')
        file.write(str(x))
        file.write('\n')
        file.close()
    except:
        
        print('Error in Saving the Balance to a File')


################ Checks
def Check_Args_Mode(browser):
    try:
        WatchAddBtn = browser.find_element_by_xpath("//div[@id ='watch-ads']")
        
        return 1
    except:
        a=1
 
def Check_ID_Expired(browser):
    try:
        # print("Checking if ID Expired")
        WatchAddBtn = browser.find_element_by_xpath("//input[@id ='payment_date']")
        # WatchAddBtn = browser.find_element(By.XPATH, '//*[text()="Package is expired"]')
        # print ('ID Expired')
        
        return 1
    except:
        # print("Correct ID")
        return 0

def Check_Correct_Login(browser):
    try:
        # print("Checking if ID Expired")
        WatchAddBtn = browser.find_element_by_xpath("//input[@id ='sender-email']")
        # WatchAddBtn = browser.find_element(By.XPATH, '//*[text()="Package is expired"]')
        # print ('Invalid Credentials')
        
        return 1
    except:
        # print("Correct ID")
        return 0

def CheckDashboardLoaded(browser,delay):
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID,'av_ads')))

    except TimeoutException:
        print ("Dashboard is taking too much time for Loading !")

def CheckRemainingAds(browser,id):
    try:
        x=browser.find_element_by_xpath("//h3[@id ='av_ads']").text
        x=x[:2]
        x=int(x)
        print('Remaining ads for ',str(id),' :',x)
        file.write("Remaining ads for ")
        file.write(str(id))
        file.write(" :")
        file.write(str(x))
        file.write('\n')

    #    time.sleep(1)
        return x
    except:
        print("Unknown Ads for ",id," Remaining")
        file.write("Unknown Ads for ")
        file.write(str(id))
        file.write(" Remaining\n")

def CheckBalance(browser):

    while True:
        try:
            balance = browser.find_element_by_xpath("//span[@id ='avail_balance']").text
            balance = balance[:-3]
            # print(balance)
            balance = str(balance)
            balance = balance.replace(',','')
            if balance == 'None':
                continue

            return balance
        except:
            print("Unknown Balance")
    


############ Extra Stuff ###############
def BtnShift():
    keyboard.press(Key.alt)
    keyboard.press(Key.tab)
    keyboard.release(Key.alt)
    keyboard.release(Key.tab)
    
def Magic ():
    print('Magic Working')
    #Enter in seconds
    timer=120
    while timer>0:
        BtnShift()
        time.sleep(0.8)
        timer=timer-1
        if(Check_Args_Mode(browser)==1):
            print("Check_Args_Mode for Browser 1 worked")
            break
        if(Check_Args_Mode(browser1)==1):
            print("Check_Args_Mode for Browser 2 worked")
            break

def BrowserChangeInstruction():
    # print('simply shift between two browsers')
    print('change to any window to let the magic happen')
    # time.sleep(2)
    # print('3 seconds')
    # time.sleep(1)
    # print('2')
    # time.sleep(1)
    # print('1')
    time.sleep(int (delay/2))

def BrowserSelection(bid,browser):
    
    if bid == 3:
        browser.header_overrides = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
    return

############ Main Code ###############
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='CPE Bot v7')
    parser.add_argument('--startbot', type=int, default=0,help='Please add 1 to start bot')
    parser.add_argument('--smartlogin', type=int, default=0,help='Please add 1 to start bot')
    args = parser.parse_args()
    

    smarrrt =args.smartlogin
    if smarrrt== 1:
        print('Running via Smart Login Mode')
        SmartLogin = True

    Check_Args_Mode =args.startbot
    if Check_Args_Mode== 1:
        print('Running via Args')
        StartBot()
    else:
        print('Running via GUI')
        ProgramRunning = True
        global app
        app = BOT_GUI()
        app.root.mainloop()

        
