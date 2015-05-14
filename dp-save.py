#!/usr/bin/python3

import sys
import os
import shutil
import time
import stat
"""
dp-save  Using this script you can control and monitor
         the existence and status of chosen python modules
         in the system path (e.g. in 'dist-packages' -folder).
         
Usage:
(a) In Linux the script must be executed by root (or with sudo)
    So the typical launching command is
        sudo python3 dp-save.py myfile.py
        
(b) In Windows the script can be executed by simply double clicking
    the script file.

Remark:
(1) 
"""

# add scripts you want to control to the following list
# this list will be appended by the command line arguments
modulelist = ['mysync_tools.py', 'foo.py']

# add the command line arguments
modulelist += sys.argv[1:]

module = {}
abc = list('abcdefghijklmnopqrstuwxyz'); i=0
for mname in modulelist:
    mfile = os.path.join(os.curdir, mname)
    if os.path.isfile(mfile):
        module[abc[i]] = [mname, mfile, os.path.getmtime(mfile)]
        i += 1

stop = 0;
while stop == 0:
    now = time.asctime(time.localtime(time.time()))
    print('\n\n\nModules now: %s' % (now))
    print("---------------------------------------------------------")
    for m in module:
        print('(%s) %s' % (m, module[m][0]))
    print("\nSystem path folders:")
    print("---------------------------------------------------------")

    plist = sys.path
    n = len(plist)
    for i in range(n):
        print('(%d) %s ' % (i, plist[i]))
        for m in module:
            pfile = os.path.join(plist[i],module[m][0])
            if os.path.isfile(pfile):
                tlm = os.path.getmtime(pfile) # time_of_last_modification
                pftime = time.asctime(time.localtime(tlm))
                if module[m][2] <= tlm:
                    print('      ok (%s) %s [%s]' % (m, module[m][0], pftime))
                else:
                    print('******** (%s) %s [%s]' % (m, module[m][0], pftime))
    print("---------------------------------------------------------")
    ready=0
    while ready==0:
        print("""Select one of the following options:
save a n     (or san, saves the module 'a' to path-folder 'n')
remove a n   (or ran, removes the module 'a' from path-folder 'n')
quit         (or q or enter) """)
        sel = input('Select: ')
        lsel = sel.split()
        if len(lsel)==0:
            stop=1; ready=1; continue
        elif len(lsel)==1:
            lsel = list(lsel[0])
        if lsel[0].startswith('q') or lsel[0].startswith('Q'):
            stop=1; ready=1; continue
        if len(lsel)!=3:
            print("""-------------------
*** Selection has three parts (or q or quit or 'enter') 
    If you give selection as one string then use one character per part.
    If n>10, then separate the parts. """)
            continue
        if not lsel[2].isdigit():
            print("""------------------
*** The third part of the selection is a digit pointing to the list
    of path folders above. Correct the selection.""")
            continue
        m = lsel[1]; 
        if m not in module:
            print("""------------------
*** The second part of the selection is a alphabet character 
    pointin to the list of modules on the top. Correct the selection.
""")
            continue
        i = int(lsel[2])
        if i not in range(len(plist)):
            print("""------------------
*** The number in your selection is invalid. 
    The third part of the selection is a digit pointing to the list
    of path folders above. Correct the selection.
""")
            continue
        if lsel[0].startswith('s') or lsel[0].startswith('S'):
            ready=1
            if i>0:
                dest = os.path.join(plist[i], module[m][0])
                shutil.copy2(module[m][1], plist[i])
        elif lsel[0].startswith('r') or lsel[0].startswith('R'):
            ready=1
            os.remove(os.path.join(plist[i],module[m][0]))
        else:
            print('Check the parts of the selection.')    
