#####################################################################
#                                                                   #
#       Nand Gate with small size Layout Gernerator                 #
#                     Created by HyungJoo Park                      #
#                                                                   #
#####################################################################

import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
from laygo2.object.netmap import NetMap
# Parameter definitions #############
# Variables
cell_type = 'nand'
nf = 1
cellname = cell_type+'_'+str(nf)+'x'
# Templates
tpmos_name = 'pmos'
tnmos_name = 'nmos'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'
# Design hierarchy
libname = 'logic_ver2'
ref_dir_template = './laygo2_example/logic_ver2/' #export this layout's information into the yaml in this dir 
ref_dir_MAG_exported = './laygo2_example/logic_ver2/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlib = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_ver2_templates.yaml')
#print(templates[tpmos_name], templates[tnmos_name], sep="\n")

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name]

# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

# 3. Create istances.
print("Create instances")
nstack = templates['nmos130_fast_center_2stack'].generate(name='nstack')
nbndl = templates['nmos130_fast_boundary'].generate(name='nbndl')
nbndr = templates['nmos130_fast_boundary'].generate(name='nbndr')
pstack = templates['pmos130_fast_center_2stack'].generate(name='pstack', transform='MX')
pbndl = templates['pmos130_fast_boundary'].generate(name='pbndl', transform='MX')
pbndr = templates['pmos130_fast_boundary'].generate(name='pbndr', transform='MX')

# 4. Place instances.
dsn.place(grid=pg, inst=nbndl, mn=[0,0])
dsn.place(grid=pg, inst=nstack, mn=pg.mn.bottom_right(nbndl))
dsn.place(grid=pg, inst=nbndr, mn=pg.mn.bottom_right(nstack))
dsn.place(grid=pg, inst=pbndl, mn=pg.mn.top_left(nbndl)+pg.mn.height_vec(pbndl))
dsn.place(grid=pg, inst=pstack, mn=pg.mn.top_right(pbndl))
dsn.place(grid=pg, inst=pbndr, mn=pg.mn.top_right(pstack))

# 5. Create and place wires.
print("Create wires")
# VSS  
# M2 Rect
_mn = [r12.mn.bottom_left(nbndl), r12.mn.bottom_right(nbndr)]
rvss0 = dsn.route(grid=r12, mn=_mn)

# tie
_mn = [r12.mn(nstack.pins['S0'])[1], r12.mn(nstack.pins['S0'])[1]+[0,-1]]
rvss1, _ = dsn.route(grid=r12, mn=_mn, via_tag=[False, True])

# VDD
# M2 Rect
_mn = [r12.mn.top_left(pbndl), r12.mn.top_right(pbndr)]
rvdd0 = dsn.route(grid=r12, mn=_mn)

# tie
_S0 = ((r12.mn(pstack.pins['S0'])[0] + r12.mn(pstack.pins['D0'])[0])/2).astype(int)
_mn = [_S0, [_S0[0],r12.mn(rvdd0)[0,1]]]
#_mn = [r12.mn(pstack.pins['D0'])[1], r12.mn(rvdd0)[0]+[2,0]]
rvdd1 = dsn.route(grid=r12, mn=_mn, via_tag=[False, True])

# B
_mn = [r12.mn(nstack.pins['G0'])[0], r12.mn(pstack.pins['G0'])[0]]
rin0 = dsn.route(grid=r23, mn=_mn)
_mn = [r12.mn(nstack.pins['G0'])[0], r12.mn(pstack.pins['G0'])[0]]
dsn.route(grid=r12, mn=_mn)
_mn = [np.mean(r23.mn.bbox(rin0), axis=0, dtype=int), np.mean(r23.mn.bbox(rin0), axis=0, dtype=int)+[1,0]]
dsn.route(grid=r23, mn=_mn, via_tag=[True, False])
dsn.via(grid=r12, mn=np.mean(r23.mn.bbox(rin0), axis=0, dtype=int))

# A
_mn = [r23.mn(pstack.pins['G1'])[0], r23.mn(nstack.pins['G1'])[0]]
_track = [_S0[0], None]
rA = dsn.route_via_track(grid=r23, mn=_mn, track=_track)
dsn.via(grid=r12, mn=r12.mn(pstack.pins['G1']))
dsn.via(grid=r12, mn=r12.mn(nstack.pins['G1']))
# _mn = [r23.mn(pstack.pins['G1'])[0], r23.mn(pstack.pins['G1'])[0]+[-1,0]]
# renb0, venb0 = dsn.route(grid=r23, mn=_mn, via_tag=[False, True])
# venb1 = dsn.via(grid=r12, mn=r12.mn(pstack.pins['G1'])[0])
# _mn = [r23.mn(pstack.pins['G1'])[0]+[-1,0], r23.mn(nstack.pins['G1'])[0]+[-1,0]]
# renb1 = dsn.route(grid=r23, mn=_mn)

# OUT
_mn = [r12.mn(pstack.pins['S0'])[0], r12.mn(pstack.pins['D0'])[0]]
dsn.route(grid=r12, mn=_mn, via_tag=[True,True])
_mn = [r23.mn(nstack.pins['D0'])[0], r23.mn(pstack.pins['D0'])[0]]
vout0, rout0, vout1 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])
vint0 = dsn.via(grid=r12, mn=r23.mn(nstack.pins['D0'])[0])
# vint1 = dsn.via(grid=r12, mn=r23.mn(pstack.pins['D0'])[1])

# DRC ISSUE
# _mn = [r23.mn(nstack.pins['D0'])[0], r23.mn(nstack.pins['D0'])[0]+[-1,0]]
# dsn.route(grid=r23, mn=_mn)
# _mn = [r23.mn(nstack.pins['G1'])[0], r23.mn(nstack.pins['G1'])[0]+[2,0]]
# dsn.route(grid=r23, mn=_mn)
# _mn = [r23.mn(pstack.pins['G1'])[0], r23.mn(pstack.pins['G1'])[0]+[2,0]]
# dsn.route(grid=r23, mn=_mn)

# 6. Create pins.
pin0 = dsn.pin(name='B', grid=r23, mn=r23.mn.bbox(rin0))
pout0 = dsn.pin(name='OUT', grid=r23, mn=r23.mn.bbox(rout0))
pA0 = dsn.pin(name='A', grid=r23, mn=r23.mn.bbox(rA[-1]))
pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.bbox(rvss0))
pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.bbox(rvdd0))

# 7. Export to physical database.
print("Export design")
grid_table = dict()
grid_table['metal1'] = r34
grid_table['metal2'] = r34
via_table = dict()
via_table["via_M3_M4_0"] = ('metal1','metal2')
via_table["via_M4_M5_0"] = ('metal2','metal3')
nMap = NetMap.import_from_design(dsn, grid_table, via_table, orient_first="vertical", layer_names=['metal1','metal2'], net_ignore = ['VSS','VDD'], lib_ref = "laygo2_example/prj_db/library.yaml")
# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library=tech.name)
# 8. Export to a template database file.
nat_temp = dsn.export_to_template(obstacle_layers=['metal1','metal2'])
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')