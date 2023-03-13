##############################################
#                                            #
#       PROJECT: SCAN CHAIN AUTOMATION       #
#       SCAN CHAIN LAYOUT GENERATOR          #
#       CREATED BY TAEHO SHIN                #
#                                            #
##############################################

import yaml
# import bag
import numpy as np
import math
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech

############################### LOAD SPEC ###############################
spec = "./laygo2_example/scan/scan_spec.yaml"
with open(spec, 'r') as stream:
   specdict = yaml.load(stream, Loader=yaml.FullLoader)

bit = specdict['bit']
row = specdict['row']
col = math.ceil(bit/row)
rename = []
for i in range(bit):
   rename.append('SCAN_DATA_OUT<'+str(i)+'>')
############################# LOAD SPEC END #############################

############################# BASIC SETTINGS  ############################
### NAMES OF GRIDS
pg_name   = 'placement_basic'
r12_name  = 'routing_12_cmos'
r23_name  = 'routing_23_cmos'
r34_name  = 'routing_34_basic'

tptap_name = 'ptap_sky'
tntap_name = 'ntap_sky'

libname  = 'scan_generated'
cellname = 'scan_chain_' + str(bit) + 'bit' # Example: scan_chain_1024bit

ref_dir_template = './laygo2_example/scan/'
ref_dir_MAG_exported = './laygo2_example/scan/TCL/'
yaml_import_path = './laygo2_example/logic/' #logic_generated.yaml path
ref_dir_layout = './magic_layout'

tlib = laygo2.interface.yaml.import_template(filename=ref_dir_template+libname+'_templates.yaml')
tlogic = laygo2.interface.yaml.import_template(filename='./laygo2_example/logic/logic_generated_templates.yaml')
# Filename example: ./laygo2_generators_private/scan/scan_generated_templates.yaml

templates = tech.load_templates()
grids = tech.load_grids(templates = templates)
pg, r12, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name]

lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)
########################### BASIC SETTINGS END ##################################

########################## CHAIN GENERATION START  ##############################
cell_list = []
tScanCell  = tlib[ 'scan_cell' ]
_size = tScanCell.bbox()[1]
_pitch = _size + r34.xy([(col+1)*3,0])
I0  = tScanCell.generate(name='I0',shape=[row, col],pitch=_pitch)
NTAP0 = templates[tntap_name].generate(name='MNT1', transform='MX', params={'nf':col, 'tie':'TAP0'},shape=[row, col],pitch=_pitch)
NTAP1 = templates[tntap_name].generate(name='MNT0', params={'nf':col, 'tie':'TAP0'},shape=[row, col],pitch=_pitch)
PTAP0 = templates[tptap_name].generate(name='MPT0', params={'nf':col, 'tie':'TAP0'},shape=[row, col],pitch=_pitch)
PTAP1 = templates[tptap_name].generate(name='MPT1', transform='MX', params={'nf':col, 'tie':'TAP0'},shape=[row, col],pitch=_pitch)
#DMY_BYPASS = tlogic['space_1x'].generate(name='BYP0', shape=[row, col],pitch=_pitch)
_cellsize = pg.mn(tScanCell.bbox())[1]
dsn.place(grid=pg, inst=I0, mn=[0,0])
dsn.place(grid=pg, inst=NTAP0, mn = [_cellsize[0],_cellsize[1]*col - _cellsize[1]/2])
dsn.place(grid=pg, inst=NTAP1, mn = [_cellsize[0],_cellsize[1]/2])
dsn.place(grid=pg, inst=PTAP0, mn = [_cellsize[0],0])
dsn.place(grid=pg, inst=PTAP1, mn = [_cellsize[0],_cellsize[1]*col])

# GLOBAL BOUNDARIES FOR DESIGN RULES
# ONLY EXECUTE WHEN ENCLOSURE DRC ERROR OCCURED
# for i in range(col):
#    # Generate Global Boundaries
#    ngbndl0 = templates['ptap_fast_left' ].generate(name='I00'+str(i))
#    ngbndl1 = templates['ptap_fast_left' ].generate(name='I01'+str(i))
#    ngbndr0 = templates['ptap_fast_right'].generate(name='I10'+str(i))
#    ngbndr1 = templates['ptap_fast_right'].generate(name='I11'+str(i))
#    pgbndl0 = templates['ntap_fast_left' ].generate(name='I20'+str(i), transform='MY')
#    pgbndl1 = templates['ntap_fast_left' ].generate(name='I21'+str(i))
#    pgbndr0 = templates['ntap_fast_right'].generate(name='I30'+str(i))
#    pgbndr1 = templates['ntap_fast_right'].generate(name='I31'+str(i))

