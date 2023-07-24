from collections import deque
from pickle import FALSE
import laygo2
import numpy as np
import laygo2.util.transform as tf

class rcNode:
    def __init__(self, rc_num):
        self.rc_num = rc_num
        self.dot_list = list()
        self.metal_list = list()

class metalNode:
    def __init__(self, layer_name, mn):
        self.layer=layer_name
        self.mn = mn
        self.net_name = set()
        self.metal_seg = list()
        self.via_list = list()
        self.visited = False
class viaNode:
    def __init__(self, layer_pair, mn):
        self.mn = mn
        self.layer_pair=layer_pair

class netMap_basic:
    def __init__(self, rc):
        self.rc = rc

    def search_rc(self, rc_num):
        start=0
        end=len(self.rc)-1
        while start <= end:
            mid = (start+end)//2
            if self.rc[mid].rc_num == rc_num:
                return mid
            elif self.rc[mid].rc_num > rc_num:
                end = mid-1
            else:
                start = mid+1
        return None
    
    def get_rc_index(self, new_rc_num):
        start = 0
        end = len(self.rc)-1
        if len(self.rc) == 0:
            return 0
        
        while start+1 < end:
            mid = (start+end)//2
            if self.rc[mid].rc_num > new_rc_num:
                end = mid
            elif self.rc[mid].rc_num < new_rc_num:
                start = mid
            else:
                return mid
            
        if self.rc[start].rc_num > new_rc_num:
            return start
        elif self.rc[end].rc_num < new_rc_num:
            return end+1
        else:
            return end


class netMap_vert(netMap_basic):
    def __init__(self, layer_name):
        self.cols = list()
        self.cols_unmerged = list()
        self.rc = self.cols
        self.layer = layer_name

    def search_metal_index(self, col_index, obj_y1): #col -> self.col 
        col = self.cols[col_index]
        start = 0
        end = len(col.metal_list)-1

        if len(col.metal_list) == 0:
            return 0
        
        while start+1 < end:
            mid = (start+end)//2
            if col.metal_list[mid].mn[0][1] > obj_y1:       
                end = mid
            elif col.metal_list[mid].mn[0][1] < obj_y1:      
                start = mid
            else:
                return mid+1

        if col.metal_list[start].mn[0][1] > obj_y1:       
            return start
        elif col.metal_list[end].mn[0][1] <= obj_y1:      
            return end+1
        else:
            return end

    def insert_metal(self, mn, net_name=None):
        if mn[0][0] < mn[1][0]:
            x1=mn[0][0]
            x2=mn[1][0]
        else:
            x1=mn[1][0]
            x2=mn[0][0]
        
        if mn[0][1] < mn[1][1]:
            y1=mn[0][1]
            y2=mn[1][1]
        else:
            y1=mn[1][1]
            y2=mn[0][1]


        for i in range (x1, x2+1):
            col_index = self.search_rc(i)
            if col_index is None:
                #self.cols에 rcNode(i)를 순서에 맞춰 삽입
                new_col_index = self.get_rc_index(i)
                self.cols.insert(new_col_index, rcNode(i))
                self.cols_unmerged.insert(new_col_index, rcNode(i))

                #red, blue list 추가
                self.cols[new_col_index].dot_list.append((y1, 'b'))
                self.cols[new_col_index].dot_list.append((y2, 'r'))

                new_node = metalNode(self.layer, [[i, y1], [i, y2]])
                new_node.net_name.add(net_name)
                #새로운 metalnode를 unmerged list에 추가
                self.cols_unmerged[new_col_index].metal_list.append(new_node)

            else:
                #red, blue list 추가
                self.cols[col_index].dot_list.append((y1, 'b'))
                self.cols[col_index].dot_list.append((y2, 'r'))

                new_node = metalNode(self.layer, [[i, y1], [i, y2]])
                new_node.net_name.add(net_name)
                #새로운 metalnode를 unmerged list에 추가
                self.cols_unmerged[col_index].metal_list.append(new_node)

                
    #insert가 끝난 뒤 마지막에 호출해주면 된다.
    def merge(self):
        #blue랑 red 비교/병합
        for col in self.cols:
            #dot들 정렬
            col.dot_list = sorted(col.dot_list, key = lambda x : x[0] + ord(x[1])/128)
            br_diff = 0
            start = 0
            end = 0
            for dot in col.dot_list:
                if br_diff == 0:
                    start = dot[0]
                if dot[1] == 'b':
                    br_diff = br_diff + 1
                else:
                    br_diff = br_diff - 1

                if br_diff < 0:
                    print("error")
                    break
                if br_diff == 0:
                    end = dot[0]
                    col.metal_list.append(metalNode(self.layer, [[col.rc_num, start], [col.rc_num, end]]))
        col_index = 0
        #unmerged list와 병합해 기타 데이터 추가
        for col_unmerged in self.cols_unmerged:
            for unmerged_metal in col_unmerged.metal_list:
                metal_index = self.search_metal_index(col_index, unmerged_metal.mn[0][1])-1
                self.cols[col_index].metal_list[metal_index].metal_seg.append(unmerged_metal)
                self.cols[col_index].metal_list[metal_index].net_name|unmerged_metal.net_name
            col_index = col_index + 1


