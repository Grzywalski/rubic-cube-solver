import random
import time

dic_cross = {}
dic_f2l1 = {}
dic_f2l2 = {}
dic_f2l3 = {}
dic_f2l4 = {}
dic_top_cross = {}

dic_top_last_edge = {}



def rot90_cw(f):
    """Rotacja 90° w prawo (zgodnie z ruchem wskazówek zegara)"""
    return [
        [f[2][0], f[1][0], f[0][0]],
        [f[2][1], f[1][1], f[0][1]],
        [f[2][2], f[1][2], f[0][2]]
    ]

def rot90_ccw(f):
    """Rotacja 90° w lewo (przeciwnie do ruchu wskazówek)"""
    return [
        [f[0][2], f[1][2], f[2][2]],
        [f[0][1], f[1][1], f[2][1]],
        [f[0][0], f[1][0], f[2][0]]
    ]
class cube:
    def __init__(self):
        self.front = [[1,1,1],[1,1,1],[1,1,1]]
        self.back = [[3,3,3],[3,3,3],[3,3,3]]
        self.right = [[2,2,2],[2,2,2],[2,2,2]]
        self.left = [[4,4,4],[4,4,4],[4,4,4]]
        self.up = [[5,5,5],[5,5,5],[5,5,5]]
        self.down = [[6,6,6],[6,6,6],[6,6,6]]


    def to_bytes(self) -> bytes:
        return bytes(
            self.front[0] + self.front[1] + self.front[2] +
            self.back[0]  + self.back[1]  + self.back[2]  +
            self.right[0] + self.right[1] + self.right[2] +
            self.left[0]  + self.left[1]  + self.left[2]  +
            self.up[0]    + self.up[1]    + self.up[2]    +
            self.down[0]  + self.down[1]  + self.down[2]
        )
        
    def cross_key(self):
        return bytes([
        self.down[0][1], self.down[1][0], self.down[1][1], self.down[1][2], self.down[2][1],
        self.front[2][1], self.back[2][1], self.right[2][1], self.left[2][1]
    ])
    
    def f2l_key_seg1(self):
        return bytes([
            self.down[0][1],self.down[0][2], *self.down[1], self.down[2][1],self.front[2][1],self.front[2][2],self.back[2][1],self.right[2][1],self.right[2][0],self.left[2][1]
        ])
        
    def f2l_key_seg2(self):
        return bytes([
            self.down[0][1],self.down[0][2], *self.down[1], self.down[2][1],self.down[2][2],self.front[2][1],self.front[2][2],self.back[2][1],self.back[1][0],self.back[2][0],self.right[2][1],self.right[2][0],self.right[1][2],
            self.right[2][2],self.left[2][1]
        ])
            
    def f2l_key_seg3(self):
        return bytes([
            self.down[0][1],self.down[0][2], *self.down[1], *self.down[2],self.front[2][1],self.front[2][2],*self.back[1],*self.back[2],*self.right[1],*self.right[2],
            self.left[2][1],self.left[1][0],self.left[2][0]
        ])
    def f2l_key_seg4(self):
        return bytes([*self.down[0],*self.down[1],*self.down[2],*self.front[1],*self.front[2],*self.right[1],*self.right[2],*self.back[1],*self.back[2],*self.left[1],*self.left[2]])
    
    def top_cross_key(self):
        return bytes([*self.up[0],*self.up[1],*self.up[2],*self.front[0],*self.right[0],*self.back[0],*self.left[0]]) 
    
    def top_all_key(self):
        return bytes([*self.front[0],*self.right[0],*self.back[0],*self.left[0]])       
    
    def moveR(self):
        temp = [self.front[0][2], self.front[1][2], self.front[2][2]]
        self.front[0][2], self.front[1][2], self.front[2][2] = self.down[0][2], self.down[1][2], self.down[2][2]
        self.down[0][2], self.down[1][2], self.down[2][2] = self.back[2][0], self.back[1][0], self.back[0][0]
        self.back[0][0], self.back[1][0], self.back[2][0] = self.up[2][2], self.up[1][2], self.up[0][2]
        self.up[0][2], self.up[1][2], self.up[2][2] = temp[0], temp[1], temp[2]
        self.right = rot90_cw(self.right)

    def moveRPrime(self):
        temp = [self.front[0][2], self.front[1][2], self.front[2][2]]
        self.front[0][2], self.front[1][2], self.front[2][2] = self.up[0][2], self.up[1][2], self.up[2][2]
        self.up[0][2], self.up[1][2], self.up[2][2] = self.back[2][0], self.back[1][0], self.back[0][0]
        self.back[0][0], self.back[1][0], self.back[2][0] = self.down[2][2], self.down[1][2], self.down[0][2]
        self.down[0][2], self.down[1][2], self.down[2][2] = temp[0], temp[1], temp[2]
        self.right = rot90_ccw(self.right)

    def moveLPrime(self):
        temp = [self.front[0][0], self.front[1][0], self.front[2][0]]
        self.front[0][0], self.front[1][0], self.front[2][0] = self.down[0][0], self.down[1][0], self.down[2][0]
        self.down[0][0], self.down[1][0], self.down[2][0] = self.back[2][2], self.back[1][2], self.back[0][2]
        self.back[0][2], self.back[1][2], self.back[2][2] = self.up[2][0], self.up[1][0], self.up[0][0]
        self.up[0][0], self.up[1][0], self.up[2][0] = temp[0], temp[1], temp[2]
        self.left = rot90_ccw(self.left)

    def moveL(self):
        temp = [self.front[0][0], self.front[1][0], self.front[2][0]]
        self.front[0][0], self.front[1][0], self.front[2][0] = self.up[0][0], self.up[1][0], self.up[2][0]
        self.up[0][0], self.up[1][0], self.up[2][0] = self.back[2][2], self.back[1][2], self.back[0][2]
        self.back[0][2], self.back[1][2], self.back[2][2] = self.down[2][0], self.down[1][0], self.down[0][0]
        self.down[0][0], self.down[1][0], self.down[2][0] = temp[0], temp[1], temp[2]
        self.left = rot90_cw(self.left)

    def moveD(self):
        temp = self.front[2][:]
        self.front[2] = self.left[2][:]
        self.left[2] = self.back[2][:]
        self.back[2] = self.right[2][:]
        self.right[2] = temp
        self.down = rot90_cw(self.down)

    def moveDPrime(self):
        temp = self.front[2][:]
        self.front[2] = self.right[2][:]
        self.right[2] = self.back[2][:]
        self.back[2] = self.left[2][:]
        self.left[2] = temp
        self.down = rot90_ccw(self.down)

    def moveU(self):
        temp = self.front[0][:]
        self.front[0] = self.right[0][:]
        self.right[0] = self.back[0][:]
        self.back[0] = self.left[0][:]
        self.left[0] = temp
        self.up = rot90_cw(self.up)

    def moveUPrime(self):
        temp = self.front[0][:]
        self.front[0] = self.left[0][:]
        self.left[0] = self.back[0][:]
        self.back[0] = self.right[0][:]
        self.right[0] = temp
        self.up = rot90_ccw(self.up)

    def moveF(self):
        self.front = rot90_cw(self.front)
        temp = self.up[2][:]
        self.up[2] = [self.left[2][2], self.left[1][2], self.left[0][2]]
        self.left[0][2], self.left[1][2], self.left[2][2] = self.down[0][0], self.down[0][1], self.down[0][2]
        self.down[0] = [self.right[2][0], self.right[1][0], self.right[0][0]]
        self.right[0][0], self.right[1][0], self.right[2][0] = temp[0], temp[1], temp[2]

    def moveFPrime(self):
        self.front = rot90_ccw(self.front)
        temp = self.up[2][:]
        self.up[2] = [self.right[0][0], self.right[1][0], self.right[2][0]]
        self.right[0][0], self.right[1][0], self.right[2][0] = self.down[0][2], self.down[0][1], self.down[0][0]
        self.down[0] = [self.left[0][2], self.left[1][2], self.left[2][2]]
        self.left[0][2], self.left[1][2], self.left[2][2] = temp[2], temp[1], temp[0]

    def moveB(self):
        self.back = rot90_cw(self.back)
        temp = self.up[0][:]
        self.up[0] = [self.right[0][2], self.right[1][2], self.right[2][2]]
        self.right[0][2], self.right[1][2], self.right[2][2] = self.down[2][2], self.down[2][1], self.down[2][0]
        self.down[2] = [self.left[0][0], self.left[1][0], self.left[2][0]]
        self.left[0][0], self.left[1][0], self.left[2][0] = temp[2], temp[1], temp[0]

    def moveBPrime(self):
        self.back = rot90_ccw(self.back)
        temp = self.up[0][:]
        self.up[0] = [self.left[2][0], self.left[1][0], self.left[0][0]]
        self.left[0][0], self.left[1][0], self.left[2][0] = self.down[2][0], self.down[2][1], self.down[2][2]
        self.down[2] = [self.right[2][2], self.right[1][2], self.right[0][2]]
        self.right[0][2], self.right[1][2], self.right[2][2] = temp[0], temp[1], temp[2]

    def print_every_move(self):
        moves = [self.moveR,self.moveRPrime,self.moveL,self.moveLPrime,self.moveU,self.moveUPrime,self.moveD,self.moveDPrime,self.moveF,self.moveFPrime,self.moveB,self.moveBPrime]
        for move in moves:
            print(f"ruch :{move}")
            move()
            move()
            self.print()
            print(f"=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=")

    
    def scramble(self):
        random.seed(time.time())
        moves = [self.moveR,self.moveRPrime,self.moveL,self.moveLPrime,self.moveU,self.moveUPrime,self.moveD,self.moveDPrime,self.moveF,self.moveFPrime,self.moveB,self.moveBPrime]
        ruchy = random.choices(moves,k=15)
        for ruch in ruchy:
            ruch()
        skrócone_nazwy = [ruch.__name__.replace("move", "") for ruch in ruchy]
        print(" -> ".join(skrócone_nazwy))
    
        
    def solve_to_cross(self):
        moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "D", "DPrime", "F", "FPrime", "B", "BPrime"]
        move_opposites = {
        "R": "RPrime", "RPrime": "R",
        "L": "LPrime", "LPrime": "L",
        "U": "UPrime", "UPrime": "U",
        "D": "DPrime", "DPrime": "D",
        "F": "FPrime", "FPrime": "F",
        "B": "BPrime", "BPrime": "B"
    }   

        def check_cross(kostka):
            down_ok = (
                kostka.down[1] == [6, 6, 6] and
                kostka.down[0][1] == 6 and
                kostka.down[2][1] == 6
            )
            f_ok = kostka.front[2][1] == 1
            b_ok = kostka.back[2][1] == 3
            r_ok = kostka.right[2][1] == 2
            l_ok = kostka.left[2][1] == 4
            return down_ok and f_ok and b_ok and r_ok and l_ok
        
        def dfs_search(cube_copy,max_depth,depth,last_move,path=None):
            if path is None:
                path = []
            if max_depth < depth:
                return None 
            for move in moves:
                if last_move is not None and move == move_opposites[last_move]:
                    continue
                method = f"move{move}"
                method_undo = f"move{move_opposites[move]}"
                getattr(cube_copy,method)()
                path.append(move)
                
                key = cube_copy.cross_key()
                if key in dic_cross:
                    candidate = path + [move_opposites[ele] for ele in dic_cross[key][::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_cross(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
                
        max_limit = 3
   
        for current_max_depth in range(1, max_limit+5):
            path = []
            find = self.copy()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."
       
    # rozwiazuje w 4 krokach f2l : po koleji kazdy naroznik i krawedz na kazdym rogu
    def solve_f2l_seg1(self):
        moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "F", "FPrime"]
        move_opposites = {
        "R": "RPrime", "RPrime": "R",
        "L": "LPrime", "LPrime": "L",
        "U": "UPrime", "UPrime": "U",
        "D": "DPrime", "DPrime": "D",
        "F": "FPrime", "FPrime": "F",
        "B": "BPrime", "BPrime": "B"
    }   

        def check_f2l(kostka):
            down_ok = (
                kostka.down[1] == [6, 6, 6] and
                kostka.down[0][1] == 6 and
                kostka.down[2][1] == 6 and
                kostka.down[0][2] == 6
            )
            f_ok = (kostka.front[2][1] == 1 and kostka.front[1][2] == 1 and kostka.front[2][2] == 1)
            b_ok = kostka.back[2][1] == 3
            r_ok = (kostka.right[2][1] == 2 and kostka.right[1][0] == 2 and kostka.right[2][0] == 2)
            l_ok = kostka.left[2][1] == 4
            return down_ok and f_ok and b_ok and r_ok and l_ok
        
        def dfs_search(cube_copy,max_depth,depth,last_move,path=None):
            if path is None:
                path = []
            if max_depth < depth:
                return None 
            for move in moves:
                if last_move is not None and move == move_opposites[last_move]:
                    continue
                method = f"move{move}"
                method_undo = f"move{move_opposites[move]}"
                getattr(cube_copy,method)()
                path.append(move)
                
                key = cube_copy.f2l_key_seg1()
                if key in dic_f2l1:
                    candidate = path + [move_opposites[ele] for ele in dic_f2l1[key][::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_f2l(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
                
        max_limit = 4
        
        for current_max_depth in range(1, max_limit+6):
            path = []
            find = self.copy()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."

    def solve_f2l_seg2(self):
            moves = ["L", "LPrime", "U", "UPrime", "B", "BPrime"]
            move_opposites = {
            "R": "RPrime", "RPrime": "R",
            "L": "LPrime", "LPrime": "L",
            "U": "UPrime", "UPrime": "U",
            "D": "DPrime", "DPrime": "D",
            "F": "FPrime", "FPrime": "F",
            "B": "BPrime", "BPrime": "B"
        }   

            def check_f2l(kostka):
                down_ok = (
                    kostka.down[1] == [6, 6, 6] and
                    kostka.down[0][1] == 6 and
                    kostka.down[2][1] == 6 and
                    kostka.down[0][2] == 6 and 
                    kostka.down[2][2] == 6
                )
                f_ok = (kostka.front[2][1] == 1 and kostka.front[1][2] == 1 and kostka.front[2][2] == 1)
                b_ok = (kostka.back[2][1] == 3 and kostka.back[1][0] == 3 and kostka.back[2][0] ==3)
                r_ok = (kostka.right[1] == [2,2,2] and kostka.right[2] == [2,2,2])
                l_ok = kostka.left[2][1] == 4
                return down_ok and f_ok and b_ok and r_ok and l_ok
            
            def dfs_search(cube_copy,max_depth,depth,last_move,path=None):
                if path is None:
                    path = []
                if max_depth < depth:
                    return None 
                for move in moves:
                    if last_move is not None and move == move_opposites[last_move]:
                        continue
                    method = f"move{move}"
                    method_undo = f"move{move_opposites[move]}"
                    getattr(cube_copy,method)()
                    path.append(move)
                    
                    key = cube_copy.f2l_key_seg2()
                    if key in dic_f2l2:
                        candidate = path + [move_opposites[ele] for ele in dic_f2l2[key][::-1]]
                        test = self.copy()
                        for m in candidate:
                            getattr(test, f"move{m}")()
                        if check_f2l(test):
                            for m in candidate:
                                getattr(self, f"move{m}")()
                            return candidate
                    
                    result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                    if result:
                        return result
                    path.pop()
                    getattr(cube_copy,method_undo)()
                return None
                    
            max_limit = 4  
            
            for current_max_depth in range(1, max_limit+6):
                path = []
                find = self.copy()
                solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
                if solution is not None:
                    return solution
            return "Nie znaleziono rozwiązania w zadanym limicie głębokości."
    
    def solve_f2l_seg3(self):
        moves = ["L", "LPrime", "U", "UPrime", "B", "BPrime"]
        move_opposites = {
        "R": "RPrime", "RPrime": "R",
        "L": "LPrime", "LPrime": "L",
        "U": "UPrime", "UPrime": "U",
        "D": "DPrime", "DPrime": "D",
        "F": "FPrime", "FPrime": "F",
        "B": "BPrime", "BPrime": "B"
    }   
                    
        def check_f2l(kostka):
            down_ok = (
                kostka.down[1] == [6, 6, 6] and
                kostka.down[0][1] == 6 and
                kostka.down[2] == [6,6,6] and
                kostka.down[0][2] == 6
                
            )
            f_ok = (kostka.front[2][1] == 1 and kostka.front[1][2] == 1 and kostka.front[2][2] == 1)
            b_ok = (kostka.back[1] == [3,3,3] and kostka.back[2] == [3,3,3])
            r_ok = (kostka.right[1] == [2,2,2] and kostka.right[2] == [2,2,2])
            l_ok = (kostka.left[2][1] == 4 and kostka.left[1][0] == 4 and kostka.left[2][0] == 4)
            return down_ok and f_ok and b_ok and r_ok and l_ok

        
        def dfs_search(cube_copy,max_depth,depth,last_move,path=None):
            if path is None:
                path = []
            if max_depth < depth:
                return None 
            for move in moves:
                if last_move is not None and move == move_opposites[last_move]:
                    continue
                method = f"move{move}"
                method_undo = f"move{move_opposites[move]}"
                getattr(cube_copy,method)()
                path.append(move)
                
                key = cube_copy.f2l_key_seg3()
                if key in dic_f2l3:
                    candidate = path + [move_opposites[ele] for ele in dic_f2l3[key][::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_f2l(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
                
        max_limit = 4    
        
        for current_max_depth in range(1, max_limit+6):
            path = []
            find = self.copy()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."
    
    def solve_f2l_seg4(self):
        moves = ["L", "LPrime", "U", "UPrime", "F", "FPrime"]
        move_opposites = {
        "R": "RPrime", "RPrime": "R",
        "L": "LPrime", "LPrime": "L",
        "U": "UPrime", "UPrime": "U",
        "D": "DPrime", "DPrime": "D",
        "F": "FPrime", "FPrime": "F",
        "B": "BPrime", "BPrime": "B"
    }   
                
        def check_f2l(kostka):
            down_ok = (
                kostka.down[1] == [6,6,6] and
                kostka.down[0] == [6,6,6] and
                kostka.down[2] == [6,6,6] )
            f_ok = (kostka.front[1] == [1,1,1] and kostka.front[2] == [1,1,1])
            b_ok = (kostka.back[1] == [3,3,3] and kostka.back[2] == [3,3,3])
            r_ok = (kostka.right[1] == [2,2,2] and kostka.right[2] == [2,2,2])
            l_ok = (kostka.left[1] == [4,4,4] and kostka.left[2] == [4,4,4])
            return down_ok and f_ok and b_ok and r_ok and l_ok
        
        def dfs_search(cube_copy,max_depth,depth,last_move,path=None):
            if path is None:
                path = []
            if max_depth < depth:
                return None 
            for move in moves:
                if last_move is not None and move == move_opposites[last_move]:
                    continue
                method = f"move{move}"
                method_undo = f"move{move_opposites[move]}"
                getattr(cube_copy,method)()
                path.append(move)
                
                key = cube_copy.f2l_key_seg4()
                if key in dic_f2l4:
                    candidate = path + [move_opposites[ele] for ele in dic_f2l4[key][::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_f2l(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
                
        max_limit = 4
 
        for current_max_depth in range(1, max_limit+6):
            path = []
            find = self.copy()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."

    def solve_top_cross(self):
        moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "F", "FPrime", "B", "BPrime"]
        
        move_opposites = {
        "R": "RPrime", "RPrime": "R",
        "L": "LPrime", "LPrime": "L",
        "U": "UPrime", "UPrime": "U",
        "D": "DPrime", "DPrime": "D",
        "F": "FPrime", "FPrime": "F",
        "B": "BPrime", "BPrime": "B"
    }   
        def check_cross(kostka):
            f2l_ok = (
                kostka.down[0] == [6,6,6] and kostka.down[1] == [6,6,6] and kostka.down[2] == [6,6,6] and
                kostka.front[1] == [1,1,1] and kostka.front[2] == [1,1,1] and
                kostka.back[1]  == [3,3,3] and kostka.back[2]  == [3,3,3] and
                kostka.right[1] == [2,2,2] and kostka.right[2] == [2,2,2] and
                kostka.left[1]  == [4,4,4] and kostka.left[2]  == [4,4,4])
            up_ok = (
                kostka.up[1] == [5, 5, 5] and
                kostka.up[0][1] == 5 and
                kostka.up[2][1] == 5 

            )
            return up_ok and f2l_ok
        
        
        def dfs_search(cube_copy,max_depth,depth,last_move,path=None):
            if path is None:
                path = []
            if max_depth < depth:
                return None 
            for move in moves:
                if last_move is not None and move == move_opposites[last_move]:
                    continue
                method = f"move{move}"
                method_undo = f"move{move_opposites[move]}"
                getattr(cube_copy,method)()
                path.append(move)
                
                key = cube_copy.top_cross_key()
                if key in dic_top_cross:
                    candidate = path + [move_opposites[ele] for ele in dic_top_cross[key][::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_cross(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
        
        max_limit = 4
 
        for current_max_depth in range(1, max_limit+4):
            path = []
            find = self.copy()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."
    
    def solve_top_perm(self):
        moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "F", "FPrime", "B", "BPrime"]
                
        move_opposites = {
        "R": "RPrime", "RPrime": "R",
        "L": "LPrime", "LPrime": "L",
        "U": "UPrime", "UPrime": "U",
        "D": "DPrime", "DPrime": "D",
        "F": "FPrime", "FPrime": "F",
        "B": "BPrime", "BPrime": "B"
    }   
        def check_cross(kostka):
            f2l_ok = (
                kostka.down[0] == [6,6,6] and kostka.down[1] == [6,6,6] and kostka.down[2] == [6,6,6] and
                kostka.front[1] == [1,1,1] and kostka.front[2] == [1,1,1] and
                kostka.back[1]  == [3,3,3] and kostka.back[2]  == [3,3,3] and
                kostka.right[1] == [2,2,2] and kostka.right[2] == [2,2,2] and
                kostka.left[1]  == [4,4,4] and kostka.left[2]  == [4,4,4])
            up_ok = (
                kostka.up[1] == [5, 5, 5] and
                kostka.up[0] == [5,5,5] and
                kostka.up[2] == [5,5,5] 

            )
            return up_ok and f2l_ok
        
        
        def dfs_search(cube_copy,max_depth,depth,last_move,path=None):
            if path is None:
                path = []
            if max_depth < depth:
                return None 
            for move in moves:
                if last_move is not None and move == move_opposites[last_move]:
                    continue
                method = f"move{move}"
                method_undo = f"move{move_opposites[move]}"
                getattr(cube_copy,method)()
                path.append(move)
                
                key = cube_copy.top_cross_key()
                if key in dic_top_cross:
                    candidate = path + [move_opposites[ele] for ele in dic_top_cross[key][::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_cross(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
        
        max_limit = 5
    
        for current_max_depth in range(1, max_limit+4):
            path = []
            find = self.copy()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."
    
    def solve_top_last_edge(self):
        moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "F", "FPrime", "B", "BPrime"]
                        
        move_opposites = {
        "R": "RPrime", "RPrime": "R",
        "L": "LPrime", "LPrime": "L",
        "U": "UPrime", "UPrime": "U",
        "D": "DPrime", "DPrime": "D",
        "F": "FPrime", "FPrime": "F",
        "B": "BPrime", "BPrime": "B"
    }   
        def check_cube(kostka):
            f2l_ok = (
                            kostka.down[0] == [6,6,6] and kostka.down[1] == [6,6,6] and kostka.down[2] == [6,6,6] and
                            kostka.front[1] == [1,1,1] and kostka.front[2] == [1,1,1] and
                            kostka.back[1]  == [3,3,3] and kostka.back[2]  == [3,3,3] and
                            kostka.right[1] == [2,2,2] and kostka.right[2] == [2,2,2] and
                            kostka.left[1]  == [4,4,4] and kostka.left[2]  == [4,4,4])
            up_ok = (
                            kostka.up[1] == [5, 5, 5] and
                            kostka.up[0] == [5,5,5] and
                            kostka.up[2] == [5,5,5] and
                            kostka.front[0][1] == 1 and
                            kostka.right[0][1] == 2 and
                            kostka.back[0][1] == 3 and 
                            kostka.left[0][1] == 4
            
                        )
            return up_ok and f2l_ok
        
        
        def dfs_search(cube_copy,max_depth,depth,last_move,path=None):
            if path is None:
                path = []
            if max_depth < depth:
                return None 
            for move in moves:
                if last_move is not None and move == move_opposites[last_move]:
                    continue
                method = f"move{move}"
                method_undo = f"move{move_opposites[move]}"
                getattr(cube_copy,method)()
                path.append(move)
                
                key = cube_copy.top_all_key()
                if key in dic_top_last_edge:
                    candidate = path + [move_opposites[ele] for ele in dic_top_last_edge[key][::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_cube(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
        
        max_limit = 5
    
        for current_max_depth in range(1, max_limit+4):
            path = []
            find = self.copy()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."

    def solve_top_last_corner(self):
        moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "F", "FPrime", "B", "BPrime"]
                        
        move_opposites = {
        "R": "RPrime", "RPrime": "R",
        "L": "LPrime", "LPrime": "L",
        "U": "UPrime", "UPrime": "U",
        "D": "DPrime", "DPrime": "D",
        "F": "FPrime", "FPrime": "F",
        "B": "BPrime", "BPrime": "B"
    }   
        solved_ref = cube()
        def check_cube(kostka):
            return kostka == solved_ref
        
        
        def dfs_search(cube_copy,max_depth,depth,last_move,path=None):
            if path is None:
                path = []
            if max_depth < depth:
                return None 
            for move in moves:
                if last_move is not None and move == move_opposites[last_move]:
                    continue
                method = f"move{move}"
                method_undo = f"move{move_opposites[move]}"
                getattr(cube_copy,method)()
                path.append(move)
                
                key = cube_copy.top_all_key()
                if key in dic_top_last_edge:
                    candidate = path + [move_opposites[ele] for ele in dic_top_last_edge[key][::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_cube(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
        
        max_limit = 5
    
        for current_max_depth in range(1, max_limit+4):
            path = []
            find = self.copy()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."

    def movetopos(self,ruchy):
        for ruch in ruchy:
            ruch()
        
    def print(self):
        print("front:")
        print(self.front[0])
        print(self.front[1])
        print(self.front[2])
        print("==========================")
        print("back:")
        print(self.back[0])
        print(self.back[1])
        print(self.back[2])
        print("==========================")
        print("right:")
        print(self.right[0])
        print(self.right[1])
        print(self.right[2])
        print("==========================")
        print("left:")
        print(self.left[0])
        print(self.left[1])
        print(self.left[2])
        print("==========================")
        print("up:")
        print(self.up[0])
        print(self.up[1])
        print(self.up[2])
        print("==========================")
        print("down:")
        print(self.down[0])
        print(self.down[1])
        print(self.down[2])
            
    def __eq__(self, other):
        if not isinstance(other, cube):
            return False
        return (
            self.front == other.front and
            self.back == other.back and
            self.right == other.right and
            self.left == other.left and
            self.up == other.up and
            self.down == other.down
        )
        
    def _to_tuple(self):
        return (
            tuple(map(tuple, self.front)),
            tuple(map(tuple, self.back)),
            tuple(map(tuple, self.right)),
            tuple(map(tuple, self.left)),
            tuple(map(tuple, self.up)),
            tuple(map(tuple, self.down))
        )
        
    def load_from_tuple(self, state):
        (front, back, right, left, up, down) = state
        self.front = [list(row) for row in front]
        self.back  = [list(row) for row in back]
        self.right = [list(row) for row in right]
        self.left  = [list(row) for row in left]
        self.up    = [list(row) for row in up]
        self.down  = [list(row) for row in down]

    def __hash__(self):
        return hash(self._to_tuple())
        
    def copy(self):
        new_cube = cube()
        new_cube.front = [row[:] for row in self.front]
        new_cube.up = [row[:] for row in self.up]
        new_cube.right = [row[:] for row in self.right]
        new_cube.left = [row[:] for row in self.left]
        new_cube.down = [row[:] for row in self.down]
        new_cube.back = [row[:] for row in self.back]
        return new_cube

def create_all_dics():
    #cross
    moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "D", "DPrime", "F", "FPrime", "B", "BPrime"]
    move_opposites = {
    "R": "RPrime", "RPrime": "R",
    "L": "LPrime", "LPrime": "L",
    "U": "UPrime", "UPrime": "U",
    "D": "DPrime", "DPrime": "D",
    "F": "FPrime", "FPrime": "F",
    "B": "BPrime", "BPrime": "B"
}   

    def dfs_build_dic(cube_copy,max_depth,depth,last_move,path=None):
        if path is None:
            path = []
        if max_depth < depth:
            return None 
        for move in moves:
            if last_move is not None and move == move_opposites[last_move]:
                continue
            method = f"move{move}"
            method_undo = f"move{move_opposites[move]}"
            getattr(cube_copy,method)()
            path.append(move)
            
            key = cube_copy.cross_key()
            if key not in dic_cross or len(path) < len(dic_cross[key]):
                dic_cross[key] = path.copy()
            
            result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
            path.pop()
            getattr(cube_copy,method_undo)()
        return None
    max_limit = 4
    path = []
    kopia = cube()
    dic_cross[kopia.cross_key()] = []
    dfs_build_dic(kopia, max_depth=max_limit, depth=1, last_move=None, path=path)    
    
    #f2l_1
    moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "F", "FPrime"]
    def dfs_build_dic(cube_copy,max_depth,depth,last_move,path=None):
        if path is None:
            path = []
        if max_depth < depth:
            return None 
        for move in moves:
            if last_move is not None and move == move_opposites[last_move]:
                continue
            method = f"move{move}"
            method_undo = f"move{move_opposites[move]}"
            getattr(cube_copy,method)()
            path.append(move)
            
            key = cube_copy.f2l_key_seg1()
            if key not in dic_f2l1 or len(path) < len(dic_f2l1[key]):
                dic_f2l1[key] = path.copy()
            
            result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
            path.pop()
            getattr(cube_copy,method_undo)()
        return None
    max_limit = 5
    path = []
    kopia = cube()
    dic_f2l1[kopia.f2l_key_seg1()] = []
    dfs_build_dic(kopia, max_depth=max_limit, depth=1, last_move=None, path=path)
    #f2l_2
    moves = ["L", "LPrime", "U", "UPrime", "B", "BPrime"]
    def dfs_build_dic(cube_copy,max_depth,depth,last_move,path=None):
        if path is None:
            path = []
        if max_depth < depth:
            return None 
        for move in moves:
            if last_move is not None and move == move_opposites[last_move]:
                continue
            
            method = f"move{move}"
            method_undo = f"move{move_opposites[move]}"
            getattr(cube_copy,method)()
            path.append(move)
            
            key = cube_copy.f2l_key_seg2()
            if key not in dic_f2l2 or len(path) < len(dic_f2l2[key]):
                dic_f2l2[key] = path.copy()
            
            result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
            path.pop()
            getattr(cube_copy,method_undo)()
        return None
    max_limit = 5
    kopia = cube()
    path = []
    dic_f2l2[kopia.f2l_key_seg2()] = []
    dfs_build_dic(kopia, max_depth=max_limit, depth=1, last_move=None, path=path)  
    #f2l_3
    moves = ["L", "LPrime", "U", "UPrime", "B", "BPrime"]
    def dfs_build_dic(cube_copy,max_depth,depth,last_move,path=None):
        if path is None:
            path = []
        if max_depth < depth:
            return None 
        for move in moves:
            if last_move is not None and move == move_opposites[last_move]:
                continue
            method = f"move{move}"
            method_undo = f"move{move_opposites[move]}"
            getattr(cube_copy,method)()
            path.append(move)
            
            key = cube_copy.f2l_key_seg3()
            if key not in dic_f2l3 or len(path) < len(dic_f2l3[key]):
                dic_f2l3[key] = path.copy()
            
            result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
            path.pop()
            getattr(cube_copy,method_undo)()
        return None
    max_limit = 5
    kopia = cube()
    dic_f2l3[kopia.f2l_key_seg3()] = []
    path = []
    dfs_build_dic(kopia, max_depth=max_limit, depth=1, last_move=None, path=path)   
    #f2l_4
    moves = ["L", "LPrime", "U", "UPrime", "F", "FPrime"]
    def dfs_build_dic(cube_copy,max_depth,depth,last_move,path=None):
        if path is None:
            path = []
        if max_depth < depth:
            return None 
        for move in moves:
            if last_move is not None and move == move_opposites[last_move]:
                continue
            method = f"move{move}"
            method_undo = f"move{move_opposites[move]}"
            getattr(cube_copy,method)()
            path.append(move)
            
            key = cube_copy.f2l_key_seg4()
            if key not in dic_f2l4 or len(path) < len(dic_f2l4[key]):
                dic_f2l4[key] = path.copy()
            
            result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
            path.pop()
            getattr(cube_copy,method_undo)()
        return None
    max_limit = 5
    kopia = cube()
    dic_f2l4[kopia.f2l_key_seg4()] = []
    path = []
    dfs_build_dic(kopia, max_depth=max_limit, depth=1, last_move=None, path=path)  
    
    #top_cross
    moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "F", "FPrime", "B", "BPrime"]
    def dfs_build_dic(cube_copy,max_depth,depth,last_move,path=None):
        if path is None:
            path = []
        if max_depth < depth:
            return None 
        for move in moves:
            if last_move is not None and move == move_opposites[last_move]:
                continue
            method = f"move{move}"
            method_undo = f"move{move_opposites[move]}"
            getattr(cube_copy,method)()
            path.append(move)
            
            key = cube_copy.top_cross_key()
            if key not in dic_top_cross or len(path) < len(dic_top_cross[key]):
                dic_top_cross[key] = path.copy()
            
            result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
            path.pop()
            getattr(cube_copy,method_undo)()
        return None
    max_limit = 7
    path = []
    kopia = cube()
    dic_top_cross[kopia.top_cross_key()] = []
    dfs_build_dic(kopia, max_depth=max_limit, depth=1, last_move=None, path=path)  
    #top_perm
    
    #top_last_edge
    moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "F", "FPrime", "B", "BPrime"]
    def dfs_build_dic(cube_copy,max_depth,depth,last_move,path=None):
        if path is None:
            path = []
        if max_depth < depth:
            return None 
        for move in moves:
            if last_move is not None and move == move_opposites[last_move]:
                continue
            method = f"move{move}"
            method_undo = f"move{move_opposites[move]}"
            getattr(cube_copy,method)()
            path.append(move)
            
            key = cube_copy.top_all_key()
            if key not in dic_top_last_edge or len(path) < len(dic_top_last_edge[key]):
                dic_top_last_edge[key] = path.copy()
            
            result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
            path.pop()
            getattr(cube_copy,method_undo)()
        return None
    max_limit = 7
    path = []
    kopia = cube()
    dic_top_last_edge[kopia.top_all_key()] = []
    dfs_build_dic(kopia, max_depth=max_limit, depth=1, last_move=None, path=path) 
    #top_last_corner



     
import pickle, os
path = "C:/Users/PC/Desktop/cube/cube_dics.pkl"
if os.path.exists(path):
    with open(path,"rb") as f:
        dic_cross, dic_f2l1, dic_f2l2, dic_f2l3, dic_f2l4, dic_top_cross,dic_top_last_edge= pickle.load(f)
else:
    create_all_dics()
    with open(path,"wb") as f:
        pickle.dump((dic_cross, dic_f2l1, dic_f2l2, dic_f2l3, dic_f2l4, dic_top_cross,dic_top_last_edge), f)
        
counter = 0
rang = 1

total_cross = 0.0
total_f2l1 = 0.0
total_f2l2 = 0.0
total_f2l3 = 0.0
total_f2l4 = 0.0
total_top_cross = 0.0
total_top_perm = 0.0
total_top_last_edge = 0.0
total_top_last_corner = 0.0

errors = []
stages = ["cross", "f2l-1", "f2l-2", "f2l-3", "f2l-4", "top-cross", "top-perm", "top-last-edge","top-last-corner"]
time_all = time.time()

for i in range(rang):
    x = cube()
    x.scramble()

    t0 = time.time()
    a = x.solve_to_cross()
    t1 = time.time()
    b = x.solve_f2l_seg1()
    t2 = time.time()
    c = x.solve_f2l_seg2()
    t3 = time.time()
    d = x.solve_f2l_seg3()
    t4 = time.time()
    e = x.solve_f2l_seg4()
    t5 = time.time()
    f = x.solve_top_cross()
    t6 = time.time()
    g = x.solve_top_perm()
    t7 = time.time()
    h = x.solve_top_last_edge()
    t8 = time.time()
    j = x.solve_top_last_corner()
    t9 = time.time()

    total_cross += t1 - t0
    total_f2l1 += t2 - t1
    total_f2l2 += t3 - t2
    total_f2l3 += t4 - t3
    total_f2l4 += t5 - t4
    total_top_cross += t6 - t5
    total_top_perm += t7 - t6
    total_top_last_edge += t8 - t7
    total_top_last_corner += t9-t8

    results = [a, b, c, d, e, f, g, h,j]

    # Sukces, jeśli żaden etap nie zwrócił ciągu znaków określającego błąd
    if all(isinstance(res, list) for res in results):
        counter += 1
    else:
        err_details = [stage for stage, res in zip(stages, results) if isinstance(res, str)]
        errors.append({"iteracja": i, "błędy": err_details})

total_elapsed = time.time() - time_all
print(f"calkowity czas:{total_elapsed}, sredni czas:{total_elapsed/rang} i succes ratio:{counter/rang} i {counter} sukcesow")

print("Średnie czasy poszczególnych etapów:")
print(f"cross:      {total_cross / rang:.4f}s")
print(f"f2l-1:      {total_f2l1 / rang:.4f}s")
print(f"f2l-2:      {total_f2l2 / rang:.4f}s")
print(f"f2l-3:      {total_f2l3 / rang:.4f}s")
print(f"f2l-4:      {total_f2l4 / rang:.4f}s")
print(f"top-cross:  {total_top_cross / rang:.4f}s")
print(f"top-perm:   {total_top_perm / rang:.4f}s")
print(f"top-last-edge:   {total_top_last_edge / rang:.4f}s")
print(f"top-last-corner:   {total_top_last_corner / rang:.4f}s\n")

if errors:
    print(f"Liczba błędnych prób: {len(errors)}")
    print("Błędy:", errors)
else:
    print("Brak błędów podczas wykonywania testu.")
    
