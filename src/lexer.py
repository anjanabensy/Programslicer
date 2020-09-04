import nltk
import ast
import re
import array as arr;
import main
from _collections import deque
import slicer as slice


global Identifiers_Output

Final_Slice =[]
Identifiers_Output = []
Keywords_Output = []
Symbols_Output = []
Conditionals_Output= []
Operators_Output = []
Numerals_Output = []
Headers_Output = []
Variable_Output = []
String_Output = []
Function_Output = []
val = []
global Main_Program

indentarray=[]
st_tree = []
tokens = []

count = 0
c = 0

RE_Identifiers = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
RE_String = "^[a-zA-Z0-9_]+[a-zA-Z0-9_]*"
RE_Conditionals = "if|else|elif|while|do|for"
RE_Integer = "^[-+]?[0-9]+$"
RE_Decimal = '[+-]?[0-9]+\.[0-9]+'
RE_Special_Characters = "[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\""
RE_Headers = "(?m)^(?:from[ ]+(\S+)[ ]+)?import[ ]+(\S+)[ ]*$"
RE_Keywords = ['False','None','True','and','as','assert','break','class','continue','split','input','def','del','elif','else','except','finally','for','from','global','if','import','in','is','not','or','pass','raise','return','try','while','with','eof!','read','input','print','write','insert','append','pop','remove','yield']

RE_Operators = "(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)"

