#2022-08-03 기준: pin 객체 관련 추가, error 출력 관련 추가 필요.
#grid.route, grid.route_via_track등의 함수에서 metal을 깔고 via를 뚫을 때마다 netMap의 Add 함수 호출.

#rows 리스트에서 해당 row에 맞는 요소의 index 반환
from sqlite3 import Row


def searchRow(rows, rowNum):
    start=0
    end=len(rows)-1
    while start <= end:
        mid = (start+end)//2
        if rows[mid].rowNum == rowNum:
            return mid
        elif rows[mid].rowNum > rowNum:
            end = mid-1
        else:
            start = mid + 1
    return None

#newMetal.xy1[1]을 기준으로 list의 제 위치에 삽입
def searchMetalIndex(row, newMetal):
    start = 0
    end = len(row.metalList)-1

    if len(row.metalList) == 0:
        return 0
    
    while start <= end:
        mid = (start+end)//2
        if row.metalList[mid].xy1[0] >= newMetal.xy1[0]:       #newMetal이 더 앞일때
            if mid == 0:
                return mid
            if row.metalList[mid-1].xy1[0] <= newMetal.xy1[0]:
                return mid-1
            end = mid-1
        else:      #newMetal이 더 뒤일때
            if mid == len(row.metalList)-1:
                return mid+1
            if row.metalList[mid+1].xy1[0]>=newMetal.xy1[0]:
                return mid+1
            start = mid + 1
    return None

def _getRowIndex(rows, newRowNum):       #이진 탐색 비슷하게 해서 newRowNum의 숫자가 들어갈 인덱스를 찾아 반환한다.
    start = 0
    end = len(rows)-1

    if len(rows) == 0:
        return 0

    while start <= end:
        mid = (start+end)//2

        if rows[mid].rowNum >= newRowNum:
            if mid == 0:
                return mid
            if rows[mid-1].rowNum <= newRowNum:
                return mid-1
            end = mid-1
        else:
            if mid == len(rows)-1:
                return mid
            if rows[mid+1].rowNum>=newRowNum:
                return mid+1
            start = mid + 1
    return None

def getRowIndex(rows, newRowNum):       #이진 탐색 비슷하게 해서 newRowNum의 숫자가 들어갈 인덱스를 찾아 반환한다.
    start = 0
    end = len(rows)-1
    if len(rows) == 0:
        return 0
    
    while start + 1 < end:
        mid = (start+end)//2
        if rows[mid].rowNum > newRowNum:
            end = mid
        elif rows[mid].rowNum < newRowNum:
            start = mid
        else:
            return mid
        
    if rows[start].rowNum > newRowNum:
        return start
    elif rows[end].rowNum < newRowNum:
        return end + 1
    else:
        return end 
    

def merge_via(vias1, vias2):
    viaList = vias1
    for via in vias2:
        if via not in viaList:
            viaList.append(via)
    return viaList
    

class rowNode:
    def __init__(self, rowNum):
        self.rowNum = rowNum
        self.metalList = list()
        
class metalNode:
    def __init__(self, point1, point2, vias, netName=None, isPin=False):
        self.xy1 = point1
        self.xy2 = point2
        self.netName = netName
        self.vias = vias
        self.isPin = isPin
        

