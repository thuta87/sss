import urllib.request
import xmltodict
import json
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from datetime import date

from fpdf import FPDF

did='DATAID'
fname='FIRST_NAME'
sname='SECOND_NAME'
tname='THIRD_NAME'
doc='TYPE_OF_DOCUMENT'
num='NUMBER'
rnum='REFERENCE_NUMBER'
ldate="LISTED_ON"
ltype="UN_LIST_TYPE"
des="DESIGNATION"
nat="NATIONALITY"
pobj={}
reporttxt="The Consolidated List includes all individuals and entities subject to measures imposed by the Security Council. The inclusion of all names on one Consolidated List is to facilitate the implementation of the measures, and neither implies that all names are listed under one regime, nor that the criteria for listing specific names are the same. For each instance where the Security Council has decided to impose measures in response to a threat, a Security Council Committee manages the sanctions regime. Each sanctions committee established by the United Nations Security Council therefore publishes the names of individuals and entities listed in relation to that committee as well as information concerning the specific measures that apply to each listed name."
slink="https://www.un.org/securitycouncil/content/un-sc-consolidated-list"
ftxt="For all comments and questions concerning all sanctions lists, including the United Nations Consolidated List, kindly contact the Secretariat via the email address: sc-sanctionslists@un.org."

with urllib.request.urlopen('https://scsanctions.un.org/resources/xml/en/consolidated.xml') as url:
    data = url.read()

data = xmltodict.parse(data)

consolidated_list=data['CONSOLIDATED_LIST']['INDIVIDUALS']['INDIVIDUAL']
consolidated_groups_list=data['CONSOLIDATED_LIST']['ENTITIES']['ENTITY']


class Person:
    def __init__(individual,name,person_t, person_n,person_rnum,person_listed,person_un_type,person_nationality,person_designation) :
        individual.name=name
        individual.person_t= person_t
        individual.person_n= person_n
        individual.person_rnum=person_rnum
        individual.person_listed=person_listed
        individual.person_un_type=person_un_type
        individual.person_nationality=person_nationality
        individual.person_designation=person_designation

# cell height
ch = 8
class PDF(FPDF):
    def __init__(self):
        super().__init__()
    def header(self):
        self.image('./logo.jpg', x = 80, y = 2, w = 50, h = 25, type = 'JPG')    
        #self.set_font('Arial', 'B', 16)
        #self.cell(0, 20, 'Sanction Screening Result', 0, 1, 'R')
        #self.cell(0, 16, str(date.today()), 0, 1, 'R')

        #self.set_font('Arial', 'B', 12)
        #self.cell(0, 20, 'GGI NIPPON LIFE', 0, 1, 'C')
        #self.cell(0, 16, 'Life Insurance', 0, 1, 'C')
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 12)
        self.cell(0, 8, f'Page {self.page_no()}', 0, 0, align='C')

def export(searchquery,searchresult):    

    pdf = PDF()
    pdf.add_page()
    today=str(date.today())
    
    pdf.set_font('Arial', 'B', 16)
    #pdf.cell(w=0, h=20, txt="Sanction Screening Result", ln=1)  
    pdf.cell(0, 40, 'UN Sanction Screening Result', 0, 1, 'C')
    #pdf.cell(0, 16, today , 0, 1, 'R')  
    pdf.set_font('Arial', '', 12)
    pdf.cell(w=30, h=ch, txt="Date: ", ln=0)
    pdf.cell(w=30, h=ch, txt=str(date.today()), ln=1)
    

    pdf.cell(w=30, h=ch, txt="Search Query: ", ln=0)
    pdf.cell(w=30, h=ch, txt=searchquery, ln=1)

    pdf.cell(w=30, h=ch, txt="Search Result: ", ln=0)
    pdf.cell(w=30, h=ch, txt=str(searchresult), ln=1)
    pdf.ln(ch)
    pdf.multi_cell(w=0, h=5, txt=reporttxt)
    pdf.ln(ch)
    pdf.multi_cell(w=0, h=5, txt=ftxt)
    pdf.ln(ch)
    pdf.multi_cell(w=0, h=5, txt=slink)
    pdf.output(f'./Sanction Screening Results.pdf', 'F')

