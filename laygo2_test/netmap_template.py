class rcNode:
    def __init__(self, rc_num):
        self.rc_num = rc_num
        self.metal_list = list()

class metalNode:
    def __init__(self, mn):
        self.mn = mn
        self.net_name = set()
        self.metal_seg = list()
        self.via_list = list()
        self.visited = False

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
    def __init__(self):
        self.cols = list()
        self.rc = self.cols

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
                new_node = metalNode([[i, y1], [i, y2]])
                new_node.net_name.add(net_name)
                new_node.metal_seg.append(new_node)
                self.cols[new_col_index].metal_list.append(new_node)
                
            else:
                new_node = metalNode([[i, y1], [i, y2]])
                new_node.net_name.add(net_name)
                new_node.metal_seg.append(new_node)
                self.merge(new_node, col_index)
                

    def merge(self, new_metal, col_index):
        new_metal_index = self.search_metal_index(col_index, new_metal.mn[0][1])

        if new_metal_index > 0:         #row의 맨 앞이 아닌 곳에 새로운 metal을 삽입하는 경우
            #먼저 바로 앞 metal과 겹치는지를 확인해 처리한다.=>겹치더라도 하나의 metal과만 겹침
            if new_metal.mn[0][1]<=self.cols[col_index].metal_list[new_metal_index-1].mn[0][1]:      #앞 metal이랑 겹치면
                metal_prev = self.cols[col_index].metal_list.pop(new_metal_index-1)
                new_name = new_metal.net_name
                new_name = new_name|metal_prev.net_name

                new_metal.metal_seg.extend(metal_prev.metal_seg)
                
                #metal_prev 끝이 newMetal 끝보다 앞에 있을 경우
                if metal_prev.mn[1][1] < new_metal.mn[1][1]:               
                    xy2 = new_metal.mn[1]
                else:
                    xy2 = metal_prev.mn[1]
                
                new_metal_tmp = metalNode([metal_prev.mn[0], xy2])
                new_metal_tmp.net_name = new_name.copy()
                new_metal_tmp.metal_seg.extend(new_metal.metal_seg)
                new_metal = new_metal_tmp
                new_metal_index=new_metal_index-1

        #뒤쪽 metal들과 겹치는지 확인해 처리
        while new_metal_index<len(self.cols[col_index].metal_list):
            if new_metal.mn[1][1]<self.cols[col_index].metal_list[new_metal_index].mn[0][1]:
                break
            
            metal_next = self.cols[col_index].metal_list.pop(new_metal_index)
            new_name = new_metal.net_name
            new_name = new_name|metal_prev.net_name

            new_metal.metal_seg.extend(metal_next.metal_seg)

            if new_metal.mn[1][1] < metal_next.mn[1][1]:          #newMetal 끝이 뒤 metal 끝보다 앞에 있을 경우
                new_metal_tmp = metalNode([new_metal.mn[0], metal_next.mn[1]])
                new_metal_tmp.net_name = new_name.copy()
                new_metal_tmp.metal_seg.extend(new_metal.metal_seg)
            else:
                new_metal_tmp = metalNode([new_metal.mn[0], new_metal.mn[1]])
                new_metal_tmp.net_name = new_name.copy()
                new_metal_tmp.metal_seg.extend(new_metal.metal_seg)
            new_metal = new_metal_tmp
        
        self.cols[col_index].metal_list.insert(new_metal_index, new_metal)


