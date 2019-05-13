from google_images_download import google_images_download
import tkinter
from tkinter import *
from tkinter import messagebox

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
    mainMenu = Tk()
    mainMenu.title("GOOGLE IMAGES DOWNLOAD")
    mainMenu.geometry('500x300')
    mainMenu.resizable(width=False, height=False)
    mainMenu.tk.call('tk', 'scaling', 1.5)

    defaultSearchHistoryValue = StringVar(mainMenu)
    defaultSearchHistoryValue.set(searchHistory[0])
    #++++row 0+++++ Keyword
    l_Keyword = Label(mainMenu, text="Keyword: ").grid(row=0, sticky=W,pady=5)
    e_Keyword = Entry(mainMenu,width=20)
    e_Keyword.grid(row=0, column=1,pady=5)
    
    
    l_Keyword = Label(mainMenu,text="Search History: ").grid(row=0,column=2,pady=5)
    om_SearchHistory = OptionMenu(mainMenu,defaultSearchHistoryValue,*searchHistory)
    om_SearchHistory.grid(row=0,column=3)
    
    #+++++row 1++++ Input Keyword choice
    l_InputOption = Label(mainMenu,text="Search by: ").grid(row=1, column=0,pady=5,sticky=W)
    inputOption = ["History","Entry"]
    defaultInputOption = StringVar(mainMenu)
    defaultInputOption.set(inputOption[0])
    om_InputOption = OptionMenu(mainMenu, defaultInputOption,*inputOption)
    om_InputOption.grid(row=1,column=1,sticky=W)
    
    #+++++row 2+++++ Limit choice 
    l_Limit = Label(mainMenu,text="Limit: ").grid(row=2,column=0,pady=5,sticky=W)
    e_Limit = Entry(mainMenu, width=20)
    e_Limit.grid(row=2,column=1,pady=5)
     #the checkbox
    varLimitOption = IntVar()
    varLimitOption.set(0)
    checkBoxInputOption = Checkbutton(mainMenu,  text="On Limit Parameter",variable= varLimitOption,).grid(row=2,column=2)
    

   #++++++row 3++++++ File extension choice
    l_FormatOption = Label(mainMenu, text="Format Option: ").grid(row=3, column=0, pady=5, sticky=W)
    defaultFormatOption = StringVar(mainMenu)
    defaultFormatOption.set(formatList[0])
    om_FormatOption = OptionMenu(mainMenu, defaultFormatOption,*formatList)
    om_FormatOption.grid(row=3,column=1,pady=5,sticky=W)
    #checkbox
    varFormatOption = IntVar()
    varFormatOption.set(0)
    checkBoxFormatOption = Checkbutton(mainMenu,  text="On Format Parameter",variable= varFormatOption,).grid(row=3,column=2)


    def returnEntry():
        global Records
        global censored_word
        global searchHistory
        #Keywords parameter
        var_inputOption = defaultInputOption.get()
        keywords = ""
        if var_inputOption == inputOption[1]:
            entry = e_Keyword.get().lower()
            print(entry)
            validated = entry_validation(entry, censored_word)
            keyword = entry
            if validated == True:
                store_parameter_value_to_dictionary("keywords",entry,Records)
                print("Keywords stored into the records") #debug
                print(Records)                                                          #debug
            else:
                messagebox.showinfo("WARNING!","You have entered keywords which are OBSCENE\nWe cannot process your request")
                return
        else:
            var_searchHistory = defaultSearchHistoryValue.get()
            print(var_searchHistory) #debug
            store_parameter_value_to_dictionary("keywords",var_searchHistory,Records)
            print(Records) #debug
           
        #Limit parameter
        limitEntry = e_Limit.get()
        print(limitEntry)#debug
        check_store(varLimitOption,"limit",limitEntry,Records)
        #Format parameter
        var_formatOption = defaultFormatOption.get()
        print(var_formatOption)
        check_store(varFormatOption,"format",var_formatOption,Records)
        #download the image
        download_images(Records)
        messagebox.showinfo("NOTIFICATION","Download success")
        if var_inputOption == inputOption[1]:
            print(keywords)
            searchHistory.append(keyword)
            print(searchHistory)
            store_keyword_to_history(searchHistory)
            searchHistory = append_txt_to_array("history_keyword.txt")
            print(searchHistory)
            om_SearchHistory = OptionMenu(mainMenu,defaultSearchHistoryValue,*searchHistory)
            om_SearchHistory.grid(row=0,column=3)
    enterEntry = Button(mainMenu, text= "Enter", command=returnEntry,bg="yellow")
    enterEntry.grid(row=4,column=1,columnspan=2,sticky='nesw')
        
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
#========GUI END=========#

#----------------MAIN-----------------#
Records = {}
searchHistory = append_txt_to_array("history_keyword.txt")
formatList = ["jpg", "gif", "png", "bmp", "svg", "webp", "ico", "raw"]
censored_word = append_txt_to_array("censored_list_of_words.txt")
mainMenu()

