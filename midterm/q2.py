from random import shuffle
from numpy import inf

class Line:
    def __init__(self, a, b, c):   # ax + by <= c
        self.a = a
        self.b = b
        self.c = c
        self.slope = -(a/b) if b != 0 else inf
    def get_y(self, x):
        if self.b == 0:
            return False
        return (self.c - self.a * x) / self.b          # 處理b=0
    def get_x(self):                # for ax = c
        return self.c / self.a
    def printing(self):
        print( self.a, 'x +', self.b,'y <=', self.c)
    
        
class Intersect:
    def __init__(self, l1, l2):
        self.l1 = l1
        self.l2 = l2
        (b, w) = self.find_intersect(l1, l2)
        self.x = b
        self.y = w
    def find_intersect(self, L1, L2):
        D  = L1.a * L2.b - L1.b * L2.a
        Dx = L1.c * L2.b - L1.b * L2.c
        Dy = L1.a * L2.c - L1.c * L2.a
        if D != 0:
            x = Dx / D
            y = Dy / D
            return (x, y)
        else:
            return (False, False)
    def printing(self):
        print('(x, y) =', self.x, ',', self.y)
        
        
class Manager:
    def __init__(self):
        self.set = []
    def size(self):
        return len(self.set)
    def get(self, idx):     # get by indx
        return self.set[idx]
    def add(self, n):
        self.set.append(n)
    def remove(self, n):
        self.set.remove(n)
    def shuffling(self):
        shuffle(self.set)
    def printing(self):
        for e in self.set:
            e.printing()
        print()
        
            
    
def init_line(inp):
    lm_up = Manager()
    lm_down = Manager()
    lm_z = Manager()
    input = [e.split(' ') for e in inp.split('\n')]
    for l in input[:-1]:
        a = float(l[0])
        b = float(l[1])
        c = float(l[2])        
        new_line = Line(a, b, c)
        if b == 0:
            lm_z.add(new_line)
        elif b < 0:
            lm_up.add(new_line)
        else:
            lm_down.add(new_line) 
    return (lm_up, lm_down, lm_z)
        
    
def find_xm(lm_up, lm_down, Xl, Xr):
    im_up = Manager()  # intersection manager
    im_down = Manager()
    myimm = [im_up, im_down]
    mylmm = [lm_up, lm_down]
    i_x = []
    for lm in mylmm:
        lmm_idx = mylmm.index(lm)
        lm.shuffling()
        list_delet = []
        for idx in range(lm.size()-1):
            if idx % 2 != 0:
                continue
            pair_i = Intersect(lm.get(idx), lm.get(idx+1))
            if pair_i.x == False and pair_i.y == False:     # 處理平行的情況
                if lm is lm_up:
                    l_delet = pair_i.l1 if pair_i.l1.get_y(0) < pair_i.l2.get_y(0) else pair_i.l2                    
                elif lm is lm_down:
                    l_delet = pair_i.l1 if pair_i.l1.get_y(0) > pair_i.l2.get_y(0) else pair_i.l2
                list_delet.append(l_delet)                          # 處理平行的情況
            elif pair_i.x > Xr:                             # 處理交點在邊界之外的情況
                if lm is lm_up:
                    l_delet = pair_i.l2 if pair_i.l1.slope < pair_i.l2.slope else pair_i.l1                    
                elif lm is lm_down:
                    l_delet = pair_i.l2 if pair_i.l1.slope > pair_i.l2.slope else pair_i.l1
                list_delet.append(l_delet)   
            elif pair_i.x < Xl:
                if lm is lm_up:
                    l_delet = pair_i.l2 if pair_i.l1.slope > pair_i.l2.slope else pair_i.l1                    
                elif lm is lm_down:
                    l_delet = pair_i.l2 if pair_i.l1.slope < pair_i.l2.slope else pair_i.l1
                list_delet.append(l_delet)                          # 處理交點在邊界之外的情況
            else:
                myimm[lmm_idx].add(pair_i)
                i_x.append(pair_i.x)
        for e in list_delet:
            lm.remove(e)
    i_x.sort()    
    Xm = i_x[int(len(i_x)/2)] if i_x else False
    return (Xm, im_up, im_down)
            
def find_margin(lm_z):
    list_l = [-inf]
    list_r = [inf]
    for l in lm_z.set:
        if l.a < 0:
            list_l.append(l.get_x())
        else:
            list_r.append(l.get_x())
    return (max(list_l), min(list_r))
    
