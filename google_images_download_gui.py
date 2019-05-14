from google_images_download import google_images_download
import tkinter
from tkinter import *
from tkinter import messagebox
import os
#------------CENSORSHIPS----------#
#Appending the list of words into array
def append_txt_to_array(txt_file):
    word_list = []
    f = open(txt_file,"r")
    for x in f:
        word_list.append(x.rstrip("\n").lower())
        word_list = list(set(word_list))
        word_list.sort()
    f.close()
    return word_list

#check keywords in word list
def entry_validation(keywords,word_list):
    for word in word_list:
        if word == keywords.lower():
            return False
    return True
#==CENSORSHIPS FUNCS END==#

#------HISTORY KEYWORD-----#
def store_keyword_to_history(keyword_array):
    f = open("history_keyword.txt","w+")
    
    for keyword in keyword_array:
        f.write("%s\n"%keyword)
    print("storing to history done")
    f.close()

#==HISTORY KEYWORD FUNCS END==#
    
#==GUI==#
def mainMenu():
    global searchHistory
    global mainMenuCounter
    global Records
    global formatList
    global userRightList
    global languageList
    global inputOption

    mainMenu = Tk()
    mainMenu.title("Google Images Download")
    mainMenu.geometry('500x300')
    mainMenu.resizable(width=False, height=False)
    mainMenu.tk.call('tk', 'scaling', 1.5)

    
    #++++row 0+++++ Keyword
    l_Keyword = Label(mainMenu, text="Keyword: ").grid(row=0, sticky=W,pady=5)
    e_Keyword = Entry(mainMenu,width=20)
    e_Keyword.grid(row=0, column=1,pady=5,sticky='ew')

    defaultSearchHistoryValue = StringVar(mainMenu)
    file_is_empty = check_empty_file("history_keyword.txt")
    print(file_is_empty)
    if file_is_empty==False:
        defaultSearchHistoryValue.set(searchHistory[0])
        l_Keyword = Label(mainMenu,text="Search History: ").grid(row=0,column=2,pady=5)
        om_SearchHistory = OptionMenu(mainMenu,defaultSearchHistoryValue,*searchHistory)
        om_SearchHistory.grid(row=0,column=3)
    
    #+++++row 1++++ Input Keyword choice
    l_InputOption = Label(mainMenu,text="Search by: ").grid(row=1, column=0,pady=5,sticky=W)
    inputOption = ["Entry","History"]
    print(inputOption)
    defaultInputOption = StringVar(mainMenu)
    defaultInputOption.set(inputOption[0])
    om_InputOption = OptionMenu(mainMenu, defaultInputOption,*inputOption)
    om_InputOption.grid(row=1,column=1,sticky='ew')

    #checkbox Numbering
    varNumberingOption = IntVar()
    varNumberingOption.set(0)
    checkBoxNumberingOption = Checkbutton(mainMenu,  text="No Numbering",variable= varNumberingOption,).grid(row=1,column=2)
    
    #+++++row 2+++++ Limit choice 
    l_Limit = Label(mainMenu,text="Limit: ").grid(row=2,column=0,pady=5,sticky=W)
    e_Limit = Entry(mainMenu, width=20)
    e_Limit.grid(row=2,column=1,pady=5,sticky='ew')
     #the checkbox
    varLimitOption = IntVar()
    varLimitOption.set(0)
    checkBoxInputOption = Checkbutton(mainMenu,  text="On Parameter",variable= varLimitOption,).grid(row=2,column=2)
    

   #++++++row 3++++++ File extension choice
    l_FormatOption = Label(mainMenu, text="Format Option: ").grid(row=3, column=0, pady=5, sticky=W)
    defaultFormatOption = StringVar(mainMenu)
    defaultFormatOption.set(formatList[0])
    om_FormatOption = OptionMenu(mainMenu, defaultFormatOption,*formatList)
    om_FormatOption.grid(row=3,column=1,pady=5,sticky='ew')
    #checkbox
    varFormatOption = IntVar()
    varFormatOption.set(0)
    checkBoxFormatOption = Checkbutton(mainMenu,  text="On Parameter",variable= varFormatOption,).grid(row=3,column=2)

    #++++++row 4++++++ user right choice 
    l_UserRightOption = Label(mainMenu, text="User Right: ").grid(row=4, column=0, pady=5, sticky=W)
    defaultUserRightOption = StringVar(mainMenu)
    defaultUserRightOption.set(userRightList[0])
    om_UserRightOption = OptionMenu(mainMenu, defaultUserRightOption,*userRightList)
    om_UserRightOption.configure(width=20)
    om_UserRightOption.grid(row=4,column=1,pady=5,sticky=W)
    #checkbox
    varUserRightOption = IntVar()
    varUserRightOption.set(0)
    checkBoxUserRightOption = Checkbutton(mainMenu,  text="On Parameter",variable= varUserRightOption,).grid(row=4,column=2)

    #++++++row 5++++++ language
    l_LanguageOption = Label(mainMenu, text="Language: ").grid(row=5, column=0, pady=5, sticky=W)
    defaultLanguageOption = StringVar(mainMenu)
    defaultLanguageOption.set(languageList[0])
    om_LanguageOption = OptionMenu(mainMenu, defaultLanguageOption,*languageList)
    om_LanguageOption.configure(width=20)
    om_LanguageOption.grid(row=5,column=1,pady=5,sticky=W)
    #checkbox
    varLanguageOption = IntVar()
    varLanguageOption.set(0)
    checkBoxLanguageOption = Checkbutton(mainMenu,  text="On Parameter",variable= varLanguageOption,).grid(row=5,column=2)

    def returnEntry():
        global Records
        global censored_word
        global searchHistory
        global inputOption
        try:
            #Keywords parameter
            var_inputOption = defaultInputOption.get()
            keywords = ""
            print(inputOption)
            if var_inputOption == inputOption[0]:
                entry = e_Keyword.get().lower()
                print(entry)
                validated = entry_validation(entry, censored_word)
                keyword = entry
                if validated == True:
                    if keyword=="":
                            messagebox.showinfo("WARNING!","Keyword must not be empty\nPlease enter something")
                            return
                    else:    
                        store_parameter_value_to_dictionary("keywords",entry,Records)
                        print("Keywords stored into the records") #debug
                        print(Records)                                                          #debug
                else:
                    messagebox.showinfo("WARNING!","You have entered keywords which are OBSCENE\nWe cannot process your request")
                    return
            else:
                var_searchHistory = defaultSearchHistoryValue.get()
                if var_searchHistory=="":
                        messagebox.showinfo("WARNING!","History is empty\nPlease use the entry")
                        return
                print(var_searchHistory) #debug
                store_parameter_value_to_dictionary("keywords",var_searchHistory,Records)
                print(Records) #debug

            #Numbering parameter
            if check_box_state(varNumberingOption)==True:
                Records["no_numbering"]=True
             #Limit parameter
            limitEntry = e_Limit.get()
            print(limitEntry)#debug
            check_store(varLimitOption,"limit",limitEntry,Records)
            #Format parameter
            var_formatOption = defaultFormatOption.get()
            print(var_formatOption)
            check_store(varFormatOption,"format",var_formatOption,Records)
            #User Right parameter
            var_userRightOption = defaultUserRightOption.get()
            print(var_userRightOption)
            check_store(varUserRightOption,"usage_rights",var_userRightOption,Records)
            #Language parameter
            var_languageOption = defaultLanguageOption.get()
            print(var_languageOption)
            check_store(varLanguageOption,"language",var_languageOption,Records)
            #download the image
            download_images(Records)
            messagebox.showinfo("NOTIFICATION","Download success")
            if var_inputOption == inputOption[0]:
                print(keywords)
                searchHistory.append(keyword)
                print(searchHistory)
                store_keyword_to_history(searchHistory)
                searchHistory = append_txt_to_array("history_keyword.txt")
                print(searchHistory)
                om_SearchHistory = OptionMenu(mainMenu,defaultSearchHistoryValue,*searchHistory)
                om_SearchHistory.grid(row=0,column=3)
            print(file_is_empty)
            if file_is_empty==True:
                defaultSearchHistoryValue.set(searchHistory[0])
                l_Keyword = Label(mainMenu,text="Search History: ").grid(row=0,column=2,pady=5)
                om_SearchHistory = OptionMenu(mainMenu,defaultSearchHistoryValue,*searchHistory)
                om_SearchHistory.grid(row=0,column=3)
        except ValueError:
            messagebox.showinfo("WARNING!","There is some value entered not intended for it's field\nPlease check your input again")
    enterEntry = Button(mainMenu, text= "Enter", command=returnEntry,bg="yellow")
    enterEntry.grid(row=7,column=1,columnspan=2,sticky='nesw')
        
    mainMenu.mainloop()

