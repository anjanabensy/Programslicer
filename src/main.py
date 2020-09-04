import nltk
import ast
import re
import array as arr;
from _collections import deque
import lexer as lex
import slicer as s
import argparse
import traceback


program = []
endline =''
vars = ''
file =''
linecount=0
Slice = ''
lexer_result = []

line_opt =[]
""" checks whether the given slice criterion is valid with respect to the program to be sliced """
def validat_slice():
    global linecount
    global Slice
    global lexer_result
    count = 0
    c1= 0
    c2= 1
    
    identifier_output = lexer_result[1]
    slicepoint = (str(Slice).split(','))
    lineno = slicepoint[0]
    identifier = slicepoint[1]
    if(int(lineno)>linecount):
        print('Program point does not exist.Please enter a valid line number')
        c1= 1
    for i in identifier_output:
        if(i.count(identifier)>=1):
            c2=0
            break
    if(c2==1):
        print('Variable does not exist within given program point.Please enter a valid variable')
    count = c1+c2
    return count 
     
""" processes the slice criterion and passes the program to the lexer module """
def loadfile(file): 
    global endline
    global linecount
    global Slice
    global lexer_result
    valid = 1
    #mylabel = tkinter.Label(root, text='')
    #mylabel["text"]=''
    f = 'Selected program'
    if(file is not None):
        proglist = list(str(program).split("\n"))
        linecount= 0
        for k in proglist:
            linecount=linecount+1
            f = f+'\n'+str(linecount)+'.'+k
        print(f)
        lexer_result = lex.tokenize_program(program)
        c=0
        while(valid>0):
            c=c+1
            Slice = input("\nEnter the slice criteria (p, V):")
            valid = validat_slice()  
    return [Slice,lexer_result]

""" sends the program and slicing criterion to the slicer module to perform the slicing"""
def getfile(program,Slice,lexer_result,filepath):
        global endline
        global vars
        global line_opt
        #print('slice val is ',slice)
        if program is not None: 
            x = str(Slice).split(',')
            endline = x[0]
            var_value = x[1]
            #res = lex.tokenize_program(program)
            s.check_Indentation(lexer_result[0])
            s.setfirstsliceno(x,lexer_result[0],lexer_result[1],lexer_result[2])
            Finalvals = s.print_Slice(lexer_result[0],lexer_result[1],endline,line_opt,lexer_result[2],filepath,x)
            s.clearvars()
            line_opt.clear()
        return Finalvals
            #print(vars)

""" adds various command line options for the application and processes them """
def argsparseroption():
    global line_opt
    parser = argparse.ArgumentParser(add_help=False)
    
    text = 'Slice criteria Format :s,v where s is the point of interest and v is the variable'
    linetext = 'Prints the slice with the line numbers of the input program'
    filetext = 'Writes the slice to the specified file and saves in src/progfiles folder'
    tracetext = 'Prints the slice with trace back details'
    
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help=text)
    requiredNamed = parser.add_argument_group('Required Arguments')
    requiredNamed.add_argument('--f',help='file to be sliced',required=True)
    parser.add_argument('--l', '--lineno', action='store_true',
                    help=linetext)
    parser.add_argument('--o','--ofile', nargs='?', const='o', type=str,help=filetext)
    parser.add_argument('--t', '--trace', action='store_true',
                    help=tracetext)

    args = parser.parse_args()
    if(args.f):
        c = args.f
    if(args.l):
        line_opt.append('l')
    if(args.o):
        line_opt.append(args.o)
    if(args.t):
        line_opt.append('t')
    return str(c)
    
""" executes the below mentioned functions when the module is executed for the first time """
if __name__ == '__main__':
   
    try:
        filepath = argsparseroption()
        #filepath = input("Enter the filepath:")
        f = open(filepath, 'r')
        program = f.read()
        res = loadfile(program)
        getfile(program,res[0],res[1],filepath)
    except Exception as e:
        print(traceback.format_exc())
        
    