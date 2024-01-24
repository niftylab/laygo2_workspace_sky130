#!/usr/bin/python
########################################################################################################################
#
# Copyright (c) 2014, Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#   disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################################################################

import laygo2.object.template
import laygo2.object.physical
import laygo2.object.database
#from . import laygo2_tech_grids

import numpy as np
import yaml
import pprint
import copy

# Template library for target technology.

# Technology parameters
tech_fname = './laygo2_tech/laygo2_tech.yaml'
with open(tech_fname, 'r') as stream:
    try:
        tech_params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
libname = list(tech_params['templates'].keys())[0]  # libname
templates = tech_params['templates'][libname]
grids = tech_params['grids'][libname]


# Template functions for primitive devices
def _mos_update_params(params):
    """Make a complete parameter table for mos"""
    if 'nf' not in params:  # number of fingers
        params['nf'] = 1
    if 'nfdmyl' not in params:  # number of left-dummy fingers
        params['nfdmyl'] = 0
    if 'nfdmyr' not in params:  # number of right-dummy fingers
        params['nfdmyr'] = 0
    if 'trackswap' not in params:  # source-drain track swap
        params['trackswap'] = False
    if 'tie' not in params:  # tie to power rail
        params['tie'] = None
    if 'bndl' not in params:  # create local left boundary
        params['bndl'] = True
    if 'bndr' not in params:  # create local right boundary
        params['bndr'] = True
    if 'gbndl' not in params:  # create global left boundary
        params['gbndl'] = False
    if 'gbndr' not in params:  # create global right boundary
        params['gbndr'] = False
    if 'unit_size_core' not in params:  # core unit size
        params['unit_size_core'] = np.array(templates['nmos130_fast_center_nf2']['unit_size'])
    if 'unit_size_dmy' not in params:  # dummy size
        params['unit_size_dmy'] = np.array(templates['nmos130_fast_dmy_nf2']['unit_size'])
    if 'unit_size_bndl' not in params:  # left boundary unit size
        params['unit_size_bndl'] = np.array(templates['nmos130_fast_boundary']['unit_size'])
    if 'unit_size_bndr' not in params:  # right boundary unit size
        params['unit_size_bndr'] = np.array(templates['nmos130_fast_boundary']['unit_size'])
    if 'unit_size_gbndl' not in params:  # left boundary unit size
        params['unit_size_gbndl'] = np.array(templates['nmos130_fast_left']['unit_size'])
    if 'unit_size_gbndr' not in params:  # right boundary unit size
        params['unit_size_gbndr'] = np.array(templates['nmos130_fast_right']['unit_size'])
    return params
    

def mos_bbox_func(params):
    """Computes x and y coordinate values from params."""
    params = _mos_update_params(params)
    xy = np.array(templates['nmos130_fast_center_nf2']['xy'])#, dtype=np.int)
    xy[1, 0] = xy[0, 0] + params['unit_size_core'][0] * params['nf']/2
    if params['gbndl']:
        xy[1, 0] += params['unit_size_gbndl'][0]
    if params['bndl']:
        xy[1, 0] += params['unit_size_bndl'][0]
    if params['nfdmyl'] > 0:
        xy[1, 0] += params['unit_size_dmy'][0] * round(params['nfdmyl']/2)
    if params['nfdmyr'] > 0:
        xy[1, 0] += params['unit_size_dmy'][0] * round(params['nfdmyr']/2)
    if params['bndr']:
        xy[1, 0] += params['unit_size_bndr'][0]
    if params['gbndr']:
        xy[1, 0] += params['unit_size_gbndr'][0]
    return xy


