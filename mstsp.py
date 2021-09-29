from builtins import object
import numpy as np
import math

dist=np.array([])
MaxFES=np.array([])
FES=0
object_input=0
MaxFES = np.append(MaxFES,[60000,60000,60000,60000,60000,60000,60000,60000,60000,60000,60000,60000,
        1200000,1200000,1200000,1200000,1200000,1200000,1200000 , 
        1200000, 1200000, 1200000, 1200000, 1200000, 1200000])

class cardinate:
    def __init__(self,a=0,b=0):
        self.x=a
        self.y=b
class City(object):
    city_vec=np.array([])
    random=np.array([])
    onpath=np.array([])
    fitness=0
    path_length=0
    d=cardinate()
    def distance(self, a, b):
        return round(math.sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y - b.y)))
    def __init__(self, input_data):
        global object_input
        object_input=input_data
        self.random=np.array([])
        mstsp_ds=["simple1_9", "simple2_10", "simple3_10", "simple4_11", "simple5_12", "simple6_12",
        "geometry1_10", "geometry2_12", "geometry3_10", "geometry4_10", "geometry5_10", "geometry6_15",
        "composite1_28", "composite2_34", "composite3_22", "composite4_33", "composite5_35", "composite6_39",	
        "composite7_42", "composite8_45", "composite9_48",  "composite10_55", "composite11_59","composite12_60", "composite13_66"]

        filename = "benchmark_MSTSP/" + str(mstsp_ds[input_data]) + ".tsp"
        file_ = open(filename,"r")

        
        # Reading from the file
        content = file_.readlines()
 

        # Iterating through the content
        # Of the file
        for line in content:
            x, y = list(map(int, line.split()))
            self.city_vec=np.append(self.city_vec,cardinate(x, y))

        file_.close()
        city_num=len(self.city_vec)
        self.city_num = city_num
        global dist
        
        filename2 = "benchmark_MSTSP/" + str(mstsp_ds[input_data]) + ".solution"
        file_2 = open(filename2,"r")
        
        content =file_2.readlines()
        
        global minf
        minf=0
        global sol
        sol=[]
        for line in content:
            sol1=list(map(int,line.split()))
            sol1.pop()
            minf=sol1.pop(0)
            sol.append(sol1)
        
        dist = np.empty((city_num, city_num), dtype=float)

        for i in range(city_num):
            for j in range(city_num):
                dist[i][j] = self.distance(self.city_vec[i],self.city_vec[j])

    def tot_dist(self, new_vec):
        global MaxFES, object_input, FES, dist
        if FES >= MaxFES[object_input]:
                return
        new_city_vec=np.array([])
        self.path_length=0
        self.fitness=0
        for i in range(self.city_num-1):
            self.path_length+=dist[int(new_vec[i][1])][int(new_vec[i+1][1])]

        self.path_length+=dist[int(new_vec[self.city_num-1][1])][int(new_vec[0][1])]
        self.fitness=self.path_length
        FES+=1
    def _get_maxfes(self,ml):
        object_input = ml
        return MaxFES[object_input]
    def _evaluate(self,arr):
        arr1=np.array([])
#         arr1=np.append(arr1,0)
        arr1=np.append(arr1,arr)
        tempRandom=Chromosome(arr)
        self.random = tempRandom.path
        self.onpath = tempRandom.op
        self.tot_dist(self.random)
#         if self.fitness%1.000>=0.5:
#             self.fitness+=1-(self.fitness%1.000)
#         else:
#             self.fitness-=self.fitness%1.000
#         self.fitness=int(self.fitness)
        return self.fitness, self.onpath
    def _for_sol(self):
        return sol
    def _min_fit(self):
        return minf

class Chromosome:
    def __init__(self,arr):
        __num=len(arr)
        path=np.empty((__num,2),dtype=float)
        for i in range(__num):
            path[i][0] = arr[i]
            path[i][1] = i

        ss=path[0][0]
        columnIndex=0
        path=path[path[:,columnIndex].argsort()]
        op = np.empty(__num)
        for i in range(__num):
            op[i] = path[i][1]
        self.path = path
        self.op = op
#         path1=np.empty((__num,2),dtype=float)
#         path1[0][0]=ss
#         path1[0][1]=0
#         j=1
#         for i in range(__num):
#             if(path[i][1]==0):
#                 continue
#             else:
#                 path1[j][0]=path[i][0]
#                 path1[j][1]=path[i][1]
#                 j+=1


class population:
    def __init__(self):
        self.NP=150
        self.chroms=np.array([])
        self.len_arr=np.array([])
        self.fitness_arr=np.array([])

    def gen_popl(self,city):
        self.chroms = np.empty((self.NP, city.city_num, 2))
        for i in range(self.NP):
            rand_path=Chromosome(np.random.rand(city.city_num))
            self.chroms[i] = rand_path.path

    def evaluate(self,c):
        for i in range(self.NP):
            c.tot_dist(self.chroms[i])
            self.len_arr=np.append(self.len_arr,c.path_length)
        self.fitness_arr=np.append(self.fitness_arr,c.path_length)
