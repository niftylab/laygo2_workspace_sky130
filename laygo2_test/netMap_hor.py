#rows 리스트에서 해당 row에 맞는 요소의 index 반환
def search_row(rows, row_num):
    start=0
    end=len(rows)-1
    while start <= end:
        mid = (start+end)//2
        if rows[mid].row_num == row_num:
            return mid
        elif rows[mid].row_num > row_num:
            end = mid-1
        else:
            start = mid+1
    return None


#newMetal.xy1[0]을 기준으로 list의 제 위치에 찾기/via가 들어갈 metal 찾는데도 이용. 기준 좌표가 같은 요소가 있는 경우 반환값은 해당 요소의 인덱스+1이 됨
def search_metal_index(row, obj_x1):
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


#이진 탐색 비슷하게 해서 new_row_num의 숫자가 들어갈 인덱스를 찾아 반환한다.
def get_row_index(rows, new_row_num):       
    start = 0
    end = len(rows)-1
    if len(rows) == 0:
        return 0
    
    while start+1 < end:
        mid = (start+end)//2
        if rows[mid].row_num > new_row_num:
            end = mid
        elif rows[mid].row_num < new_row_num:
            start = mid
        else:
            return mid
        
    if rows[start].row_num > new_row_num:
        return start
    elif rows[end].row_num < new_row_num:
        return end+1
    else:
        return end 

#via의 좌표, 세로 layer(layer1), 가로 layer(layer2)를 입력받음.
def insert_via(via_mn, layer1, layer2):
    col_index = search_col(layer1.cols, via_mn[1])
    if col_index is None:
        print("Error: no metal on via")
        return
    metal_index = search_metal_index(layer1.cols[col_index], via_mn[0])-1
    if metal_index == -1:
        print("Error: no metal on via")
        return
    layer1_metal = layer1.cols[col_index].metal_list[metal_index]
    if layer1_metal.mn[1][1] > via_mn[0]:           #추후 netMap_ver의 구현에 따라 부등호 방향 달라질 수도 있음
        print("Error: no metal on via")
        return
    
    row_index = search_row(layer2.rows, via_mn[1])
    if row_index is None:
        print("Error: no metal on via")
        return
    metal_index = search_metal_index(layer2.rows[row_index], via_mn[0])-1
    if metal_index == -1:
        print("Error: no metal on via")
        return
    layer2_metal = layer2.rows[row_index].metal_list[metal_index]
    if layer2_metal.mn[1][0] < via_mn[0]:
        print("Error: no metal on via")
        return
    
    layer1_metal.via_list.append([layer2_metal, layer2, via_mn])
    layer2_metal.via_list.append([layer1_metal, layer1, via_mn])

   
class rowNode:
    def __init__(self, row_num):
        self.row_num = row_num
        self.metal_list = list()


class metalNode:
    def __init__(self, mn, pin=None):
        self.mn = mn
        self.net_name = list()
        self.metal_seg = list()
        self.via_list = list()
        self.pin = pin
        self.color = None
        

