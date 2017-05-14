#!/usr/bin/python3
import sys
import os

if len(sys.argv) < 3:
    print("no entry point or extensions provided")
    sys.exit()

if not os.path.isdir(sys.argv[1]):
    print("entry point does not exist")
    sys.exit()

if ( len(sys.argv[2]) == 0 ):
    print("extention list is empty")
    sys.exit()

loc = 0
fc = 0
filedata = ''

# disqualify lines beginning with
disqualifiers = ["/", "#"]
if ( len(sys.argv) >= 4 )
    disqualifiers = sys.argv.split(",")

# test on extensions (ext1, ext2)
extensions = sys.argv[2].split(",")

for sd, d, filelist in os.walk(sys.argv[1]):
    for f in filelist:
        filepath = sd + os.sep + f
        for extension in extensions:
            if filepath.endswith(extension):
                fileh = open(filepath, 'r')
                filedata = fileh.readlines()
                fileh.close()
                locf = 0
                for fileline in filedata:
                    fileline = fileline.strip()
                    fileline = fileline.replace(' ', '')
                    if not len(fileline) == 0:
                        locf += 1
                    if len(fileline) > 2:
                        if any(x in fileline[:1] for x in disqualifiers):
                            locf -= 1
                print(str(locf) + " loc in " + filepath)
                loc += locf
                fc += 1

print("\ncardinality: " + str(fc))
print("mean loc: " + str(loc/fc))
print("total loc: " + str(loc))
