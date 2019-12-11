#!/usr/bin/env python
# coding: utf-8
import io
from narocessor import Processor

if __name__ == '__main__':
    fout = io.StringIO()
    fin = open("sample.txt", "r")
    
    p = Processor(fin, fout)
    p.preprocess()
    
    fin.close()
    fout.close()
