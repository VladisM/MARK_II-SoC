#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# emulator.py
#
# Part of MARK II project. For informations about license, please
# see file /LICENSE .
#
# author: Vladislav Mlejnecký
# email: v.mlejnecky@seznam.cz


from cpu.MARK import MARK
import disassembler
import getopt, sys, version
import Tkinter as tk
import ttk
import tkMessageBox

class globalDefs():
    """Global definitions are stored here"""

    rom0mif = None
    uart0map = None
    gui = False

class mainWindow(tk.Frame):
    """Main window for emulator GUI"""

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

        self.createVariables()
        self.createWidgets()

        self.soc = MARK(globalDefs.rom0mif, globalDefs.uart0map)

        self.updateRegs()
        self.updateMems()
        self.updateDisasmView()

        self.master.title('MARK-II GUI Emulator')

    #create variables for register entry widgets"
    def createVariables(self):
        #variables for registers
        self.r0v = tk.StringVar()
        self.r1v = tk.StringVar()
        self.r2v = tk.StringVar()
        self.r3v = tk.StringVar()
        self.r4v = tk.StringVar()
        self.r5v = tk.StringVar()
        self.r6v = tk.StringVar()
        self.r7v = tk.StringVar()
        self.r8v = tk.StringVar()
        self.r9v = tk.StringVar()
        self.r10v = tk.StringVar()
        self.r11v = tk.StringVar()
        self.r12v = tk.StringVar()
        self.r13v = tk.StringVar()
        self.r14v = tk.StringVar()
        self.r15v = tk.StringVar()
        #variables for run to command
        self.runtov = tk.StringVar()
        self.runtoUpdateRegv = tk.IntVar()
        self.runtoUpdateMemv = tk.IntVar()
        self.forceExitRunTo = False

    #create all widgets in window
    def createWidgets(self):

        #frames
        self.regframe = tk.LabelFrame(self, text="Registers")
        self.regframe.grid(column=0, row=0, padx=5, pady=2, sticky=tk.N+tk.S)

        self.controlframe = tk.LabelFrame(self, text="Control")
        self.controlframe.grid(column=1, row=0, padx=5, pady=2, sticky=tk.N+tk.S)

        self.memFrame = tk.LabelFrame(self, text="Memory")
        self.memFrame.grid(column=0, row=1, columnspan=2, padx=5, pady=2, sticky=tk.N+tk.S)

        self.disasmFrame = tk.LabelFrame(self, text="Disassembler")
        self.disasmFrame.grid(column=2, row=0, rowspan=2, padx=5, pady=2, sticky=tk.N+tk.S)

        #control buttons (they are in control frame)
        self.controlframe.tickbutton = tk.Button(self.controlframe, text="Tick", width=6, command=self.tickButton_callback)
        self.controlframe.tickbutton.grid(column=0, row=0, padx=5, pady=2)

        self.controlframe.tickbutton = tk.Button(self.controlframe, text="Reset", width=6,  command=self.resetButton_callback)
        self.controlframe.tickbutton.grid(column=1, row=0, padx=5, pady=2)

        self.controlframe.tickbutton = tk.Button(self.controlframe, text="Exit", width=6,  command=self.exitButton_callback)
        self.controlframe.tickbutton.grid(column=2, row=0, padx=5, pady=2)

        self.controlframe.runtoframe = tk.LabelFrame(self.controlframe, text="Run to")
        self.controlframe.runtoframe.grid(column=0, row=1, padx=5, pady=2, columnspan=3)

        self.controlframe.runtoframe.runto = tk.Entry(self.controlframe.runtoframe, textvariable=self.runtov)
        self.controlframe.runtoframe.runto.grid(column=0, row=0, padx=5, pady=2)

        self.controlframe.runtoframe.runtobutton = tk.Button(self.controlframe.runtoframe, text="Run!", width=6, command=self.runtoButton_callback)
        self.controlframe.runtoframe.runtobutton.grid(column=1, row=0, padx=5, pady=2)

        self.controlframe.runtoframe.checkframe = tk.Frame(self.controlframe.runtoframe)
        self.controlframe.runtoframe.checkframe.grid(column=0, row=1, padx=5, pady=2)

        self.controlframe.runtoframe.checkframe.runtocheckregs = tk.Checkbutton(self.controlframe.runtoframe.checkframe, text = "Regs?", variable = self.runtoUpdateRegv)
        self.controlframe.runtoframe.checkframe.runtocheckregs.grid(column=0, row=0, padx=5, pady=2)

        self.controlframe.runtoframe.checkframe.runtocheckmems = tk.Checkbutton(self.controlframe.runtoframe.checkframe, text = "Mems?", variable = self.runtoUpdateMemv)
        self.controlframe.runtoframe.checkframe.runtocheckmems.grid(column=1, row=0, padx=5, pady=2)

        self.controlframe.runtoframe.stopbutton = tk.Button(self.controlframe.runtoframe, text="Stop!", width=6, command=self.runtoStopButton_callback)
        self.controlframe.runtoframe.stopbutton.grid(column=1, row=1, padx=5, pady=2)

        #registers (in register frame)
        self.regframe.labelr0 = tk.Label(self.regframe, text="R0:")
        self.regframe.labelr0.grid(column=0, row=0, padx=5, pady=2)

        self.regframe.labelr1 = tk.Label(self.regframe, text="R1:")
        self.regframe.labelr1.grid(column=0, row=1, padx=5, pady=2)

        self.regframe.labelr2 = tk.Label(self.regframe, text="R2:")
        self.regframe.labelr2.grid(column=0, row=2, padx=5, pady=2)

        self.regframe.labelr3 = tk.Label(self.regframe, text="R3:")
        self.regframe.labelr3.grid(column=0, row=3, padx=5, pady=2)

        self.regframe.labelr4 = tk.Label(self.regframe, text="R4:")
        self.regframe.labelr4.grid(column=0, row=4, padx=5, pady=2)

        self.regframe.labelr5 = tk.Label(self.regframe, text="R5:")
        self.regframe.labelr5.grid(column=0, row=5, padx=5, pady=2)

        self.regframe.labelr6 = tk.Label(self.regframe, text="R6:")
        self.regframe.labelr6.grid(column=0, row=6, padx=5, pady=2)

        self.regframe.labelr7 = tk.Label(self.regframe, text="R7:")
        self.regframe.labelr7.grid(column=0, row=7, padx=5, pady=2)

        self.regframe.labelr8 = tk.Label(self.regframe, text="R8:")
        self.regframe.labelr8.grid(column=2, row=0, padx=5, pady=2)

        self.regframe.labelr9 = tk.Label(self.regframe, text="R9:")
        self.regframe.labelr9.grid(column=2, row=1, padx=5, pady=2)

        self.regframe.labelr10 = tk.Label(self.regframe, text="R10:")
        self.regframe.labelr10.grid(column=2, row=2, padx=5, pady=2)

        self.regframe.labelr11 = tk.Label(self.regframe, text="R11:")
        self.regframe.labelr11.grid(column=2, row=3, padx=5, pady=2)

        self.regframe.labelr12 = tk.Label(self.regframe, text="R12:")
        self.regframe.labelr12.grid(column=2, row=4, padx=5, pady=2)

        self.regframe.labelr13 = tk.Label(self.regframe, text="R13:")
        self.regframe.labelr13.grid(column=2, row=5, padx=5, pady=2)

        self.regframe.labelr14 = tk.Label(self.regframe, text="R14:")
        self.regframe.labelr14.grid(column=2, row=6, padx=5, pady=2)

        self.regframe.labelr15 = tk.Label(self.regframe, text="R15:")
        self.regframe.labelr15.grid(column=2, row=7, padx=5, pady=2)

        self.regframe.entryr0 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r0v)
        self.regframe.entryr0.grid(column=1, row=0, padx=5, pady=2)

        self.regframe.entryr1 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r1v)
        self.regframe.entryr1.grid(column=1, row=1, padx=5, pady=2)

        self.regframe.entryr2 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r2v)
        self.regframe.entryr2.grid(column=1, row=2, padx=5, pady=2)

        self.regframe.entryr3 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r3v)
        self.regframe.entryr3.grid(column=1, row=3, padx=5, pady=2)

        self.regframe.entryr4 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r4v)
        self.regframe.entryr4.grid(column=1, row=4, padx=5, pady=2)

        self.regframe.entryr5 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r5v)
        self.regframe.entryr5.grid(column=1, row=5, padx=5, pady=2)

        self.regframe.entryr6 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r6v)
        self.regframe.entryr6.grid(column=1, row=6, padx=5, pady=2)

        self.regframe.entryr7 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r7v)
        self.regframe.entryr7.grid(column=1, row=7, padx=5, pady=2)

        self.regframe.entryr8 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r8v)
        self.regframe.entryr8.grid(column=3, row=0, padx=5, pady=2)

        self.regframe.entryr9 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r9v)
        self.regframe.entryr9.grid(column=3, row=1, padx=5, pady=2)

        self.regframe.entryr10 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r10v)
        self.regframe.entryr10.grid(column=3, row=2, padx=5, pady=2)

        self.regframe.entryr11 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r11v)
        self.regframe.entryr11.grid(column=3, row=3, padx=5, pady=2)

        self.regframe.entryr12 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r12v)
        self.regframe.entryr12.grid(column=3, row=4, padx=5, pady=2)

        self.regframe.entryr13 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r13v)
        self.regframe.entryr13.grid(column=3, row=5, padx=5, pady=2)

        self.regframe.entryr14 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r14v)
        self.regframe.entryr14.grid(column=3, row=6, padx=5, pady=2)

        self.regframe.entryr15 = tk.Entry(self.regframe, width=10, disabledforeground="#000", disabledbackground="#fff", state=tk.DISABLED, textvariable=self.r15v)
        self.regframe.entryr15.grid(column=3, row=7, padx=5, pady=2)

        #memory view (text widgets with scroll bars)
        self.memFrame.rom0frame = tk.LabelFrame(self.memFrame, text="rom0")
        self.memFrame.rom0frame.grid(column=0, row=0, padx=5, pady=2)

        self.memFrame.rom0frame.rom0 = tk.Text(self.memFrame.rom0frame, undo=False, width=21, height=16, state=tk.DISABLED)
        self.memFrame.rom0frame.rom0.grid(column=0, row=0)

        self.memFrame.rom0frame.scrollY = tk.Scrollbar(self.memFrame.rom0frame, orient=tk.VERTICAL, command=self.memFrame.rom0frame.rom0.yview)
        self.memFrame.rom0frame.scrollY.grid(row=0, column=1, sticky=tk.N+tk.S)

        self.memFrame.rom0frame.rom0['yscrollcommand'] = self.memFrame.rom0frame.scrollY.set


        self.memFrame.ram0frame = tk.LabelFrame(self.memFrame, text="ram0")
        self.memFrame.ram0frame.grid(column=1, row=0, padx=5, pady=2)

        self.memFrame.ram0frame.ram0 = tk.Text(self.memFrame.ram0frame, undo=False, width=21, height=16, state=tk.DISABLED)
        self.memFrame.ram0frame.ram0.grid(column=0, row=0)

        self.memFrame.ram0frame.scrollY = tk.Scrollbar(self.memFrame.ram0frame, orient=tk.VERTICAL, command=self.memFrame.ram0frame.ram0.yview)
        self.memFrame.ram0frame.scrollY.grid(row=0, column=1, sticky=tk.N+tk.S)

        self.memFrame.ram0frame.ram0['yscrollcommand'] = self.memFrame.ram0frame.scrollY.set


        self.memFrame.ram1frame = tk.LabelFrame(self.memFrame, text="ram1")
        self.memFrame.ram1frame.grid(column=2, row=0, padx=5, pady=2)

        self.memFrame.ram1frame.ram1 = tk.Text(self.memFrame.ram1frame, undo=False, width=21, height=16, state=tk.DISABLED)
        self.memFrame.ram1frame.ram1.grid(column=0, row=0)

        self.memFrame.ram1frame.scrollY = tk.Scrollbar(self.memFrame.ram1frame, orient=tk.VERTICAL, command=self.memFrame.ram1frame.ram1.yview)
        self.memFrame.ram1frame.scrollY.grid(row=0, column=1, sticky=tk.N+tk.S)

        self.memFrame.ram1frame.ram1['yscrollcommand'] = self.memFrame.ram1frame.scrollY.set

        #disassbled memory view

        self.disasmFrame.helpFrame = tk.Frame(self.disasmFrame)
        self.disasmFrame.helpFrame.grid(column=0,row=0, columnspan=2, pady=2)

        self.disasmFrame.helpFrame.disasmText = tk.Text(self.disasmFrame.helpFrame, undo=False, width=45, height=30, state=tk.DISABLED)
        self.disasmFrame.helpFrame.disasmText.grid(column=0, row=0)

        self.disasmFrame.helpFrame.scrollY = tk.Scrollbar(self.disasmFrame.helpFrame, orient=tk.VERTICAL, command=self.disasmFrame.helpFrame.disasmText.yview)
        self.disasmFrame.helpFrame.scrollY.grid(row=0, column=1, sticky=tk.N+tk.S)

        self.disasmFrame.helpFrame.disasmText['yscrollcommand'] = self.disasmFrame.helpFrame.scrollY.set

        self.disasmFrame.disasmbutton = tk.Button(self.disasmFrame, text="Disasmble", width=6,  command=self.disasmButton_callback)
        self.disasmFrame.disasmbutton.grid(column=1, row=1, padx=5, pady=2)

        self.disasmFrame.disasmSelect = ttk.Combobox(self.disasmFrame, values=("rom0", "ram0", "ram1"), state='readonly')
        self.disasmFrame.disasmSelect.grid(column=0, row=1, padx=5, pady=2)
        self.disasmFrame.disasmSelect.current(0)

    #callbacks functions
    def tickButton_callback(self):
        self.soc.tick()
        self.updateRegs()
        self.updateMems()

    def resetButton_callback(self):
        self.soc.reset()
        self.updateRegs()
        self.updateMems()

    def exitButton_callback(self):
        del self.soc
        self.quit()

    def disasmButton_callback(self):
        self.updateDisasmView(self.disasmFrame.disasmSelect.current())

    def runtoButton_callback(self):

        #convert string into number
        number = self.runtov.get()
        result = None

        if type(number) == int:
            result = number

        else:
            if len(number) >= 2:
                try:
                    if number[0:2] == '0x':
                        result = int(number, 16)
                    elif number[0:2] == '0b':
                        result = int(number, 2)
                    else:
                        result = int(number, 10)
                except:
                    result = None
            else:
                try:
                    result = int(number, 10)
                except:
                    result = None

        if result != None:

            while result != int(self.soc.cpu0.getRegByName("PC")):

                if self.forceExitRunTo == True:
                    break

                self.soc.tick()

                if self.runtoUpdateRegv.get() == 1:
                    self.updateRegs()
                if self.runtoUpdateMemv.get() == 1:
                    self.updateMems()

                self.update()

            self.updateMems()
            self.updateRegs()

            self.forceExitRunTo = False

        else:
            tkMessageBox.showwarning(title="'Run to' Warning", message="Given address in entry 'run to' box is not valid number. Plese use HEX, DEC or BIN number in C-like syntax.")

    def runtoStopButton_callback(self):
        self.forceExitRunTo = True

    #update content of register fields
    def updateRegs(self):
        self.r0v.set( "0x" + (hex(int(self.soc.cpu0.regs[0])).split('x')[1]).zfill(8) )
        self.r1v.set( "0x" + (hex(int(self.soc.cpu0.regs[1])).split('x')[1]).zfill(8) )
        self.r2v.set( "0x" + (hex(int(self.soc.cpu0.regs[2])).split('x')[1]).zfill(8) )
        self.r3v.set( "0x" + (hex(int(self.soc.cpu0.regs[3])).split('x')[1]).zfill(8) )
        self.r4v.set( "0x" + (hex(int(self.soc.cpu0.regs[4])).split('x')[1]).zfill(8) )
        self.r5v.set( "0x" + (hex(int(self.soc.cpu0.regs[5])).split('x')[1]).zfill(8) )
        self.r6v.set( "0x" + (hex(int(self.soc.cpu0.regs[6])).split('x')[1]).zfill(8) )
        self.r7v.set( "0x" + (hex(int(self.soc.cpu0.regs[7])).split('x')[1]).zfill(8) )
        self.r8v.set( "0x" + (hex(int(self.soc.cpu0.regs[8])).split('x')[1]).zfill(8) )
        self.r9v.set( "0x" + (hex(int(self.soc.cpu0.regs[9])).split('x')[1]).zfill(8) )
        self.r10v.set( "0x" + (hex(int(self.soc.cpu0.regs[10])).split('x')[1]).zfill(8) )
        self.r11v.set( "0x" + (hex(int(self.soc.cpu0.regs[11])).split('x')[1]).zfill(8) )
        self.r12v.set( "0x" + (hex(int(self.soc.cpu0.regs[12])).split('x')[1]).zfill(8) )
        self.r13v.set( "0x" + (hex(int(self.soc.cpu0.regs[13])).split('x')[1]).zfill(8) )
        self.r14v.set( "0x" + (hex(int(self.soc.cpu0.regs[14])).split('x')[1]).zfill(8) )
        self.r15v.set( "0x" + (hex(int(self.soc.cpu0.regs[15])).split('x')[1]).zfill(8) )

    #update whole memory view
    def updateMems(self):
        self.updateRom0()
        self.updateRam0()
        self.updateRam1()

    #update rom0 view
    def updateRom0(self):
        self.memFrame.rom0frame.rom0['state'] = tk.NORMAL   #enable editing
        first, last = self.memFrame.rom0frame.rom0.yview()  #backup scroll bar position
        self.memFrame.rom0frame.rom0.delete(1.0, tk.END)    #delete memory view

        #print all mem item from rom0 into text widget
        linecounter = 0
        for item in self.soc.rom0.mem:

            #convert everiting in hex
            address = "0x" + (hex(linecounter).split('x')[1]).zfill(6)
            value = "0x" + (hex(int(self.soc.rom0.mem[linecounter])).split('x')[1]).zfill(8)

            if linecounter != 0:
                self.memFrame.rom0frame.rom0.insert(tk.END, "\n")

            #print line
            self.memFrame.rom0frame.rom0.insert(tk.END, address + " : " + value)

            linecounter = linecounter + 1

        #disable eiditing again and restore scroll bar
        self.memFrame.rom0frame.rom0['state'] = tk.DISABLED
        self.memFrame.rom0frame.rom0.yview_moveto(first)

    #update ram0 view
    def updateRam0(self):
        self.memFrame.ram0frame.ram0['state'] = tk.NORMAL
        first, last = self.memFrame.ram0frame.ram0.yview()
        self.memFrame.ram0frame.ram0.delete(1.0, tk.END)

        linecounter = 0
        for item in self.soc.ram0.mem:
            address = "0x" + (hex(linecounter + 1024).split('x')[1]).zfill(6)   #add offset
            value = "0x" + (hex(int(self.soc.ram0.mem[linecounter])).split('x')[1]).zfill(8)

            if linecounter != 0:
                self.memFrame.ram0frame.ram0.insert(tk.END, "\n")

            self.memFrame.ram0frame.ram0.insert(tk.END, address + " : " + value)

            linecounter = linecounter + 1

        self.memFrame.ram0frame.ram0['state'] = tk.DISABLED
        self.memFrame.ram0frame.ram0.yview_moveto(first)

    #update ram1 view
    def updateRam1(self):
        self.memFrame.ram1frame.ram1['state'] = tk.NORMAL
        first, last = self.memFrame.ram1frame.ram1.yview()
        self.memFrame.ram1frame.ram1.delete(1.0, tk.END)

        linecounter = 0
        for item in self.soc.ram1.mem:
            address = "0x" + (hex(linecounter +  1048576).split('x')[1]).zfill(6)
            value = "0x" + (hex(int(self.soc.ram1.mem[linecounter])).split('x')[1]).zfill(8)

            if linecounter != 0:
                self.memFrame.ram1frame.ram1.insert(tk.END, "\n")

            self.memFrame.ram1frame.ram1.insert(tk.END, address + " : " + value)

            linecounter = linecounter + 1

        self.memFrame.ram1frame.ram1['state'] = tk.DISABLED
        self.memFrame.ram1frame.ram1.yview_moveto(first)

    #update disassembled memory view
    def updateDisasmView(self, mem=0):
        #enable edit and delete all text
        self.disasmFrame.helpFrame.disasmText['state'] = tk.NORMAL
        self.disasmFrame.helpFrame.disasmText.delete(1.0, tk.END)

        #decide what memory will be disassembled
        if mem == 0:
            mem_to_disasm = self.soc.rom0.mem
            offset = 0
        elif mem == 1:
            mem_to_disasm = self.soc.ram0.mem
            offset = 0x400
        elif mem == 2:
            mem_to_disasm = self.soc.ram1.mem
            offset = 0x100000
        else:
            mem_to_disasm = self.soc.rom0.mem
            offset = 0

        #go thru all memitems in selected memory
        linecounter = 0
        for item in mem_to_disasm:
            address = "0x" + (hex(linecounter + offset).split('x')[1]).zfill(6) #format address
            value = "0x" + (hex(int(item)).split('x')[1]).zfill(8)              #format value at address
            disasmInstruction = disassembler.decodeInstruction(item)             #disassemble instruction

            if disasmInstruction == None:   #if instruction is not valid print empty line
                disasmInstruction = ""

            if linecounter != 0:            #first line dosn't have \n before
                self.disasmFrame.helpFrame.disasmText.insert(tk.END, "\n")

            #print line
            self.disasmFrame.helpFrame.disasmText.insert(tk.END, address + " : " + value + " : " + disasmInstruction)

            linecounter = linecounter + 1

        #disable editing again
        self.disasmFrame.helpFrame.disasmText['state'] = tk.DISABLED

