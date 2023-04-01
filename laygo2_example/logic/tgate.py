###################################################
#                                                 #
#       Transmission Gate Layout Gernerator       #
#             Created by Hyungjoo Park            #
#                                                 #
###################################################

import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech

# Parameter definitions #############
# Variables
cell_type = 'tgate'
nf_list = [2,4,8]
# Templates
tpmos_name = 'pmos_sky'
tnmos_name = 'nmos_sky'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r23_basic_name = 'routing_23_basic'
# Design hierarchy
libname = 'logic_generated'
ref_dir_template = './laygo2_example/logic/' #export this layout's information into the yaml in this dir 
ref_dir_MAG_exported = './laygo2_example/logic/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
#tlib = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_generated_templates.yaml')
print(templates[tpmos_name], templates[tnmos_name], sep="\n")

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23, r23_basic = grids[pg_name], grids[r12_name], grids[r23_name], grids[r23_basic_name]
print(grids[pg_name], grids[r12_name], grids[r23_name], sep="\n")

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
   in0 = tnmos.generate(name='MN0', params={'nf':nf})
   ip0 = tpmos.generate(name='MP0',transform='MX', params={'nf':nf})
   
   nspace0 = templates['nmos13_fast_space_1x'].generate(name='nspace0', shape=[2,1])
   pspace0 = templates['pmos13_fast_space_1x'].generate(name='pspace0', shape=[2,1], transform='MX')
   
   # 4. Place instances.
   dsn.place(grid=pg, inst=nspace0, mn=[0,0])
   dsn.place(grid=pg, inst=in0, mn=pg.mn.bottom_right(nspace0))
   dsn.place(grid=pg, inst=pspace0, mn=pg.mn.top_left(nspace0)+pg.mn.height_vec(pspace0))
   dsn.place(grid=pg, inst=ip0, mn=pg.mn.top_right(pspace0))
   
   # 5. Create and place wires.
   print("Create wires")
   
   # IN
   _mn = [r23.mn(in0.pins['S'])[0], r23.mn(ip0.pins['S'])[0]]
   vin0, rin0, vin1 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])
   
   # OUT
   _mn = [r23.mn(in0.pins['D'])[1], r23.mn(ip0.pins['D'])[1]]
   vout0, rout0, vout1 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])
   
   # EN
   _mn = [r23.mn(in0.pins['G'])[0], r23.mn(in0.pins['G'])[0]+[-3,0]]
   ren0, ven0 = dsn.route(grid=r23, mn=_mn, via_tag=[False, True])
   _mn = [r23.bbox(ren0)[0], r23.mn.bbox(ren0)[0]+[0,2]]
   ren1 = dsn.route(grid=r23, mn=_mn)
   
   # ENB
   _mn = [r23.mn(ip0.pins['G'])[0], r23.mn(ip0.pins['G'])[0]+[-2,0]]
   renb0, venb0 = dsn.route(grid=r23, mn=_mn, via_tag=[False, True])
   _mn = [r23.mn.bbox(renb0)[0]+[0,-2], r23.mn.bbox(renb0)[0]]
   renb1 = dsn.route(grid=r23, mn=_mn)
    
   # VSS
   rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(nspace0), r12.mn(in0.pins['RAIL'])[1]])
   
   # VDD
   rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(pspace0), r12.mn(ip0.pins['RAIL'])[1]])
    
   # 6. Create pins.
   pin0 = dsn.pin(name='I', grid=r23, mn=r23.mn.bbox(rin0))
   pen0 = dsn.pin(name='EN', grid=r23, mn=r23.mn.bbox(ren1))
   penb0 = dsn.pin(name='ENB', grid=r23, mn=r23.mn.bbox(renb1))
   pout0 = dsn.pin(name='O', grid=r23, mn=r23.mn.bbox(rout0))
   pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
   pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))
   
   # 7. Export to physical database.
   print("Export design")
   
   # Uncomment for BAG export
   laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')
   
   # 8. Export to a template database file.
   nat_temp = dsn.export_to_template()
   laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
