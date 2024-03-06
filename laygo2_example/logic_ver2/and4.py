###########################################
#                                         #
#      clock gate Layout Generator        #
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
cell_type = 'and4'
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
nf=2
cellname = cell_type+'_'+str(nf)+'x'
print('--------------------')
print('Now Creating '+cellname)

# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

# 3. Create istances.
print("Create instances")
nand0 = tlib['nand_'+str(nf)+'x'].generate(name='nand0')
nand1 = tlib['nand_'+str(nf)+'x'].generate(name='nand1')
nor0 = tlib['nor_'+str(nf)+'x'].generate(name='nor0')

# 4. Place instances.
dsn.place(grid=pg, inst=nand0, mn=[0,0])
dsn.place(grid=pg, inst=nand1, mn=pg.mn.bottom_right(nand0))
dsn.place(grid=pg, inst=nor0, mn=pg.mn.bottom_right(nand1))
# 5. Create and place wires.
print("Create wires")

# internal
mn_list = [r23.mn(nand0.pins['OUT'])[0], r23.mn(nor0.pins['B'])[0]]
_track = [None, r23.mn(nand0.pins['OUT'])[0,1]-1]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

mn_list = [r23.mn(nand1.pins['OUT'])[0], r23.mn(nor0.pins['A'])[0]]
_track = [None, r23.mn(nand0.pins['OUT'])[0,1]]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# VSS
rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(nand0), r12.mn.bottom_right(nor0)])
# VDD
rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(nand0), r12.mn.top_right(nor0)])

# 6. Create pins.
pD = dsn.pin(name='A3', grid=r23, mn=r23.mn.bbox(nand0.pins['B']))
pC = dsn.pin(name='A2', grid=r23, mn=r23.mn.bbox(nand0.pins['A']))
pB = dsn.pin(name='A1', grid=r23, mn=r23.mn.bbox(nand1.pins['B']))
pA = dsn.pin(name='A0', grid=r23, mn=r23.mn.bbox(nand1.pins['A']))
pout = dsn.pin(name='OUT', grid=r23, mn=r23.mn.bbox(nor0.pins['OUT']))
pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))

# 7. Export to physical database.
print("Export design")
grid_table = dict()
grid_table['metal1'] = r34
grid_table['metal2'] = r34
via_table = dict()
via_table["via_M3_M4_0"] = ('metal1','metal2')
nMap = NetMap.import_from_design(dsn, grid_table, via_table, orient_first="vertical", layer_names=['metal1','metal2'], net_ignore = ['VSS','VDD'], lib_ref = "laygo2_example/prj_db/library.yaml")
# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template(obstacle_layers=['metal1','metal2'])
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')