#Other functions
def check_box_state(checkBoxVariable):
    if checkBoxVariable.get()==1:
        return True
    return False

def store_parameter_value_to_dictionary (parameter,value,dictionary):
    dictionary[parameter] = value

def check_store(checkBoxVariable,parameter,value,dictionary):
    if check_box_state(checkBoxVariable)==True:
        store_parameter_value_to_dictionary(parameter,value,dictionary)
        print("stored")
        print(dictionary)

def download_images(dictionary):
    global Records
    response = google_images_download.googleimagesdownload()
    arguments = Records
    paths = response.download(arguments)


def check_empty_file(txt_file):
    if  os.stat(txt_file).st_size==0:
        return True
    return False
#========GUI END=========#

#----------------MAIN-----------------#
Records = {}
inputOption=[]
searchHistory = append_txt_to_array("history_keyword.txt")
formatList = ["jpg", "gif", "png", "bmp", "svg", "webp", "ico", "raw"]
userRightList =["labeled-for-reuse-with-modifications","labeled-for-reuse","labeled-for-noncommercial-reuse-with-modification","labeled-for-nocommercial-reuse"]
languageList = ["Arabic", "Chinese (Simplified)", "Chinese (Traditional)", "Czech", "Danish", "Dutch", "English", "Estonian. Finnish", "French", "German", "Greek", "Hebrew", "Hungarian", "Icelandic", "Italian", "Japanese", "Korean", "Latvianm", "Lithuanian", "Norwegian", "Portuguese", "Polish", "Romanian", "Russian", "Spanish", "Swedish", "Turkish"]
censored_word = append_txt_to_array("censored_list_of_words.txt")
mainMenu()

