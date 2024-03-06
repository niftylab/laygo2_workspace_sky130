######################################
#                                    #
#       NOR Layout Gernerator        #
#      Created by Hyungjoo Park      #
#                                    #
######################################

import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
from laygo2.object.netmap import NetMap
# Parameter definitions #############
# Variables
cell_type = 'nor'
nf_list = [2,4]
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
   in0 = tnmos.generate(name='MN0', params={'nf': nf, 'tie': 'S'})
   ip0 = tpmos.generate(name='MP0', transform='MX', params={'nf': nf, 'tie': 'S'})
   in1 = tnmos.generate(name='MN1', params={'nf': nf, 'tie': 'S'})
   ip1 = tpmos.generate(name='MP1', transform='MX', params={'nf': nf})

# 4. Place instances.
   dsn.place(grid=pg, inst=in0, mn=[0,0])
   dsn.place(grid=pg, inst=ip0, mn=pg.mn.top_left(in0) + pg.mn.height_vec(ip0))
   dsn.place(grid=pg, inst=in1, mn=pg.mn.bottom_right(in0))
   dsn.place(grid=pg, inst=ip1, mn=pg.mn.top_right(ip0))

# 5. Create and place wires.
   print("Create wires")
   # A
   if nf == 2:
      _mn = [r23.mn(in1.pins['G'])[0], r23.mn(ip1.pins['G'])[0]]
      _track = [r23.mn(in1.pins['G'])[0,0]-1, None]
      rA_t0 = dsn.route_via_track(grid=r23, mn=_mn, track=_track)
   else:
      _mn = [r23.mn(in1.pins['G'])[0], r23.mn(ip1.pins['G'])[0]]
      vA0, rA0, vA1 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])

   # B
   _mn = [r23.mn(in0.pins['G'])[0], r23.mn(ip0.pins['G'])[0]]
   vB0, rB0, vB1 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])

   # Internal
   _mn = [r12.mn(ip0.pins['D'])[0], r12.mn(ip1.pins['S'])[0]]
   _track = [r12.mn(ip1.pins['S'])[0][0]-1,None]
   rintp0 = dsn.route_via_track(grid=r12, mn=_mn, track=_track)

   # OUT
   _mn = [r12.mn(in0.pins['D'])[1], r12.mn(in1.pins['D'])[0]]
   dsn.route(grid=r12, mn=_mn)
   _mn = [r23.mn(in1.pins['D'])[1], r23.mn(ip1.pins['D'])[1]]
   vout0, rout0, vout1 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])

   # VSS
   rvss0 = dsn.route(grid=r12, mn=[r12.mn(in0.pins['RAIL'])[0], r12.mn(in1.pins['RAIL'])[1]])

   # VDD
   rvdd0 = dsn.route(grid=r12, mn=[r12.mn(ip0.pins['RAIL'])[0], r12.mn(ip1.pins['RAIL'])[1]])

# 6. Create pins.
   if nf==2:
      pinA = dsn.pin(name='A', grid=r23, mn=r23.mn.bbox(rA_t0[2]))
   else:
      pinA = dsn.pin(name='A', grid=r23, mn=r23.mn.bbox(rA0))
   pinB = dsn.pin(name='B', grid=r23, mn=r23.mn.bbox(rB0))
   pout0 = dsn.pin(name='OUT', grid=r23, mn=r23.mn.bbox(rout0))
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
   nat_temp = dsn.export_to_template(obstacle_layers=['metal1','metal2'])
   laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')