#!/usr/bin/python
#from tqdm import tqdm
import ast, os, time, sys, Queue, threading, atexit

CHARS = " \n1234567890%^&*-+=,.)]}<>?|/:abcdefghijklmnopqrstuvwxyz(_[{:"
FALSTART = " \n1234567890%^&*-+=,.)]}<>?|/:"
MAX_LENGTH = 40

bfsq = Queue.PriorityQueue()
bfsq.put((0,""))
chkq = Queue.Queue()
wrtq = Queue.Queue()
#f1 = open("log1","a")
#atexit.register(f1.close)
#f2 = open("log2","a")
#atexit.register(f2.close)
#f3 = open("log3","a")
#atexit.register(f3.close)
#bar1 = tqdm(unit="idea", unit_scale=True, file=f1)
#bar2 = tqdm(unit="attempt", unit_scale=True, file=f2)
#bar3 = tqdm(unit="success", unit_scale=True, file=f3)

class Treer(threading.Thread):
    def run(self):
        while True:
            start = bfsq.get()[1]
            for c in FALSTART:
                if start.startswith(c):
                    continue
            if len(start) > 5 and len(start.strip()) != len(start):
                continue
            try:
                #bar1.update(1)
                if "a" in start and "b" in start:
                    ast.parse(start)
                    chkq.put(start)
            except:
                pass
            if len(start) < MAX_LENGTH:
                for c in CHARS:
                    bfsq.put((MAX_LENGTH-len(start+c),start+c))

class Checker(threading.Thread):
    def run(self):
        while True:
            prog = chkq.get()
            try:
                #bar2.update(1)
                data = {"a": 5}
                exec(prog, {}, data)
                if data.get("b", None) != 120:
                    continue
                data = {"a": 6}
                exec(prog, {}, data)
                if data.get("b", None) != 720:
                    continue
                wrtq.put(prog)
            except:
                continue

class Writer(threading.Thread):
    def run(self):
        self.i = 0
        while True:
            code = wrtq.get()
            self.i += 1
            #bar3.update(1)
            with open("sol%i.py" % self.i,"w") as f:
                f.write(code)

writer = Writer()
writer.setName("Writer")
writer.setDaemon(True)
writer.start()

checkers = []

for i in range(1):
    checkers.append(Checker())
    checkers[i].setName("Checker-%i"%i)
    checkers[i].setDaemon(True)
    checkers[i].start()

treers = []

for i in range(4):
    treers.append(Treer())
    treers[i].setName("Treer-%i"%i)
    treers[i].setDaemon(True)
    treers[i].start()

while True:
    print(str(bfsq.qsize())+"\t"+str(chkq.qsize())+"\t"+str(writer.i))
    time.sleep(1)