#print help message into console
def usage():
    print """
Example usage: emulator -g -p /dev/pts/2 -r rom.mif

        Simple emulator of MARK-II SoC. Emulating systim, uart0, rom0, ram0, ram1,
    intController and cpu. For more information please see:
    https://github.com/VladisM/MARK_II/

Arguments:
    -h --help           Print this help and exit.
    -p --port           Device where uart0 will be conected. Can be
                        /dev/pts/2 for example.
    -r --rom            Filename of file that will be loaded into rom0.
    -g --gui            Run with simple GUI.
       --version        Print version number and exit.
    """

#get arguments from command line
def get_args():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ghr:p:", ["gui", "help", "port", "rom", "version"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(1)

    for option, value in opts:
        if option in ("-h", "--help"):
            usage()
            sys.exit()
        elif option == "--version":
            print "Emulator for MARK-II " + version.version
            sys.exit()
        elif option in ("-r", "--rom"):
            globalDefs.rom0mif = value
        elif option in ("-p", "--port"):
            globalDefs.uart0map = value
        elif option in ("-g", "--gui"):
            globalDefs.gui = True
        else:
            print "Unrecognized option " + option
            print "Type 'emulator -h' for more informations."
            sys.exit(1)

    if globalDefs.rom0mif == None:
        print "Missing file for rom0. Aborting emulation."
        sys.exit(1)

    if globalDefs.uart0map == None:
        print "Missing port for uart0. Aborting emulation."
        sys.exit(1)

def main():
    get_args()

    print "MARK-II GUI emulator " + version.version
    print "UART0 mapped into \"" + globalDefs.uart0map + "\""
    print "ROM0 loaded with \"" + globalDefs.rom0mif + "\""

    if globalDefs.gui == True:
        #run in GUI mode
        app = mainWindow()
        app.mainloop()

    else:
        #run in CLI mode
        print "For exit from emulator please use CTRL+C."

        soc = MARK(globalDefs.rom0mif, globalDefs.uart0map)

        while True:
            try:
                soc.tick()
            except KeyboardInterrupt:
                del soc
                print "Emulator halted by CTRL+C, exiting now.."
                break
            except SystemExit:
                del soc
                print "Emulator halted by internall call sys.exit(), exiting now..."
                break

    return 0

if __name__ == '__main__':
    main()
