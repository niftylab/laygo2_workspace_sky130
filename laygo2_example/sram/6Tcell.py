#####################################################################
#                                                                   #
#       Tri-State Inverter with small size  Layout Gernerator       #
#                     Created by Taeho Shin                         #
#                                                                   #
#####################################################################

import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
import laygo2.object.physical as phy

# Parameter definitions #############
# Variables
cell_type = '6Tcell'
nf = 1
# Templates
tpmos_name = 'pmos'
tnmos_name = 'nmos'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'
# Design hierarchy
libname = 'sram'
cellname = cell_type+'_'+str(nf)+'x'
ref_dir_template = './laygo2_example/sram/' #export this layout's information into the yaml in this dir 
ref_dir_MAG_exported = ref_dir_template+'TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates_tech = tech.load_templates()
tpmos, tnmos = templates_tech[tpmos_name], templates_tech[tnmos_name]
templates = laygo2.interface.yaml.import_template(filename=ref_dir_template+'sram_templates.yaml')

print("Load grids")
grids = tech.load_grids(templates=templates_tech)
pg, r12, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name]
print(grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name], sep="\n")

# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

# 3. Create istances.
print("Create instances")
nstack0 = templates['nmos130_2stack'].generate(name='nstack0')
nstack1 = templates['nmos130_2stack'].generate(name='nstack1', transform='MY')
nbndl = templates['nmos130_boundary'].generate(name='nbndl')
nbndr = templates['nmos130_boundary'].generate(name='nbndr')
pstack0 = templates['pmos130_2stack'].generate(name='pstack0', transform='MX')
pspace0 = templates['pmos130_space'].generate(name='nspace0', transform='MX')
pspace1 = templates['pmos130_space'].generate(name='nspace1', transform='MX')
pbndl = templates['pmos130_boundary'].generate(name='pbndl', transform='MX')
pbndr = templates['pmos130_boundary'].generate(name='pbndr', transform='MX')

# 4. Place instances.
pg_list = [0]*2
pg_list[1] = [pbndl,pspace0,pstack0,pspace1,pbndr]
pg_list[0] = [nbndl,nstack0,nstack1,nbndr,None]
dsn.place(grid=pg, inst=pg_list,mn=[0,0])

# 5. Create and place wires.
print("Create wires")
# Q
_mn = [r12.mn(nstack0.pins['S0'])[0], r12.mn(pstack0.pins['D0'])[0]]
vQ0, rQ, vQ1 = dsn.route(grid=r23, mn=_mn, via_tag=[True,True])
_mn = [r12.mn(pstack0.pins['G1'])[0]]
_mn.append(_mn[0]+[0,1])
_mn.append(_mn[1]-[2,0])
dsn.route(grid=r12, mn=_mn, via_tag = [False, True, False])
dsn.via(grid=r23, mn=_mn[2])
# Qbar
_mn = [r12.mn(nstack1.pins['S0'])[0], r12.mn(pstack0.pins['D1'])[0]]
vQb0, rQb, vQb1 = dsn.route(grid=r23, mn=_mn, via_tag=[True,True])
_mn = [r12.mn(pstack0.pins['G0'])[0]]
_mn.append(_mn[0]-[0,1])
_mn.append(_mn[1]+[2,0])
dsn.route(grid=r12, mn=_mn, via_tag = [False, True, False])
dsn.via(grid=r23, mn=_mn[2])

'''
# IN
_mn = [r12.mn(nstack.pins['G0'])[0], r12.mn(pstack.pins['G0'])[0]]
rin0 = dsn.route(grid=r23, mn=_mn)
_mn = [r12.mn(nstack.pins['G0'])[0], r12.mn(pstack.pins['G0'])[0]]
dsn.route(grid=r12, mn=_mn)
_mn = [np.mean(r23.mn.bbox(rin0), axis=0, dtype=int), np.mean(r23.mn.bbox(rin0), axis=0, dtype=int)+[2,0]]
dsn.route(grid=r23, mn=_mn, via_tag=[True, False])
dsn.via(grid=r12, mn=np.mean(r23.mn.bbox(rin0), axis=0, dtype=int))

# OUT
_mn = [r23.mn(nstack.pins['D0'])[0], r23.mn(pstack.pins['D0'])[1]]
vout0, rout0, vout1 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])
vint0 = dsn.via(grid=r12, mn=r23.mn(nstack.pins['D0'])[0])
vint1 = dsn.via(grid=r12, mn=r23.mn(pstack.pins['D0'])[1])

# EN
_mn = [r23.mn(nstack.pins['G1'])[0], r23.mn(nstack.pins['G1'])[0]+[1,0]]
ren0, ven0 = dsn.route(grid=r23, mn=_mn, via_tag=[False, True])
ven1 = dsn.via(grid=r12, mn=r12.mn(nstack.pins['G1'])[0])
_mn = [r23.mn(nstack.pins['G1'])[0]+[1,0], r23.mn(pstack.pins['G1'])[0]+[1,0]]
ren1 = dsn.route(grid=r23, mn=_mn)

# ENB
_mn = [r23.mn(pstack.pins['G1'])[0], r23.mn(pstack.pins['G1'])[0]+[-1,0]]
renb0, venb0 = dsn.route(grid=r23, mn=_mn, via_tag=[False, True])
venb1 = dsn.via(grid=r12, mn=r12.mn(pstack.pins['G1'])[0])
_mn = [r23.mn(pstack.pins['G1'])[0]+[-1,0], r23.mn(nstack.pins['G1'])[0]+[-1,0]]
renb1 = dsn.route(grid=r23, mn=_mn)

# VSS  
# M2 Rect
_mn = [r12.mn.bottom_left(nbndl), r12.mn.bottom_right(nspace1)]
rvss0 = dsn.route(grid=r12, mn=_mn)

# tie
_mn = [r12.mn(nstack.pins['S0'])[0], r12.mn(nstack.pins['S0'])[0]+[0,-1]]
rvss1, _ = dsn.route(grid=r12, mn=_mn, via_tag=[False, True])

# VDD
# M2 Rect
_mn = [r12.mn.top_left(pbndl), r12.mn.top_right(pspace1)]
rvdd0 = dsn.route(grid=r12, mn=_mn)

# tie
_mn = [r12.mn(pstack.pins['S0'])[1], r12.mn(rvdd0)[0]+[1,0]]
rvdd1 = dsn.route(grid=r12, mn=_mn, via_tag=[False, True])

# 6. Create pins.
pin0 = dsn.pin(name='I', grid=r23, mn=r23.mn.bbox(rin0))
pout0 = dsn.pin(name='O', grid=r23, mn=r23.mn.bbox(rout0))
pen0 = dsn.pin(name='EN', grid=r23, mn=r23.mn.bbox(ren1))
penb0 = dsn.pin(name='ENB', grid=r23, mn=r23.mn.bbox(renb1))
pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.bbox(rvss0))
pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.bbox(rvdd0))
'''
# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