class netMap_hor:
    def __init__(self):
        self.rows = list()
        
    #정렬된 row와 새로 깔 metal 받아서 merge
    def merge(self, new_metal, row_index):
        new_metal_index = search_metal_index(self.rows[row_index], new_metal.mn[0][0])

        if new_metal_index > 0:         #row의 맨 앞이 아닌 곳에 새로운 metal을 삽입하는 경우
            #먼저 바로 앞 metal과 겹치는지를 확인해 처리한다.=>겹치더라도 하나의 metal과만 겹침
            if new_metal.mn[0][0]<=self.rows[row_index].metal_list[new_metal_index-1].mn[1][0]:      #앞 metal이랑 겹치면
                metal_prev = self.rows[row_index].metal_list.pop(new_metal_index-1)
                new_name = new_metal.net_name
                for name in metal_prev.net_name:
                    if name not in new_name:
                        new_name.append(name)

                new_metal.metal_seg.extend(metal_prev.metal_seg)

                if new_metal.pin is None and metal_prev.pin is not None:
                    new_pin = metal_prev.pin
                elif new_metal.pin is not None and metal_prev.pin is None:
                    new_pin = new_metal.pin
                elif new_metal.pin is not None and metal_prev.pin is not None:
                    print("Warning: pin name overlap")
                    new_pin = new_metal.pin+'/'+metal_prev.pin
                else:
                    new_pin = None
                
                #metal_prev 끝이 newMetal 끝보다 앞에 있을 경우
                if metal_prev.mn[1][0] < new_metal.mn[1][0]:               
                    xy2 = new_metal.mn[1]
                else:
                    xy2 = metal_prev.mn[1]
                
                new_metal_tmp = metalNode([metal_prev.mn[0], xy2], pin=new_pin)
                new_metal_tmp.net_name.extend(new_name)
                new_metal_tmp.metal_seg.extend(new_metal.metal_seg)
                new_metal = new_metal_tmp
                new_metal_index=new_metal_index-1

        #뒤쪽 metal들과 겹치는지 확인해 처리
        while new_metal_index<len(self.rows[row_index].metal_list):
            if new_metal.mn[1][0]<self.rows[row_index].metal_list[new_metal_index].mn[0][0]:
                break
            
            metal_next = self.rows[row_index].metal_list.pop(new_metal_index)
            new_name = new_metal.net_name
            for name in metal_next.net_name:
                if name not in new_name:
                    new_name.append(name)

            new_metal.metal_seg.extend(metal_next.metal_seg)

            if new_metal.pin is None and metal_next.pin is not None:
                new_pin = metal_next.pin
            elif new_metal.pin is not None and metal_next.pin is None:
                new_pin = new_metal.pin
            elif new_metal.pin is not None and metal_next.pin is not None:
                print("Warning: pin name overlap")
                new_pin = new_metal.pin+'/'+metal_next.pin
            else:
                new_pin = None

            if new_metal.mn[1][0] < metal_next.mn[1][0]:          #newMetal 끝이 뒤 metal 끝보다 앞에 있을 경우
                new_metal_tmp = metalNode([new_metal.mn[0], metal_next.mn[1]], pin=new_pin)
                new_metal_tmp.net_name.extend(new_name)
                new_metal_tmp.metal_seg.extend(new_metal.metal_seg)
            else:
                new_metal_tmp = metalNode([new_metal.mn[0], new_metal.mn[1]], pin=new_pin)
                new_metal_tmp.net_name.extend(new_name)
                new_metal_tmp.metal_seg.extend(new_metal.metal_seg)
            new_metal = new_metal_tmp
        
        self.rows[row_index].metal_list.insert(new_metal_index, new_metal)
        
    #구버전 insert_metal
    '''def insert_metal(self, mn, net_name=None):
        if mn[0][1] != mn[1][1]:
            print('Not horizontal')
        else:
            row_index = search_row(self.rows, mn[0][1])
            if row_index is None:
                #self.rows에 rowNode(mn[0][1])를 순서에 맞춰 삽입
                new_row_index = get_row_index(self.rows, mn[0][1])
                self.rows.insert(new_row_index, rowNode(mn[0][1]))
                new_node = metalNode(mn)
                new_node.net_name.append(net_name)
                new_node.metal_seg.append(new_node)
                self.rows.[new_row_index].metal_list.append(new_node)
            else:
                new_node = metalNode(mn)
                new_node.net_name.append(net_name)
                new_node.metal_seg.append(new_node)
                self.merge(new_node, row_index)'''
                
    #신버전 insert_metal
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
            row_index = search_row(self.rows, i)
            if row_index is None:
                #self.rows에 rowNode(i)를 순서에 맞춰 삽입
                new_row_index = get_row_index(self.rows, i)
                self.rows.insert(new_row_index, rowNode(i))
                new_node = metalNode([[x1, i], [x2, i]])
                new_node.net_name.append(net_name)
                new_node.metal_seg.append(new_node)
                self.rows[new_row_index].metal_list.append(new_node)
            else:
                new_node = metalNode([[x1, i], [x2, i]])
                new_node.net_name.append(net_name)
                new_node.metal_seg.append(new_node)
                self.merge(new_node, row_index)

    def insert_pin(self, pin):            #pin은 pin의 좌표를 표시하는 mn과 이름을 표시하는 name 변수를 가지고 있다고 생각하고 작성
        mn = pin.mn
        pin_name = pin.name
        row_index = search_row(self.rows, mn[1])
        if row_index is None:
            print("Error: no metal on pin")
            return
        metal_index = search_metal_index(self.rows[row_index], mn[0])-1
        metal = self.rows[row_index].metal_list[metal_index]
        if metal.mn[1][0] < mn[0]:
            print("Error: no metal on pin")
            return
        metal.pin = pin_name
        return metal