#    # Place Global boundaries
#    # Left
#    dsn.place(grid=pg, inst=pgbndl0, mn=pg.mn.bottom_left(I0[0,i-1]))
#    dsn.place(grid=pg, inst=ngbndl0, mn=pg.mn.top_left(pgbndl0))
#    dsn.place(grid=pg, inst=ngbndl1, mn=pg.mn.top_left(ngbndl0))
#    dsn.place(grid=pg, inst=pgbndl1, mn=pg.mn.top_left(ngbndl1))
#    # Right
#    dsn.place(grid=pg, inst=pgbndr0, mn=pg.mn.bottom_right(I0[-1,i-1]))
#    dsn.place(grid=pg, inst=ngbndr0, mn=pg.mn.top_left(pgbndr0))
#    dsn.place(grid=pg, inst=ngbndr1, mn=pg.mn.top_left(ngbndr0))
#    dsn.place(grid=pg, inst=pgbndr1, mn=pg.mn.top_left(ngbndr1))

# connect power rail between rows
_pitch_vec = r12.mn(r34.xy([(col+1)*3,0]))
_init_vec = r12.mn.bottom_right(I0[0,0])
for row_idx in range(row-1):
   _vec = (_init_vec + _pitch_vec)*row_idx + _init_vec
   _mn = [_vec, _vec + _pitch_vec ]
   for idx in range(col*2+1):
      dsn.route(grid=r12, mn=_mn)
      _mn[0][1] = _mn[0][1]+8
      _mn[1][1] = _mn[1][1]+8

# from array index to list index
full_row = bit-row*((col-1))
for row_idx in range(full_row):
   for col_idx in range(col):
      cell_list.append(I0[row_idx,col_idx])

for row_idx in range(full_row, row):
   for col_idx in range(col-1):
      cell_list.append(I0[row_idx,col_idx])

cell_eff = cell_list[0:bit]
cell_dummy = cell_list[bit:]

# SCAN_LOAD, SCAN_EN, SCAN_GATE
# connect each nodes with single vertical M3 of full rows
for row_idx in range(full_row):
   _mn = [r23.mn(I0[row_idx,0].pins['SCAN_LOAD'])[0], r23.mn(I0[row_idx,-1].pins['SCAN_LOAD'])[0]]
   dsn.route(grid=r23, mn=_mn)

   _mn = [r23.mn(I0[row_idx,0].pins['SCAN_EN'  ])[0], r23.mn(I0[row_idx,-1].pins['SCAN_EN'  ])[0]]
   dsn.route(grid=r23, mn=_mn)

   _mn = []
   for col_idx in range(col):
      _mn.append( r34.mn(I0[row_idx,col_idx].pins['SCAN_GATE'])[1] )
   _track = [(r34.mn(I0[row_idx,0].pins['SCAN_DATA_OUT'])[0,0]+10),None]
   dsn.route_via_track(grid=r34,mn=_mn,track=_track)

cells_in_rest_col = col-1
# unfilled rows
for row_idx in range(full_row, row):
   _mn = [r23.mn(I0[row_idx,0].pins['SCAN_LOAD'])[0], r23.mn(I0[row_idx,cells_in_rest_col-1].pins['SCAN_LOAD'])[0]]
   dsn.route(grid=r23, mn=_mn)

   _mn = [r23.mn(I0[row_idx,0].pins['SCAN_EN'  ])[0], r23.mn(I0[row_idx,cells_in_rest_col-1].pins['SCAN_EN'  ])[0]]
   dsn.route(grid=r23, mn=_mn)

   _mn = []
   for col_idx in range(col):
      _mn.append( r34.mn(I0[row_idx,col_idx].pins['SCAN_GATE'])[1] )
   _track = [(r34.mn(I0[row_idx,0].pins['SCAN_DATA_OUT'])[0,0]+10),None]
   dsn.route_via_track(grid=r34,mn=_mn,track=_track)