class netMap_hor(netMap_basic):
    def __init__(self, layer_name):
        self.rows = list()
        self.rows_unmerged = list()
        self.rc = self.rows
        self.layer=layer_name
    def search_metal_index(self, row_index, obj_x1): #row -> self.row
        row = self.rows[row_index]
        start = 0
        end = len(row.metal_list)-1

        if len(row.metal_list) == 0:
            return 0
        
        while start+1 < end:
            mid = (start+end)//2
            if row.metal_list[mid].mn[0][0] > obj_x1:       
                end = mid
            elif row.metal_list[mid].mn[0][0] < obj_x1:      
                start = mid
            else:
                return mid+1

        if row.metal_list[start].mn[0][0] > obj_x1:       
            return start
        elif row.metal_list[end].mn[0][0] <= obj_x1:      
            return end+1
        else:
            return end

    def insert_metal(self, mn, net_name=None):
        if mn[0][0] < mn[1][0]:
            x1=mn[0][0]
            x2=mn[1][0]
        else:
            x1=mn[1][0]
            x2=mn[0][0]
        
        if mn[0][1] < mn[1][1]:
            y1=mn[0][1]
            y2=mn[1][1]
        else:
            y1=mn[1][1]
            y2=mn[0][1]

        for i in range (y1, y2+1):
            row_index = self.search_rc(i)
            if row_index is None:
                #self.rows에 rowNode(i)를 순서에 맞춰 삽입
                new_row_index = self.get_rc_index(i)
                self.rows.insert(new_row_index, rcNode(i))
                self.rows_unmerged.insert(new_row_index, rcNode(i))

                #red, blue list 추가
                self.rows[new_row_index].dot_list.append((x1, 'b'))
                self.rows[new_row_index].dot_list.append((x2, 'r'))

                new_node = metalNode(self.layer, [[x1, i], [x2, i]])
                new_node.net_name.add(net_name)
                #새로운 metalnode를 unmerged list에 추가
                self.rows_unmerged[new_row_index].metal_list.append(new_node)

            else:
                #red, blue list 추가
                self.rows[row_index].dot_list.append((x1, 'b'))
                self.rows[row_index].dot_list.append((x2, 'r'))

                new_node = metalNode(self.layer, [[x1, i], [x2, i]])
                new_node.net_name.add(net_name)
                #새로운 metalnode를 unmerged list에 추가
                self.rows_unmerged[row_index].metal_list.append(new_node)


    def merge(self):
        #blue랑 red 비교/병합
        for row in self.rows:
            #dot들 정렬
            row.dot_list = sorted(row.dot_list, key = lambda x : x[0] + ord(x[1])/128)
            br_diff = 0
            start = 0
            end = 0
            for dot in row.dot_list:
                if br_diff == 0:
                    start = dot[0]
                if dot[1] == 'b':
                    br_diff = br_diff + 1
                else:
                    br_diff = br_diff - 1

                if br_diff < 0:
                    print("error")
                    break
                if br_diff == 0:
                    end = dot[0]
                    row.metal_list.append(metalNode(self.layer, [[start, row.rc_num], [end, row.rc_num]]))

        row_index = 0
        #unmerged list와 병합해 기타 데이터 추가
        for row_unmerged in self.rows_unmerged:
            for unmerged_metal in row_unmerged.metal_list:
                metal_index = self.search_metal_index(row_index, unmerged_metal.mn[0][0])-1
                self.rows[row_index].metal_list[metal_index].metal_seg.append(unmerged_metal)
                self.rows[row_index].metal_list[metal_index].net_name|unmerged_metal.net_name
            row_index = row_index+1


