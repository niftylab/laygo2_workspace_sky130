##########################################################
#                                                        #
#              2-to-1 MUX Layout Gernerator              #
#     Contributors: T. Shin, S. Park, Y. Oh, T. Kang     #
#                 Last Update: 2022-05-27                #
#                                                        #
##########################################################

import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech

# Parameter definitions #############
# Design Variables
cell_type = 'mux2to1'
nf_list = [2]

# Templates
tpmos_name = 'pmos_sky'
tnmos_name = 'nmos_sky'

# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'

# Design hierarchy
libname = 'logic_generated'
ref_dir_template = './laygo2_example/logic/' #export this layout's information into the yaml in this dir 
ref_dir_MAG_exported = './laygo2_example/logic/TCL/'
yaml_import_path = './laygo2_example/logic/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tlogic = laygo2.interface.yaml.import_template(filename= yaml_import_path +'logic_generated_templates.yaml')
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
# tlib = laygo2.interface.yaml.import_template(filename=export_path+'logic_generated_templates.yaml') # Uncomment if you use the logic templates
# print(templates[tpmos_name], templates[tnmos_name], sep="\n") # Uncomment if you want to print templates

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name]
# print(grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name], sep="\n") # Uncomment if you want to print grids

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
   in0 = tnmos.generate(name='MN0',                 params={'nf': nf, 'tie': 'S'})
   in1 = tnmos.generate(name='MN1',                 params={'nf': nf})
   in2 = tnmos.generate(name='MN2',                 params={'nf': nf})
   in3 = tnmos.generate(name='MN3',                 params={'nf': nf, 'tie': 'S'})
   in4 = tnmos.generate(name='MN4',                 params={'nf': nf, 'tie': 'S'}) 
   ip0 = tpmos.generate(name='MP0', transform='MX', params={'nf': nf, 'tie': 'S'})
   ip1 = tpmos.generate(name='MP1', transform='MX', params={'nf': nf})
   ip2 = tpmos.generate(name='MP2', transform='MX', params={'nf': nf})
   ip3 = tpmos.generate(name='MP3', transform='MX', params={'nf': nf, 'tie': 'S'})
   ip4 = tpmos.generate(name='MP4', transform='MX', params={'nf': nf, 'tie': 'S'})
   nspace0 = templates['nmos13_fast_space_2x'].generate(name='nspace0')
   nspace1 = templates['nmos13_fast_space_2x'].generate(name='nspace1')
   pspace0 = templates['pmos13_fast_space_2x'].generate(name='pspace0', transform='MX')
   pspace1 = templates['pmos13_fast_space_2x'].generate(name='pspace1', transform='MX')
   tap0 = tlogic['TAP'].generate(name='TAP0')
   
# 4. Place instances.
   dsn.place(grid=pg, inst=in0,     mn=[0,0])
   dsn.place(grid=pg, inst=in1,     mn=pg.mn.bottom_right(in0))
   dsn.place(grid=pg, inst=nspace0, mn=pg.mn.bottom_right(in1))
   dsn.place(grid=pg, inst=nspace1, mn=pg.mn.bottom_right(nspace0))
   dsn.place(grid=pg, inst=in2,     mn=pg.mn.bottom_right(nspace1))
   dsn.place(grid=pg, inst=in3,     mn=pg.mn.bottom_right(in2))
   dsn.place(grid=pg, inst=in4,     mn=pg.mn.bottom_right(in3))
   
   dsn.place(grid=pg, inst=ip0,     mn=pg.mn.top_left(in0) + pg.mn.height_vec(ip0))
   dsn.place(grid=pg, inst=ip1,     mn=pg.mn.top_right(ip0))
   dsn.place(grid=pg, inst=pspace0, mn=pg.mn.top_right(ip1))
   dsn.place(grid=pg, inst=pspace1, mn=pg.mn.top_right(pspace0))
   dsn.place(grid=pg, inst=ip2,     mn=pg.mn.top_right(pspace1))
   dsn.place(grid=pg, inst=ip3,     mn=pg.mn.top_right(ip2))
   dsn.place(grid=pg, inst=ip4,     mn=pg.mn.top_right(ip3))
   dsn.place(grid=pg, inst=tap0,    mn=pg.mn.bottom_right(in4))
