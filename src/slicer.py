import nltk
import ast
import re
import array as arr;
from _collections import deque
import main
import lexer as lex


Final_Slice =[]
st_tree = []
val = []
Slice = []
temp = []
myvals = []
endline = ''
markpoint = 0
parentnodes =[]


#identifies the parent statement of each statement using indentation of each program line
def check_Indentation(indentarray):
    minindent = (min(indentarray))[1]
    global st_tree
        
    for l in range(0,len(indentarray)):
    #if else of elif found search for if with same indent and make it the parent
        if((indentarray[l][2].find('else')>=0) or (indentarray[l][2].find('elif')>=0)):
            #print(indentarray[l])
            for j in range(0,len(indentarray)):
                if(indentarray[j][2].find('if')>=0 and indentarray[j][1]==indentarray[l][1]):
                    stm = indentarray[j][0]
                    st_tree.append([l+1,stm]) 
                    break
        elif(indentarray[l][1]==minindent):
            st_tree.append([l+1,0])
        elif(indentarray[l][1]==indentarray[l-1][1]):
            st_tree.append([l+1,st_tree[l-1][1]])
        elif(indentarray[l][1] > indentarray[l-1][1]):
            st_tree.append([l+1,l])
#if indent is less than prev line find the line in array with same indent and append its parent to this line
        elif(indentarray[l][1] < indentarray[l-1][1]):
            st = indentarray[l]
            for i in range(0,len(indentarray)):
                if(st[1]==indentarray[i][1]):
                    ind = indentarray[i][0]
                    st_tree.append([st[0],st_tree[ind-1][1]])
                    break
               
    
#identifies the last line within the interest point where the variable is defined  
def setfirstsliceno(sv,indentarray,Identifiers_Output,Function_Output):
    global Final_Slice
    global st_tree
    global Slice
    
    Slice = []
    
    endval = int(sv[0])
    varval = sv[1]
    slice = []
    
    c=0
    myvars1 = []
    myvars2 = []
    val1 = 0
    val2 = 0
    
    for i in range(len(Identifiers_Output)-1, -1, -1):
        lno = int(Identifiers_Output[i][0])
        
        if(Identifiers_Output[i][1]==varval and (Identifiers_Output[i][2]=='defined') and int(Identifiers_Output[i][0])<=endval):
            myvars1.append(Identifiers_Output[i][0])
            
        if(Identifiers_Output[i][1]==varval and (Identifiers_Output[i][2]=='du') and int(Identifiers_Output[i][0])<=endval):
            myvars2.append(Identifiers_Output[i][0])
    #take max line of the statements defining a variable      
    if(len(myvars1)>0):
        val1 = max(myvars1)
        Final_Slice.append(val1) 
        Slice.append(val1)
    # check if the defined and used var line > max of defined line    
    if(myvars2):
        for k in myvars2:
            if(k>val1):
                Final_Slice.append(k) 
                Slice.append(k)
        
    #print('The first slice is ',Final_Slice) 
    funcalls(indentarray, Identifiers_Output, endval,Function_Output)
     
def funcalls(indentarray,Identifiers_Output,endline,Function_Output):
    global Final_Slice
    c = get_Variables(Identifiers_Output,endline)
    if(c>0):
        v = get_FinalSlice(Identifiers_Output, endline,indentarray,Function_Output)
        if(v>0):
            funcalls(indentarray, Identifiers_Output, endline,Function_Output)
            
#gets the used variables present in the lines to be included in the slice
def get_Variables(Identifiers_Output,endline):
        global temp
        global Slice
        global myvals
        temp.clear()
        global Final_Slice
        c=0

        for i in range(len(Slice)-1, -1, -1):
            for k in range(len(Identifiers_Output)-1, -1, -1):  
                if(Identifiers_Output[k][0]==Slice[i] and Identifiers_Output[k][2]in['used','fu'] and Identifiers_Output[k][2] not in myvals):
                        temp.append([Identifiers_Output[k][1],Slice[i],Identifiers_Output[k][2]]) 
                        myvals.append([Identifiers_Output[k][1],Slice[i],Identifiers_Output[k][2]]) 
                        c=c+1
    
        #print("temp values :",temp)
        #print("Final ",Final_Slice) 
        return c
    