def _mos_route(devtype, params):
    """internal function to create routing structure of mosfets"""
    params = _mos_update_params(params)

    # Routing offsets
    offset = np.array([0, 0])
    offset_rail = np.array([0, 0])
    offset_dmyl = np.array([0, 0])
    offset_dmyr = np.array([0, 0])
    if params['gbndl']:
        offset[0] += params['unit_size_gbndl'][0]
    offset_rail[0] = offset[0]
    if params['bndl']:
        offset[0] += params['unit_size_bndl'][0]
    offset_dmyl[0] = offset[0]
    offset[0] += params['unit_size_dmy'][0] * round(params['nfdmyl']/2)
    offset_dmyr[0] = offset[0] + params['unit_size_core'][0] * round(params['nf']/2)
    nelements = dict()
    # Basic terminals
    if devtype == 'nmos' or devtype == 'pmos':
        ref_temp_name = 'nmos130_fast_center_nf2'  # template for param calculations
        ref_dmy_temp_name = 'nmos130_fast_center_nf2'  # dummy template for param calculations
        ref_pin_name = 'S0'  # left-most pin for parameter calculations
        name_list = ['G', 'S', 'D']  
        if params['trackswap']:  # source-drain track swap
            yidx_list = [3, 2, 1]  # y-track list
        else:
            yidx_list = [3, 1, 2]
        pin_name_list = ['G0', 'S0', 'D0']  # pin nam list to connect
    elif devtype == 'ptap' or devtype == 'ntap':
        ref_temp_name = 'ptap_fast_center_nf2_v2'
        ref_dmy_temp_name = 'ptap_fast_center_nf2_v2'
        ref_pin_name = 'TAP0'
        name_list = ['TAP0', 'TAP1']
        if params['trackswap']:  # source-drain track swap
            yidx_list = [2, 1]
        else:
            yidx_list = [1, 2]
        pin_name_list = ['TAP0', 'TAP1']
    for _name, _yidx, _pin_name in zip(name_list, yidx_list, pin_name_list):
        if params['tie'] == _name: 
            continue  # do not generate routing elements
        # compute routing cooridnates
        x0 = templates[ref_temp_name]['pins'][_pin_name]['xy'][0][0]
        x1 = templates[ref_temp_name]['pins'][_pin_name]['xy'][1][0]
        x = round((x0 + x1)/2) + offset[0] # center coordinate 
        x0 = x
        x1 = x + params['unit_size_core'][0] * round(params['nf']/2-1)
        if _pin_name == ref_pin_name:  # extend route to S1 
            x1 += params['unit_size_core'][0]
        
        y = grids['routing_12_cmos']['horizontal']['elements'][_yidx] + offset[1]
        vextension = round(grids['routing_12_cmos']['horizontal']['width'][_yidx]/2)
        if x0 == x1:  # zero-size wire
            hextension = grids['routing_12_cmos']['vertical']['extension0'][0] 
            if _pin_name == 'G0' and params['nf'] == 2: # extend G route when nf is 2 to avoid DRC errror
                hextension = hextension + 0
            elif _pin_name == 'D0' and params['nf'] == 2 and params['tie'] != 'D': # extend D route when nf is 2 and not tied with D
                hextension = hextension + 0
            elif _pin_name == 'S0' and params['nf'] == 2 and params['tie'] != 'S': # extend S route when nf is 2 and not tied with S
                hextension = hextension + 0
        else:
            hextension = grids['routing_12_cmos']['vertical']['extension'][0] + 28
        rxy = [[x0, y], [x1, y]]
        rlayer=grids['routing_12_cmos']['horizontal']['layer'][_yidx]
        # metal routing
        color = grids['routing_12_cmos']['horizontal']['ycolor'][_yidx]
        rg = laygo2.object.Rect(xy=rxy, layer=rlayer, name='R' + _name + '0', 
                                hextension=hextension, vextension=vextension, color=color)
        nelements['R' + _name + '0'] = rg
        # via
        vname = grids['routing_12_cmos']['via']['map'][0][_yidx]
        idx = round(params['nf']/2)
        if _pin_name == ref_pin_name:  # extend route to S1 
            idx += 1
        ivia = laygo2.object.Instance(name='IV' + _name + '0', xy=[x, y], libname=libname, cellname=vname, 
                                      shape=[idx, 1], pitch=params['unit_size_core'], 
                                      unit_size=params['unit_size_core'], pins=None, transform='R0')
        nelements['IV'+_name + '0'] = ivia
    # Horizontal rail
    x0 = templates[ref_temp_name]['pins'][ref_pin_name]['xy'][0][0]
    x1 = templates[ref_temp_name]['pins'][ref_pin_name]['xy'][1][0]
    x = round((x0 + x1)/2) + offset_rail[0] # center coordinate 
    x0 = x
    x1 = x + params['unit_size_core'][0] * round(params['nf']/2)
    x1 += params['unit_size_dmy'][0] * round(params['nfdmyl']/2)
    x1 += params['unit_size_dmy'][0] * round(params['nfdmyr']/2)
    if params['bndl']:
        x1 += params['unit_size_bndl'][0]
    if params['bndr']:
        x1 += params['unit_size_bndr'][0]
    y=grids['routing_12_cmos']['horizontal']['elements'][0] + offset_rail[1]
    vextension = round(grids['routing_12_cmos']['horizontal']['width'][0]/2)
    hextension = grids['routing_12_cmos']['vertical']['extension'][0] 
    rxy = [[x0, y], [x1, y]]
    rlayer=grids['routing_12_cmos']['horizontal']['layer'][0]
    color = grids['routing_12_cmos']['horizontal']['ycolor'][0]
    # metal routing
    rg = laygo2.object.Rect(xy=rxy, layer=rlayer, name='RRAIL0', 
                            hextension=hextension, vextension=vextension, color=color)
    nelements['RRAIL0'] = rg
    # Tie to rail
    if params['tie'] is not None:
        # routing
        if params['tie'] == 'D':
            idx = round(params['nf']/2)
            _pin_name = 'D0'
        if params['tie'] == 'S':
            idx = round(params['nf']/2) + 1
            _pin_name = 'S0'
        if params['tie'] == 'TAP0':
            idx = round(params['nf']/2) + 1
            _pin_name = 'TAP0'
        if params['tie'] == 'TAP1':
            idx = round(params['nf']/2)
            _pin_name = 'TAP1'
        x0 = templates[ref_temp_name]['pins'][_pin_name]['xy'][0][0]
        x1 = templates[ref_temp_name]['pins'][_pin_name]['xy'][1][0]
        x = round((x0 + x1)/2) + offset[0]  # center coordinate 
        _x = x
        for i in range(idx):
            hextension = round(grids['routing_12_cmos']['vertical']['width'][0]/2)
            vextension = grids['routing_12_cmos']['horizontal']['extension'][0] 
            y0=grids['routing_12_cmos']['horizontal']['elements'][0] + offset[1]
            y1=grids['routing_12_cmos']['horizontal']['elements'][1] + offset[1]
            rxy = [[_x, y0], [_x, y1]]
            rlayer=grids['routing_12_cmos']['vertical']['layer'][0]
            color = grids['routing_12_cmos']['vertical']['xcolor'][0] 
            rg = laygo2.object.Rect(xy=rxy, layer=rlayer, name='RTIE' + str(i), 
                                    hextension=hextension, vextension=vextension, color=color)
            nelements['RTIE' + str(i)] = rg
            _x += params['unit_size_core'][0]
        # via
        vname = grids['routing_12_cmos']['via']['map'][0][0]
        ivia = laygo2.object.Instance(name='IVTIE0', xy=[x, y0], libname=libname, cellname=vname, 
                                      shape=[idx, 1], pitch=params['unit_size_core'], 
                                      unit_size=[0, 0], pins=None, transform='R0')
        nelements['IVTIE'+_name + '0'] = ivia
    # Tie to rail - dummy left
    if params['nfdmyl'] > 0:  
        if devtype == 'nmos' or devtype == 'pmos':
            if params['bndl']:  # terminated by boundary
                pin_name = 'S0'
                idx_offset = 0
            else:
                pin_name = 'G0'
                idx_offset = -1
        elif devtype == 'ptap' or devtype == 'ntap':
            if params['bndl']:  # terminated by boundary
                pin_name = 'TAP0'
                idx_offset = 0
            else:
                pin_name = 'TAP1'
                idx_offset = -1
        x0 = templates[ref_dmy_temp_name]['pins'][pin_name]['xy'][0][0]
        x1 = templates[ref_dmy_temp_name]['pins'][pin_name]['xy'][1][0]
        x = round((x0 + x1)/2) + offset_dmyl[0]  # center coordinate 
        _x = x
        idx = round(params['nfdmyl']) + idx_offset
        for i in range(idx):
            hextension = round(grids['routing_12_cmos']['vertical']['width'][0]/2)
            vextension = grids['routing_12_cmos']['horizontal']['extension'][0] 
            y0=grids['routing_12_cmos']['horizontal']['elements'][0] + offset_dmyl[1]
            y1=grids['routing_12_cmos']['horizontal']['elements'][1] + offset_dmyl[1]
            rxy = [[_x, y0], [_x, y1]]
            rlayer=grids['routing_12_cmos']['vertical']['layer'][0]
            color = grids['routing_12_cmos']['vertical']['xcolor'][0]
            rg = laygo2.object.Rect(xy=rxy, layer=rlayer, name='RTIEDMYL' + str(i), 
                                    hextension=hextension, vextension=vextension, color=color)
            nelements['RTIEDMYL' + str(i)] = rg
            _x = _x + round(params['unit_size_dmy'][0]/2)
        # via
        vname = grids['routing_12_cmos']['via']['map'][0][0]
        ivia = laygo2.object.Instance(name='IVTIEDMYL0', xy=[x, y0], libname=libname, cellname=vname, 
                                      shape=[idx, 1], pitch=params['unit_size_dmy']*np.array([0.5, 1]), 
                                      unit_size=[0, 0], pins=None, transform='R0')
        nelements['IVTIEDMYL'+_name + '0'] = ivia
    # Tie to rail - dummy right
    if params['nfdmyr'] > 0:
        if devtype == 'nmos' or devtype == 'pmos':
            if params['bndr']:  # terminated by boundary
                pin_name = 'G0'  
                idx_offset = 0
            else:
                pin_name = 'G0'
                idx_offset = -1
        elif devtype == 'ptap' or devtype == 'ntap':
            if params['bndr']:  # terminated by boundary
                pin_name = 'TAP1'
                idx_offset = 0
            else:
                pin_name = 'TAP1'
                idx_offset = -1
        x0 = templates[ref_dmy_temp_name]['pins'][pin_name]['xy'][0][0]
        x1 = templates[ref_dmy_temp_name]['pins'][pin_name]['xy'][1][0]
        x = round((x0 + x1)/2) + offset_dmyr[0]  # center coordinate 
        _x = x
        idx = round(params['nfdmyr']) + idx_offset
        for i in range(idx):
            hextension = round(grids['routing_12_cmos']['vertical']['width'][0]/2)
            vextension = grids['routing_12_cmos']['horizontal']['extension'][0] 
            y0=grids['routing_12_cmos']['horizontal']['elements'][0] + offset_dmyr[1]
            y1=grids['routing_12_cmos']['horizontal']['elements'][1] + offset_dmyr[1]
            rxy = [[_x, y0], [_x, y1]]
            rlayer=grids['routing_12_cmos']['vertical']['layer'][0]
            color = grids['routing_12_cmos']['vertical']['xcolor'][0]
            rg = laygo2.object.Rect(xy=rxy, layer=rlayer, name='RTIEDMYR' + str(i), hextension=hextension, vextension=vextension, color=color)
            nelements['RTIEDMYR' + str(i)] = rg
            _x = _x + round(params['unit_size_dmy'][0]/2)
        # via
        vname = grids['routing_12_cmos']['via']['map'][0][0]
        ivia = laygo2.object.Instance(name='IVTIEDMYR0', xy=[x, y0], libname=libname, cellname=vname, 
                                      shape=[idx, 1], pitch=params['unit_size_dmy']*np.array([0.5, 1]), 
                                      unit_size=[0, 0], pins=None, transform='R0')
        nelements['IVTIEDMYR'+_name + '0'] = ivia
    return nelements


def mos_pins_func(devtype, params):
    """Generate a pin dictionary from params."""
    params = _mos_update_params(params)
    pins = dict()
    # generate a virtual routing structure for reference
    route_obj = _mos_route(devtype=devtype, params=params)
    if 'RG0' in route_obj:  # gate
        g_obj = route_obj['RG0']
        pins['G'] = laygo2.object.Pin(xy=g_obj.xy, layer=g_obj.layer, netname='G')
    if 'RD0' in route_obj:  # drain
        d_obj = route_obj['RD0']
        pins['D'] = laygo2.object.Pin(xy=d_obj.xy, layer=d_obj.layer, netname='D')
    if 'RS0' in route_obj:  # source
        s_obj = route_obj['RS0']
        pins['S'] = laygo2.object.Pin(xy=s_obj.xy, layer=s_obj.layer, netname='S')
    if 'RRAIL0' in route_obj:  # rail
        r_obj = route_obj['RRAIL0']
        pins['RAIL'] = laygo2.object.Pin(xy=r_obj.xy, layer=r_obj.layer, netname='RAIL')
    return pins


def nmos_pins_func(params):
    return mos_pins_func(devtype='nmos', params=params)


def pmos_pins_func(params):
    return mos_pins_func(devtype='nmos', params=params)


