##########################################
#                                        #
#       Inverter Layout Gernerator       #
#         Created by Taeho Shin          #
#                                        #
##########################################

import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech

# Parameter definitions #############
# Variables
cell_type = ['inv_tap']
#nf_list = [2, 4, 6, 8, 10, 12, 16, 24, 32, 36, 40, 50, 64, 72, 100]
#nf_list = [2, 4, 6, 8, 10, 12, 16, 24, 32]
nf_list = [2,4]
# Templates
tpmos_name = 'pmos_sky'
tnmos_name = 'nmos_sky'
tptap_name = 'ptap_sky'
tntap_name = 'ntap_sky'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
# Design hierarchy
libname = 'logic_generated'
# cellname in for loop
ref_dir_template = './laygo2_example/logic/' #export this layout's information into the yaml in this dir 
ref_dir_MAG_exported = './laygo2_example/logic/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tptap, tntap = templates[tptap_name], templates[tntap_name] 
#tlib = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_generated_templates.yaml')
print(templates[tpmos_name], templates[tnmos_name], sep="\n")

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23 = grids[pg_name], grids[r12_name], grids[r23_name]
print(grids[pg_name], grids[r12_name], grids[r23_name], sep="\n")

lib = laygo2.object.database.Library(name=libname)

for celltype in cell_type:
   for nf in nf_list:
      cellname = celltype+'_'+str(nf)+'x'
      print('--------------------')
      print('Now Creating '+cellname)
      
      # 2. Create a design hierarchy
      dsn = laygo2.object.database.Design(name=cellname, libname=libname)
      lib.append(dsn)
      
      # 3. Create instances.
      print("Create instances")
      in0 = tnmos.generate(name='MN0', params={'nf': nf, 'tie': 'S'})
      ip0 = tpmos.generate(name='MP0', transform='MX', params={'nf': nf,'tie': 'S'})
      intp0 = tntap.generate(name='MNT0', params={'nf':2, 'tie':'TAP0'})
      iptp0 = tptap.generate(name='MPT0', transform='MX', params={'nf':2, 'tie':'TAP0'})
      # 4. Place instances.
      #   dsn.place(grid=pg, inst=[[in0], [ip0]], mn=[0,0])
      #   dsn.place(grid=pg, inst=[[in0 ,in1], [ip0, ip1]], mn=[0,0])
      dsn.place(grid=pg, inst=in0, mn=[0,0])
      dsn.place(grid=pg, inst=ip0, mn=pg.mn.top_left(in0) + pg.mn.height_vec(ip0))
      dsn.place(grid=pg, inst=intp0, mn=pg.mn.bottom_right(in0))
      dsn.place(grid=pg, inst=iptp0, mn=pg.mn.top_right(ip0))
      # 5. Create and place wires.
      print("Create wires")
      # IN
      _mn = [r23.mn(in0.pins['G'])[0], r23.mn(ip0.pins['G'])[0]]
      _track = [r23.mn(in0.pins['G'])[0,0]-1, None]
      rin0 = dsn.route_via_track(grid=r23, mn=_mn, track=_track)
      for routeObj in rin0:
         if type(routeObj) is list:
            print(routeObj[0])
         else:
            print(routeObj)
      # OUT
      if celltype == 'inv':
         _mn = [r23.mn(in0.pins['D'])[1], r23.mn(ip0.pins['D'])[1]]
         vout0, rout0, vout1 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])
         print(rout0)
      elif celltype == 'inv_hs':
         for i in range(int(nf/2)):
            _mn = [r23.mn(in0.pins['D'])[0]+[2*i,0], r23.mn(ip0.pins['D'])[0]+[2*i,0]]
            vout0, rout0, vout1 = dsn.route(grid=r23, mn=_mn, via_tag=[True, True])
            print("metal :", rout0)
            pout0 = dsn.pin(name='O'+str(i), grid=r23, mn=r23.mn.bbox(rout0))
            print("pin :",pout0)
      # VSS
      rvss0 = dsn.route(grid=r12, mn=[r12.mn(in0.pins['RAIL'])[0], r12.mn(in0.pins['RAIL'])[1]])
      print(rvss0)
      # VDD
      rvdd0 = dsn.route(grid=r12, mn=[r12.mn(ip0.pins['RAIL'])[0], r12.mn(ip0.pins['RAIL'])[1]])
      print(rvdd0)
      # 6. Create pins.
      pin0 = dsn.pin(name='I', grid=r23, mn=r23.mn.bbox(rin0[2]))
      if celltype == 'inv':
         pout0 = dsn.pin(name='O', grid=r23, mn=r23.mn.bbox(rout0))
      pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
      pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))
      
      # 7. Export to physical database.
      print("Export design")
      print("")
      
      # Uncomment for BAG export
      laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')
      # 8. Export to a template database file.
      nat_temp = dsn.export_to_template()
      laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
