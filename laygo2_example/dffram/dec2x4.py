###########################################
#                                         #
#      2x4 decoder Layout Generator       #
#        Created by HyungJoo Park         #   
#                                         #
###########################################


import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
from laygo2.object.netmap import NetMap
# Parameter definitions #############
# Variables
cell_type = 'dec2x4'
nf = 2
nf_inv = 2
# Templates
tpmos_name = 'pmos'
tnmos_name = 'nmos'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'
r45_name = 'routing_45_basic'
# Design hierarchy
libname = 'dffram'
ref_dir_template = './laygo2_example/' #export this layout's information into the yaml in this dir 
ref_dir_export = './laygo2_example/dffram/'
ref_dir_MAG_exported = './laygo2_example/dffram/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlogic_prim = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_ver2/logic_ver2_templates.yaml')
tlogic_adv = laygo2.interface.yaml.import_template(filename=ref_dir_template+'dffram/dffram_templates.yaml')

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23, r34, r45 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name], grids[r45_name]

cellname = cell_type+'_'+str(nf)+'x'
print('--------------------')
print('Now Creating '+cellname)

# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

# 3. Create istances.
print("Create instances")
inv0 = tlogic_prim['inv_'+str(nf_inv)+'x'].generate(name='inv0')
inv1 = tlogic_prim['inv_'+str(nf_inv)+'x'].generate(name='inv1')
ands=list()
for i in range(4):
    ands.append([tlogic_prim['nand3_'+str(nf)+'x'].generate(name='nand3_'+str(i)), 
        tlogic_prim['inv_'+str(nf_inv)+'x'].generate(name='inv_'+str(i))])

# 4. Place instances.
dsn.place(grid=pg, inst=inv0, mn=[0,0])
dsn.place(grid=pg, inst=inv1, mn=pg.mn.bottom_right(inv0))
mn_left = pg.mn.bottom_right(inv1)
for i in range(4):
    dsn.place(grid=pg, inst=ands[i][0], mn=mn_left)
    mn_left = pg.mn.bottom_right(ands[i][0])
    dsn.place(grid=pg, inst=ands[i][1], mn=mn_left)
    mn_left = pg.mn.bottom_right(ands[i][1])
# 5. Create and place wires.
print("Create wires")

# A0bar
mn_list = [r34.mn(inv1.pins['O'])[0], r34.mn(ands[0][0].pins['A'])[0], r34.mn(ands[2][0].pins['A'])[0]]
_track = [None, r34.mn(inv1.pins['O'])[0,1]-2]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# A0
mn_list = [r34.mn(inv1.pins['I'])[0], r34.mn(ands[1][0].pins['A'])[0], r34.mn(ands[3][0].pins['A'])[0]]
_track = [None, r34.mn(inv1.pins['I'])[0,1]+1]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# A1bar
mn_list = [r34.mn(inv0.pins['O'])[1], r34.mn(ands[0][0].pins['B'])[1], r34.mn(ands[1][0].pins['B'])[1]]
_track = [None, r34.mn(inv0.pins['O'])[1,1]+1]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# A1
mn_list = [r34.mn(inv0.pins['I'])[0], r34.mn(ands[2][0].pins['B'])[0], r34.mn(ands[3][0].pins['B'])[0]]
_track = [None, r34.mn(inv0.pins['I'])[0,1]+2]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# nand-inv internal
for i in range(4):
    mn_list = [r23.mn(ands[i][0].pins['Y'])[1], r23.mn(ands[i][1].pins['I'])[1]]
    _track = [None, (r23.mn(ands[i][1].pins['I'])[0,1] + r23.mn(ands[i][1].pins['I'])[1,1])/2]
    dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
#Enable
mn_list=[]
for i in range(4):
    mn_list.append(r34.mn(ands[i][0].pins['C'])[0])
_track = [None, r34.mn(ands[i][0].pins['C'])[0,1]]
rEN = dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
# VSS
rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(inv0), r12.mn.bottom_right(ands[3][1])])
# VDD
rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(inv0), r12.mn.top_right(ands[3][1])])

# 6. Create pins.
pA0 = dsn.pin(name='A0', grid=r23, mn=r23.mn.bbox(inv1.pins['I']))
pA1 = dsn.pin(name='A1', grid=r23, mn=r23.mn.bbox(inv0.pins['I']))
pEN = dsn.pin(name='EN', grid=r34, mn=r34.mn.bbox(rEN[-1]))
pout=list()
for i in range(4):
    pout.append(dsn.pin(name='Y'+str(i), grid=r23, mn=r23.mn.bbox(ands[i][1].pins['O'])))
pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))

# 7. Export to physical database.
print("Export design")
grid_table = dict()
grid_table['metal1'] = r34
grid_table['metal2'] = r34
grid_table['metal3'] = r45
via_table = dict()
via_table["via_M3_M4_0"] = ('metal1','metal2')
via_table["via_M4_M5_0"] = ('metal2','metal3')
nMap = NetMap.import_from_design(dsn, grid_table, via_table, orient_first="vertical", layer_names=['metal1','metal2','metal3'], net_ignore = ['VSS','VDD'], lib_ref = "laygo2_example/prj_db/library.yaml")   
# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library="sky130A")

# 8. Export to a template database file.
nat_temp = dsn.export_to_template(obstacle_layers=['metal1','metal2','metal3'])
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')