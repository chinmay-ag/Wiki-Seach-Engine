#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 12:32:12 2017
@author: chinmay
"""

import xml.sax
import re
import timeit
import tokeniser
import Index_creation
from collections import defaultdict
import sys

global_dic=defaultdict(dict)
title_dic=defaultdict(str)
temp_file_count=0
document_count=0
title_count=0
title_file_count=0
#regular expressions..
reg_el='== *External +[lL]inks *== *\n(.*?\n)*?\n'
reg_ref='== *References *== *\n(.*?\n)*?\n'
reg_ib='\{\{Infobox(.*?\n)+?\}\}'
reg_cat='\[\[ *Category:.*?\]\]'
#######################################
#e:external links
#i:infobox
#t:title
#r:references
#c:category
#b:bodytext

with open('stopwords.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 
content_stop={}
for i in content:
    content_stop[i]=1


class WikiHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.prevData=""
        self.id=""
        self.iden=""
        self.text = ""
        self.external_links=""
        self.infobox=""
        self.title=""
        self.references=""
        self.category=""
        self.count=0
        
    
    def startElement(self, tag, attributes):
        self.CurrentData = tag  

    def endElement(self, tag):
        
        global global_dic
        global title_dic
        global content
        
        tempory_list=[]
              
        if self.CurrentData=="text":
             try:                 
                 self.external_links = re.search(reg_el,self.text).group()
                 #call tokeniser here
                 tempory_list=tokeniser.tokenise(self.external_links,self.id,'e',content_stop)
                 if tempory_list:    
                     for item in tempory_list:
                         if item not in global_dic:
                            global_dic[item][self.iden]=[0,0,0,0,0,0]
                         if self.iden in global_dic[item].keys():
                             global_dic[item][self.iden][2]+=1
                         else:
                             global_dic[item][self.iden]=[0,0,1,0,0,0]
                 tempory_list=[]
                 self.external_links=""                 
             except:
                 self.external_links=""
             
             try:                 
                 self.infobox = re.search(reg_ib,self.text).group()
                 #call tokeniser here
                 tempory_list=tokeniser.tokenise(self.infobox,self.id,'i',content_stop)
                 if tempory_list:
                     for item in tempory_list:
                         if item not in global_dic:
                            global_dic[item][self.iden]=[0,0,0,0,0,0]
                         if self.iden in global_dic[item].keys():
                             global_dic[item][self.iden][4]+=1
                         else:
                             global_dic[item][self.iden]=[0,0,0,0,1,0]
                 tempory_list=[]
                 self.infobox=""                 
             except:
                 self.infobox=""             
             
             try:
                 self.references=re.search(reg_ref,self.text).group()
                 tempory_list=tokeniser.tokenise(self.references,self.id,'r',content_stop)
                 if tempory_list:
                     for item in tempory_list:
                         if item not in global_dic:
                            global_dic[item][self.iden]=[0,0,0,0,0,0]
                         if self.iden in global_dic[item].keys():
                             global_dic[item][self.iden][5]+=1
                         else:
                             global_dic[item][self.iden]=[0,0,0,0,0,1]
                         
                 tempory_list=[]
                 self.references=""
             except:
                 self.references=""
             temp=[]
             temp=re.findall(reg_cat,self.text)
             self.category=''.join(temp)
             #call tokeniser here
             tempory_list=tokeniser.tokenise(self.category,self.id,'c',content_stop)             
             if tempory_list:    
                 for item in tempory_list:
                     if item not in global_dic:
                            global_dic[item][self.iden]=[0,0,0,0,0,0]  
                     if self.iden in global_dic[item].keys():
                         global_dic[item][self.iden][1]+=1
                     else:
                         global_dic[item][self.iden]=[0,1,0,0,0,0]
                     
                 tempory_list=[]
             self.category=""
             
             self.text=re.sub(reg_el," ",self.text)
             self.text=re.sub(reg_ib," ",self.text)
             self.text=re.sub(reg_ref," ",self.text)
             self.text=re.sub(reg_cat," ",self.text)
             self.text=re.sub(r'runfile.*Desktop/ire\'\)'," ",self.text)
             
             tempory_list=tokeniser.tokenise(self.text,self.id,'b',content_stop)
             if tempory_list:
                 for item in tempory_list:
                     if item not in global_dic:
                            global_dic[item][self.iden]=[0,0,0,0,0,0]
                     if self.iden in global_dic[item].keys():
                         global_dic[item][self.iden][0]+=1
                     else:
                         global_dic[item][self.iden]=[1,0,0,0,0,0]
             tempory_list=[]
#             print (self.text)    
             self.text=""
             
         
            
        if self.CurrentData=="id" and self.prevData == "ns":
            global title_count
            global title_file_count
            self.iden=self.id
            title_dic[self.iden]=self.title
            title_count+=1
            if title_count>=1000:
                fp=open("title/file"+str(title_file_count),"w")
                title_file_count+=1
                for lkey in title_dic:
                    fp.write(str(lkey)+":"+str(title_dic[lkey])+"\n")
                fp.close()
                laf=open("title/toffset.txt","a+")   
                laf.write(str(lkey)+'\n')
                laf.close()
                title_count=0
                title_dic=defaultdict(str)
                
#            print(self.prevData,":",self.CurrentData,self.title)
            tempory_list=tokeniser.tokenise(self.title,self.id,'t',content_stop)    
            if tempory_list:
#                 print ('yed')
                 for item in tempory_list:
                     if item not in global_dic:
                         global_dic[item][self.iden]=[0,0,0,0,0,0]  
                     if self.iden in global_dic[item].keys():
                         global_dic[item][self.iden][3]+=1
                     else:
                         global_dic[item][self.iden]=[0,0,0,1,0,0]
                        
            tempory_list=[]
        self.prevData=self.CurrentData
        
        if tag=="page":
            global temp_file_count
            global document_count
            numm=50*1024*1024
            self.count+=1
            document_count+=1
            if (sys.getsizeof(global_dic) > numm):
                Index_creation.write_to_file("file"+str(temp_file_count),global_dic)
                global_dic=defaultdict(dict)
                temp_file_count+=1
                self.count=0
            
    def characters(self, content):
        if self.CurrentData == "text":  
            self.text += content  
        elif self.CurrentData == "id"and len(content.strip())>0:  
            self.id = content
        elif self.CurrentData == "title" and len(content.strip())>0:

            self.title=content
            
start = timeit.default_timer()
                    
if ( __name__ == "__main__"):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

Handler = WikiHandler()
parser.setContentHandler( Handler )
#parser.parse(sys.argv[1])
parser.parse("enwiki-latest-pages-articles-multistream.xml")
Index_creation.write_to_file("file"+str(temp_file_count),global_dic)
with open("output_files/No_of_docs.txt","w") as ft:
        ft.write(str(document_count))

fp=open("title/file"+str(title_file_count),"w")
title_file_count+=1
for lkey in title_dic:
    fp.write(str(lkey)+":"+str(title_dic[lkey])+"\n")
fp.close()
laf=open("title/toffset.txt","a+")   
laf.write(str(lkey)+'\n')
laf.close()
title_count=0
title_dic=defaultdict(str)
Index_creation.merge_files(temp_file_count)
stop = timeit.default_timer()
print (stop - start)
