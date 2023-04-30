###########################################
#                                         #
#  parsing information from verilog code  #
#           Created by S.Y. Lee           #
#                                         #
###########################################

from __future__ import absolute_import
from __future__ import print_function
import sys
import os

# the next line can be removed after installation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyverilog
from pyverilog.vparser.parser import parse

def info_from_verilog_code(filename):

    filelist = [filename]

    for f in filelist:
        if not os.path.exists(f):
            raise IOError("file not found: " + f)
    
    ast, directives = parse(filelist)

    # ast.show()

    # =========== Extract Module info =========== #
    ModuleDef = ast.children()  # start from source object
    while True:
        for el in ModuleDef:
            if type(el) != pyverilog.vparser.ast.ModuleDef : continue
            else : ModuleDef = el
    
        if type(ModuleDef) == pyverilog.vparser.ast.ModuleDef : break
        ModuleDef = ModuleDef[0].children()     # need fix for accurate code..
        
    # --> ModuleDef contains Name, ParamList, PortList, Items
    Name = ModuleDef.name
    # ParamList
    Paramlist = ModuleDef.paramlist.params
    # In/Out ports & Instances
    decl_info = dict(); instance_info = []  # informations of each item
    inputs = []; outputs = []; inouts = []; wires = []; regs = []; integers = []    # for decl_info
    for item in ModuleDef.items:
        # In / Out / Wire
        if type(item) == pyverilog.vparser.ast.Decl :
            for i in item.list:
                if type(i) == pyverilog.vparser.ast.Input :
                    name = i.name
                    if i.width != None:
                        for j in range(int(i.width.msb.value) - int(i.width.lsb.value) + 1):
                            inputs.append(f"{name}[{j}]")
                    else: inputs.append(name)
                if type(i) == pyverilog.vparser.ast.Output :
                    name = i.name
                    if i.width != None:
                        for j in range(int(i.width.msb.value) - int(i.width.lsb.value) + 1):
                            outputs.append(f"{name}[{j}]")
                    else: outputs.append(name)
                if type(i) == pyverilog.vparser.ast.Inout :
                    name = i.name
                    if i.width != None:
                        for j in range(int(i.width.msb.value) - int(i.width.lsb.value) + 1):
                            inouts.append(f"{name}[{j}]")
                    else: inouts.append(name)
                if type(i) == pyverilog.vparser.ast.Wire :
                    name = i.name
                    if i.width != None:
                        for j in range(int(i.width.msb.value) - int(i.width.lsb.value) + 1):
                            wires.append(f"{name}[{j}]")
                    else: wires.append(name)
                if type(i) == pyverilog.vparser.ast.Reg :
                    name = i.name
                    if i.width != None:
                        for j in range(int(i.width.msb.value) - int(i.width.lsb.value) + 1):
                            regs.append(f"{name}[{j}]")
                    else: regs.append(name)
                if type(i) == pyverilog.vparser.ast.Integer :
                    name = i.name
                    if i.width != None:
                        for j in range(int(i.width.msb.value) - int(i.width.lsb.value) + 1):
                            integers.append(f"{name}[{j}]")
                    else: integers.append(name)

        # Instances
        elif type(item) == pyverilog.vparser.ast.InstanceList :
            for i in item.instances:
                ports = dict()
                for port in i.portlist:
                    if type(port.argname) == pyverilog.vparser.ast.Pointer:
                        ports[port.portname] = f"{port.argname.var}[{port.argname.ptr}]"
                    elif type(port.argname) == pyverilog.vparser.ast.Identifier:
                        ports[port.portname] = port.argname.name
                instance_info.append({"Module" : i.module,\
                                      "name" : i.name,\
                                      "paramlist" : i.parameterlist,\
                                      "portlist" : ports})
                                                    # portname : str
                                                    # argname : <class 'pyverilog.vparser.ast.Identifier'>
                                                    # argname.name : str
    
    decl_info["Input"] = inputs
    decl_info["Output"] = outputs
    decl_info["Inout"] = inouts
    decl_info["Wire"] = wires
    decl_info["Reg"] = regs
    decl_info["Integer"] = integers
    # =========================================== #

    for lineno, directive in directives:
        print('Line %d : %s' % (lineno, directive))

    return Name, Paramlist, decl_info, instance_info

if __name__ == '__main__':
    filename = "./verilog_to_laygo/yosys_test/counter_netlist.v"
    name, paramlist, decl_info, inst_info = info_from_verilog_code(filename)
    print()
    print(name)
    print(paramlist)
    print(decl_info)
    for i in inst_info :
        print(i)