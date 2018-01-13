# Project Milestone 
# Name: Mikit Kanakia
# Original Creation Date: 2/20/2017
# Original Modification Date: 2/21/2017
# Description: The program performs bag of words and outputs HTML file by using web scrapping and libraries.
# Assumptions:
# 1: UTF-8 Encoding is done
# 2: Run the program in Windows Machine
# 3: Program will take 2 minutes to execute and one file index.html will be generated and several inventors and keyword files as well.
# 4: Program has 3 input files:
# a: Milestone4_Bigrams_MikitKanakia.csv --> Bigrams file for compund words
# b: Milestone4_Sub_MikitKanakia.csv --> Substitution file for stemming
# c: Milestone4_Del_MikitKanakia.txt --> noise file to remove the stop words


import re
import csv
import requests
from bs4 import BeautifulSoup


def main():
    print("Milestone 4")
    aanm = "carnegie+mellon" #to be used in the project as the input
    alinks_list = []
    final_links = []
    stopwords = []
    string0 =""
    string1 =""
    bag = []
    bag_all = []
    bag_final = []

    file_content_list = []
    
    #Lists
    appl_no_list = [] #main
    appl_name_list = [] #main
    appl_abstract_list = [] #main
    appl_inventors_list = [] #for key words ---- to be changed for single one
    appl_inventors_list_appl_no = []
    
    temp_Inventor3=[]
    temp_Inventor4=[]
    distinct_inventor= [] #main
    distinct_inventor_application= [] #main contains numbers
    dis_int_count = 0

    bag_distinct = [] #main
    bag_applno_list = []
    distinct_bag_applno = [] #main contains numbers
    dis_word_count = 0
    


    #All files
    
    bigrams_file = open('Milestone4_Bigrams_MikitKanakia.csv', 'r', encoding='utf-8', errors = 'ignore')
    subfile = open('Milestone4_Sub_MikitKanakia.csv', 'r', encoding='utf-8', errors = 'ignore')
    noisefile = open('Milestone4_Del_MikitKanakia.txt', 'r', encoding='utf-8', errors = 'ignore')
    
    # opeing the main page and parsing
    html = requests.get("http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.html&r=0&p=1&f=S&l=50&Query=aanm%2F%22carnegie+mellon%22+AND+PD%2F4%2F1%2F2016-%3E6%2F30%2F2016&d=PG01")
    html_text = html.text
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    
    #finding all the hyperlinks
    for link in soup.find_all('a'):
        alink = str(link.get('href'))
        if alink.find(aanm) != -1 and alink.find("ebiz") == -1: #to scrap the links of patent applications
            alinks_list.append(link.get('href'))

    #distinct hyperlinks
    for i in alinks_list:
        if i not in final_links: 
            final_links.append(i)
               
    #appending the website
    for i in range(0,len(final_links)):
        final_links[i] = "http://appft.uspto.gov" + final_links[i]   

    
    # start of single application process
    #for i in range(0,len(final_links)):
    for i in range(0,15):
        html = requests.get(final_links[i])
        html_text = html.text
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text()

        file_content_list.append(text) #for the keywords task


        

        
        # reading the data from the file
        #print(soup.prettify())
        #print(text)

        #Application No

        app_no_index = text.index("Appl. No.")
        get_app_no = text[app_no_index:app_no_index+24]
        set_app_no = ""      
        
        for i in get_app_no.split("\n"):
            set_app_no+=i.strip() + " "

        set_app_no = set_app_no.replace("Appl. No.:","").strip()

        #print("Application Number:")
        #print(set_app_no)

        appl_no_list.append(set_app_no.strip())


        #Application Name

        get_app_name = soup.find_all('font')[3].getText().strip()
        set_app_name = ""      
        
        for i in get_app_name.split("\n"):
            set_app_name+=i.strip() + " "

        #print("Application Name:")
        #print(set_app_name.strip())
        appl_name_list.append(set_app_name.strip().upper())



        #Abstract

        get_abstract = soup.find_all('p')[1].getText()
        set_abstract = ""      
        
        for i in get_abstract.split("\n"):
            set_abstract+=i.strip() + " "

        #print("Abstract:")
        #print(set_abstract.strip())

        appl_abstract_list.append(set_abstract.strip())
        
        #Inventors
        get_inventors = text[text.find("Inventors:"):text.find("Applicant:")]
        set_inventors = ""      
        
        for i in get_inventors.split("\n"):
            set_inventors+=i.strip() + " "
        
        set_inventors = set_inventors.replace("Inventors:","").strip() + ";"
        
        #print("Inventors:")
        #print(set_inventors)


        appl_inventors_list.append(set_inventors)

    #inventors processing

    for j in range(0,len(appl_inventors_list)):

        temp_Inventor3 = appl_inventors_list[j].split(";")

        # splitting the names

    
        for i in range(0,len(temp_Inventor3)-1,3):

            #Stripping and storing
            temp_Inventor3[i] = temp_Inventor3[i].strip()
            temp_Inventor3[i+1] = temp_Inventor3[i+1].strip()
        
            temp_Inventor3[i+1] = re.sub('[A-Z]\.',"",temp_Inventor3[i+1]).strip() #Removing initials of middlename by regex 
            temp_Inventor3[i+1] = re.sub('\s[A-Za-z]+$',"",temp_Inventor3[i+1]) #Removing middle name by regex
   

            #logic to remove Upper Case to Capitalize
        
            if temp_Inventor3[i+1].isupper() == True: #fistname and middlename
                temp_Inventor3[i+1] = temp_Inventor3[i+1].strip().capitalize()
        
            if temp_Inventor3[i].isupper() == True:  #last name
                temp_Inventor3[i] = temp_Inventor3[i].strip().capitalize()

            final_invent_name = temp_Inventor3[i+1].strip().capitalize() + " " + temp_Inventor3[i].strip().capitalize()
        

            temp_Inventor4.append(temp_Inventor3[i+1].strip().capitalize() + " " + temp_Inventor3[i].strip().capitalize())   
    
    
            temp_invent = [final_invent_name,j]
            appl_inventors_list_appl_no.append(temp_invent)
            


    for i in temp_Inventor4:
        if i not in distinct_inventor: #new inventor add application no
            distinct_inventor.append(i)
            distinct_inventor_application.append([appl_inventors_list_appl_no[dis_int_count][1]])
        else: # already exist increase the counter
            index = distinct_inventor.index(i)
            distinct_inventor_application[index].append(appl_inventors_list_appl_no[dis_int_count][1])

        dis_int_count+=1

    
    #Keywords processing do not modify till the end ------------------------


    for j in range(0,len(file_content_list)):
        string0 = file_content_list[j]
        bag = [] #empty bag for every pass
        
        #removing whitespaces
        string0 = string0.replace('-',"_")
        string0 = string0.replace('\n'," ")
        string0 = string0.replace('\t'," ")
        string0 = string0.replace('\r'," ")
        string0 = string0.replace('\f'," ")
        string1 = re.sub( r'\s+', ' ', string0)

        #punctuation cleaning
        punct = [".", ",","?","!", "@","$","%","&","*","(",")","-","+","=", "/","\"","'","[","]","{","}",";",":","|","^","<",">","#","`","~","\\"]

        for i in punct:
            string1 = string1.replace(i,"")

        #numbers cleaning
        numbers = ["1", "2","3","4", "5","6","7","8","9","0"]

        for i in numbers:
            string1 = string1.replace(i,"")

        #read the bigrams file
        csv_bigrams_file = csv.reader(bigrams_file)

        #replace bigram words
        for i in csv_bigrams_file:
            string1 = string1.replace(i[0],i[1])

        #read the substitute file
        csv_subfile = csv.reader(subfile)

        #replace substitute words
        for i in csv_subfile:
           string1 = string1.replace(" "+i[0]+" ", " "+i[1]+" ")

        #bag of words
        bagofwords = string1.split(" ")

        #stripping and lower case for bag of words
        for i in range(0,len(bagofwords) -1):
            bagofwords[i] = bagofwords[i].strip().lower()
            bagofwords[i] = bagofwords[i].strip("_")

        #distinct values
        for i in bagofwords:
            if i not in bag: 
               bag.append(i)
   
        #clean the noise using list
        #read the noise file
        for line in noisefile:  
            stopwords.append(line.strip())

        #removing white spaces from the list
        bag.remove('')
    
        for i in stopwords:
            if (i in bag) == True:
                bag.remove(i)

        for i in range(0,len(bag)):
            temp_word = [bag[i],j]
            bag_applno_list.append(temp_word)
   
        bag_all += bag

        #end of keywords processing for a single application

    

    for i in bag_all:
        if i not in bag_distinct: #new keyword add application no
            bag_distinct.append(i)
            distinct_bag_applno.append([bag_applno_list[dis_word_count][1]])
        else: # already exist increase the counter
            index = bag_distinct.index(i)
            distinct_bag_applno[index].append(bag_applno_list[dis_word_count][1])

        dis_word_count+=1

    

    #Keywords processing end --------------------------------------------


    # final writing of the files

    print(len(bag_distinct))

    
    #write the index.html
    #preparing the output file    
    outfile = open("index.html", "w" , encoding='utf-8', errors = 'ignore')

    line = "<html>\n<head>\n<title>U.S. Patent Application</title>\n</head>\n<body>\n<h1>U.S. Patent Application</h1>\n<br>\n"
    outfile.write(line)

    line = "<h2><u>Keywords</u></h2>\n<ul>\n"
    outfile.write(line)

    for i in range(0,len(bag_distinct)):
         line = "<li><a href =\""+ bag_distinct[i] + ".html\">"+ bag_distinct[i]+"</a></li>" + '\n'
         outfile.write(line)

    line = "</ul>\n<br>\n"
    outfile.write(line)
    
    line = "</body>\n</html>"
    outfile.write(line)               
    bigrams_file.close()
    subfile.close()
    noisefile.close()
    outfile.close()
    print("index.html is created.")



    #preparing keywords file

    
    #for i in range(0,len(bag_distinct)):
    for i in range(0,3): # change during submission

        outfile = open(bag_distinct[i]+".html", "w" , encoding='utf-8', errors = 'ignore')  

        line = "<html>\n<head>\n<title>"+bag_distinct[i]+"</title>\n</head>\n<body>\n<h1>"+bag_distinct[i]+"</h1>\n<br>\n"
        outfile.write(line)

        line = "<a href = \"index.html\">HOME</a><hr>\n<br>\n"
        outfile.write(line) 
        print(bag_distinct[i])
        
        for j in range(0,len(distinct_bag_applno[i])):
            
            index = distinct_bag_applno[i][j]
      
            
            line = "Application No: " + appl_no_list[index] +"<br>\n<br>\n"
            outfile.write(line)
         
            line = "Application Name: " + appl_name_list[index]+"<br>\n<br>\n"
            outfile.write(line)

            inventorlink = ""

            for k in range(0,len(distinct_inventor_application)):
                if index in distinct_inventor_application[k]:
                    inventorlink += "<a href = \"" + distinct_inventor[k] + ".html\">" + distinct_inventor[k] + "</a> "

            line = "Inventors: " + inventorlink +"<br>\n<br>\n"
            outfile.write(line)
                    
            line = "Abstract: " + appl_abstract_list[index] +"<br>\n<br>\n"
            outfile.write(line)

            line = "<hr>\n<br>\n"
            outfile.write(line)  
        
        
        line = "</body>\n</html>"
        outfile.write(line)               



        outfile.close()

    print("keywords created.")

 
    #preparing inventors file


    for i in range(0,len(distinct_inventor)):

        outfile = open(distinct_inventor[i]+".html", "w" , encoding='utf-8', errors = 'ignore')  

        line = "<html>\n<head>\n<title>"+distinct_inventor[i]+"</title>\n</head>\n<body>\n<h1>"+distinct_inventor[i]+"</h1>\n<br>\n"
        outfile.write(line)
        
        line = "<a href = \"index.html\">HOME</a><hr>\n<br>\n"
        outfile.write(line) 
        
        for j in range(0,len(distinct_inventor_application[i])):
            
            index = distinct_inventor_application[i][j]
      
            
            line = "Application No: " + appl_no_list[index] +"<br>\n<br>\n"
            outfile.write(line)
       
            line = "Application Name: " + appl_name_list[index]+"<br>\n<br>\n"
            outfile.write(line)

            line = "Abstract: " + appl_abstract_list[index] +"<br>\n<br>\n"
            outfile.write(line)

            line = "<hr>\n<br>\n"
            outfile.write(line) 
        
        
        line = "</body>\n</html>"
        outfile.write(line)               



        outfile.close()

    print("inventors created.")


    

#main function
main()