# row to row connection
for row_idx in range(row-1): # iteration : row-1 times
   _mn = [r34.mn(I0[row_idx,0].pins['SCAN_LOAD'])[0], r34.mn(I0[row_idx+1,0].pins['SCAN_LOAD'])[0]]
   dsn.route(grid=r34, mn=_mn, via_tag=[True, True])

   _mn = [r34.mn(I0[row_idx,0].pins['SCAN_EN'])[0], r34.mn(I0[row_idx+1,0].pins['SCAN_EN'])[0]]
#   _track = [None, np.mean(r34.mn(I0[0,0].pins['SCAN_EN'])[:,1], dtype=int)+4]
   _track = [None, r34.mn(I0[row_idx,0].pins['SCAN_EN'])[1,1]+3]
   dsn.route_via_track(grid=r34, mn=_mn, track=_track)

   _mn = [r34.mn(I0[row_idx,0].pins['SCAN_GATE'])[1], r34.mn(I0[row_idx+1,0].pins['SCAN_GATE'])[1]]
   _track = [None, r34.mn(I0[row_idx,0].pins['SCAN_GATE'])[1,1]+4]
   dsn.route_via_track(grid=r34, mn=_mn, track=_track)

# SCAN_CLK chain
# reversed index is needed
# rull rows
for row_idx in range(full_row):
   for col_idx in reversed(range(col-1)): # reversed index
      _mn = [r34.mn(I0[row_idx, col_idx+1].pins['SCAN_CLK_OUT'])[0], r34.mn(I0[row_idx, col_idx].pins['SCAN_CLK'])[1]]
      _track = [r34.mn(I0[row_idx, col_idx+1].pins['SCAN_CLK'])[0,0]-2, None]
      SCAN_CLK_chain = dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.via(grid=r34, mn=_mn[0])
      dsn.via(grid=r34, mn=_mn[1])

# unfilled rows
for row_idx in range(full_row, row):
   for col_idx in reversed(range(col-2)): # reversed index & one time less iteration
      _mn = [r34.mn(I0[row_idx, col_idx+1].pins['SCAN_CLK_OUT'])[0], r34.mn(I0[row_idx, col_idx].pins['SCAN_CLK'])[1]]
      _track = [r34.mn(I0[row_idx, col_idx].pins['SCAN_CLK'])[0,0]-2, None]
      SCAN_CLK_chain = dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.via(grid=r34, mn=_mn[0])
      dsn.via(grid=r34, mn=_mn[1])

# row to row connection
iter_total = row-1
if row * col == bit:
   for i in range(full_row-1): # one time less iteration
      _mn = [np.mean(r34.mn(cell_list[col-1 + col*i].pins['SCAN_CLK']), axis=0, dtype=int), r34.mn(cell_list[col + col*i].pins['SCAN_CLK_OUT'])[1]]
      _track = [r34.mn(cell_list[col + col*i].pins['SCAN_CLK_OUT'])[1,0]-2, None]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.via(grid=r34, mn=_mn[0])
      dsn.via(grid=r34, mn=_mn[1])

else:
   # full rows
   for i in range(full_row):
      _mn = [np.mean(r34.mn(cell_list[col * (i+1) -1].pins['SCAN_CLK']), axis=0, dtype=int), r34.mn(cell_list[col * (i+1)].pins['SCAN_CLK_OUT'])[1]]
      _track = [r34.mn(cell_list[col * (i+1)].pins['SCAN_CLK_OUT'])[1,0]-2, None]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.via(grid=r34, mn=_mn[0])
      dsn.via(grid=r34, mn=_mn[1])

   # unfilled rows
   for i in range(iter_total - full_row):
      _mn = [np.mean(r34.mn(cell_list[col-2 + full_row*col + (col-1)*i].pins['SCAN_CLK']), axis=0, dtype=int), r34.mn(cell_list[col-1 + full_row*col + (col-1)*i].pins['SCAN_CLK_OUT'])[1]]
      _track = [r34.mn(cell_list[col-1 + full_row*col + (col-1)*i].pins['SCAN_CLK_OUT'])[1,0]-2, None]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.via(grid=r34, mn=_mn[0])
      dsn.via(grid=r34, mn=_mn[1])