#analyze each word of every program statement and categorizes them as identifier,number,operator based on regex
def tokenize_program(program):
    global tokens
    global indentarray
    global Identifiers_Output
    
    c = 0   
    prog = program.split('\n')

    match_counter = 0
    Slice =[]
    Source_Code=[]
    Identifiers_Output=[]
    n=1
    for line in prog:
        Source_Code.append(line)    
        indentarray.append([n,len(re.findall("^ *", line)[0]),line])
        n=n+1

    myvals = []
     
    display_counter = 0
    nm = 1
    for line in Source_Code:
        c=c+1
        #print('val of c is',c)
        #print("The line no",c," is ",line)
        if(line.startswith("import")):
            print(line)
            tokens = nltk.word_tokenize(line)
        else:
            tokens = nltk.wordpunct_tokenize(line)

        stack = deque()
        for i in tokens:
            stack.append(i)
        
        ctr = stack.copy()
        myline = indentarray[c-1][2]
        singlequote_str =re.findall(r'\'(.+?)\'',myline)
        doublequote_str =re.findall(r'\"(.+?)\"',myline)
        stringlist =[]
        if(singlequote_str):
            for i in singlequote_str:
                stringlist.extend(nltk.wordpunct_tokenize(i))
        if(doublequote_str):
            for i in doublequote_str:
                stringlist.extend(nltk.wordpunct_tokenize(i))
            
        assignvar = ['=','=\'\'','=""','="','=\'','=[]','*=','+=','-=','/=']
        arraymethod = ['append','pop','insert','remove']
        
        #fetching the variables on RHS and LHS
        val = [value for value in line if value in assignvar] 
        if(val):
            val = str(val[0])
            ind = line.index(val)
            rhs = []
            lhs = []
            rtok = nltk.wordpunct_tokenize(line[0:ind].strip())
            for r in rtok:
                rhs.append(r)
            ltok = nltk.wordpunct_tokenize(line[ind+1:len(line)].strip())
            for ls in ltok:
                lhs.append(ls)
        
        while(stack):
            v = stack.pop()
            if(re.findall(RE_Conditionals, v )):
                Conditionals_Output.append([c,v])
            elif(re.findall(RE_Integer, v ) or re.findall(RE_Decimal, v )):
                Numerals_Output.append([c,v])
            elif(re.findall(RE_Operators, v )):
                Operators_Output.append([c,v]) 
            elif(re.findall(RE_Headers, v )):
                Headers_Output.append([c,v])
            elif(re.findall(RE_Special_Characters, v )):
                Symbols_Output.append([c,v])
            elif(RE_Keywords.count(v)>0):
                Keywords_Output.append([c,v])
            elif((ctr.count('if')>0 or ctr.count('while')>0 or ctr.count('elif')>0) and re.findall(RE_Identifiers, v ) and v not in Keywords_Output):
                Identifiers_Output.append([c,v,'used'])  
            elif(stringlist.count(v)>0 and re.findall(RE_String, v )):
                String_Output.append([c,v,'String']) 
            elif(ctr.count('print')>0 and re.findall(RE_Identifiers, v )):
                Identifiers_Output.append([c,v,'used'])
            elif(re.findall(RE_Identifiers, v ) and ctr.count('return')>0):
                Identifiers_Output.append([c,v,'used'])  
            #checks if the array and value appended to array method is used or defined
            elif(re.findall(RE_Identifiers, v ) and any(item in ctr for item in arraymethod)):
                if(any(item in stack for item in arraymethod)):
                    Identifiers_Output.append([c,v,'used'])  
                else:  
                    Identifiers_Output.append([c,v,'du']) 
            #checks if it's a function definition
            elif(re.findall(RE_Identifiers, v ) and v==ctr[1]  and ctr[0]=='def' and re.findall(RE_Identifiers,ctr[0])):
                Function_Output.append([c,v,'defined'])  
            #categorizes the function arguments in function definition as function variables
            elif(re.findall(RE_Identifiers, v ) and ctr[0]=='def' and stack.count('(')>=1 and v!= ctr[1]):
                Identifiers_Output.append([c,v,'fvars'])
            #catogerizes the function call return variables 
            elif(re.findall(RE_Identifiers, v ) and (ctr.count('(')>0  and stack.count('(')==0)or (ctr.count('()')>0  and stack.count('()')==0)):
                    if(stack.count('=')>0 or ctr.count('=')==0):
                        Identifiers_Output.append([c,v,'fu'])
                    elif(ctr.count(v)>1):
                        Identifiers_Output.append([c,v,'du']) 
                    else:
                        #if function assigned to var categorize that var as defined
                        Identifiers_Output.append([c,v,'defined']) 
            #checks if variable is within a function call and categorize as used 
            elif(re.findall(RE_Identifiers, v ) and stack.count('(')>=1 and re.findall(RE_Identifiers,ctr[0])):
                if(ctr.count(v)>1):
                    Identifiers_Output.append([c,v,'du']) 
                else:
                    Identifiers_Output.append([c,v,'used']) 
            #checks if variable is the defined variable of for loop statement
            elif(re.findall(RE_Identifiers, v ) and ctr.count('for')>0 and ctr[1]==v):
                Identifiers_Output.append([c,v,'defined']) 
            elif(re.findall(RE_Identifiers, v ) and ctr.count('for')>0 and ctr[len(ctr)-2]==v):
                Identifiers_Output.append([c,v,'used'])
            #categorizes the variables as used or defined based on assignment operator
            elif(any(item in ctr for item in assignvar)): 
                #check if variable in in RHS is present on LHS as well
                if(lhs.count(v)>0 and not(any(item in stack for item in assignvar))):
                    Identifiers_Output.append([c,v,'du']) 
                #check if variable in in LHS is present on RHS as well
                elif(rhs.count(v)>0 and any(item in stack for item in assignvar)):
                    Identifiers_Output.append([c,v,'du']) 
                #check if var is on RHS and statement contains any increment decrement operator
                elif(not(any(item in stack for item in ['*=','+=','-=','/='])) and any(item in ctr for item in ['*=','+=','-=','/=']) and re.findall(RE_Identifiers, v )):
                    Identifiers_Output.append([c,v,'du']) 
                 
                elif(any(item in stack for item in assignvar) and re.findall(RE_Identifiers, v )):
                    Identifiers_Output.append([c,v,'used'])   
                elif(v in assignvar or v in [0-9]):
                    pass
                elif(re.findall(RE_Identifiers, v )):
                    Identifiers_Output.append([c,v,'defined'])            
    
    #print(Identifiers_Output)
    #print(Function_Output)
   # print(Numerals_Output)
   # print(Conditionals_Output)
    return [indentarray,Identifiers_Output,Function_Output]
   