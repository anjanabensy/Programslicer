The program slicer could be executed by running the main.py file. Please run the file with help command to understand the command line options provided with the tool. The program slicer takes a programpath as input and asks for a slicing criterion. The slicing criterion(V,p) contains a variable V and a point of interest p. It then generates a sub-program that contains only those program statements relevant to the computation of the variable specified in the slicing criterion.

Help Function Syntax: python main.py -h
 
 Example Execution
 
 C:\Users\asus\git\PythonProgramSlicer\PythonProgramSlicer\src> python main.py --f progfiles\whileloop.py

Selected program

1.def main() :

2.    sum = 0

3.    i = 1

4.    while(i <= 10):

5.        sum=i+1

6.        i=i+1

7.    print(sum)

8.    print(i)

Enter the slice criteria (p, V):8,i

******Final Slice ['8', 'i'] of progfiles\whileloop.py ******

def main() :

    i = 1
    
    while(i <= 10):
    
        i=i+1
