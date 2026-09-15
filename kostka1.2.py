import random
import time

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
        self.ruch_map = {
                "U": self.moveU,
                "UPrime": self.moveUPrime,
                "D": self.moveD,
                "DPrime": self.moveDPrime,
                "R": self.moveR,
                "RPrime": self.moveRPrime,
                "L": self.moveL,
                "LPrime": self.moveLPrime,
                "F": self.moveF,
                "FPrime": self.moveFPrime,
                "B": self.moveB,
                "BPrime": self.moveBPrime
            }
    def to_bytes(self) -> bytes:
        """Konwertuje 6 ścianek do jednego ciągu 54 bajtów (hashable)."""
        return (
            self.front.tobytes() +
            self.back.tobytes() +
            self.right.tobytes() +
            self.left.tobytes() +
            self.up.tobytes() +
            self.down.tobytes()
        )
    def cross_key(self):
        return bytes([
        self.down[0][1], self.down[1][0], self.down[1][1], self.down[1][2], self.down[2][1],
        self.front[2][1], self.back[2][1], self.right[2][1], self.left[2][1]
    ])
    
    def f2l_key_bot(self):
        return bytes([
            *self.down[0], *self.down[1], *self.down[2],*self.front[2],*self.back[2],*self.right[2],*self.left[2]
        ])
        
    def f2l_key_top(self):
        return bytes([
            *self.down[0], *self.down[1], *self.down[2],
            *self.front[1], *self.front[2],
            *self.back[1],  *self.back[2],
            *self.right[1], *self.right[2],
            *self.left[1],  *self.left[2]
        ])
    
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
                if key not in dic or len(path) < len(dic[key]):
                    dic[key] = path.copy()
                
                result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
        
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
                if key in dic:
                    candidate = dic[key] + [move_opposites[ele] for ele in path[::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_cross(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        print(f"Znaleziono rozwiazanie {candidate}")
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
                
        max_limit = 3
        path = []
        dic = {}
        kopia = self.copy()
        dic[self.cross_key()] = []
        dfs_build_dic(kopia, max_depth=max_limit+1, depth=1, last_move=None, path=path)     
        
        for current_max_depth in range(1, max_limit+4):
            path = []
            find = cube()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."
       
    def solve_to_2l_bottom(self):
        moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "D", "DPrime", "F", "FPrime", "B", "BPrime"]
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
                kostka.down[0] == [6, 6, 6] and
                kostka.down[2] == [6, 6, 6]
            )
            f_ok = (kostka.front[2] == [1,1,1])
            b_ok = (kostka.back[2] == [3,3,3])
            r_ok = (kostka.right[2] == [2,2,2])
            l_ok = (kostka.left[2] == [4,4,4])
            return down_ok and f_ok and b_ok and r_ok and l_ok

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
                
                key = cube_copy.f2l_key_bot()
                if key not in dic or len(path) < len(dic[key]):
                    dic[key] = path.copy()
                
                result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
        
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
                
                key = cube_copy.f2l_key_bot()
                if key in dic:
                    candidate = dic[key] + [move_opposites[ele] for ele in path[::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_f2l(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        print(f"Znaleziono rozwiazanie {candidate}")
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
                
        max_limit = 6
        path = []
        dic = {}
        kopia = self.copy()
        dic[self.f2l_key_bot()] = []
        dfs_build_dic(kopia, max_depth=max_limit+1, depth=1, last_move=None, path=path)     
        
        for current_max_depth in range(1, max_limit+3):
            path = []
            find = cube()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."
    
    def solve_to_2l_top(self):
        moves = ["R", "RPrime", "L", "LPrime", "U", "UPrime", "D", "DPrime", "F", "FPrime", "B", "BPrime"]
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
                kostka.down[0] == [6, 6, 6] and
                kostka.down[2] == [6, 6, 6]
            )
            f_ok = (kostka.front[1] == [1,1,1] and kostka.front[2] == [1,1,1])
            b_ok = (kostka.back[1] == [3,3,3] and kostka.back[2] == [3,3,3])
            r_ok = (kostka.right[1] == [2,2,2] and kostka.right[2] == [2,2,2])
            l_ok = (kostka.left[1] == [4,4,4] and kostka.left[2] == [4,4,4])
            return down_ok and f_ok and b_ok and r_ok and l_ok

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
                
                key = cube_copy.f2l_key_top()
                if key not in dic or len(path) < len(dic[key]):
                    dic[key] = path.copy()
                
                result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
        
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
                
                key = cube_copy.f2l_key_top()
                if key in dic:
                    candidate = dic[key] + [move_opposites[ele] for ele in path[::-1]]
                    test = self.copy()
                    for m in candidate:
                        getattr(test, f"move{m}")()
                    if check_f2l(test):
                        for m in candidate:
                            getattr(self, f"move{m}")()
                        print(f"Znaleziono rozwiazanie {candidate}")
                        return candidate
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
                
        max_limit = 4
        path = []
        dic = {}
        kopia = self.copy()
        dic[self.f2l_key_top()] = []
        dfs_build_dic(kopia, max_depth=max_limit+1, depth=1, last_move=None, path=path)     
        
        for current_max_depth in range(1, max_limit+2):
            path = []
            find = cube()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."

    def solve_top_layer(self):
        pass

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

x = cube()
x.scramble()
#import tracemalloc
#tracemalloc.start()
timer = time.time()
z = x.solve_to_cross()
print(time.time()-timer)
print("=============================================")
timer = time.time()
y = x.solve_to_2l_bottom()
print(time.time()-timer)
print(y)
x.print()
#current, peak = tracemalloc.get_traced_memory()
#print(f"Aktualne zużycie: {current / 10**6:.2f} MB")
#print(f"Najwyższe zużycie (Peak): {peak / 10**6:.2f} MB")
#tracemalloc.stop()


