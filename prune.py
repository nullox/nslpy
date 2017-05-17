#!/usr/bin/python3
import os
import sys
import string
import random
from os import listdir
from os.path import isfile, join

# secure file erasure utility
#
# examples of invoke:
#
# 1. erases all files contained in the given directory
# => python3 prune.py /home/userident/outdated_finance_data/
#
# 2. erases all files contained in the given directory AND sub directories
# => python3 prune.py /home/userident/outdated_finance_data/ -r
#
# 3. erases all files contained in the given directory exclusing files with
#    substrings 2017, 2016, 2015 (retaining last three years)
# => python3 prune.py /home/userident/outdated_finance_data/ 2017,2016,2015
#
# 4. erases all files contained in the given directory with 10 passes
# => python3 prune.py /home/userident/outdated_finance_data/ 10
#
# 5. erases all files contained in the given directory AND sub directories
#    with 10 passes
# => python3 prune.py /home/userident/outdated_finance_data/ -r 10

# provides an input to backtrack upon erroneous invoke
def query(question, default="no"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

# generates a 32-character length string (UPPERCASE)
def randomstr():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(256))

# secure erasure
def prune(fp, passes):
    nfp = "";
    try:
        filelent = os.stat(fp)
        blen = filelent.st_size
        fileh = open(fp, "r+b")
        for p in range(passes):
            fileh.seek(0)
            fileh.write(os.urandom(blen))
        fileh.close()

        path_t = fp.split(os.path.sep)
        for p in range(passes):
            rstr = randomstr()[:len(path_t[len(path_t)-1])]
            path_t[len(path_t) - 1] = rstr
            nfp = ""
            for t in path_t:
                nfp = nfp + t + os.path.sep
            nfp = nfp[:-1]
            os.rename(fp, nfp)
            fp = nfp

        os.remove(fp)
        print(str(passes*blen) +" bytes written: "+ nfp)

    except NotImplementedError:
        print("host has no installed source of randomness")

    except:
        print("unknown error occurred")

# tests whether param is numeric
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#... script entry point
if len(sys.argv) < 2:
    print("no entry point or exclusions provided")
    sys.exit()

if not os.path.exists(sys.argv[1]):
    print("path parameter is invalid")
    sys.exit()

if not os.path.isdir(sys.argv[1]):
    print("path parameter is not a directory")
    sys.exit()

# confirmation
if not query("please confirm you wish to proceed?"):
    print("operation cancelled...")
    sys.exit()

# filename snippets to exclude in the prune
exclusionCount = 0
exclusions = []
if len(sys.argv) >= 3:
    if not is_number(sys.argv[2]):
        exclusions = sys.argv[2].split(",")

# recursive mode, will trawl down sub directories, use with caution
recurse = False
for flag in sys.argv:
    if flag == "-r":
        recurse = True

# default pass parameter, may be increased if desired
defaultpasses = 2
pass_param_placement = 0
for flag in sys.argv:
    if is_number(flag):
        defaultpasses = flag

# single directory mode
if not recurse:
    files = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
    for f in files:
        if not any(x in sys.argv[1] + f for x in exclusions):
            prune(sys.argv[1] + f, defaultpasses)
    sys.exit()
else:
    # prune all contents
    for sd, d, filelist in os.walk(sys.argv[1]):
        for f in filelist:
            filepath = sd + os.sep + f
            if not any(x in filepath for x in exclusions):
                prune(filepath, defaultpasses)
            else:
                exclusionCount += 1
    # remove tree parts
    if exclusionCount == 0:
        for sd, d, filelist in os.walk(sys.argv[1], topdown=False):
            os.rmdir(sd)