def ptap_pins_func(params):
    return mos_pins_func(devtype='ptap', params=params)


def ntap_pins_func(params):
    return mos_pins_func(devtype='ntap', params=params)


def mos_generate_func(devtype, name=None, shape=None, pitch=None, transform='R0', params=None):
    """Generates an instance from the input parameters."""
    # Compute parameters
    params = _mos_update_params(params)

    # Create the base mosfet structure.
    nelements = dict()
    cursor = [0, 0]
    # Left global boundary
    if params['gbndl']:
        if devtype == 'nmos':
            cellname = 'nmos130_fast_left'
        elif devtype == 'pmos':
            cellname = 'pmos130_fast_left'
        elif devtype == 'ptap':
            cellname = 'ptap_fast_left'
        elif devtype == 'ntap':
            cellname = 'ntap_fast_left'
        igbndl = laygo2.object.Instance(name='IBNDL0', xy=cursor, libname=libname, cellname=cellname, 
                                       pitch=params['unit_size_gbndl'], unit_size=params['unit_size_gbndl'])
        nelements['IGBNDL0'] = igbndl
        cursor = igbndl.bottom_right
    # Left local boundary
    if params['bndl']:
        if devtype == 'nmos':
            cellname = 'nmos130_fast_boundary'
        elif devtype == 'pmos':
            cellname = 'pmos130_fast_boundary'
        elif devtype == 'ptap':
            cellname = 'ptap_fast_boundary'
        elif devtype == 'ntap':
            cellname = 'ntap_fast_boundary'
        ibndl = laygo2.object.Instance(name='IBNDL0', xy=cursor, libname=libname, cellname=cellname, 
                                       pitch=params['unit_size_bndl'], unit_size=params['unit_size_bndl'])
        nelements['IBNDL0'] = ibndl
        cursor = ibndl.bottom_right
    # Left dummy
    if params['nfdmyl'] > 0:
        if devtype == 'nmos':
            cellname = 'nmos130_fast_dmy_nf2'
        elif devtype == 'pmos':
            cellname = 'pmos130_fast_dmy_nf2'
        elif devtype == 'ptap':
            cellname = 'ptap_fast_center_nf2_v2'
        elif devtype == 'ntap':
            cellname = 'ntap_fast_center_nf2_v2'
        idmyl = laygo2.object.Instance(name='IDMYL0', xy=cursor, libname=libname, 
                                       cellname=cellname, shape=[round(params['nfdmyl']/2), 1], 
                                       pitch=params['unit_size_dmy'], unit_size=params['unit_size_dmy'])
        nelements['IDMYL0'] = idmyl
        cursor = idmyl.bottom_right
    # Core mosfet
    if devtype == 'nmos':
        cellname = 'nmos130_fast_center_nf2'
    elif devtype == 'pmos':
        cellname = 'pmos130_fast_center_nf2'
    elif devtype == 'ptap':
        cellname = 'ptap_fast_center_nf2_v2'
    elif devtype == 'ntap':
        cellname = 'ntap_fast_center_nf2_v2'
    icore = laygo2.object.Instance(name='IM0', xy=cursor, libname=libname, 
                                   cellname=cellname, shape=[round(params['nf']/2), 1], 
                                   pitch=params['unit_size_core'], unit_size=params['unit_size_core'], 
                                   pins=None, transform='R0')
    nelements['IM0'] = icore
    cursor = icore.bottom_right
    # Right dummy
    if params['nfdmyr'] > 0:
        if devtype == 'nmos':
            cellname = 'nmos130_fast_dmy_nf2'
        elif devtype == 'pmos':
            cellname = 'pmos130_fast_dmy_nf2'
        elif devtype == 'ptap':
            cellname = 'ptap_fast_center_nf2_v2'
        elif devtype == 'ntap':
            cellname = 'ntap_fast_center_nf2_v2'
        idmyr = laygo2.object.Instance(name='IDMYR0', xy=cursor, libname=libname, 
                                       cellname=cellname, shape=[round(params['nfdmyr']/2), 1], 
                                       pitch=params['unit_size_dmy'], unit_size=params['unit_size_dmy'])
        nelements['IDMYR0'] = idmyr
        cursor = idmyr.bottom_right
    # Right local boundary
    if params['bndr']:
        if devtype == 'nmos':
            cellname = 'nmos130_fast_boundary'
        elif devtype == 'pmos':
            cellname = 'pmos130_fast_boundary'
        elif devtype == 'ptap':
            cellname = 'ptap_fast_boundary'
        elif devtype == 'ntap':
            cellname = 'ntap_fast_boundary'
        ibndr = laygo2.object.Instance(name='IBNDR0', xy=cursor, libname=libname, cellname=cellname, 
                                       pitch=params['unit_size_bndr'], unit_size=params['unit_size_bndr'])
        nelements['IBNDR0'] = ibndr
        cursor = ibndr.bottom_right
    # Right global boundary
    if params['gbndr']:
        if devtype == 'nmos':
            cellname = 'nmos130_fast_right'
        elif devtype == 'pmos':
            cellname = 'pmos130_fast_right'
        elif devtype == 'ptap':
            cellname = 'ptap_fast_right'
        elif devtype == 'ntap':
            cellname = 'ntap_fast_right'
        igbndr = laygo2.object.Instance(name='IBNDR0', xy=cursor, libname=libname, cellname=cellname, 
                                       pitch=params['unit_size_gbndr'], unit_size=params['unit_size_gbndr'])
        nelements['IGBNDR0'] = igbndr
     
    # Routing
    nelements.update(_mos_route(devtype=devtype, params=params))

    # Create pins
    pins = mos_pins_func(devtype=devtype, params=params)
    #nelements.update(pins)  # Add physical pin structures to the virtual object.

    # Unit size
    inst_xy = mos_bbox_func(params=params)
    inst_unit_size = [inst_xy[1, 0] - inst_xy[0, 0], inst_xy[1, 1] - inst_xy[0, 1]]

    # Pitch
    if pitch is None:
        pitch = inst_unit_size
    
    # Generate and return the final instance
    inst = laygo2.object.VirtualInstance(name=name, xy=np.array([0, 0]), libname=libname, cellname='myvcell_'+devtype,
                                         native_elements=nelements, shape=shape, pitch=pitch,
                                         transform=transform, unit_size=inst_unit_size, pins=pins)
    return inst


def nmos_generate_func(name=None, shape=None, pitch=None, transform='R0', params=None):
    return mos_generate_func(devtype='nmos', name=name, shape=shape, pitch=pitch, transform=transform, params=params)


def pmos_generate_func(name=None, shape=None, pitch=None, transform='R0', params=None):
    return mos_generate_func(devtype='pmos', name=name, shape=shape, pitch=pitch, transform=transform, params=params)


def ptap_generate_func(name=None, shape=None, pitch=None, transform='R0', params=None):
    return mos_generate_func(devtype='ptap', name=name, shape=shape, pitch=pitch, transform=transform, params=params)


def ntap_generate_func(name=None, shape=None, pitch=None, transform='R0', params=None):
    return mos_generate_func(devtype='ntap', name=name, shape=shape, pitch=pitch, transform=transform, params=params)


# # Flexible templates
# def mos_flex_generate_func(devtype, name=None, shape=None, pitch=None, transform='R0', params=None):
#     """Generates a flexible mos instance from the input parameters."""
#     # Compute parameters
#     params = _mos_update_params(params)
#     w=params['wf']  # finger width
    
#     # Bbox
#     inst_xy = mos_bbox_func(params=params)
#     inst_unit_size = [inst_xy[1, 0] - inst_xy[0, 0], inst_xy[1, 1] - inst_xy[0, 1]]

#     # Create the base mosfet structure.
#     nelements = dict()
#     # Implant
#     if devtype == 'nmos_flex':
#         rimp = laygo2.object.Rect(xy=inst_xy, layer=['NP', 'drawing'], name='RIM0_FLEX_IMP') 
#         nelements['RIM0_FLEX_IMP'] = rimp
#     elif devtype == 'pmos_flex':
#         rimp = laygo2.object.Rect(xy=inst_xy, layer=['PP', 'drawing'], name='RIM0_FLEX_IMP') 
#         nelements['RIM0_FLEX_IMP'] = rimp
#         rnw = laygo2.object.Rect(xy=inst_xy, layer=['NW', 'drawing'], name='RIM0_FLEX_NW') 
#         nelements['RIM0_FLEX_NW'] = rnw
    