# SCAN_OUT to SCAN_IN
# full rows
for row_idx in range(full_row):
   for col_idx in range(col-1):
      _mn = [r34.mn(I0[row_idx,col_idx].pins['SCAN_OUT'])[1], r34.mn(I0[row_idx, col_idx+1].pins['SCAN_IN'])[0]]
      _track = [r34.mn(I0[row_idx,col_idx].pins['SCAN_OUT'])[1,0]-6, None]
      SCAN_OUT_chain = dsn.route_via_track(grid=r34, mn=_mn, track=_track)      
      dsn.via(grid=r34, mn=_mn[0])
      dsn.via(grid=r34, mn=_mn[1])

# unfilled rows
for row_idx in range(full_row, row):
   for col_idx in range(col-2): # reversed index & one time less iteration
      _mn = [r34.mn(I0[row_idx, col_idx].pins['SCAN_OUT'])[1], r34.mn(I0[row_idx, col_idx+1].pins['SCAN_IN'])[0]]
      _track = [r34.mn(I0[row_idx, col_idx].pins['SCAN_OUT'])[1,0]-6, None]
      SCAN_OUT_chain = dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.via(grid=r34, mn=_mn[0])
      dsn.via(grid=r34, mn=_mn[1])


# row to row connection
iter_total = row-1
if row * col == bit:
   for i in range(full_row-1): # one time less iteration
      _mn = [r34.mn(cell_list[col-1 + col*i].pins['SCAN_OUT'])[0], r34.mn(cell_list[col + col*i].pins['SCAN_IN'])[0]]
      _track = [r34.mn(cell_list[col + col*i].pins['SCAN_IN'])[1,0]-2, None]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.via(grid=r34, mn=_mn[0])
      dsn.via(grid=r34, mn=_mn[1])

else:
#    # full rows
   for i in range(full_row):
      _mn = [r34.mn(cell_list[col-1 + col*i].pins['SCAN_OUT'])[0], r34.mn(cell_list[col + col*i].pins['SCAN_IN'])[0]]
      _track = [r34.mn(cell_list[col + col*i].pins['SCAN_IN'])[1,0]-2, None]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.via(grid=r34, mn=_mn[0])
      dsn.via(grid=r34, mn=_mn[1])

#    # unfilled rows
   for i in range(iter_total - full_row):
      _mn = [r34.mn(cell_list[col-2 + full_row*col + (col-1)*i].pins['SCAN_OUT'])[0], r34.mn(cell_list[col-1 + full_row*col + (col-1)*i].pins['SCAN_IN'])[0]]
      _track = [r34.mn(cell_list[col-1 + full_row*col + (col-1)*i].pins['SCAN_IN'])[1,0]-2, None]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.via(grid=r34, mn=_mn[0])
      dsn.via(grid=r34, mn=_mn[1])

# SCAN_DATA_OUT top sort
# full rows
idx=0
for row_idx in range(full_row):
   for col_idx in range(col):
      end_pt = r34.mn.top_right(I0[row_idx,col-1])+[(col+1)*2+col_idx, 0]
      _mn = [ r34.mn(I0[row_idx,col_idx].pins['SCAN_DATA_OUT'])[0], end_pt ]
      _track = [None, r34.mn(I0[row_idx,col_idx].pins['SCAN_DATA_OUT'])[0,1]-2]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.pin(name=rename[idx], grid=r34, mn=[end_pt-[0,3], end_pt]) # pin position to the tail of M3      
      idx+=1

# unfilled rows
for row_idx in range(full_row, row):
   for col_idx in range(col-1):
      end_pt = r34.mn.top_right(I0[row_idx,col-1])+[(col+1)*2+col_idx, 0]
      _mn = [ r34.mn(I0[row_idx,col_idx].pins['SCAN_DATA_OUT'])[0], r34.mn.top_right(I0[row_idx,col-1])+[(col+1)*2+col_idx, 0] ]
      _track = [None, r34.mn(I0[row_idx,col_idx].pins['SCAN_DATA_OUT'])[0,1]-2]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track)  
      dsn.pin(name=rename[idx], grid=r34, mn=[end_pt-[0,3], end_pt]) # pin position to the tail of M3  
      idx+=1

