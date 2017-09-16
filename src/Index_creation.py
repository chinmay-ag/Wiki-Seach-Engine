#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 17:18:05 2017

@author: chinmay
"""

from collections import defaultdict
import heapq
from itertools import groupby
import sys

def write_to_file(filename,smalldic):
    a = open("folder/"+filename,"w+")
    keys=smalldic.keys()
    keys=sorted(keys)
    
    for i in keys:
        s=""
        s=s+i+","
        for j in sorted(list(smalldic[i].keys())):
            s=s+j+":"
            temporary=smalldic[i][j]
            if temporary[3] > 0:
                s=s+"t"+str(temporary[3])
            if temporary[2] > 0:
                s=s+"e"+str(temporary[2])
            if temporary[0] > 0:
                s=s+"b"+str(temporary[0])
            if temporary[1] > 0:
                s=s+"c"+str(temporary[1])
            if temporary[5] > 0:
                s=s+"r"+str(temporary[5])
            if temporary[4] > 0:
                s=s+"i"+str(temporary[4])
            s=s+";"
        a.write(s+"\n")
    a.close()
    
def add_to_heap(fpointer,l,heap,file_ptrs,dic):
    l=l.strip()
    l=l.strip('\n')
    flag=0
    parts=l.split(',')
    
    if parts[0] in dic:
        flag=1
    
    subparts=parts[1].split(';')
    for entry in subparts[:-1]:
        last_level=entry.split(':')
#        print(parts[0],last_level[0],last_level[1])
        dic[parts[0]][int(last_level[0])]=[0,0,0,0,0,0] 
        m=[''.join(g) for _, g in groupby(last_level[1], str.isalpha)]
        for f in range(0,len(m)):
            if m[f]=='t':
                dic[parts[0]][int(last_level[0])][0]+=int(m[f+1])
            if m[f]=='e':
                dic[parts[0]][int(last_level[0])][1]+=int(m[f+1])
            if m[f]=='b':
                dic[parts[0]][int(last_level[0])][2]+=int(m[f+1])
            if m[f]=='c':
                dic[parts[0]][int(last_level[0])][3]+=int(m[f+1])
            if m[f]=='r':
                dic[parts[0]][int(last_level[0])][4]+=int(m[f+1])
            if m[f]=='i':
                dic[parts[0]][int(last_level[0])][5]+=int(m[f+1])
                            
    if flag==1:
        return True
    else:
        heapq.heappush(heap,parts[0])
        file_ptrs[parts[0]]=fpointer
        return False
    
def write(output_buffer,wf):
#    keys=output_buffer.keys()
#    keys=sorted(keys)
#    
#    for i in keys:
#        s=""
#        s=s+i+","
#        for j in sorted(list(output_buffer[i].keys())):
#            s=s+str(j)+":"
#            temporary=output_buffer[i][j]
#            if temporary[0] > 0:
#                s=s+"t"+str(temporary[0])
#            if temporary[1] > 0:
#                s=s+"e"+str(temporary[1])
#            if temporary[2] > 0:
#                s=s+"b"+str(temporary[2])
#            if temporary[3] > 0:
#                s=s+"c"+str(temporary[3])
#            if temporary[4] > 0:
#                s=s+"r"+str(temporary[4])
#            if temporary[5] > 0:
#                s=s+"i"+str(temporary[5])
#            s=s+";"
#        print (output_buffer)
        wf.write(output_buffer)
    
def merge_files(temp_file_count):
    heap=[]
    counter=0
    fm=open("output_files/offset.txt","a+")
    num=512*512
    num5=5*num
    file_ptrs=defaultdict()
    output_buffer=""
    dic=defaultdict(dict)
    gh=''

    wf=open("output_files/output"+str(counter)+".txt","a+")
    for item in range (0,temp_file_count+1):
        fp=open("folder/file"+str(item),"r")
        line=''
        line=fp.readline()
        while line!='' and add_to_heap(fp,line,heap,file_ptrs,dic):
            line=fp.readline()
#    print("hi1")
    while len(heap):
#        print("hi2")
        lines=heapq.heappop(heap)
        
        if wf.tell()>num5:
            write(output_buffer,wf)
            output_buffer=""
            wf.close()
            counter+=1
            wf=open("output_files/output"+str(counter)+".txt","a+")
            fm.write(gh+' '+str(counter-1)+'\n')
        
#        print("hi3")
        gh=lines
        pointer=file_ptrs[lines]
#        print("hi33")

  ###################################      #
        temp_str=""
        temp_str+=str(lines)+','
#        print(lines)
#        hjk=input()
        for abc in dic[lines]:
#            print(abc)
            temp_str+=str(abc)+":"
            tempoe=dic[lines][abc]
            if tempoe[0] > 0:
                temp_str=temp_str+"t"+str(tempoe[0])
            if tempoe[1] > 0:
                temp_str=temp_str+"e"+str(tempoe[1])
            if tempoe[2] > 0:
                temp_str=temp_str+"b"+str(tempoe[2])
            if tempoe[3] > 0:
                temp_str=temp_str+"c"+str(tempoe[3])
            if tempoe[4] > 0:
                temp_str=temp_str+"r"+str(tempoe[4])
            if tempoe[5] > 0:
                temp_str=temp_str+"i"+str(tempoe[5])
            temp_str=temp_str+";"
            
#        print("hi4")
 ######################################
        output_buffer+=temp_str
        output_buffer+='\n'
#        output_buffer[lines]=dic[lines]        
        #check size of buffer and write to dic
        if sys.getsizeof(output_buffer) > num:
            write(output_buffer,wf)
            output_buffer=""
        #also check the file size whether new file is required or not
#        print("hi5")
        file_ptrs.pop(lines)
        dic.pop(lines)
        line=''
        line=pointer.readline()
        while line!='' and add_to_heap(pointer,line,heap,file_ptrs,dic):
            line=pointer.readline()            
#        print("hi6")
    
#    output_buffer=defaulldic
    write(output_buffer,wf)
    wf.close()    
#    print (mapper)    
    fm.write(gh+' '+str(counter)+'\n')
    
    
        