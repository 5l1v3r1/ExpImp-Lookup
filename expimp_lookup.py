#!/usr/bin/python
'''
Quick tool that finds Portable Executable files in given directory tree
and looks for export and import names that contain a specified string.

Ruben Ventura [tr3w]
the.tr3w at gmail dot com
(@tr3w_)
'''

import optparse
import sys
import os
from PEace import PEace

def usage():
    print "Usage: %s [0|1|2] \"string_to_search\" [\"directory\" | \"filename\"]"
    print "\t 0 looks for exports"
    print "\t 1 looks for imports"
    print "\t 2 looks for both exports and imports"
    print "\t string_to_search: string to search in export and import names"
    print "\t filename: to scan, if directory given it will scan all contained PEs"
    
    sys.exit(-1)
    
def run(searchExports, searchImports, search_string, path):
    pe_extensions = ['.cpl', '.exe', '.dll', '.ocx', '.sys', '.scr', '.drv', '.efi', '.fon']
    pe = []
    
    try:
        os.listdir(path)
        for r, d, f in os.walk(path):
            for files in f:
                pe_path = "%s/%s" % (r, files)
                if os.path.splitext(files)[1].lower() in pe_extensions:
                    pe.append(pe_path)
    except:
        pe.append(path)
    
    for p in pe:
        try:
            PE = PEace(p)
            print "\n[*] Scanned: %s" % p
            if searchExports:
                for Export in PE.ExportModules or []:
                    if search_string in Export:
                        print "\t[+] Export found: %s" % Export
            if searchImports:
                for Import in PE.ImportModules or []:
                    if search_string in Import:
                        print "\t[+] Import found: %s" % Import
        except Exception:
            print "\n[!] Error occured while searching in %s:" % p
    
    
    print "\n[*] Done!"

if len(sys.argv) != 4:
    usage()
searchExports = searchImports = 0
if sys.argv[1] == '0':
    searchExports = 1
elif sys.argv[1] == '1':
    searchImports = 1
elif sys.argv[1] == '2':
    searchExports = searchImports = 2
else:
    usage()
    
run(searchExports, searchImports, sys.argv[2], sys.argv[3])
