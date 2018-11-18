#!/usr/bin/env python3
import sys
from code_check3 import CodeCheck
def main():
    code_checker = CodeCheck("C:\FILES and WORKS\CODE\Python\GOBANG\\better_score4.py", 15)
    if not code_checker.check_code():
        print(code_checker.errormsg)
    else:
        print('pass')

if __name__ == '__main__':
    main()