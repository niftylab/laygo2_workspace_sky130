###########################################
#                                         #
#      D-Flip Flop Layout Generator       #
#         Created by Taeho Shin           #   
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
cell_type = 'dff'
nf_list = [2]#,4]
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

for nf in nf_list:
   cellname = cell_type+'_'+str(nf)+'x'
   print('--------------------')
   print('Now Creating '+cellname)

# 2. Create a design hierarchy
   lib = laygo2.object.database.Library(name=libname)
   dsn = laygo2.object.database.Design(name=cellname, libname=libname)
   lib.append(dsn)

# 3. Create istances.
   print("Create instances")
   inv0 = tlib['inv_'+str(nf)+'x'].generate(name='inv0', netmap={"I": "CLK", "O": "ICLKB"})
   inv1 = tlib['inv_'+str(nf)+'x'].generate(name='inv1', netmap={"I": "ICLKB", "O": "ICLK"})
   inv2 = tlib['inv_'+str(nf)+'x'].generate(name='inv2', netmap={"I": "FLCH", "O": "LCH"})
   inv3 = tlib['inv_'+str(nf)+'x'].generate(name='inv3', netmap={"I": "BLCH", "O": "O"}) 

   tinv0 = tlib['tinv_'+str(nf)+'x'].generate(name='tinv0', netmap={"I": "I", "O": "FLCH", "EN": "ICLKB", "ENB": "ICLK"})
   tinv1 = tlib['tinv_'+str(nf)+'x'].generate(name='tinv1', netmap={"I": "LCH", "O": "BLCH", "EN": "ICLK", "ENB": "ICLKB"})

   tinv_small0 = tlib['tinv_small_1x'].generate(name='tinv_small0', netmap={"I": "LCH", "O": "FLCH", "EN": "ICLK", "ENB": "ICLKB"})
   tinv_small1 = tlib['tinv_small_1x'].generate(name='tinv_small1', netmap={"I": "OUT", "O": "BLCH", "EN": "ICLKB", "ENB": "ICLK"})

# 4. Place instances.
   dsn.place(grid=pg, inst=inv0, mn=[0,0])
   dsn.place(grid=pg, inst=inv1, mn=pg.mn.bottom_right(inv0))
   dsn.place(grid=pg, inst=tinv0, mn=pg.mn.bottom_right(inv1))
   dsn.place(grid=pg, inst=tinv_small0, mn=pg.mn.bottom_right(tinv0))
   dsn.place(grid=pg, inst=inv2, mn=pg.mn.bottom_right(tinv_small0))
   dsn.place(grid=pg, inst=tinv1, mn=pg.mn.bottom_right(inv2))
   dsn.place(grid=pg, inst=tinv_small1, mn=pg.mn.bottom_right(tinv1))
   dsn.place(grid=pg, inst=inv3, mn=pg.mn.bottom_right(tinv_small1))
   
   # 5. Create and place wires.
   print("Create wires")
   
   # 1st M4
   
   _mn = [r34.mn(inv1.pins['O'])[0], r34.mn(tinv_small1.pins['ENB'])[0]]
   _track = [None, r34.mn(inv1.pins['O'])[0,1]-2]
   mn_list=[]
   mn_list.append(r34.mn(inv1.pins['O'])[0])
   mn_list.append(r34.mn(tinv0.pins['ENB'])[0])
   mn_list.append(r34.mn(tinv1.pins['EN'])[0])
   mn_list.append(r34.mn(tinv_small0.pins['EN'])[0])
   mn_list.append(r34.mn(tinv_small1.pins['ENB'])[0])
   dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
   
   # 2nd M4
   _track[1] += 1
   mn_list=[]
   mn_list.append(r34.mn(inv0.pins['O'])[0])
   mn_list.append(r34.mn(inv1.pins['I'])[0])
   mn_list.append(r34.mn(tinv0.pins['EN'])[0])
   mn_list.append(r34.mn(tinv1.pins['ENB'])[0])
   mn_list.append(r34.mn(tinv_small0.pins['ENB'])[0])
   mn_list.append(r34.mn(tinv_small1.pins['EN'])[0])
   dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
   
   # 3rd M4
   _track[1] += 1
   mn_list=[]
   mn_list.append(r34.mn(inv2.pins['I'])[0])
   mn_list.append(r34.mn(tinv0.pins['O'])[0])
   mn_list.append(r34.mn(tinv_small0.pins['O'])[0])
   dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
 
   mn_list=[]
   mn_list.append(r34.mn(inv3.pins['I'])[0])
   mn_list.append(r34.mn(tinv1.pins['O'])[0])
   mn_list.append(r34.mn(tinv_small1.pins['O'])[0])
   dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
   
   # 4th M4
   _track[1] += 1
   mn_list=[]
   mn_list.append(r34.mn(inv2.pins['O'])[0])
   mn_list.append(r34.mn(tinv1.pins['I'])[0])
   mn_list.append(r34.mn(tinv_small0.pins['I'])[0])
   dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
  
   mn_list=[]
   mn_list.append(r34.mn(inv3.pins['O'])[0])
   mn_list.append(r34.mn(tinv_small1.pins['I'])[0]) 
   dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
  
   # VSS
   rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(inv0), r12.mn.bottom_right(inv3)])
   
   # VDD
   rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(inv0), r12.mn.top_right(inv3)])
   
   # 6. Create pins.
   pin0 = dsn.pin(name='I', grid=r23, mn=r23.mn.bbox(tinv0.pins['I']))
   pclk0 = dsn.pin(name='CLK', grid=r23, mn=r23.mn.bbox(inv0.pins['I']))
   pout0 = dsn.pin(name='O', grid=r23, mn=r23.mn.bbox(inv3.pins['O']))
   pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
   pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))
   
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
   nat_temp = dsn.export_to_template(metal_table=grid_table, net_ignore = ['VSS','VDD'])
   laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
   # laygo2.interface.yaml.export_design(dsn, filename=ref_dir_template+libname+'_templates.yaml',obs_layers=['metal1','metal2'], mode='append')