class netMap:
#member : type
#layers : dict
#layers_orient : dict
#pins : list
#_via_table : dict
#grid : laygo2.object.grid
#orient : bool
    def __init__(self, grid, via_table:dict, orient_first="vertical",layer_names:list=['M1','M2','M3','M4','M5']):
        self.layers=dict()
        self.layers_orient=dict()
        self.pins=list()
        self.vias=list()
        self._via_table=via_table
        self.grid=grid
        if orient_first=="vertical":
            self.orient_order = True
            for idx in range(len(layer_names)//2):
                self.layers[layer_names[idx*2]] = netMap_vert(layer_names[idx*2])
                self.layers[layer_names[idx*2+1]] = netMap_hor(layer_names[idx*2+1])
                self.layers_orient[layer_names[idx*2]] = "vertical"
                self.layers_orient[layer_names[idx*2+1]] = "horizontal"
            if len(layer_names)%2 == 1:
                self.layers[layer_names[-1]] = netMap_vert(layer_names[-1])
                self.layers_orient[layer_names[-1]] = "vertical"

        elif orient_first=="horizontal":
            self.orient_order = False
            for idx in range(len(layer_names)//2):
                self.layers[layer_names[idx*2]] = netMap_hor(layer_names[idx*2])
                self.layers[layer_names[idx*2+1]] = netMap_vert(layer_names[idx*2+1])
                self.layers_orient[layer_names[idx*2]] = "horizontal"
                self.layers_orient[layer_names[idx*2+1]] = "vertical"
            if len(layer_names)%2 == 1:
                self.layers[layer_names[-1]] = netMap_hor(layer_names[-1])
                self.layers_orient[layer_names[-1]] = "horizontal"
        else:
            print("wrong orient")
    
    def translate_rect(self, elem, master): # translate mn of metals of (virtual)instances
        mxy = master.xy
        mtf = master.transform
        _xy = np.sort(elem.xy, axis=0)  # make sure obj.xy is sorted
        _xy = mxy + np.dot(_xy, tf.Mt(mtf).T)
        return self.grid.mn(_xy)
        #self.layers[elem.layer[0]].insert_metal(self.grid.mn(_xy), netname=elem.netname) # TODO: insert metal로 바꿀 것    
    
    def insert_metal(self, metal):
        return self.layers[metal.layer[0]].insert_metal(self.grid.mn(metal.xy), net_name=metal.netname)

    def merge(self):
        for layer in self.layers.values():
            layer.merge()
    
    def insert_instance_blackbox(self, inst):
        pin_list = list()
        for pin in inst.pins.values():
            # _mn = [[-9999,-9999],[9999,9999]]
            # _mn[0][0] = round(pin.xy[0][0]/72)
            # _mn[0][1] = round(pin.xy[0][1]/72)
            # _mn[1][0] = round(pin.xy[1][0]/72)
            # _mn[1][1] = round(pin.xy[1][1]/72)
            self.layers[pin.layer[0]].insert_metal(self.grid.mn(pin), net_name=pin.netname)
            pin_list.append(pin)
        return pin_list

    def insert_virtual_instance(self, vinst): 
        via_list=list()
        pin_list=list()
        for velem in vinst.native_elements.values():
            if velem.__class__ == laygo2.object.Rect: #insert metals of a virtual instance
                _mn = self.translate_rect(velem, vinst)
                self.layers[velem.layer[0]].insert_metal(_mn, net_name=velem.netname)
            # vias of instance & virtual instance are not inserted -> changed. vias are inerted
            elif self.is_via(velem):
                via_list.append(viaNode(self._via_table[velem.cellname], self.grid.mn(velem.xy)))
        #TODO: implement insert instance code
        for vpin in vinst.pins.values():
            pin_list.append(vpin)
        return pin_list, via_list

    def insert_pin(self, pin):
        _layer_name = pin.layer[0]
        _layer = self.layers[_layer_name]
        # somehow grid.mn(pin.xy) dosen't work (it returns 'None' for numbers those are not multiple of 72)
        # _mn = [[-9999,-9999],[9999,9999]]
        # _mn[0][0] = round(pin.xy[0][0]/72)
        # _mn[0][1] = round(pin.xy[0][1]/72)
        # _mn[1][0] = round(pin.xy[1][0]/72)
        # _mn[1][1] = round(pin.xy[1][1]/72)
        _mn = self.grid.mn(pin)
    #    print(_layer_name, _mn, pin.netname, pin.name)
        if _mn[0][0] > _mn[1][0]:
            _mn[0][0], _mn[1][0]=_mn[1][0], _mn[0][0]       
        if _mn[0][1] > _mn[1][1]:
            _mn[0][1], _mn[1][1]=_mn[1][1], _mn[0][1]

        if self.layers_orient[_layer_name] == "horizontal":
            for i in range(_mn[0][1], _mn[1][1]+1):
                _row_idx = self.layers[_layer_name].search_rc(i)
                if _row_idx is None: # error case
                    print("pin error: No metal on "+_layer_name+', y='+str(_mn[0][1]))
                if _layer.rows[_row_idx].metal_list[0].mn[0][0] > _mn[0][0]:
                    print("pin error: No metal on "+_layer_name+', x='+str(_mn[0][0])+', y='+str(_mn[0][1]))
                elif _layer.rows[_row_idx].metal_list[len(_layer.rows[_row_idx].metal_list)-1].mn[1][0] < _mn[1][0]:
                    print("pin error: No metal on "+_layer_name+', x='+str(_mn[1][0])+', y='+str(_mn[0][1]))
                # invariant: node[0].x1 <= pinx1 <= pinx2 <= node[last].x2
                _pin_idx = _layer.search_metal_index(_row_idx, _mn[0][0])-1
                if _layer.rows[_row_idx].metal_list[_pin_idx].mn[1][0] < _mn[1][0]:
                    print("pin error: No metal on "+_layer+', x='+str(_mn[1][0])+', y='+str(_mn[0][1]))
                self.pins.append((pin,_layer.rows[_row_idx].metal_list[_pin_idx]))
        else: # layer orient == vertical
            for i in range(_mn[0][0], _mn[1][0]+1):
                _col_idx = self.layers[_layer_name].search_rc(i)
                if _col_idx is None: # error case
                    print("pin error: No metal on "+_layer_name+', x= %d' % (_mn[0][1]))
                if _layer.cols[_col_idx].metal_list[0].mn[0][1] > _mn[0][1]:
                    print("pin error: No metal on "+_layer_name+', x= %d, y= %d' % (_mn[0][0],_mn[0][1]))
                elif _layer.cols[_col_idx].metal_list[len(_layer.cols[_col_idx].metal_list)-1].mn[1][1] < _mn[1][1]:
                    print("pin error: No metal on "+_layer_name+', x= %d, y= %d' % (_mn[1][0],+_mn[0][1]))
                # invariant: node[0].y1 <= piny1 <= piny2 <= node[last].y2
                _pin_idx = _layer.search_metal_index(_col_idx, _mn[0][1])-1
                if _layer.cols[_col_idx].metal_list[_pin_idx].mn[1][1] < _mn[1][1]:
                    print("pin error: No metal on "+_layer_name+', x= %d, y= %d' % (_mn[1][0],_mn[1][1]))
                self.pins.append((pin,_layer.cols[_col_idx].metal_list[_pin_idx]))

    def is_via(self, _inst):
        if _inst.cellname in self._via_table:
            return True
        else: 
            return False

    def insert_via(self, via):
        # if not self.is_via(inst):
        #     print("error:"+inst+"is not_via")
        #via_mn, layer1(vertical), layer2(horizontal) mapping
        via_mn = via.mn
        if self.layers_orient[via.layer_pair[0]] == "vertical":
            layer1_name, layer2_name = via.layer_pair
        else:
            layer2_name, layer1_name = via.layer_pair
        layer1, layer2 = self.layers[layer1_name], self.layers[layer2_name]
        col_index = layer1.search_rc(via_mn[0])
        if col_index is None:
            print("Error: no metal on layer= "+layer1_name+" x="+str(via_mn[0]))
            return
        metal_index = layer1.search_metal_index(col_index, via_mn[1])-1
        if metal_index == -1:
            print("Error: no metal on via: layer="+layer1_name+" x="+str(via_mn[0]))
            return
        layer1_metal = layer1.cols[col_index].metal_list[metal_index]
        if layer1_metal.mn[1][1] < via_mn[1]:
            print("Error: no metal on via: layer="+layer1_name+" x="+str(via_mn[0])+" y="+str(via_mn[1]))
            return

        row_index = layer2.search_rc(via_mn[1])
        if row_index is None:
            print("Error: no metal on layer= "+layer2_name+" y="+str(via_mn[1]))
            return
        metal_index = layer2.search_metal_index(row_index, via_mn[0])-1
        if metal_index == -1:
            print("Error: no metal on via: layer= "+layer2_name+" y="+str(via_mn[1]))
            return
        layer2_metal = layer2.rows[row_index].metal_list[metal_index]
        if layer2_metal.mn[1][0] < via_mn[0]:
            print("Error: no metal on via: layer="+layer2_name+" x="+str(via_mn[0])+" y="+str(via_mn[1]))
            return
        
        layer1_metal.via_list.append([layer2_metal, layer2, via_mn])
        layer2_metal.via_list.append([layer1_metal, layer1, via_mn])
    
    def check_node(self, ref_net_name, metal):
        _netname = metal.net_name
        if len(_netname) == 1 and ref_net_name not in _netname:
            if _netname == {None}:
                metal.net_name.remove(None)
                metal.net_name.add(ref_net_name)
            else:    
                print(_netname,end='')
                print(' is connected to',end=' ')
                print(set([ref_net_name]))
                print(metal.layer, metal.mn)
        elif len(_netname) == 2:
            if None in _netname and _netname - {None} == {ref_net_name}:
                metal.net_name.remove(None)
            else:
                print(_netname,end='')
                print(' are connected to',end=' ')
                print(set([ref_net_name]))
                print(metal.layer, metal.mn)
        else:
            pass

    def net_traverse(self, pin, pin_net_name,pin_set): # travel net graph in BFS order. Source node is pin
        # if pin.visited == True: # pin nodes also could be visited by previous traverse
        #     return
        if pin_net_name in pin_set:
            if pin.visited == False:
                print("open error: %s [(%d %d),(%d %d)] is not connected to same named net" %(pin_net_name,pin.mn[0][0],pin.mn[0][1],pin.mn[1][0],pin.mn[1][1]))
            #     pin.visited = True
            else:
            #     pass
            # #    print("Warning: %s is repeated but connected to same named net"%(pin_net_name))
                return
        else:
            pin_set.add(pin_net_name)
        queue = deque([pin])
        # ref_net = set()
        # ref_net.add(pin_net_name)
        # set the pin node visited
        pin.visited = True
        # repeat until the queue is empty
        while queue:
            # pop v and check netname of v
            v = queue.popleft()
            self.check_node(pin_net_name, v)
            # if len(v.net_name) > 1:
                
            #     print(v.net_name,end='')
            #     print(' are connected to',end=' ')
            #     print(pin_net_name)
            #     print(v.layer, v.mn)
            # elif not v.net_name == ref_net:
            #     print(v.net_name,end='')
            #     print(" is connected to ",end='')
            #     print(pin_net_name)
            #     print(v.layer, v.mn)
            # else: 
            #     pass
            # insert nodes that connected to v and not visited 
            for node, layer, via_mn in v.via_list:
                if not node.visited:
                    queue.append(node)
                    node.visited = True
    @classmethod
    def lvs_check(cls, dsn, grid, via_table, orient_first="vertical", layer_names=['M1','M2','M3','M4','M5']):
        nMap = cls(grid=grid, via_table=via_table, orient_first=orient_first, layer_names=layer_names)
        pin_list = list()
        pin_set = set()
        for pin in dsn.pins.values():
            pin_list.append(pin)
        for vinst in dsn.virtual_instances.values():
            _pin_list, _via_list = nMap.insert_virtual_instance(vinst)
            pin_list.extend(_pin_list)
            nMap.vias.extend(_via_list)
        for inst in dsn.instances.values():
            if nMap.is_via(inst):
                nMap.vias.append(viaNode(nMap._via_table[inst.cellname], nMap.grid.mn(inst.xy)))
            else:
                pin_list.extend(nMap.insert_instance_blackbox(inst))
        for rect in dsn.rects.values():
            _metal = nMap.insert_metal(rect)
        #unmerged->merge
        nMap.merge()
        for via in nMap.vias:
            nMap.insert_via(via)
        for pin in pin_list:
            nMap.insert_pin(pin)
        #lvs test by bfs
        for pin, pin_node in nMap.pins:
            print("pin name: %s, netname: %s, layer: %s, xy:[[%d %d][%d %d]], pin_node.xy:"\
                % (pin.name, pin.netname,pin.layer[0],nMap.grid.mn(pin)[0][0],nMap.grid.mn(pin)[0][1],nMap.grid.mn(pin)[1][0],nMap.grid.mn(pin)[1][1]),end='')
            print(pin_node.mn)
            nMap.net_traverse(pin_node,pin.netname,pin_set)
        for layer in nMap.layers.values():
            for mlist in layer.rc:
                for metal in mlist.metal_list:
                    if metal.visited is not True:
                        print(metal.layer, metal.mn, metal.net_name)