#     cursor = [0, 0]
#     # Left global boundary
#     if params['gbndl']:
#         cursor[0] += params['unit_size_gbndl'][0]
#     # Left local boundary
#     if params['bndl']:
#         cursor[0] += params['unit_size_bndl'][0]
#     # Left dummy
#     if params['nfdmyl'] > 0:
#         if devtype == 'nmos_flex':
#             cellname = 'nch_lvt'
#         elif devtype == 'pmos_flex':
#             cellname = 'pch_lvt'
#         idmyl_pcell_params = {
#             "Wfg":str(w)+"n",
#             "fingers":str(params['nfdmyl']),
#             "impLayer":False,
#             "nwLayer":False,
#         }
#         idmyl_xy_offset = np.array([70, 610-w])  # offset between core position and pcell origin.
#         idmyl_flex = laygo2.object.Instance(name='IM0', xy=cursor+idmyl_xy_offset, libname='tsmcN45',
#                                             cellname=cellname, shape=[1, 1], 
#                                             pitch=params['unit_size_dmy'], 
#                                             unit_size=params['unit_size_dmy'], 
#                                             params = {"pcell_params":idmyl_pcell_params},
#                                             pins=None, transform='R0')
#         nelements['IDMYL0_FLEX'] = idmyl_flex
#         # Core mosfet - Gate structure
#         # Gate poly
#         for i in range(round(params['nfdmyl']/2)):
#             rg_xy = [[cursor[0] + 70+params['unit_size_dmy'][0]*i, 765],\
#                      [cursor[0] + 290+params['unit_size_dmy'][0]*i, 865]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['PO', 'drawing'], 
#                                     name='RIDMYL0_FLEX_G_PO0_'+str(i)) 
#             nelements['RIDMYL0_FLEX_G_PO0_'+str(i)] = rg
#             rg_xy = [[cursor[0] + 70+params['unit_size_dmy'][0]*i, 700],\
#                      [cursor[0] + 110+params['unit_size_dmy'][0]*i, 765]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['PO', 'drawing'], 
#                                     name='RIDMYL0_FLEX_G_PO1_'+str(i)) 
#             nelements['RIDMYL0_FLEX_G_PO1_'+str(i)] = rg
#             rg_xy = [[cursor[0] + 250+params['unit_size_dmy'][0]*i, 700],\
#                      [cursor[0] + 290+params['unit_size_dmy'][0]*i, 765]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['PO', 'drawing'], 
#                                     name='RIDMYL0_FLEX_G_PO2_'+str(i)) 
#             nelements['RIDMYL0_FLEX_G_PO2_'+str(i)] = rg
#         # Gate M1
#         for i in range(round(params['nfdmyl']/2)):
#             rg_xy = [[cursor[0] + 125+params['unit_size_dmy'][0]*i, 685],\
#                      [cursor[0] + 235+params['unit_size_dmy'][0]*i, 885]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['M1', 'drawing'], 
#                                     name='RIDMYL0_FLEX_G_M1_0_'+str(i))
#             nelements['RIDMYL0_FLEX_G_M1_0_'+str(i)] = rg
#             rg_xy = [[cursor[0] + 145+params['unit_size_dmy'][0]*i, 610],\
#                      [cursor[0] + 215+params['unit_size_dmy'][0]*i, 885]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['M1', 'drawing'], 
#                                     name='RIDMYL0_FLEX_G_M1_1_'+str(i))
#             nelements['RIDMYL0_FLEX_G_M1_1_'+str(i)] = rg
#         # Gate contact
#         for i in range(round(params['nfdmyl']/2)):
#             rg_xy = [[cursor[0] + 150+params['unit_size_dmy'][0]*i, 785],\
#                      [cursor[0] + 210+params['unit_size_dmy'][0]*i, 845]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['CO', 'drawing'], 
#                                     name='RIDMYL0_FLEX_G_CO_'+str(i))
#             nelements['RIDMYL0_FLEX_G_CO_'+str(i)] = rg
#         cursor[0] += params['unit_size_dmy'][0] * params['nfdmyl']/2
#     # Core mosfet - Cell name
#     if devtype == 'nmos_flex':
#         cellname = 'nch_lvt'
#     elif devtype == 'pmos_flex':
#         cellname = 'pch_lvt'
#     icore_pcell_params = {
#         "Wfg":str(w)+"n",
#         "fingers":str(params['nf']),
#         "impLayer":False,
#         "nwLayer":False,
#     }
#     # Core mosfet - core pcell
#     icore_xy_offset = np.array([70, 610-w])  # offset between core position and pcell origin.
#     icore_flex = laygo2.object.Instance(name='IM0', xy=cursor+icore_xy_offset, libname='tsmcN45',
#                                    cellname=cellname, shape=[1, 1], 
#                                    pitch=params['unit_size_core'], 
#                                    unit_size=params['unit_size_core'], 
#                                    params = {"pcell_params":icore_pcell_params},
#                                    pins=None, transform='R0')
#     nelements['IM0_FLEX'] = icore_flex
#     # Core mosfet - Gate structure
#     # Gate poly
#     for i in range(round(params['nf']/2)):
#         rg_xy = [[cursor[0] + 70+params['unit_size_core'][0]*i, 765],\
#                  [cursor[0] + 290+params['unit_size_core'][0]*i, 865]]
#         rg = laygo2.object.Rect(xy=rg_xy, layer=['PO', 'drawing'], name='RIM0_FLEX_G_PO0_'+str(i)) 
#         nelements['RIM0_FLEX_G_PO0_'+str(i)] = rg
#         rg_xy = [[cursor[0] + 70+params['unit_size_core'][0]*i, 700],\
#                  [cursor[0] + 110+params['unit_size_core'][0]*i, 765]]
#         rg = laygo2.object.Rect(xy=rg_xy, layer=['PO', 'drawing'], name='RIM0_FLEX_G_PO1_'+str(i)) 
#         nelements['RIM0_FLEX_G_PO1_'+str(i)] = rg
#         rg_xy = [[cursor[0] + 250+params['unit_size_core'][0]*i, 700],\
#                  [cursor[0] + 290+params['unit_size_core'][0]*i, 765]]
#         rg = laygo2.object.Rect(xy=rg_xy, layer=['PO', 'drawing'], name='RIM0_FLEX_G_PO2_'+str(i)) 
#         nelements['RIM0_FLEX_G_PO2_'+str(i)] = rg
#     # Gate M1
#     for i in range(round(params['nf']/2)):
#         rg_xy = [[cursor[0] + 125+params['unit_size_core'][0]*i, 685],\
#                  [cursor[0] + 235+params['unit_size_core'][0]*i, 885]]
#         rg = laygo2.object.Rect(xy=rg_xy, layer=['M1', 'drawing'], name='RIM0_FLEX_G_M1_'+str(i))
#         nelements['RIM0_FLEX_G_M1_'+str(i)] = rg
#     # Gate contact
#     for i in range(round(params['nf']/2)):
#         rg_xy = [[cursor[0] + 150+params['unit_size_core'][0]*i, 785],\
#                  [cursor[0] + 210+params['unit_size_core'][0]*i, 845]]
#         rg = laygo2.object.Rect(xy=rg_xy, layer=['CO', 'drawing'], name='RIM0_FLEX_G_CO_'+str(i))
#         nelements['RIM0_FLEX_G_CO_'+str(i)] = rg