# SCAN_DATA_IN top sort
# full rows
idx=0
for row_idx in range(full_row):
   for col_idx in range(col):
      end_pt = r34.mn.top_right(I0[row_idx,col-1])+[col_idx, 0]
      _mn = [ r34.mn(I0[row_idx,col_idx].pins['SCAN_DATA_IN'])[1], end_pt ]
      _track = [None, r34.mn(I0[row_idx,col_idx].pins['SCAN_DATA_IN'])[1,1]+3]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.pin(name='SCAN_DATA_IN<'+str(idx)+'>', grid=r34, mn=[end_pt-[0,3], end_pt]) # pin position to the tail of M3
      idx+=1

# unfilled rows
for row_idx in range(full_row, row):
   for col_idx in range(col-1):
      end_pt = r34.mn.top_right(I0[row_idx,col-1])+[col_idx, 0]
      _mn = [ r34.mn(I0[row_idx,col_idx].pins['SCAN_DATA_IN'])[1], end_pt ]
      _track = [None, r34.mn(I0[row_idx,col_idx].pins['SCAN_DATA_IN'])[1,1]+3]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track)
      dsn.pin(name='SCAN_DATA_IN<'+str(idx)+'>', grid=r34, mn=[end_pt-[0,3], end_pt]) # pin position to the tail of M3
      idx+=1

# SCAN_GATE_VALUE top sort
# full rows
idx=0
for row_idx in range(full_row):
   for col_idx in range(col):
      end_pt = r34.mn.top_right(I0[row_idx,col-1])+[(col+1)+col_idx, 0]
      _mn = [ r34.mn(I0[row_idx,col_idx].pins['SCAN_GATE_VALUE'])[0], r34.mn.top_right(I0[row_idx,col-1])+[(col+1)+col_idx, 0] ]
      _track = [None, r34.mn(I0[row_idx,col_idx].pins['SCAN_GATE_VALUE'])[0,1]-2]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track) 
      dsn.pin(name='SCAN_GATE_VALUE<'+str(idx)+'>', grid=r34, mn=[end_pt-[0,3], end_pt]) # pin position to the tail of M3     
      idx+=1

# unfilled rows
for row_idx in range(full_row, row):
   for col_idx in range(col-1):
      end_pt = r34.mn.top_right(I0[row_idx,col-1])+[(col+1)+col_idx, 0]
      _mn = [ r34.mn(I0[row_idx,col_idx].pins['SCAN_GATE_VALUE'])[0], r34.mn.top_right(I0[row_idx,col-1])+[(col+1)+col_idx, 0] ]
      _track = [None, r34.mn(I0[row_idx,col_idx].pins['SCAN_GATE_VALUE'])[0,1]-2]
      dsn.route_via_track(grid=r34, mn=_mn, track=_track) 
      dsn.pin(name='SCAN_GATE_VALUE<'+str(idx)+'>', grid=r34, mn=[end_pt-[0,3], end_pt]) # pin position to the tail of M3           
      idx+=1

# VERTICAL POWER RAIL
_mn = [r23.mn.bottom_left(I0[0,0])+[1,0],r23.mn.top_left(I0[0,-1])+[1,0]]
rvdd = dsn.route(grid=r23, mn=_mn, via_tag=[True,True])
dsn.pin(name='VDD', grid=r23, mn=r23.mn.bbox(rvdd[1]), netname='VDD') 
_mn = [r23.mn.bottom_left(I0[0,0])+[3,8],r23.mn.top_left(I0[0,-1])+[3,-8]]
rvss = dsn.route(grid=r23, mn=_mn, via_tag=[True,True])
dsn.pin(name='VSS', grid=r23, mn=r23.mn.bbox(rvss[1]), netname='VSS')
for col_idx in range(col-1):
   dsn.via(grid=r23, mn=r23.mn.bottom_left(I0[0,col_idx+1])+[1,0]) # VDD VIA
   dsn.via(grid=r23, mn=r23.mn.bottom_left(I0[0,col_idx+1])+[3,8]) # VSS VIA

