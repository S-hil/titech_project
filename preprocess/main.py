#!/usr/bin/env python
# coding: utf-8
import io
from narocessor import Processor

if __name__ == '__main__':
    fout = io.StringIO()
    #fin = open("sample.txt", "r")
    fin = io.StringIO("JSON here\n「テスト1」です。「再帰『テスト2』です。」なり。\n")
    
    p = Processor(fin, fout)
    p.preprocess()
    print(fout.getvalue())
    
    fin.close()
    fout.close()