#     cursor[0] += params['unit_size_core'][0] * params['nf']/2
#     # Right dummy
#     if params['nfdmyr'] > 0:
#         if devtype == 'nmos_flex':
#             cellname = 'nch_lvt'
#         elif devtype == 'pmos_flex':
#             cellname = 'pch_lvt'
#         idmyr_pcell_params = {
#             "Wfg":str(w)+"n",
#             "fingers":str(params['nfdmyr']),
#             "impLayer":False,
#             "nwLayer":False,
#         }
#         idmyr_xy_offset = np.array([70, 610-w])  # offset between core position and pcell origin.
#         idmyr_flex = laygo2.object.Instance(name='IM0', xy=cursor+idmyr_xy_offset, libname='tsmcN45',
#                                             cellname=cellname, shape=[1, 1], 
#                                             pitch=params['unit_size_dmy'], 
#                                             unit_size=params['unit_size_dmy'], 
#                                             params = {"pcell_params":idmyr_pcell_params},
#                                             pins=None, transform='R0')
#         nelements['IDMYR0_FLEX'] = idmyr_flex
#         # Core mosfet - Gate structure
#         # Gate poly
#         for i in range(round(params['nfdmyr']/2)):
#             rg_xy = [[cursor[0] + 70+params['unit_size_dmy'][0]*i, 765],\
#                      [cursor[0] + 290+params['unit_size_dmy'][0]*i, 865]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['PO', 'drawing'], 
#                                     name='RIDMYR0_FLEX_G_PO0_'+str(i)) 
#             nelements['RIDMYR0_FLEX_G_PO0_'+str(i)] = rg
#             rg_xy = [[cursor[0] + 70+params['unit_size_dmy'][0]*i, 700],\
#                      [cursor[0] + 110+params['unit_size_dmy'][0]*i, 765]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['PO', 'drawing'], 
#                                     name='RIDMYR0_FLEX_G_PO1_'+str(i)) 
#             nelements['RIDMYR0_FLEX_G_PO1_'+str(i)] = rg
#             rg_xy = [[cursor[0] + 250+params['unit_size_dmy'][0]*i, 700],\
#                      [cursor[0] + 290+params['unit_size_dmy'][0]*i, 765]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['PO', 'drawing'], 
#                                     name='RIDMYR0_FLEX_G_PO2_'+str(i)) 
#             nelements['RIDMYR0_FLEX_G_PO2_'+str(i)] = rg
#         # Gate M1
#         for i in range(round(params['nfdmyr']/2)):
#             rg_xy = [[cursor[0] + 125+params['unit_size_dmy'][0]*i, 685],\
#                      [cursor[0] + 235+params['unit_size_dmy'][0]*i, 885]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['M1', 'drawing'], 
#                                     name='RIDMYR0_FLEX_G_M1_0_'+str(i))
#             nelements['RIDMYR0_FLEX_G_M1_0_'+str(i)] = rg
#             rg_xy = [[cursor[0] + 145+params['unit_size_dmy'][0]*i, 610],\
#                      [cursor[0] + 215+params['unit_size_dmy'][0]*i, 885]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['M1', 'drawing'], 
#                                     name='RIDMYR0_FLEX_G_M1_1_'+str(i))
#             nelements['RIDMYR0_FLEX_G_M1_1_'+str(i)] = rg
#         # Gate contact
#         for i in range(round(params['nfdmyr']/2)):
#             rg_xy = [[cursor[0] + 150+params['unit_size_dmy'][0]*i, 785],\
#                      [cursor[0] + 210+params['unit_size_dmy'][0]*i, 845]]
#             rg = laygo2.object.Rect(xy=rg_xy, layer=['CO', 'drawing'], 
#                                     name='RIDMYR0_FLEX_G_CO_'+str(i))
#             nelements['RIDMYR0_FLEX_G_CO_'+str(i)] = rg
#         cursor[0] += params['unit_size_dmy'][0] * params['nfdmyr']/2
#     # Right local boundary
#     if params['bndr']:
#         cursor[0] += params['unit_size_bndr'][0]
#     # Right global boundary
#     if params['gbndr']:
#         cursor[0] += params['unit_size_gbndr'][0]
     
#     # Routing
#     if devtype == 'nmos_flex':
#         devtype = 'nmos'
#     if devtype == 'pmos_flex':
#         devtype = 'pmos'
#     nelements.update(_mos_route(devtype=devtype, params=params))
#     nelements.update(_mos_route(devtype=devtype, params=params))

#     # Create pins
#     pins = mos_pins_func(devtype=devtype, params=params)
#     #nelements.update(pins)  # Add physical pin structures to the virtual object.

#     # Unit size
#     inst_unit_size = [inst_xy[1, 0] - inst_xy[0, 0], inst_xy[1, 1] - inst_xy[0, 1]]
    
#     # Pitch
#     if pitch is None:
#         pitch = inst_unit_size
    
#     # Generate and return the final instance
#     inst = laygo2.object.VirtualInstance(name=name, xy=np.array([0, 0]), libname=libname, cellname='myvcell_'+devtype,
#                                          native_elements=nelements, shape=shape, pitch=pitch,
#                                          transform=transform, unit_size=inst_unit_size, pins=pins)
#     return inst

# def nmos_flex_generate_func(name=None, shape=None, pitch=None, transform='R0', params=None):
#     return mos_flex_generate_func(devtype='nmos_flex', name=name, shape=shape, pitch=pitch, transform=transform, params=params)

# def pmos_flex_generate_func(name=None, shape=None, pitch=None, transform='R0', params=None):
#     return mos_flex_generate_func(devtype='pmos_flex', name=name, shape=shape, pitch=pitch, transform=transform, params=params)

# Create template library
def load_templates():
    """Load template to a template library object"""
    tlib = laygo2.object.database.TemplateLibrary(name=libname)
    # Native templates
    for tn, tdict in templates.items():
        # bounding box
        bbox = np.array(tdict['xy'])
        # pins
        pins = None
        if 'pins' in tdict:
            pins = dict()
            for pn, _pdict in tdict['pins'].items():
                pins[pn] = laygo2.object.Pin(xy=_pdict['xy'], layer=_pdict['layer'], netname=pn)
        t = laygo2.object.template.NativeInstanceTemplate(libname=libname, cellname=tn, bbox=bbox, pins=pins)
        tlib.append(t)
    
    # Derived templates will be added here
    # Transistors
    # Transistor layouts are created in laygo and stored as a virtual instance.
    tnmos = laygo2.object.template.UserDefinedTemplate(name='nmos', bbox_func=mos_bbox_func, 
                                   pins_func=mos_pins_func, generate_func=nmos_generate_func)
    tpmos = laygo2.object.template.UserDefinedTemplate(name='pmos', bbox_func=mos_bbox_func, 
                                   pins_func=mos_pins_func, generate_func=pmos_generate_func)
    tptap = laygo2.object.template.UserDefinedTemplate(name='ptap', bbox_func=mos_bbox_func, 
                                   pins_func=mos_pins_func, generate_func=ptap_generate_func)
    tntap = laygo2.object.template.UserDefinedTemplate(name='ntap', bbox_func=mos_bbox_func, 
                                   pins_func=mos_pins_func, generate_func=ntap_generate_func)
    tlib.append([tpmos, tnmos, tptap, tntap])
    
    # Flexible transistors (transistors with variable finger widths)
    # tnmos_flex = laygo2.object.template.UserDefinedTemplate(name='nmos_flex', bbox_func=mos_bbox_func, 
    #                                pins_func=mos_pins_func, generate_func=nmos_flex_generate_func)
    # tpmos_flex = laygo2.object.template.UserDefinedTemplate(name='pmos_flex', bbox_func=mos_bbox_func, 
    #                                pins_func=mos_pins_func, generate_func=pmos_flex_generate_func)
    # tlib.append([tnmos_flex, tpmos_flex])
    return tlib


def generate_cut_layer(dsn,grids,tlib,templates):
    r23     = grids["routing_23_cmos"]
    r23_cut = grids["routing_23_cmos_cut"] 
    dsn.rect_space("M0",r23,r23_cut,150)