### GENERATE PINS
# SCAN_CLK_OUT, SCAN_IN, SCAN_EN
pin_list = ['SCAN_CLK_OUT', 'SCAN_EN']
for pin in pin_list:
   _mn = np.asarray([r34.mn.bbox(cell_eff[0].pins[pin])[0], r34.mn.bbox(cell_eff[0].pins[pin])[0]+[3,0]])
   _mn[:,1] = np.mean(r34.mn.bbox(cell_eff[0].pins[pin])[:,1], dtype=int)
   rpin0 = dsn.route(grid=r34, mn=_mn, via_tag=[True, False])

   _mn = np.asarray([r34.mn.bbox(rpin0[1])[1], r34.mn.bottom_left(cell_eff[0])])
   _mn[:,0] = r34.mn.bbox(rpin0[1])[1,0]
   rpin1 = dsn.route(grid=r34, mn=_mn, via_tag=[True, False])
   dsn.pin(name=pin, grid=r34, mn=[r34.mn.bbox(rpin1[1])[0], r34.mn.bbox(rpin1[1])[0]+[0,3]])

# SCAN_GATE
# _mn = [r45.mn(cell_eff[0].pins['SCAN_GATE'])[1], r45.mn.bottom_left(cell_eff[0])]
_mn = [r34.mn(cell_eff[0].pins['SCAN_GATE'])[1], r34.mn.bottom_left(cell_eff[0])]
_mn[1][0] = _mn[0][0] = r34.mn(cell_eff[0].pins['SCAN_DATA_OUT'])[0,0]+10
rpin0 = dsn.route(grid=r34, mn=_mn)
dsn.pin(name='SCAN_GATE', grid=r34, mn=[r34.mn.bbox(rpin0)[0], r34.mn.bbox(rpin0)[0]+[0,3]])


# SCAN_CLK, SCAN_OUT
_mn = [ r34.mn(cell_eff[-1].pins['SCAN_CLK'])[1], r34.mn(cell_eff[-1].pins['SCAN_CLK'])[1] - [6,0], r34.mn.top_left(I0[row-1,col-1])]
_mn[2][0] = _mn[1][0]
dsn.route(grid=r34, mn = _mn, via_tag=[True, True, False])
dsn.pin(name='SCAN_CLK', grid=r34, mn=[ _mn[2]-[0,3], _mn[2]])

_mn = [r34.mn(cell_eff[0].pins['SCAN_IN'])[1], r34.mn(cell_eff[0].pins['SCAN_IN'])[0] - [0,5]]
dsn.route(grid=r34, mn = _mn, via_tag=[False,False])
dsn.pin(name='SCAN_IN', grid=r34, mn=[ _mn[1], _mn[1]+[0,3] ])

_mn = [r34.mn(cell_eff[-1].pins['SCAN_OUT'])[1]-[1,0], r34.mn(cell_eff[-1].pins['SCAN_OUT'])[1]+[2,0], r34.mn.top_right(I0[row-1,col-1])]
_mn[2][0] = _mn[1][0]
dsn.route(grid=r34, mn = _mn, via_tag=[False,True,False])
dsn.via(grid=r34, mn=r34.mn(cell_eff[-1].pins['SCAN_OUT'])[1])
dsn.pin(name='SCAN_OUT', grid=r34, mn=[ _mn[2]-[0,3], _mn[2] ])
# SCAN_LOAD
_mn = [r34.mn.bottom_left(cell_eff[0]), r34.mn(cell_eff[0].pins['SCAN_LOAD'])[0]]
_mn[0][0] = _mn[1][0]
dsn.route(grid=r34, mn=_mn, via_tag=[False, False])
dsn.pin(name='SCAN_LOAD', grid=r34, mn=_mn)

print('%dbit %d X %d scan chain generated'%(bit,row,col))
################################### CHAIN GENERATION END ##########################################

### EXPORT TO BAG
# SKILL script for load in Virtuoso
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported+libname+'_'+cellname+'.tcl', libpath = ref_dir_layout, cellname=None, scale=1, reset_library=False, tech_library="sky130A")

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
# Filename example: ./laygo2_generators_private/scan/scan_generated_templates.yaml 