#gets the program line numbers of the statements where the variables identified by get_variables() are defined
def get_FinalSlice(Identifiers_Output,endline,indentarray,Function_Output):
        global Slice
        global temp
        global Final_Slice
        global st_tree
        c=0
        Slice.clear()
        #print("temp in final",temp)
        #print('endline val',endline)
       
        for i in range(len(temp)-1, -1, -1): 
            myvars1 =[]
            myvars2 = []
            myval1 = 0
            myval2 = 0
            
            for k in range(len(Identifiers_Output)-1, -1, -1):  
                if(temp[i][2]!='fu' and Identifiers_Output[k][1]==temp[i][0] and Identifiers_Output[k][0]<=int(endline) and Identifiers_Output[k][0]<temp[i][1] and Identifiers_Output[k][0] not in Final_Slice):
                    line = Identifiers_Output[k][0]
                    if(Identifiers_Output[k][2] =='du'):
                        myvars1.append(line)
                        Slice.append(Identifiers_Output[k][0])
                    elif(Identifiers_Output[k][2] =='defined'):
                        myvars2.append(line)
                        c=c+1
            
            if(myvars2):
                myval2 = max(myvars2)
                Final_Slice.append(myval2)
                Slice.append(myval2)
                
            if(myvars1):
                for j in myvars1:
                    if(j > myval2):
                        Final_Slice.append(j)
                        Slice.append(j)
        
            if(temp[i][2]=='fu'):
                for k in range(len(Function_Output)-1, -1, -1): 
                    fname = Function_Output[k][1]
                    if(temp[i][0]==fname):
                        Final_Slice.append(Function_Output[k][0])
                        Slice.append(Function_Output[k][0])
                        c=c+1
                        for a in range(len(indentarray)-1, -1, -1): 
                            lno = Function_Output[k][0]
                            if(indentarray[a][2].count('return')>0 and indentarray[lno][1]==indentarray[a][1] and indentarray[a][0]<=endline):
                                Final_Slice.append(indentarray[a][0])
                                Slice.append(indentarray[a][0]) 
                                c=c+1
                            
                    
            
        #print("Final slice ",Final_Slice) 
        #print("new slice ",Slice) 
    #print("new values:",val)
        if(c>0):
            Final_Slice = list(dict.fromkeys(Final_Slice))  
        return c
    
#identifies the parent statements of the statements to be added in slice
def addparent(indentarray,Identifiers_Output,endline,Function_Output):
    global Final_Slice
    global st_tree
    global Slice
   
    Slice = []
    
    Final_Slice = list(dict.fromkeys(Final_Slice))
    Final_Slice.sort()

    result = st_tree.count(st_tree[0]) == len(st_tree)
    if(not(result)):
        for i in Final_Slice:
            val = st_tree[i-1][1]
            if(val!=0 and val not in Final_Slice):
                Final_Slice.append(val)
                Slice.append(val)
                funcalls(indentarray, Identifiers_Output, endline,Function_Output)
                addparent(indentarray,Identifiers_Output,endline,Function_Output)
        Final_Slice.sort()
        
#print the slice based on the command line option selected
def print_Slice(indentarray,Identifiers_Output,endline,arg,Function_Output) :
   
    addparent(indentarray,Identifiers_Output,endline,Function_Output)  
    print("Final Slice values are :", Final_Slice)
    if(arg):
        if(str(arg[0])=='l'):
            print("\n\n ******Final Slice******")  
            for i in Final_Slice:
                print(str(i)+'.'+str(indentarray[i-1][2]))
            
        elif(str(arg[0]).count('.py')==1):
            filename = str(arg[0]).strip()
            with open('progfiles/'+filename, "w") as outF:
                for i in Final_Slice:
                    outF.write(str(indentarray[i-1][2]))
                    outF.write("\n")
                outF.close()
            print('Output file saved under src/progfiles/',filename)
        
        elif(arg.count('t')>0):
            s = Final_Slice.copy()
            s.sort(reverse=True)
            for i in s:
                for j in Identifiers_Output:
                    if(int(j[0])==i):
                        typ = j[2]
                        if(typ=='du'):
                            typ = 'defined and used'
                        print('[',j[0],',\'',j[1],'\',\'',typ,'\']')
                    
            print("\n\n ******Final Slice******")  
            for i in Final_Slice:
                print(str(i),'.',str(indentarray[i-1][2]))       
            
        elif(arg[0]=='o'):
            print("\n\n ******Final Slice******")  
            for i in Final_Slice:
                print(str(indentarray[i-1][2]))
    c = Final_Slice.copy()
    return c

#clears the lists and arrays after every run
def clearvars():
    global Final_Slice
    global st_tree
    Final_Slice.clear()
    st_tree.clear()
    lex.indentarray.clear()
    lex.Identifiers_Output.clear()
    
            

            


    
    
    