def generate_tap(dsn, grids, tlib, templates, type_iter='nppn', type_extra=None, transform_iter='0X0X', transform_extra=None, side='both'): 
    """ This function generates taps on the left, right or both side of the design.

        parameters
        ----------
        type_iter : str
            list of transistor types if iterating taps. Even if there should be ptap, the type is 'n' since there are NMOS on the design.
        type_extra : str
            list of transistor types of extra taps
        transform_iter : str
            list of transform types of iterating taps
        transform_extra : str
            list of transform types of extra taps
        side: str
            tap generation side. both / left / right

        type_iter and transform_iter should have identical length.
    """

    pg         = grids["placement_basic"]           # Load basic placement grid for placing taps.
    height_tap = grids["routing_23_cmos"].height//2 # Calculate the height of tap which is generally the half of the CMOS height.
    
    bbox             = dsn.bbox                         # The bbox of the design.
    height_dsn       = bbox[1][1]                       # The height of the design.
    total_num_of_tap = np.int(height_dsn // height_tap) # Total number of taps. 8 taps are needed if there are 4 CMOS grids in the design. 5 taps if 2 CMOS grids and 1 half-CMOS.
    iter_len         = len(type_iter)                   # length of iteration
    print('======== TAP GENERATION START ========')
    print('Total number of taps on each side: ' + str(total_num_of_tap))
    print('Iteration tap type: {0}. Transform: {1}'.format(type_iter, transform_iter))
    print('Extra tap type: {0}. Transform: {1}'.format(type_extra, transform_extra))
 
    def iteration(iter, type_iter):
        ltap_list = []
        rtap_list = []
        ltapbnd_list = []
        rtapbnd_list = []
        for idx in range(iter): # number of iteration
            i=0
            for celltype in type_iter: # in each iteration
                ltap_list.append(templates[celltype+'mos4_fast_tap'].generate(name='LTAP'+str(idx)+str(i), transform='R0' if transform_iter[i]=='0' else 'MX'))
                rtap_list.append(templates[celltype+'mos4_fast_tap'].generate(name='RTAP'+str(idx)+str(i), transform='R0' if transform_iter[i]=='0' else 'MX'))
                ltapbnd_name = 'ptap_fast_left' if celltype == 'n' else 'ntap_fast_left'
                rtapbnd_name = 'ptap_fast_right' if celltype == 'n' else 'ntap_fast_right'
                ltapbnd_list.append(templates[ltapbnd_name].generate(name='LTAPBND'+str(idx)+str(i), transform='R0' if transform_iter[i]=='0' else 'MX'))
                rtapbnd_list.append(templates[rtapbnd_name].generate(name='RTAPBND'+str(idx)+str(i), transform='R0' if transform_iter[i]=='0' else 'MX'))
                i+=1
        return ltap_list, rtap_list, ltapbnd_list, rtapbnd_list

    if total_num_of_tap%iter_len == 0: # full iteration
        ltap_list, rtap_list, ltapbnd_list, rtapbnd_list = iteration(iter = total_num_of_tap//iter_len, type_iter = type_iter)

    else: # iteration + extra taps
        ltap_list, rtap_list, ltapbnd_list, rtapbnd_list = iteration(iter = (total_num_of_tap-len(type_extra))//iter_len, type_iter = type_iter) # Iteration
        i=0
        for celltype in type_extra: # Extra taps
            ltap_list.append(templates[celltype+'mos4_fast_tap'].generate(name='LTAPEND'+celltype+str(i), transform='R0' if transform_extra[i]=='0' else 'MX'))
            rtap_list.append(templates[celltype+'mos4_fast_tap'].generate(name='RTAPEND'+celltype+str(i), transform='R0' if transform_extra[i]=='0' else 'MX'))
            ltapbnd_name = 'ptap_fast_left' if celltype == 'n' else 'ntap_fast_left'
            rtapbnd_name = 'ptap_fast_right' if celltype == 'n' else 'ntap_fast_right'
            ltapbnd_list.append(templates[ltapbnd_name].generate(name='LTAPBND'+celltype+str(i), transform='R0' if transform_iter[i]=='0' else 'MX'))
            rtapbnd_list.append(templates[rtapbnd_name].generate(name='RTAPBND'+celltype+str(i), transform='R0' if transform_iter[i]=='0' else 'MX'))
            i+=1
    
    # Place TAPs on the design.
    if side == 'both':
        dsn.place(grid=pg, inst=np.array(rtap_list   ).reshape(len(rtap_list   ),1), mn=pg.mn.bottom_right(bbox))
        dsn.place(grid=pg, inst=np.array(rtapbnd_list).reshape(len(rtapbnd_list),1), mn=pg.mn.bottom_right(rtap_list[0]))
        dsn.place(grid=pg, inst=np.array(ltap_list   ).reshape(len(ltap_list   ),1), mn=pg.mn.bottom_left(bbox)         - pg.mn.width_vec(ltap_list[0]))
        dsn.place(grid=pg, inst=np.array(ltapbnd_list).reshape(len(ltapbnd_list),1), mn=pg.mn.bottom_left(ltap_list[0]) - pg.mn.width_vec(ltapbnd_list[0]))
    elif side == 'left':
        dsn.place(grid=pg, inst=np.array(ltap_list   ).reshape(len(ltap_list   ),1), mn=pg.mn.bottom_left(bbox)         - pg.mn.width_vec(ltap_list[0]))
        dsn.place(grid=pg, inst=np.array(ltapbnd_list).reshape(len(ltapbnd_list),1), mn=pg.mn.bottom_left(ltap_list[0]) - pg.mn.width_vec(ltapbnd_list[0]))
    elif side == 'right':
        dsn.place(grid=pg, inst=np.array(rtap_list   ).reshape(len(rtap_list   ),1), mn=pg.mn.bottom_right(bbox))
        dsn.place(grid=pg, inst=np.array(rtapbnd_list).reshape(len(rtapbnd_list),1), mn=pg.mn.bottom_right(rtap_list[0])) 

    bbox = dsn.bbox

    if bbox[0][0] != 0:
        for _dsn in dsn:
            dsn.elements[_dsn].xy -= [bbox[0][0],0]

    print('========= TAP GENERATION END =========')

def generate_gbnd(dsn, grids, templates):
    """ This function generates GLOBAL BOUNDARY on the design.
        Check the name of GBND cells since those are different by each template library. """

    # Call placement grid and calculate the bounding box of the design.
    pg = grids["placement_basic"]
    bbox_xy = dsn.bbox
    bbox_mn = pg.mn(dsn.bbox)
    
    # Call each dummy GBND cell from template library to calculate the height and width of each cell.
    gbnd_vertical_dmy   = templates["boundary_topleft"].generate(name="gbnd_vertical_dmy"  )
    gbnd_horizontal_dmy = templates["boundary_top"    ].generate(name="gbnd_horizontal_dmy")
    gbnd_corner_dmy     = templates["boundary_topleft"].generate(name="gbnd_corner_dmy"    )
    
    # Calculate the number of mosaic and generate GBND cells to be placed. 
    num_horizontal = bbox_mn[1][0]-bbox_mn[0][0]
    itop_gb   = templates["boundary_top"].generate( name="gbnd_top", transform='MX', shape=[num_horizontal, 1] )
    ibot_gb   = templates["boundary_top"].generate( name="gbnd_bot", transform='R0', shape=[num_horizontal, 1] ) 

    num_vertical = bbox_mn[1][1]//pg.mn.height(gbnd_vertical_dmy)
    ileft_gb  = templates["boundary_topleft"].generate( name="gbnd_left",  transform='R0', shape=[1, num_vertical] )
    iright_gb = templates["boundary_topleft"].generate( name="gbnd_right", transform='MY', shape=[1, num_vertical] )  

    ibl_gb    = templates["boundary_topleft"].generate( name="gbnd_bl", transform='R0'   )  
    ibr_gb    = templates["boundary_topleft"].generate( name="gbnd_br", transform='MY'   )  
    itr_gb    = templates["boundary_topleft"].generate( name="gbnd_tr", transform='R180' )  
    itl_gb    = templates["boundary_topleft"].generate( name="gbnd_tl", transform='MX'   )  

    # Place GBND cells on the design.    
    dsn.place(grid=pg, inst=itop_gb,   mn=pg.mn.top_left(    bbox_xy) + pg.mn.height_vec(gbnd_horizontal_dmy)) # TOP
    dsn.place(grid=pg, inst=ibot_gb,   mn=pg.mn.bottom_left( bbox_xy) - pg.mn.height_vec(gbnd_horizontal_dmy)) # BOTTOM

    dsn.place(grid=pg, inst=ileft_gb,  mn=pg.mn.bottom_left( bbox_xy) - pg.mn.width_vec( gbnd_vertical_dmy  )) # LEFT
    dsn.place(grid=pg, inst=iright_gb, mn=pg.mn.bottom_right(bbox_xy) + pg.mn.width_vec( gbnd_vertical_dmy  )) # RIGHT
 
    dsn.place(grid=pg, inst=ibl_gb,    mn=pg.mn.bottom_left( ibot_gb) - pg.mn.width_vec( gbnd_corner_dmy    )) # BOTTOM LEFT CORNER
    dsn.place(grid=pg, inst=ibr_gb,    mn=pg.mn.bottom_right(ibot_gb) + pg.mn.width_vec( gbnd_corner_dmy    )) # BOTTOM RIGHT CORNER
    dsn.place(grid=pg, inst=itl_gb,    mn=pg.mn.top_left(   ileft_gb) + pg.mn.height_vec(gbnd_corner_dmy    )) # TOP LEFT CORNER
    dsn.place(grid=pg, inst=itr_gb,    mn=pg.mn.top_right( iright_gb) + pg.mn.height_vec(gbnd_corner_dmy    )) # TOP RIGHT CORNER

    bbox_xy = dsn.bbox

    if bbox_xy[0][0] != 0:
        for _dsn in dsn:
            dsn.elements[_dsn].xy -= [bbox_xy[0][0],0]

def generate_pwr_rail(dsn, grids, tlib=None, templates=None, route_type='cmos', netname=None, vss_name='VSS', vdd_name='VDD', rail_swap=False, vertical=False, pin_num=0, pin_pitch=0):
    """ This function generates supply rails (POWER, GROUND).

        The names of power nets can be assigned arbitrarily.
        
        Parameters
        ----------
        route_type : str
            the type of routing ('cmos', 'mos', 'cmos_flipped')
        netname : str or list
            the name of nets
            EX) 'VDD', ['VDD', 'VSS'], ['VDD', 'VSS', ['VDD', -1]]
        vss_name : str
            the name of GROUND net (It will be removed.)
        vdd_name : str
            the name of POWER net (It will be removed.)
        rail_swap : boolean
            Determine the bottom rail is GND or POWER net. 0 for GND 1 for POWER.
        vertical : boolean
            whether generate vertical wires for connecting each horizontal rail
        pin_num : int
            the number of pins
        pin_pitch : int
            the pitch between pins in the abstract coordinate
    """

    print('=========== SUPPLY RAIL GENERATION START ===========')
    # 1. Load grids
    r23 = grids['routing_23_{0}'.format(route_type)]                                        # "CMOS grid" to calculate the number of power rails
    if route_type != 'mos': r23t = grids['routing_23_{0}_thick'.format(route_type)]         # "CMOS grid" to make M3 vertical rails.
    else: r23t = grids['routing_23_{0}'.format(route_type)]                                 # "MOS grid" to calculate the number of power rails
    

    # 2. Calculate the number of power rails in the design
    bbox = dsn.bbox
    grid_cnt = bbox[1,1] // r23.height
    bottom_rail = [r23.mn.bottom_left(bbox), r23.mn.bottom_right(bbox)]                     # bbox for M2 bottom rail

    if netname == None:
        """
            This block is for the old-version users.
            It will be removed later. :D
        """

        print("\n[WARNING] generate_pwr_rail with vss_name/vdd_name arguments will be deprecated.\n")
        if grid_cnt%2 == 0:
            iter_vdd = grid_cnt//2
            iter_vss = grid_cnt//2 + 1

        else:
            iter_vdd = (grid_cnt+1)//2
            iter_vss = (grid_cnt+1)//2

        pw_len = 2

        rvss = []
        rvdd = []
        vss_set = [iter_vss, rvss, vss_name]
        vdd_set = [iter_vdd, rvdd, vdd_name]

        pw_set = np.array([vss_set, vdd_set])

        if rail_swap: 
            pw_set[0][2] = vdd_name
            pw_set[1][2] = vss_name
        
        pw_iter = grid_cnt + 1 
        rail_count = {}
        rail_change = {}
    
    else:
        # 3. Generate a power rail list.
        pw_iter = grid_cnt + 1 

        # Check the type of netname.
        if type(netname) == str:
            netname = netname.split()
            rail_change = {}

        else:
            rail_change = {}
            for _name in netname:
                if type(_name) == list:
                    try: 
                        if _name[1] < 0: _name[1] += pw_iter
                        rail_change[_name[0]].append(_name[1])
                    except: 
                        rail_change[_name[0]]= [_name[1]]
        
        # Create a power rail list.
        netname = list(filter(lambda x: type(x)==str, netname))
        pw_len = len(netname)
        pw_set = np.empty(shape=(pw_len, 3), dtype=object)

        # Calculate the number of iterations of each power net.      
        pw_set[:pw_len,0] = pw_iter // pw_len
        pw_set[0:(pw_iter % pw_len), 0] += 1

        for i in range(pw_len): 
            pw_set[i, 1] = []
            pw_set[i, 2] = netname[i]
        
        # Rail swap for Iterated rails (Optional).
        if rail_swap: pw_set[:pw_len,2] = np.flip(pw_set[:pw_len,2])

        # Revise the list.
        for _name, _num in rail_change.items():
            for idx in _num:
                pw_set[(idx%pw_len), 0] -= 1
            
            if _name in netname:
                pin_ex = pw_set[:,2].tolist().index(_name)
                pw_set[pin_ex, 0] += len(_num)
            
            else:
                pw_extra = [len(_num), [], _name]
                pw_set = np.append(pw_set, [pw_extra], axis=0)

        # Count the number of each rail.
        rail_count = {}
        for _name, _num in rail_change.items():
            for idx in _num:
                rail_count[idx] = _name
        
        # Remove zero-rails.
        zero_list = list(np.where(pw_set[:,0]==0))[0]
        pw_set = np.delete(pw_set, zero_list, 0)
        pw_len -= len(zero_list)

    # 4. Generate iterated power rails
    pin_name = []

    for idx in range(pw_iter):
        pin = idx % pw_len
        iter = idx // pw_len

        # Generate a horizontal rail
        _mn = bottom_rail
        _mn[0][1] = r23.n(r23.height) * (pw_len*iter+pin)
        _mn[1][1] = r23.n(r23.height) * (pw_len*iter+pin)

        route = dsn.route(grid=r23, mn=_mn)
        
        # Check the netname.
        if idx in rail_count.keys():
            _netname = rail_count[idx]
            pin = pw_set[:,2].tolist().index(_netname)
            pw_set[pin][1].append(route)
            pin_name.append("{0}:".format(_netname))
        
        else: 
            pw_set[pin][1].append(route)
            pin_name.append(pw_set[pin][2]+':')

        # Generate the vertical vias (Optional).
        if vertical & (pw_set[pin][0] != 1):
            if pin % 2 == 0: dsn.via(grid=r23t, mn=r23t.mn.bottom_left(pw_set[pin][1][-1])-[pin,0])
            else: dsn.via(grid=r23t, mn=r23t.mn.bottom_right(pw_set[pin][1][-1])+[pin-1,0])
    
    bbox = dsn.bbox

    for idx in range(len(pw_set)):
        # Generate the vertical rails (Optional).
        if vertical & (pw_set[idx][0] != 1) :
            if idx % 2 == 0:
                _mn = [r23t.mn.bottom_left(pw_set[idx][1][0])-[idx,0], r23t.mn.bottom_left(pw_set[idx][1][-1])-[idx,0]]
            else:
                _mn = [r23t.mn.bottom_right(pw_set[idx][1][0])+[(idx-1),0], r23t.mn.bottom_right(pw_set[idx][1][-1])+[(idx-1),0]]
            dsn.route(grid=r23t, mn=_mn)
        
    
        # Rail extension (Optional).
        if vertical & any(1 < i for i in pw_set[:,0]):
            for x in range(len(pw_set[idx][1])):
                pw_set[idx][1][x].xy[0][0] = bbox[0][0]
                pw_set[idx][1][x].xy[1][0] = bbox[1][0]

    # 5. Check whether two variables (pin_num and pin_pitch) are entered properly.
    bottom_rail = [r23.mn.bottom_left(bbox), r23.mn.bottom_right(bbox)]

    if (pin_num == 0) & (pin_pitch == 0) : pin_num = 1 
    elif (pin_num < 0) | (pin_pitch < 0) :
        pin_num = 1
        pin_pitch = 0
        print('\n[WARNING] You entered negative number.\n')
    elif (pin_num != 0) & (pin_pitch != 0) : 
        pin_pitch = 0
        print('\n[WARNING] You have to choose between pin_num or pin_pitch.\nLAYGO2 follows <pin_num> this time.\n')

    pwidth = bottom_rail[1][0] - bottom_rail[0][0]

    # 6. Compare between pwidth and (pin_num / pin_pitch).
    if pin_num != 0: 
        if pin_num > pwidth:
            pin_num = pwidth
            pin_pitch = 1
            print('"You want too many pins. x_x')
            print('The maximum number of pins : {0}"\n'.format(pwidth))
        else: pin_pitch = pwidth//pin_num
    elif pin_pitch != 0: 
        if pin_pitch > pwidth: 
            pin_pitch = pwidth
            print('"You want too wide pitch. x_x')
            print("The minimum number of pin : 1")
            print('Thus, one pin is generated each."\n')
        pin_num = pwidth // pin_pitch

    # 7. Generate iterated power rails.
    for idx in range(pw_iter):
        pin = idx % pw_len
        iter = idx // pw_len

        _mn = bottom_rail
        _mn[0][1] = r23.n(r23.height) * (pw_len*iter+pin)
        _mn[1][1] = r23.n(r23.height) * (pw_len*iter+pin)

        pmin = _mn[0]
        pmax = _mn[1]
        pp = np.array([pmin, pmin]) + np.array([[(pwidth%pin_num)//2, 0], [(pwidth%pin_num)//2, 0]])

        for pn in range(0, pin_num):
            pp[1] += [pin_pitch, 0]
            dsn.pin(name="net{0}_{1}".format(idx, pn), grid=r23, mn=pp, netname=pin_name[idx])
            pp[0] += [pin_pitch, 0]

    # 8. Set X coordinate as zero.
    if bbox[0][0] != 0:
        for _dsn in dsn:
            dsn.elements[_dsn].xy -= [bbox[0][0],0]

    # 9. Print messages about the results.
    print('\nThe number of rails of your design is {0}.\n'.format(grid_cnt) + "The number of pins of your design is {0}.\n".format(len(pw_set)) + '\nName of Iterated net:')

    for i in range(pw_len): print('{0}. "{1}"'.format(i, pw_set[i][2]))
    if rail_change:
        print('\nName of Changed net:')
        for _num, _name in sorted(rail_count.items()): print('Rail #{0} :  "{1}"'.format(_num, _name))    
    print('\n============ SUPPLY RAIL GENERATION END ============')

def extend_wire(dsn, layer='M4', target=500):
    """
    Extend routing wires to meet the design rules about area or width of wires. This function is executed as follows:
    1. Find matched rects with the given layer in design.
    2. Check the direction of rect (horizontal or vertical). Do nothing if the rect is zero sized.
    3. Calculate total width/height of the rect and check whether the rect violates the design rule.
    4. Calculate delta (amount of extension) and create rect with new extension but maintaining bbox.
    5. Append new rects to the design and delete old rects.
    
    Parameters
    ----------
    dsn : laygo2.object.database.Design
        Design to be implemented.
    layer : str
        Name of layer for extension.
    target : int
        Target width/height of wires to be extended.
    """

    rect_list = dsn.get_matchedrects_by_layer([layer, 'drawing'])    
    for rect in rect_list:
        if rect.height == 0 and rect.width == 0:
            direction = 'horizontal' if layer in ['M2','M4','M6'] else 'vertical'
            check = rect.width + 2*rect.hextension if direction == 'horizontal' else rect.height + 2*rect.vextension
            
            if check < target:
                delta = (target - check)//2
                if direction == 'horizontal':
                    p = laygo2.object.physical.Rect(xy=rect.bbox, layer=rect.layer, hextension=rect.hextension0+delta, 
                    vextension=rect.vextension0, color=rect.color)
                else:
                    p = laygo2.object.physical.Rect(xy=rect.bbox, layer=rect.layer, hextension=rect.hextension0, 
                    vextension=rect.vextension0+delta, color=rect.color)

                dsn.append(p)

                for key, value in list(dsn.items()):
                    if value == rect:
                        del dsn.elements[key]
                    else:
                        pass
            else:
                pass

        else:
            direction = 'horizontal' if rect.height == 0 else 'vertical'
            check = rect.width + 2*rect.hextension if direction == 'horizontal' else rect.height + 2*rect.vextension

            if check < target:
                delta = (target - check)//2
                if direction == 'horizontal':
                    hextension = round(rect.hextension+delta, -1)
                    p = laygo2.object.physical.Rect(xy=rect.bbox, layer=rect.layer, hextension=hextension, 
                    vextension=rect.vextension, color=rect.color)
                else:
                    vextension = round(rect.vextension+delta, -1)
                    p = laygo2.object.physical.Rect(xy=rect.bbox, layer=rect.layer, hextension=rect.hextension, 
                    vextension=vextension, color=rect.color)

                dsn.append(p)

                for key, value in list(dsn.items()):
                    if value == rect:
                        del dsn.elements[key]
                    else:
                        pass
            else:
                pass

def fill_by_instance(dsn, grids, tlib, templates, inst_name:tuple, canvas_area="full", shape=[1,1], iter_type=("R0","MX"), pattern_direction='v', fill_sort='filler'):
    """ Fill empty layout space by given instances.
        
        Parameters
        ----------
        inst_name : tuple
            the name of the instance to fill empty layout space.
        canvas_area : "full" or list
            the range of the space to be filled.
        shape : list
            the shape of the given instances.
        iter_type : tuple
            Transform types of iterating instances.
        pattern_direction : str
            Determine the direction of iterating instances. ('v' : vertical, 'h' : horizontal)
        fill_sort : str
            the name of the created iterating instances.
    """

    print('\n=========== FILLING EMPTY LAYOUT SPACE START ===========')

    pg = grids["placement_basic"]

    # 1. Check the canvas.
    dsnbbox = pg.mn(dsn.bbox)

    offset  = dsnbbox[0]
    width   = dsnbbox[1][0] - 0
    height  = dsnbbox[1][1] - dsnbbox[0][1]

    canvas = np.zeros((height, width), dtype=int)

    def check_occupied(canvas, physical, index):
        bbox = pg.mn(physical.bbox)
        x0 = bbox[0][0]
        x1 = bbox[1][0]
        y0 = bbox[0][1]
        y1 = bbox[1][1]
        if x0 == x1 and y0 == y1:
            return
        canvas[y0:y1, x0:x1] = index

    index = 1

    for n, inst in dsn.instances.items():
        check_occupied(canvas, inst, index)
        index = index + 1
    for n, vinst in dsn.virtual_instances.items():
        check_occupied(canvas, vinst, index)
        index = index + 1

    if canvas_area != "full":
        bbox_l0 = pg.mn.bottom_left(canvas_area[0])
        bbox_l1 = pg.mn.bottom_right(canvas_area[0])
        bbox_r0 = pg.mn.top_left(canvas_area[1])
        bbox_r1 = pg.mn.top_right(canvas_area[1])

        width   = abs(bbox_r1[0] - bbox_l0[0])
        height  = abs(bbox_r1[1] - bbox_l0[1])
        offset  = bbox_l0

        canvas = canvas[bbox_l0[1]:bbox_r1[1],bbox_l0[0]:bbox_r1[0]]
    else:
        bbox_l0 = dsnbbox[0]
        bbox_l1 = dsnbbox[0] + [dsnbbox[1][0],0]
        bbox_r0 = dsnbbox[1] - [dsnbbox[1][0],0]
        bbox_r1 = dsnbbox[1]

    def check_name(inst_name, boundary_name):
        if type(inst_name) == str:
            inst_name = inst_name.split()
        else:
            for _name in inst_name:
                if type(_name) == list:
                    try:
                        boundary_name[_name[0]].append(_name[1])
                    except:
                        boundary_name[_name[0]] = [_name[1]]

        inst_name = list(filter(lambda x: type(x)==str, inst_name))
        return inst_name, boundary_name

    # 2. Fill the empty space.
    boundary_name = {}
    inst_name, boundary_name = check_name(inst_name, boundary_name)

    filler   = templates[inst_name[0]].generate(name=fill_sort, transform="R0", shape=shape)

    f_height = pg.mn(filler)[1][1]
    f_width  = pg.mn(filler)[1][0]
    n_mod    = int(height / f_height)
    print(boundary_name)
    for _name, _num in boundary_name.items():
        for i in range(len(_num)):
            if _num[i] < 0: 
                if pattern_direction == 'v': boundary_name[_name][i] += ((bbox_r0[1]-bbox_l1[1]) // f_height)
                elif pattern_direction == 'h': boundary_name[_name][i] += ((bbox_r0[0]-bbox_l1[0]) // f_width)

    boundary_count = {}
    for _name, _num in boundary_name.items():
        for idx in _num:
            boundary_count[idx] = _name

    pattern_name = 0
    for y in range(n_mod):
        buffers = []

        if pattern_direction == 'v':
            if y in boundary_count.keys(): it = boundary_count[y]
            else: 
                it = inst_name[pattern_name]
                pattern_name = (pattern_name + 1) % len(inst_name)
        elif pattern_direction == 'h': pattern_name = 0

        for x in range(width):
            if canvas[f_height * y, x] == 0:
                buffers.append(True)

                if np.array_equal(buffers, [True] * f_width):
                    if pattern_direction == 'h':
                        h_num = int((x - (bbox_l1[0] - bbox_l0[0])) / f_width)
                        if h_num in boundary_count.keys(): 
                            it = boundary_count[h_num]
                        else: 
                            it = inst_name[pattern_name]
                            if h_num != 0: pattern_name = (pattern_name + 1) % len(inst_name)
                        
                    tf = iter_type[int(y % len(iter_type))]
                    _mn = np.asarray([x-f_width+1, y * f_height])+offset
                    if tf == "MX": _mn = _mn + [0, f_height]
                    dsn.place(grid=pg, inst=templates[it].generate(name=fill_sort + f"{x}_{y * f_height}", transform=tf, shape=shape), mn=_mn)
                    buffers = []
            else:
                buffers = []
    print('============ FILLING EMPTY LAYOUT SPACE END ============')
    return canvas

def post_process( dsn, grids, tlib, templates ):
    generate_cut_layer(dsn, grids, tlib, templates)  

# Tests
if __name__ == '__main__':
    # Create templates.
    print("Create templates")
    _templates = load_templates()
    for tn, t in _templates.items():
        print(t)
