#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import r2pipe

# Flag format
flag = "bzhctf{"

# Open binary and apply configuration set in mate.rr2
# The binary needs some input in stdin, so we need to use
# the mate.rr2 file
r2 = r2pipe.open("./completementalouest")
r2.cmd("e dbg.profile=mate.rr2")

# reopen the binary with debugging capabilities
r2.cmd("doo") 
# set breakpoint on an instruction that allow us to
# get the character to extract
r2.cmd("db 0x4012a1") 

try:
    # Let's say we don't know the password length
    # Just try to fetch new chars until it crashes
    while True:

        # continue until breakpoint is hit
        r2.cmd("dc")

        # Once the breakpoint is hit, extract the char value from rax
        rax = r2.cmd("dr rax")
        char = "{:x}".format(int(rax, 16))

        flag += chr(int(rax, 16))

        # Extract "[rbp-4]" value
        target = r2.cmd("px 1@rbp-4").split("\n")[1].split(" ")[0]

        # Set the good char at rbp-4 in order to go to the next step
        r2.cmd("wx {} @ {}".format(char, target))


# Program will crash, but flag will be generated so...
except Exception, e:

    # clear screen, it is full of debug output
    sys.stderr.write("\x1b[2J\x1b[H")

    flag += "}"
    print """
    ┏┓ ┏━┓┏━╸╻╺━┓╻ ╻┏━╸╺┳╸┏━╸   ┏━┓┏━┓╺┓ ┏━┓
    ┣┻┓┣┳┛┣╸ ┃┏━┛┣━┫┃   ┃ ┣╸    ┏━┛┃┃┃ ┃   ┃
    ┗━┛╹┗╸┗━╸╹┗━╸╹ ╹┗━╸ ╹ ╹     ┗━╸┗━┛╺┻╸  ╹
    ┌───────────────────────────────────────'
    │
    │  Reverse "Mate" - Cyberserker & r2
    │ """
    sys.stdout.write("    └──> " + flag + "\n\n")
    sys.exit(0)
