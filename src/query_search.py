#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 19:44:14 2017

@author: chinmay
"""
import tokeniser
from collections import defaultdict
from itertools import groupby
import re
import math
import heapq
import timeit

tit_dic=[]

def file_search(list_of_tokens,l,docs):
    
    global tit_dic
    tfidf=defaultdict(float)
    for words in list_of_tokens:         
        i=0
        n=len(l)
        while(l[i]<words):
            if(i==(n-1)):
                break
            i+=1    
#        print(l[i])
        with open("output_files/output"+str(i)+'.txt','r') as fu:
            for line in fu:
                line=line.strip(' ')
                line=line.strip('\n')
                parts=line.split(',')
                if parts[0]==words:
                    subparts=parts[1].split(';')
                    nodocs=len(subparts)-1
                    temp= math.log10((float(docs)/float(nodocs)))
                    
                    for entry in subparts[:-1]:
                        sumi=0.0
                        if len(subparts)>200000 and 't' not in entry:
                            continue
                        last_level=entry.split(':')
                        tflag=0
                        m=[''.join(g) for _, g in groupby(last_level[1], str.isalpha)]
                        for f in range(0,len(m)):
                            if m[f]=='t':
                                sumi+=float(m[f+1])
                                tflag=1
                            if m[f]=='e':
                                sumi+=0.05*float(m[f+1])
                            if m[f]=='b':
                                sumi+=0.3*float(m[f+1])
                            if m[f]=='c':
                                sumi+=0.1*float(m[f+1])
                            if m[f]=='r':
                                sumi+=0.05*float(m[f+1])
                            if m[f]=='i':
                                sumi+=0.2*float(m[f+1])
#                        print(sumi)
                           
                        sumi=math.log10(1+sumi)
                        if tflag==1:
                                sumi*=(3/len(list_of_tokens))
                        else:
                        	sumi*=temp                            
                        tfidf[last_level[0]]+=sumi
   #        print(tfidf)
        fu.close()               
    x=heapq.nlargest(10, tfidf, key=tfidf.get)
#    print(tit_dic)
    
    for hj in x:
        it=-1
        for slitem in tit_dic:
            it+=1
            if int(hj)<slitem:
                break
        ofp=open("title/file"+str(it),"r")
        for rbc in ofp:
            rbc=rbc.strip(' ')
            rbc=rbc.strip('\n')
            rbc=rbc.split(':')
            if int(rbc[0])==int(hj):
                kkk=""
                for cv in rbc[1:]:
                    kkk+=str(cv)+':'
                kkk=kkk[:-1]
                print(str(hj)+" "+kkk+"\n")
                break
        ofp.close()
#    print(x)

             
def file_search2(go2,setter,l,docs):
    global tit_dic
    fl=0
    tfidf=defaultdict(float)
    k=-1
    for zerolev in go2:
        k+=1
        for words in zerolev:         
            i=0
            n=len(l)
            while(l[i]<words):
                if(i==(n-1)):
                    break
                i+=1    
    #        print(l[i])
            with open("output_files/output"+str(i)+'.txt','r') as fu:
                for line in fu:
                    line=line.strip(' ')
                    line=line.strip('\n')
                    parts=line.split(',')
                    if parts[0]==words:
                        subparts=parts[1].split(';')
                        nodocs=len(subparts)-1
                        temp= math.log10((float(docs)/float(nodocs)))
    #                    print(temp)
                        for entry in subparts[:-1]:
                            if setter[k][0] and 't' not in entry:
                                continue
                            if setter[k][1] and 'e' not in entry:
                                continue
                            if setter[k][2] and 'b' not in entry:
                                continue
                            if setter[k][3] and 'c' not in entry:
                                continue
                            if setter[k][4] and 'r' not in entry:
                                continue
                            if setter[k][5] and 'i' not in entry:
                                continue
                            
                            sumi=0.0
                            last_level=entry.split(':')
                            if fl==1:
                                if last_level[0] not in tfidf.keys():
                                    continue                            
                            m=[''.join(g) for _, g in groupby(last_level[1], str.isalpha)]
                            
                            for f in range(0,len(m)):
                                if m[f]=='t' and setter[k][0]==1:
                                    sumi+=(float(m[f+1]))
                                if m[f]=='e'and setter[k][1]==1:
                                    sumi+=float(m[f+1])
                                if m[f]=='b'and setter[k][2]==1:
                                    sumi+=float(m[f+1])
                                if m[f]=='c'and setter[k][3]==1:
                                    sumi+=float(m[f+1])
                                if m[f]=='r'and setter[k][4]==1:
                                    sumi+=float(m[f+1])
                                if m[f]=='i'and setter[k][5]==1:
                                    sumi+=float(m[f+1])
    #                        print(sumi)
                            sumi=math.log10(1+sumi)
                            sumi*=temp
                            
                            tfidf[last_level[0]]+=sumi
    #        print(tfidf)
            fu.close()      
            fl=1
    x=heapq.nlargest(10, tfidf, key=tfidf.get)
#    print(x,tit_dic[int(x)])
    
    for hj in x:
        it=-1
        for slitem in tit_dic:
            it+=1
            if int(hj)<slitem:
                break
        ofp=open("title/file"+str(it),"r")
        for rbc in ofp:
            rbc=rbc.strip(' ')
            rbc=rbc.strip('\n')
            rbc=rbc.split(':')
            if int(rbc[0])==int(hj):
                kkk=""
                for cv in rbc[1:]:
                    kkk+=str(cv)+':'
                kkk=kkk[:-1]
                print(str(hj)+" "+kkk+"\n")
                break
        ofp.close()
    
def main():
    global tit_dic
    
    with open("title/toffset.txt","r") as cb:
        for sthin in cb:
            sthin=sthin.strip(' ')
            sthin=sthin.strip('\n')
            tit_dic.append(int(sthin))
    
    with open('stopwords.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    content_stop={}
    for i in content:
        content_stop[i]=1
    f.close()
    l=[]
    docs=0
    with open("output_files/offset.txt","r") as fin:
        for line in fin:
            line=line.strip(' ')
            line=line.strip('\n')
            parts=line.split(' ')
            if parts[0]:
                l.append(parts[0])
    fin.close()
    with open("output_files/No_of_docs.txt","r") as ft:
        for line in ft:
            line=line.strip(' ')
            line=line.strip('\n')
            docs=int(line)           
    ft.close()
#    print(l)
    while(1):
        
        print ("Enter the query")
        query=input()
#        if (query[0]=='t' or query[0]=='e' or query[0]=='b'or query[0]=='c' or query[0]=='r'or query[0]=='i')and query[1]==':':
#            print ('yes')
        start = timeit.default_timer()
        if re.search(r'[t|b|c|e|i]:',query[:2]):
            setter=[]
            go=[]
            query=query.strip()
            query=query.strip('\n')
            query_parts=query.split(' ')
            ghj=""
            sett=[0,0,0,0,0,0]
            for item in query_parts:
                if ':' in item:
                    if 't' in item:
                        sett[0]=1
                    if 'e' in item:
                        sett[1]=1
                    if 'b' in item:
                        sett[2]=1
                    if 'c' in item:
                        sett[3]=1
                    if 'r' in item:
                        sett[4]=1
                    if 'i' in item:
                        sett[5]=1
                    setter.append(sett)
                    sett=[0,0,0,0,0,0]
                    if ghj:
                        go.append(ghj)
                    ghj=""
                else:
                    ghj=ghj+' '+item
#                    print(ghj)
            if ghj:
                go.append(ghj)               
            
            go2=[]
            for some in go:
                some=some.strip()
                list_of_tokens=tokeniser.tokenise(some,123,'q',content_stop)
                if list_of_tokens:
                    go2.append(list_of_tokens)               
            file_search2(go2,setter,l,docs)  
        
        else:
            list_of_tokens=tokeniser.tokenise(query,123,'q',content_stop)
            if list_of_tokens:
                file_search(list_of_tokens,l,docs)            
            else:
                print("Query invalid")
        stop = timeit.default_timer()
        print (stop - start)
    


if __name__ == "__main__":                                            
    main()