#!/usr/bin/python3

import mido
import sys,os,time
import _thread

#timidity -iA -B4,8 -OsSu1 --resample=l -a --voice-lpf=d --noise-shaping=0 --default-program=2 -s 44kHz
# -V 0.3 --output-mono --volume=255 -V 0.3

print("out put ports:")
for i in mido.get_output_names():
  print(i)
print("input ports")
for i in mido.get_input_names():
  print(i)

outport, inport = None,None

default_output= "TiMidity:TiMidity port 0"
default_input = "AXELVOX KEY49J:AXELVOX KEY49J MIDI 1 32:0"

import tkinter as tk
from tkinter import ttk
from tkinter import * 


vSplitTheKeybaord = False
vSplitTheKeybaordFromNum = 55
vProgram1Num = 81
vProgram2Num = 10 # 45 82 88 91  92 96  94  98 | 103 105 114
vSplitKeyBoardTransponse1 = -12
vSplitKeyBoardTransponse2 = 0

def stopAll():
  if outport == None:
    return
  print(vProgram1Num,vProgram2Num)
  for i in range(127):
    outport.send( mido.Message('note_off',channel=0, note=i ) )
    outport.send( mido.Message('note_off',channel=1, note=i ) )

def apply():
  global vSplitTheKeybaord, vSplitTheKeybaordFromNum, vProgram1Num, vProgram2Num, vSplitKeyBoardTransponse1, vSplitKeyBoardTransponse2
  if outport == None:
    return
  #
  stopAll()
  #
  print("fvsplitkeyboard:", fvsplitkeyboard.get())
  vSplitTheKeybaord        = fvsplitkeyboard.get()
  vSplitTheKeybaordFromNum = int(fvSplitKeyBoardFromNum.get())
  vSplitKeyBoardTransponse1 = int(fvSplitKeyBoardTransponse1.get())
  vSplitKeyBoardTransponse2 = int(fvSplitKeyBoardTransponse2.get())

  vProgram1Num = int(Programm1.get())
  vProgram2Num = int(Programm2.get())

  outport.send( mido.Message('program_change', channel=0, program=vProgram1Num) )
  #time.sleep(0.25)
  outport.send( mido.Message('program_change', channel=1, program=vProgram2Num) )

  print('clicked')

#control_change channel=0 control=7 value=48 t

def mainloop():
  global outport, inport
  outport = mido.open_output( voutput.get() )
  inport = mido.open_input( vinput.get() )
  apply()

  for msg in inport:
    if msg.type in ['note_on', 'note_off']:
      if vSplitTheKeybaord:
        if msg.note > vSplitTheKeybaordFromNum:
          msg.channel=1
          msg.note+= vSplitKeyBoardTransponse2
        else:
          msg.channel=0
          msg.note+= vSplitKeyBoardTransponse1
    
    print(msg)
    outport.send(msg)

def connect():
  fbConnect["state"] = "disabled"
  try:
   _thread.start_new_thread(mainloop, ())
  except:
    print ("Error: unable to start thread")
    return

root = Tk()

root.geometry('320x200')
#root.configure(background='#F0F8FF')
root.title('Split midi keyboard for timidity')
deffont=('arial', 12, 'normal')

Button(root, text='Apply',  font=deffont, command=apply ).place(x=220, y=30)
fbConnect = Button(root, text="Connect",  font=deffont, command=connect )
fbConnect.place(x=220, y=60)
Button(root, text='StopNotes',  font=deffont, command=stopAll ).place(x=220, y=90)

fvProgramm1 = IntVar(root)
fvProgramm1.set(vProgram1Num)

fvProgramm2 = IntVar(root)
fvProgramm2.set(vProgram2Num)
fvsplitkeyboard = BooleanVar(root)
fvsplitkeyboard.set(True)

fvSplitKeyBoardFromNum = IntVar(root)
fvSplitKeyBoardFromNum.set(vSplitTheKeybaordFromNum)

fvSplitKeyBoardTransponse1 = IntVar(root)
fvSplitKeyBoardTransponse1.set(vSplitKeyBoardTransponse1)

fvSplitKeyBoardTransponse2 = IntVar(root)
fvSplitKeyBoardTransponse2.set(vSplitKeyBoardTransponse2)


Label(root, text='Ch1 Prgm:',  font=deffont).place(x=10, y=10)
Label(root, text='Ch2 Prgm:',  font=deffont).place(x=100, y=10)

Programm1= Spinbox(root, textvariable=fvProgramm1, from_=0, to=128, font=deffont,  width=3, command=apply)
Programm1.place(x=10, y=30)


Programm2= Spinbox(root, textvariable=fvProgramm2, from_=0, to=128, font=deffont,  width=3, command=apply)
Programm2.place(x=100, y=30)

Checkbutton(root, text='Split the keyboard', variable=fvsplitkeyboard,  font=deffont, command=apply).place(x=10, y=52)
Label(root, text='Split from:',  font=deffont).place(x=10, y=70)
Label(root, text='Transpose:',  font=deffont).place(x=10, y=90)
Spinbox(root, textvariable=fvSplitKeyBoardFromNum, from_=1, to=128, font=deffont, width=4, command=apply).place(x=80, y=70)
Spinbox(root, textvariable=fvSplitKeyBoardTransponse1, from_=-127, to=128, font=deffont,  width=4, command=apply).place(x=80, y=90)
Spinbox(root, textvariable=fvSplitKeyBoardTransponse2, from_=-127, to=128, font=deffont,  width=4, command=apply).place(x=130, y=90)

voutput = StringVar(root)
vinput = StringVar(root)

Label(root, text='Output:',  font=deffont).place(x=10, y=120)
Label(root, text='Input:',  font=deffont).place(x=10, y=150)

fvoutput = OptionMenu(root, voutput, *mido.get_output_names() )
fvoutput.place(x=60, y=120)

fvinput = OptionMenu(root, vinput, *mido.get_output_names() )
fvinput.place(x=60, y=150)

voutput.set(default_output)
vinput.set(default_input)

root.mainloop()