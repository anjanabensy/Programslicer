import unittest
import main
import os.path
import lexer as lex


class Test(unittest.TestCase):
        
    def test_case1(self):
        desired_slice = [1, 3, 4, 5]
        filename = "progfiles\\whileloop.py"
        file = open(filename, "r")
        program =file.read()
        file.close()
        res = lex.tokenize_program(program)
        result = main.getfile(program,'8,sum',res,filename)
        self.assertEqual(desired_slice,result,'While Test case failed')
    
    def test_case2(self):
        desired_slice =  [4, 5, 6, 12, 13, 14, 15]
        filename = "progfiles\\ifelseprog.py"
        file = open(filename, "r")
        program =file.read()
        file.close()
        res = lex.tokenize_program(program)
        result = main.getfile(program,'15,a',res,filename)
        self.assertEqual(desired_slice,result,'If else Test case failed')
        
    def test_case3(self):
        desired_slice =   [1, 2, 3, 4, 5, 6, 9]
        filename = "progfiles\\funcall.py"
        file = open(filename, "r")
        program =file.read()
        file.close()
        res = lex.tokenize_program(program)
        result = main.getfile(program,'9,z',res,filename)
        self.assertEqual(desired_slice,result,' Function call Test case failed')
        
    def test_case4(self):
        desired_slice =   [1, 2, 3, 4, 5, 6, 8]
        filename = "progfiles\\uinput.py"
        file = open(filename, "r")
        program =file.read()
        file.close()
        res = lex.tokenize_program(program)
        result = main.getfile(program,'9,sum',res,filename)
        self.assertEqual(desired_slice,result,' User Input Test case failed')
        
    def test_case5(self):
        desired_slice =   [1, 2, 3, 4, 5, 7, 9]
        filename = "progfiles\\nested.py"
        file = open(filename, "r")
        program =file.read()
        file.close()
        res = lex.tokenize_program(program)
        result = main.getfile(program,'12,a',res,filename)
        self.assertEqual(desired_slice,result,' Nested If Test case failed')
        
    def test_case6(self):
        desired_slice =   [1, 3, 4, 5]
        filename = "progfiles\\forloopandlist.py"
        file = open(filename, "r")
        program =file.read()
        file.close()
        res = lex.tokenize_program(program)
        result = main.getfile(program,'6,y',res,filename)
        self.assertEqual(desired_slice,result,'List Test case failed')
   
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()