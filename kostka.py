import numpy as np
import random
import time

class cube:
    def __init__(self):
        self.front = np.array([[1,1,1],[1,1,1],[1,1,1]], dtype=np.uint8)
        self.back = np.array([[3,3,3],[3,3,3],[3,3,3]], dtype=np.uint8)
        self.right = np.array([[2,2,2],[2,2,2],[2,2,2]], dtype=np.uint8)
        self.left = np.array([[4,4,4],[4,4,4],[4,4,4]], dtype=np.uint8)
        self.up = np.array([[5,5,5],[5,5,5],[5,5,5]], dtype=np.uint8)
        self.down = np.array([[6,6,6],[6,6,6],[6,6,6]], dtype=np.uint8)
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
            self.down[0,1], self.down[1,0], self.down[1,1], self.down[1,2], self.down[2,1],
            self.front[2,1], self.back[2,1], self.right[2,1], self.left[2,1]
        ])
    
    def moveR(self):
        temp = self.front[:,2].copy() 
        self.front[:,2] = self.down[:,2]
        self.down[:,2] = np.flip(self.back[:,0])
        self.back[:,0] = np.flip(self.up[:,2])
        self.up[:,2] = temp
        self.right = np.rot90(self.right,k=3)
     
    def moveRPrime(self):
        temp = self.front[:,2].copy() 
        self.front[:,2] = self.up[:,2]
        self.up[:,2] = np.flip(self.back[:,0])
        self.back[:,0] = np.flip(self.down[:,2])
        self.down[:,2] = temp
        self.right = np.rot90(self.right)
    
    def moveLPrime(self):
        temp = self.front[:,0].copy() 
        self.front[:,0] = self.down[:,0]
        self.down[:,0] = np.flip(self.back[:,2])
        self.back[:,2] = np.flip(self.up[:,0])
        self.up[:,0] = temp
        self.left = np.rot90(self.left)
    
    def moveL(self):
        temp = self.front[:,0].copy() 
        self.front[:,0] = self.up[:,0]
        self.up[:,0] = np.flip(self.back[:,2])
        self.back[:,2] = np.flip(self.down[:,0])
        self.down[:,0] = temp
        self.left = np.rot90(self.left,k=3)
    
    def moveD(self):
        temp = self.front[2,:].copy()
        self.front[2,:] = self.left[2,:]
        self.left[2,:] = self.back[2,:]
        self.back[2,:] = self.right[2,:]
        self.right[2,:] = temp
        self.down = np.rot90(self.down,k=3)
    
    def moveDPrime(self):
        temp = self.front[2,:].copy()
        self.front[2,:] = self.right[2,:]
        self.right[2,:] = self.back[2,:]
        self.back[2,:] = self.left[2,:]
        self.left[2,:] = temp
        self.down = np.rot90(self.down)
    
    def moveU(self):
        temp = self.front[0,:].copy()
        self.front[0,:] = self.right[0,:]
        self.right[0,:] = self.back[0,:]
        self.back[0,:] = self.left[0,:]
        self.left[0,:] = temp
        self.up = np.rot90(self.up)  
    
    def moveUPrime(self):
        temp = self.front[0,:].copy()
        self.front[0,:] = self.left[0,:]
        self.left[0,:] = self.back[0,:]
        self.back[0,:] = self.right[0,:]
        self.right[0,:] = temp
        self.up = np.rot90(self.up,k=3)
    
    def moveF(self):
        self.front =  np.rot90(self.front,k=3)
        temp = self.up[2,:].copy()
        self.up[2,:] = np.flip(self.left[:,2])
        self.left[:,2] = self.down[0,:]
        self.down[0,:] = np.flip(self.right[:,0])
        self.right[:,0] = temp
    
    def moveFPrime(self):
        self.front =  np.rot90(self.front)
        temp = self.up[2,:].copy()
        self.up[2,:] = np.flip(self.right[:,0])
        self.right[:,0] = self.down[0,:]
        self.down[0,:] = np.flip(self.left[:,2])
        self.left[:,2] = temp
    
    def moveB(self):
        self.back = np.rot90(self.back,k=3)
        temp = self.up[0, :].copy()
        self.up[0, :] = np.flip(self.right[:, 2])
        self.right[:, 2] = self.down[2, :]
        self.down[2, :] = np.flip(self.left[:, 0])
        self.left[:, 0] = temp
    
    def moveBPrime(self):
        self.back = np.rot90(self.back)
        temp = self.up[0, :].copy()
        self.up[0, :] = np.flip(self.left[:, 0])
        self.left[:, 0] = self.down[2, :]
        self.down[2, :] = np.flip(self.right[:, 2])
        self.right[:, 2] = temp

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
            row_ok = np.array_equal(kostka.down[1, :], [6, 6, 6])
            col_ok = np.array_equal(kostka.down[:, 1], [6, 6, 6])
            f_ok = kostka.front[2,1] == 1
            b_ok = kostka.back[2,1] == 3
            r_ok = kostka.right[2,1] == 2
            l_ok = kostka.left[2,1] == 4
            return row_ok and col_ok and f_ok and b_ok and r_ok and l_ok

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
                if key not in dic:
                    dic[key] = path.copy()
                
                result = dfs_build_dic(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
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
                        return 1
                
                result = dfs_search(cube_copy,max_depth,depth+1,move,path)
                if result:
                    return result
                path.pop()
                getattr(cube_copy,method_undo)()
            return None
                
        max_limit = 5
        path = []
        dic = {}
        kopia = self.copy()
        
        wynik = dfs_build_dic(kopia, max_depth=max_limit, depth=1, last_move=None, path=path)     
        
        for current_max_depth in range(4, max_limit+1):
            
            path = []
            find = cube()
            solution = dfs_search(find, max_depth=current_max_depth, depth=1, last_move=None, path=path)   
            if solution is not None:
                return solution
        return "Nie znaleziono rozwiązania w zadanym limicie głębokości."
       
    def solve_to_2l(self):
        pass


    def solve_top_layer(self):
        pass

    def movetopos(self,ruchy):
        for ruch in ruchy:
            ruch()
        
    def print(self):
        print("front:")
        print(self.front)
        print("==========================")
        print("back:")
        print(self.back)
        print("==========================")
        print("right:")
        print(self.right)
        print("==========================")
        print("left:")
        print(self.left)
        print("==========================")
        print("up:")
        print(self.up)
        print("==========================")
        print("down:")
        print(self.down)
            
    def __eq__(self, other):
        if not isinstance(other, cube):
            return False
        return (np.array_equal(self.front, other.front) and
                np.array_equal(self.back, other.back) and
                np.array_equal(self.right, other.right) and
                np.array_equal(self.left, other.left) and
                np.array_equal(self.up, other.up) and
                np.array_equal(self.down, other.down))
        
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
        copy = cube()
        copy.front = self.front.copy()
        copy.up = self.up.copy()
        copy.right = self.right.copy()
        copy.left = self.left.copy()
        copy.down = self.down.copy()
        copy.back = self.back.copy()
        return copy 

x = cube()
x.scramble()
#import tracemalloc
#tracemalloc.start()
timer = time.time()
z = x.solve_to_cross()
print(z)
print(time.time()-timer)


#current, peak = tracemalloc.get_traced_memory()
#print(f"Aktualne zużycie: {current / 10**6:.2f} MB")
#print(f"Najwyższe zużycie (Peak): {peak / 10**6:.2f} MB")
#tracemalloc.stop()