def check(_inputval,_dobj):
    olist.configure(state='normal')
    olist.delete('1.0',END)
    sresult=0
    #pattern2 = '\d+' #extract digit from string
    dobj=json.loads(_dobj)
    if len(_inputval)>0 :
        if not all(x.isspace() for x in _inputval):
            if all(x.isalpha() or x.isspace() for x in _inputval):   #not include digit and include space for name
                for pid in dobj.keys():
                    pattern1 = dobj[pid]['Name']
                    result=_inputval.upper() in pattern1
                    if result==True:
                        sresult+=1
                        pmsg="Full Name: "+dobj[pid]['Name']+"\n"+"Passport no: "+dobj[pid]['Number']+"\n"+"Listed on: "+dobj[pid]['Listed_Date']+"\n"+"Reference no: "+dobj[pid]['Ref_Number']+"\n"+"UN List Type: "+dobj[pid]['UN_Type']+"\nNationality: "
                        for n in dobj[pid]['Nationality']:                       
                            if type(n) is str: 
                                pmsg += "(" +str(dobj[pid]['Nationality'].index(n)+1) +") " + n.replace('\n',' ')  +"\n"
                            else:
                                for ns in n:
                                    pmsg += "(" +str(n.index(ns)+1) +") " + ns.replace('\n',' ')  +"\n"
                        
                        pmsg+="Designation: "
                        for d in dobj[pid]['Designation']:
                            if type(d) is str:
                                pmsg += "(" +str(dobj[pid]['Designation'].index(d)+1) +") " + d.replace('\n',' ')  +"\n"
                            else:
                                for ds in d:
                                    pmsg += "(" +str(d.index(ds)+1) +") " + ds.replace('\n',' ') +"\n"
                                            
                        pmsg+="\n\n"                
                        olist.insert(INSERT,pmsg)                
            else:
                for pid in dobj.keys():
                    pattern2 = dobj[pid]['Number']

                    result=_inputval in pattern2
                    
                    if result==True:
                        sresult+=1
                        pmsg="Full Name: "+dobj[pid]['Name']+"\n"+"Passport no: "+dobj[pid]['Number']+"\n"+"Listed on: "+dobj[pid]['Listed_Date']+"\n"+"Reference no: "+dobj[pid]['Ref_Number']+"\n"+"UN List Type: "+dobj[pid]['UN_Type']+"\nNationality: "
                        for n in dobj[pid]['Nationality']:
                            if type(n) is str: 
                                pmsg += "(" +str(dobj[pid]['Nationality'].index(n)+1) +") " + n.replace('\n',' ')  +"\n"
                            else:
                                for ns in n:
                                    pmsg += "(" +str(n.index(ns)+1) +") " + ns.replace('\n',' ')  +"\n"
                        
                        pmsg+="Designation: "    
                        for d in dobj[pid]['Designation']:
                            if type(d) is str:
                                pmsg += "(" +str(dobj[pid]['Designation'].index(d)+1) +") " + d.replace('\n',' ')  +"\n"
                            else:
                                for ds in d:
                                    pmsg += "(" +str(d.index(ds)+1) +") " + ds.replace('\n',' ')  +"\n"
                                            
                        pmsg+="\n\n"                  
                        olist.insert(INSERT,pmsg)
            if sresult==0:
                pmsg="No records found."
                olist.insert(INSERT,pmsg)
        bexport.configure(state='normal')    
    else:
        pmsg="Please input full name or passport numbers to sanction screening."
        olist.insert(INSERT,pmsg)
        bexport.configure(state='disabled')
    olist.configure(state='disabled')

    return sresult

for person in consolidated_list:
    full_name=""
    idnum=""   
    idtype=""
    lidate=""
    ultype=""
    ref=""
    desin=[]
    nation=[]

    
    if nat in person.keys():
        nation.append(person[nat]['VALUE'])        


    if des in person.keys():
        desin.append(person[des]['VALUE'])
    
    if fname in person.keys() or rnum in person.keys() or ldate in person.keys() or ltype in person.keys():
        full_name += person[fname]
        ref=person[rnum]
        lidate=person[ldate]
        ultype=person[ltype]

    if sname in person.keys():
        if sname is not None: 
            if person[sname] is not None: 
                full_name += " "
                full_name += person[sname]
    
    if tname in person.keys():
        if tname is not None:
            if person[tname] is not None:
                full_name += " "            
                full_name += person[tname]
                       
    if 'INDIVIDUAL_DOCUMENT' in person.keys():        
        if person['INDIVIDUAL_DOCUMENT'] is not None: 
            if len(person['INDIVIDUAL_DOCUMENT'])>0 and len(person['INDIVIDUAL_DOCUMENT'])==1 :
                for indoc in person['INDIVIDUAL_DOCUMENT']:
                    if type(indoc) is not str:                        
                        if indoc is not None:
                            if 'Passport' in indoc['TYPE_OF_DOCUMENT'] :
                                idtype=indoc['TYPE_OF_DOCUMENT']
                                if 'NUMBER' in indoc:
                                    if indoc['NUMBER'] is not None:  
                                        idnum=indoc['NUMBER'] 
            else:
                for indoc2 in person['INDIVIDUAL_DOCUMENT']:
                    if type(indoc2) is str:
                        if person['INDIVIDUAL_DOCUMENT'][indoc2] == 'Passport':
                            if 'NUMBER' in person['INDIVIDUAL_DOCUMENT']:
                                idnum=person['INDIVIDUAL_DOCUMENT']['NUMBER']                          
                    else:
                        if indoc2 is not None:
                            if indoc2['TYPE_OF_DOCUMENT']=="Passport":
                                for idc in indoc2:                            
                                    if idc=="NUMBER":
                                        idnum=indoc2[idc]
    p=Person(full_name,idtype,idnum,ref,lidate,ultype,nation,desin)  
 
    pobj[person[did]]={"Name":p.name,"Number":p.person_n,"Ref_Number":p.person_rnum,"Listed_Date":p.person_listed,"UN_Type":p.person_un_type,"Nationality":p.person_nationality,"Designation":p.person_designation}
    
    jobj=json.dumps(pobj)
    

#creating the application main window.   
window = tk.Tk()
#Entering the event main loop  
window.title("United Nations Security Council Consolidated List Screening System")
window.geometry('1200x1000')

lblinput = tk.Label(text="Please enter the name or passport number: ",font=('Helvetica', 12, 'bold'))
lblinput.pack()

uinput=tk.Entry(window,width=50)

olist=scrolledtext.ScrolledText(window,width=300,height=80)
olist.configure(state='disabled')

bsubmit=tk.Button(text="Search",width=40, command=lambda: check(uinput.get(),jobj))

bexport=tk.Button(text="Export", width=40, command=lambda: export(uinput.get(),check(uinput.get(),jobj)))
bexport.configure(state="disabled")

uinput.pack()

bsubmit.pack(padx=5,pady=10,side=tk.TOP)
bexport.pack(padx=5,pady=10,side=tk.TOP)

olist.pack()

window.mainloop()