# 5. Create and place wires.
   print("Create wires")

   # I0
   _mn = [r23.mn(in0.pins['G'])[0], r23.mn(ip0.pins['G'])[0]]
   vin00, rin00, vin01 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])
   
   # I1
   _mn = [r23.mn(in3.pins['G'])[1], r23.mn(ip3.pins['G'])[1]]
   vin10, rin10, vin11 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])
   
   # OUT
   _mn = [r23.mn(in4.pins['D'])[1], r23.mn(ip4.pins['D'])[1]]
   vout0, rout0, vout1 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])
   
   # EN0
   _mn = [r23.mn(in1.pins['G'])[0], r23.mn(ip2.pins['G'])[0]]
   _track = [r23.mn.bbox(nspace0)[1,0],None]
   ren0 = dsn.route_via_track(grid=r23, mn=_mn, track=_track)
   
   # EN1
   _mn = [r23.mn(in2.pins['G'])[0], [r23.mn.bbox(pspace0)[0,0], r23.mn(ip1.pins['D'])[0,1]]]
   _track = [r23.mn.bbox(nspace1)[1,0], None]
   ren1 = dsn.route_via_track(grid=r23, mn=_mn, track=_track)
   
   _mn = [r23.mn(ip1.pins['G'])[0], [r23.mn.bbox(pspace0)[0,0], r23.mn(ip1.pins['D'])[0,1]]]
   _track = [r23.mn.bbox(nspace0)[0,0], None]
   dsn.route_via_track(grid=r23, mn=_mn, track=_track)
   
   ################################ ADDED FOR DRC ################################
   _mn = [r23.mn.bbox(ren1[1][0])[0], r23.mn.bbox(ren1[1][0])[0]+[0,1]]
   dsn.route(grid=r23, mn=_mn)
   ############################## LINES FOR DRC END ##############################

   # Internal
   _mn = [r23.mn(in0.pins['D'])[0], r23.mn(in1.pins['D'])[0]]
   dsn.route(grid=r23, mn=_mn)

   _mn = [r23.mn(ip0.pins['D'])[0], r23.mn(ip1.pins['D'])[0]]
   dsn.route(grid=r23, mn=_mn)
   
   _mn = [r23.mn(in1.pins['S'])[0], r23.mn(ip2.pins['S'])[1]]
   _track = [r23.mn(in2.pins['S'])[1,0], None]
   dsn.route_via_track(grid=r23, mn=_mn, track=_track)

   if nf == 2:
      _mn = [r23.mn(ip1.pins['S'])[1], r23.mn(in4.pins['G'])[0]]
      _track = [r23.mn(in4.pins['RAIL'])[0,0], None]
      dsn.route_via_track(grid=r23, mn=_mn, track=_track)

      _mn = [r23.mn(ip4.pins['G'])[0], r23.mn(in4.pins['G'])[0]]
      dsn.route_via_track(grid=r23, mn=_mn, track=_track)

   else:
      _mn = [r23.mn(ip1.pins['S'])[1], r23.mn(in4.pins['G'])[0]]
      _track = [r23.mn(in4.pins['G'])[0,0], None]
      dsn.route_via_track(grid=r23, mn=_mn, track=_track)
      dsn.via(grid=r23, mn=r23.mn(ip4.pins['G'])[0])
   
   _mn = [r23.mn(in2.pins['D'])[0], r23.mn(in3.pins['D'])[0]]
   dsn.route(grid=r23, mn=_mn)

   _mn = [r23.mn(ip2.pins['D'])[0], r23.mn(ip3.pins['D'])[0]]
   dsn.route(grid=r23, mn=_mn)
   
   # VSS
   rvss0 = dsn.route(grid=r12, mn=[r12.mn(in0.pins['RAIL'])[0], r12.mn(in4.pins['RAIL'])[1]])
   
   # VDD
   rvdd0 = dsn.route(grid=r12, mn=[r12.mn(ip0.pins['RAIL'])[0], r12.mn(ip4.pins['RAIL'])[1]])
   
# 6. Create pins.
   pin0 = dsn.pin(name='I0', grid=r23, mn=r23.mn.bbox(rin00))
   pin1 = dsn.pin(name='I1', grid=r23, mn=r23.mn.bbox(rin10))
   pen0 = dsn.pin(name='EN0', grid=r23, mn=r23.mn.bbox(ren0[2]))
   pen1 = dsn.pin(name='EN1', grid=r23, mn=r23.mn.bbox(ren1[2]))
   pout0 = dsn.pin(name='O', grid=r23, mn=r23.mn.bbox(rout0))
   pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
   pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))
   
# 7. Export to physical database.
   print("Export design")
   print("")
   laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')
   # Filename example: ./laygo2_generators_private/logic/skill/logic_generated_mux2to1_2x.il
   
# 8. Export to a template database file.
   nat_temp = dsn.export_to_template()
   laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
   # Filename example: ./laygo2_generators_private/logic/logic_generated_templates.yaml