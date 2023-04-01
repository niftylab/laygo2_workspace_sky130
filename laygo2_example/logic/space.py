##########################################################
#                                                        #
#                 SPACE Layout Gernerator                #
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
cell_type = 'space'
nf_list = [1,2,4,8,14]

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
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
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
   nspace = templates['nmos13_fast_space_1x'].generate(name='nspace',                 shape=[nf, 1])
   pspace = templates['pmos13_fast_space_1x'].generate(name='pspace', transform='MX', shape=[nf, 1])
   
# 4. Place instances.
   dsn.place(grid=pg, inst=nspace, mn=[0,0])
   dsn.place(grid=pg, inst=pspace, mn=pg.mn.top_left(nspace)+pg.mn.height_vec(nspace))
   
# 5. Create and place wires.
   print("Create wires")
   
   # VSS
   if nf != 1:
      rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(nspace), r12.mn.bottom_right(nspace)])
   
   # VDD
      rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(pspace), r12.mn.top_right(pspace)])
   
# 6. Create pins.
      pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
      pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))
   
# 7. Export to physical database.
   print("Export design")
   print("")
   laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported+libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')
      
   # 8. Export to a template database file.
   nat_temp = dsn.export_to_template()
   laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
   # Filename example: ./laygo2_generators_private/logic/logic_generated_templates.yaml