class netMap_hor(netMap_basic):
    def __init__(self):
        self.rows = list()
        self.rc = self.rows

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
                new_node = metalNode([[x1, i], [x2, i]])
                new_node.net_name.add(net_name)
                new_node.metal_seg.append(new_node)
                self.rows[new_row_index].metal_list.append(new_node)
            else:
                new_node = metalNode([[x1, i], [x2, i]])
                new_node.net_name.add(net_name)
                new_node.metal_seg.append(new_node)
                self.merge(new_node, row_index)

    def merge(self, new_metal, row_index):
        new_metal_index = self.search_metal_index(row_index, new_metal.mn[0][0])

        if new_metal_index > 0:         #row의 맨 앞이 아닌 곳에 새로운 metal을 삽입하는 경우
            #먼저 바로 앞 metal과 겹치는지를 확인해 처리한다.=>겹치더라도 하나의 metal과만 겹침
            if new_metal.mn[0][0]<=self.rows[row_index].metal_list[new_metal_index-1].mn[1][0]:      #앞 metal이랑 겹치면
                metal_prev = self.rows[row_index].metal_list.pop(new_metal_index-1)
                new_name = new_metal.net_name
                new_name = new_name|metal_prev.net_name

                new_metal.metal_seg.extend(metal_prev.metal_seg)
                
                #metal_prev 끝이 newMetal 끝보다 앞에 있을 경우
                if metal_prev.mn[1][0] < new_metal.mn[1][0]:               
                    xy2 = new_metal.mn[1]
                else:
                    xy2 = metal_prev.mn[1]
                
                new_metal_tmp = metalNode([metal_prev.mn[0], xy2])
                new_metal_tmp.net_name = new_name.copy()
                new_metal_tmp.metal_seg.extend(new_metal.metal_seg)
                new_metal = new_metal_tmp
                new_metal_index=new_metal_index-1

        #뒤쪽 metal들과 겹치는지 확인해 처리
        while new_metal_index<len(self.rows[row_index].metal_list):
            if new_metal.mn[1][0]<self.rows[row_index].metal_list[new_metal_index].mn[0][0]:
                break
            
            metal_next = self.rows[row_index].metal_list.pop(new_metal_index)
            new_name = new_metal.net_name
            new_name = new_name|metal_prev.net_name

            new_metal.metal_seg.extend(metal_next.metal_seg)

            if new_metal.mn[1][0] < metal_next.mn[1][0]:          #newMetal 끝이 뒤 metal 끝보다 앞에 있을 경우
                new_metal_tmp = metalNode([new_metal.mn[0], metal_next.mn[1]])
                new_metal_tmp.net_name.extend = new_name.copy()
                new_metal_tmp.metal_seg.extend(new_metal.metal_seg)
            else:
                new_metal_tmp = metalNode([new_metal.mn[0], new_metal.mn[1]])
                new_metal_tmp.net_name = new_name.copy()
                new_metal_tmp.metal_seg.extend(new_metal.metal_seg)
            new_metal = new_metal_tmp
        
        self.rows[row_index].metal_list.insert(new_metal_index, new_metal)


class netMap:
#member : type
#layers : dict
#layers_orient : dict
#pins : list
#_via_table : dict
#grid : laygo2.object.grid
#orient : bool
    def __init__(self, grid, via_table:dict, orient_first="vertical",layer_names:list=['m1','m2','m3','m4','m5']):
        self.layers=dict()
        self.layers_orient=dict()
        self.pins=list()
        self._via_table=via_table
        self.grid=grid
        if orient_first=="vertical":
            self.orient_order = True
            for idx in range(len(layer_names)//2):
                self.layers[layer_names[idx]] = netMap_vert()
                self.layers[layer_names[idx+1]] = netMap_hor()
                self.layers_orient[layer_names[idx]] = "vertical"
                self.layers_orient[layer_names[idx+1]] = "horizontal"
            if len(layer_names)%2 == 1:
                self.layers[layer_names[-1]] = netMap_vert()
                self.layers_orient[layer_names[-1]] = "vertical"

        elif orient_first=="horizontal":
            self.orient_order = False
            for idx in range(len(layer_names)//2):
                self.layers[layer_names[idx]] = netMap_hor()
                self.layers[layer_names[idx+1]] = netMap_vert()
                self.layers_orient[layer_names[idx]] = "horizontal"
                self.layers_orient[layer_names[idx+1]] = "vertical"
            if len(layer_names)%2 == 1:
                self.layers[layer_names[-1]] = netMap_hor()
                self.layers_orient[layer_names[-1]] = "horizontal"
        else:
            print("wrong orient")
    
    def insert_metal(self, metal):
        pass
    
    def insertPin(self, pin):
        pass

    def is_via(self, _inst):
        if _inst.cellname in self._via_table:
            return True
        else: 
            return False

    def insert_via(self, inst):
        if not netMap.is_via(inst):
            print("error:"+inst+"is not_via")
        #via_mn, layer1(vertical), layer2(horizontal) mapping
        via_mn = self.grid.mn(inst.xy)
        if self.layers_orient[self._via_table[inst.cellname][0]] == "vertical":
            layer1, layer2 = self._via_table[inst.cellname]
        else:
            layer2, layer1 = self._via_table[inst.cellname]
        
        col_index = layer1.search_col(layer1.cols, via_mn[1])
        if col_index is None:
            print("Error: no metal on via")
            return
        metal_index = layer1.search_metal_index(layer1.cols[col_index], via_mn[0])-1
        if metal_index == -1:
            print("Error: no metal on via")
            return
        layer1_metal = layer1.cols[col_index].metal_list[metal_index]
        if layer1_metal.mn[1][1] < via_mn[1]:
            print("Error: no metal on via")
            return

        row_index = layer2.search_row(layer2.rows, via_mn[1])
        if row_index is None:
            print("Error: no metal on via")
            return
        metal_index = layer2.search_metal_index(layer2.rows[row_index], via_mn[0])-1
        if metal_index == -1:
            print("Error: no metal on via")
            return
        layer2_metal = layer2.rows[row_index].metal_list[metal_index]
        if layer2_metal.mn[1][0] < via_mn[0]:
            print("Error: no metal on via")
            return
        
        layer1_metal.via_list.append([layer2_metal, layer2, via_mn])
        layer2_metal.via_list.append([layer1_metal, layer1, via_mn])