class netMap_hor:
    def __init__(self):
        self.rows = list()
        
    #정렬된 row와 새로 깔 metal 받아서 merge
    def merge(self, newMetal, rowIndex):
        newMetal_index = searchMetalIndex(self.rows[rowIndex], newMetal)

        if newMetal_index == 0:         #row의 맨 앞에 새로운 metal을 삽입하는 경우
            if newMetal_index == len(self.rows[rowIndex].metalList):
                self.rows[rowIndex].metalList.insert(newMetal_index, newMetal)
            else:        #뒤쪽 원소들과 겹치는지 확인해 겹치면 merge
                nextMetal_index = newMetal_index
                while nextMetal_index<len(self.rows[rowIndex].metalList):
                    if newMetal.xy2[0]<self.rows[rowIndex].metalList[nextMetal_index].xy1[0]:
                        break
                    else:
                        if newMetal.netName != self.rows[rowIndex].metalList[nextMetal_index].netName:
                            print("error")

                        if newMetal.isPin == True or self.rows[rowIndex].metalList[nextMetal_index].xy1[0] == True:
                            nextMetal_index = nextMetal_index+1
                            continue

                        metal_next = self.rows[rowIndex].metalList.pop(nextMetal_index)

                        viaList = merge_via(newMetal.vias, metal_next.vias)

                        if newMetal.xy2[0]<metal_next.xy2[0]:          #newMetal 끝이 뒤 metal 끝보다 앞에 있을 경우
                            newMetal = metalNode(newMetal.xy1, metal_next.xy2, viaList, newMetal.netName)
                        else:
                            newMetal = metalNode(newMetal.xy1, newMetal.xy2, viaList, newMetal.netName)
            
                self.rows[rowIndex].metalList.insert(newMetal_index, newMetal)

        else:
            #먼저 바로 앞 metal과 겹치는지를 확인해 처리한다.=>겹치더라도 하나의 metal과만 겹침
            if newMetal.xy1[0]<=self.rows[rowIndex].metalList[newMetal_index-1].xy2[0]:      #앞 metal이랑 겹치면
                if newMetal.netName != self.rows[rowIndex].metalList[newMetal_index-1].netName:
                    print("error")

                if newMetal.isPin == False and self.rows[rowIndex].metalList[newMetal_index-1].xy1[0] == False:
                    metal_prev = self.rows[rowIndex].metalList.pop(newMetal_index-1)
                    viaList = merge_via(newMetal.vias, metal_prev.vias)
                    newMetal = metalNode(metal_prev.xy1, newMetal.xy2, viaList, newMetal.netName)
                    newMetal_index=newMetal_index-1

            #뒤쪽 metal들과 겹치는지 확인해 처리
            nextMetal_index = newMetal_index
            while nextMetal_index<len(self.rows[rowIndex].metalList):
                if newMetal.xy2[0]<self.rows[rowIndex].metalList[nextMetal_index].xy1[0]:
                    break
                else:
                    if newMetal.netName != self.rows[rowIndex].metalList[nextMetal_index].netName:
                        print("error")

                    if newMetal.isPin == True or self.rows[rowIndex].metalList[nextMetal_index].xy1[0] == True:
                        nextMetal_index = nextMetal_index+1
                        continue

                    metal_next = self.rows[rowIndex].metalList.pop(nextMetal_index)

                    viaList = merge_via(newMetal.vias, metal_next.vias)

                    if newMetal.xy2[0]<metal_next.xy2[0]:          #newMetal 끝이 뒤 metal 끝보다 앞에 있을 경우
                        newMetal = metalNode(newMetal.xy1, metal_next.xy2, viaList, newMetal.netName)
                    else:
                        newMetal = metalNode(newMetal.xy1, newMetal.xy2, viaList, newMetal.netName)
        
            self.rows[rowIndex].metalList.insert(newMetal_index, newMetal)

        
            
        
    # def insertMetal(self, mn, via1, via2, netName=None):        #(grid.route 기준)__mn, netName, via_tag[i], [i+1] 넘겨주면 됨
    #     #에러발생
    #     point1=mn[0]
    #     point2=mn[1]
    #     if point1[1] != point2[1]:
    #         print('Not horizontal')
    #     else:
    #         rowIndex = searchRow(self.rows, point1[1])
    #         if rowIndex is None: 
    #             #self.rows에 rowNode(point1[1])를 순서에 맞춰 삽입
    #             newRowIndex = getRowIndex(self.rows, point1[1])
    #             self.rows.insert(newRowIndex, rowNode(point1[1]))
                
    #             vias=list()
    #             if via1 == True:
    #                 vias.append(point1)
    #             if via2 == True:
    #                 vias.append(point2)
                
    #             self.merge(metalNode(point1, point2, vias, netName), newRowIndex)
    #         else:
    #             vias=list()
    #             if via1 == True:
    #                 vias.append(point1)
    #             if via2 == True:
    #                 vias.append(point2)
    #             self.merge(metalNode(point1, point2, vias, netName), rowIndex)
                

    def insertPin(self, mn, netName=None):
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
            rowIndex = searchRow(self.rows, i)
            if rowIndex is None:
                #self.rows에 rowNode(i)를 순서에 맞춰 삽입
                newRowIndex = getRowIndex(self.rows, i)
                self.rows.insert(newRowIndex, rowNode(i))
                vias=list()
                self.merge(metalNode([x1, i], [x2, i], vias, netName, isPin=True), newRowIndex)
            else:
                vias=list()
                self.merge(metalNode([x1, i], [x2, i], vias, netName, isPin=True), rowIndex)
    
    