def f_up(Xm, lm_up):
    mylist = []
    for l in lm_up.set:
        mylist.append(l.get_y(Xm))
    return max(mylist)
    
def f_down(Xm, lm_down):
    mylist = []
    for l in lm_down.set:
        mylist.append(l.get_y(Xm))
    return min(mylist)
    
def get_slope(Xm, Ym, lm):
    s = []
    for l in lm.set:
        if abs(l.get_y(Xm) - Ym) < 0.0001 :       # 要做誤差值
            s.append(l.slope)
    return (max(s), min(s))
    
def read_input(name):
    with open(name, 'r') as f:
        out = ''
        f.readline()
        for line in f:
            out += line
    return out 
        
def write_result(name, val):
    with open(name, 'w') as f:
        f.write(str(val))

if __name__ == '__main__':        

    inp = read_input('./2DLP-5.txt')
    (lm_up, lm_down, lm_z) = init_line(inp)     #line manager
    (Xl, Xr) = find_margin(lm_z)
    result = None
    
    while True:
        if lm_up.size() <= 1 and lm_down.size() <= 1:
            l_last = lm_up.get(0)
            if l_last.slope > 0:
                output = int(l_last.get_y(Xl)) if Xl != -inf else '-INF'
            elif l_last.slope < 0:
                output = int(l_last.get_y(Xr)) if Xr != inf else '-INF'
            else:
                output = int(l_last.get_y(0))
            print(output)
            result = output
            break        
        (Xm, im_up, im_down) = find_xm(lm_up, lm_down, Xl, Xr)
        #lmm = [lm_up, lm_down, lm_z]
        if not Xm:          # 如果遇到每條都是平行線的情況 就找不到Xm
            continue
        
        (Ax, Ay) = (Xm, (f_up(Xm, lm_up)))
        (Bx, By) = (Xm, (f_down(Xm, lm_down)))
        (Smax, Smin) = get_slope(Ax, Ay, lm_up)
        (Tmax, Tmin) = get_slope(Bx, By, lm_down)
        if (Ay <= By and Smin <= Smax < 0) or (Ay > By and Smax < Tmin):   # Xm < X*   注意比較的誤差值
            for i in im_up.set:
                if i.x <= Xm:
                    l1s = i.l1.slope
                    l2s = i.l2.slope
                    if l1s > l2s:               # 沒處理兩個slope一樣的情況
                        lm_up.remove(i.l2)
                    elif l1s < l2s:
                        lm_up.remove(i.l1)
            for i in im_down.set:
                if i.x <= Xm:
                    l1s = i.l1.slope
                    l2s = i.l2.slope
                    if l1s > l2s:               # 沒處理兩個slope一樣的情況
                        lm_down.remove(i.l1)
                    elif l1s < l2s:
                        lm_down.remove(i.l2)
            Xl = Xm
        elif (Ay <= By and Smax >= Smin > 0) or (Ay > By and Smin > Tmax):   # X* < Xm
            for i in im_up.set:
                if i.x >= Xm:
                    l1s = i.l1.slope
                    l2s = i.l2.slope
                    if l1s > l2s:               # 沒處理兩個slope一樣的情況
                        lm_up.remove(i.l1)
                    elif l1s < l2s:
                        lm_up.remove(i.l2)
            for i in im_down.set:
                if i.x >= Xm:
                    l1s = i.l1.slope
                    l2s = i.l2.slope
                    if l1s > l2s:               # 沒處理兩個slope一樣的情況
                        lm_down.remove(i.l2)
                    elif l1s < l2s:
                        lm_down.remove(i.l1)
            Xr = Xm
        elif Ay <= By and Smin <= 0 <= Smax : # Xm = X*
            print(int(Ay))
            result = int(Ay)
            break
        elif Ay > By and (Smax >= Tmin and Smin <= Tmax):  # No ans
            print('NA')
            result = 'NA'
            break
        
    write_result('output.txt', result)

"""
9
1 1 10
7 -3 68
6 6 27
6 7 54
6 -4 36
-1 -1 -20
-5 9 36
4 -6 54
-4 11 78
"""

""" 1
10
5 -3 -140
287 17 -6
280 -101 232
219 -120 157
77 171 -62
57 206 -61
-206 193 256
88 233 -111
73 212 24
-1 0 133
"""
            
#切記比較時要誤差值   
# 未處理平行 + u1u2邊界