import random
import math
import sys

# Problem Parameter.
global N_C  #number of customers
global N_V  #number of vehicles
global V_C  #vehicle capacity
N_C = 30
N_V = 10
V_C = 50

#Depot Coordinate.
global D_X
global D_Y
D_X = 50
D_Y = 50


def vehical(v,V_C):
  global V
  D = {
      "vid":v,
       "cap":V_C,
       "load":0,
       "curloc":0,
       "closed":0,
  }
  dcopy = D.copy()
  V.append(dcopy)

def add_customer_to_vehical():
  pass
def check_if_fits(Vid,val):
  if V[Vid]["load"]+val<=V_C: 
    return True
  else:
    return False

# function of UCE

def UCE():
  for i in range(1,N_C+1):
    #print(Node[i]["IR"])
    if Node[i]["IR"]==False: 
      return True
  return False

# defination of greedy solution.

def greedy_sol():
  global Cost
  global MinCost
  global Candcost
  Vid = 0  #vehical index
  Candidate = -1
  Cost = 0
  EndCost = 0
  CustIndex = 0
  while(UCE()):
    #print("in while",' ',Vid)
    F = 0       
    CI = 0      # current index
    Candidate = -1
    MinCost = 100000000000
    if(len(VR[Vid]) == 0):   #if length of any route is 0, vehicle will start from depot
      V[Vid]["load"] += Node[0]["demand"]
      V[Vid]["curloc"] = Node[0]["id"]
      VR[Vid].append(Node[0]["id"])
      VR1[Vid].append(Node[0]["id"])
    #print(VR[Vid])
     
    for i in range(1,N_C+1):
      #print('i : ', i)
      if(Node[i]["IR"] == False):
        if(check_if_fits(Vid,Node[i]["demand"])):
          CandCost = dist[V[Vid]["curloc"]][i] 
          #print('Vid Curloc is : ',V[Vid]["curloc"],' i : ', i, ' CandCost is ', CandCost)
          if(MinCost  > CandCost):
            MinCost = CandCost
            CustIndex = i
            Candidate = i
    
    if Candidate == -1:  #not able to satisfy any vehicle
      #print("-1")
      if Vid+1<N_V:   #not the last vehicle
        if V[Vid]["curloc"] != 0:       #if wherever it is present, bring it back to depo, as it won't satisfy any more customers
          EndCost=dist[V[Vid]["curloc"]][0]
          VR[Vid].append(Node[0]["id"])
          VR1[Vid].append(Node[0]["id"])
          V[Vid]["load"] += Node[0]["demand"]
          V[Vid]["curloc"] = Node[0]["id"]
          Cost+=EndCost
        Vid=Vid+1
      else:           #all vehicles exhausted
        #print("vechile id is : ", Vid)
        #print("Something strange happend")
        sys.exit()

    else:       #wherever it went, update the location, and load of the vehicle and update the router-path of the vehicle
      VR[Vid].append(Candidate)
      VR1[Vid].append(Candidate)
      V[Vid]["load"] += Node[Candidate]["demand"]
      V[Vid]["curloc"] = Node[Candidate]["id"]
      Node[Candidate]["IR"] = True
      #Cost = Cost+MinCost
    
  EndCost = dist[V[Vid]["curloc"]][0]  #finally all vehicles go back to depo
  VR[Vid].append(0)
  VR1[Vid].append(0)
  Cost = Cost+EndCost   #final cost after all cars go back to depo
  #print("IN GREEDY", Cost)
  # print(VR)



def IntraLocalSearch():
  global rt
  global MovingNodeDemand
  global VehIndexFrom
  global VehIndexTo
  global BestNCost
  global NeightboorCost
  global Cost
  global Ans 
  rt = []
  Ans=Cost
  swapIndexA=-1
  swapIndexB=-1
  swapRoute=-1

  MaxIteration=50
  iteration_number=0
  Termination=False
  while(Termination == False):
    iteration_number+=1
    BestNCost=10000
    for VehIndex in range(0,N_V):
      RouteLength = len(VR1[VehIndex])
      for i in range(1,RouteLength-1):
        for j in range(0,RouteLength-1):
          if((j!=i) and (j!=i-1)):
            a=VehIndex
            MCst1 = dist[VR1[a][i-1]][VR1[a][i]]
            MCst2 = dist[VR1[a][i]][VR1[a][i+1]]
            MCst3 = dist[VR1[a][j]][VR1[a][j+1]]
            ACst1 = dist[VR1[a][i-1]][VR1[a][i+1]]
            ACst2 = dist[VR1[a][j]][VR1[a][i]]
            ACst3 = dist[VR1[a][i]][VR1[a][j+1]]

            M = (MCst1+MCst2+MCst3)
            S = (ACst1+ACst2+ACst3)

            NeightboorCost=S-M
            if(NeightboorCost<BestNCost):
              BestNCost=NeightboorCost
              swapIndexA=i
              swapIndexB=j
              swapRoute=VehIndex
    #print("in intra ",swapIndexA,' ',swapIndexB, swapRoute)
    if(BestNCost<0):
      rt.clear()
      rt=VR1[swapRoute].copy()
      #print(rt)
      swapNode = rt[swapIndexA]
      del rt[swapIndexA]
      if(swapIndexA<swapIndexB):
        rt.insert(swapIndexB,swapNode)
      else:
        rt.insert(swapIndexB+1,swapNode)
      Ans +=BestNCost
      VR1[swapRoute] = rt.copy()
    else:
      Termination=True
    if(iteration_number == MaxIteration):
      Termination = True
      


def InterLocalSearch():
  global ans
  global RouteFrom
  global RouteTo
  global MovingNodeDemand
  global VehIndexFrom
  global VehIndexTo
  global BestNCost
  global NeightboorCost
  global Cost
  ans = 0
  RouteFrom = []
  RouteTo = []
  swapIndexA=-1
  swapIndexB=-1
  swapRouteFrom=-1
  swapRouteTo=-1

  MaxIteration = 50
  iteration_number = 0
  #for i in range(N_V+1):
    #print(i,' ',len(VR[i]))
  Termination =False
  while(Termination==False):
    iteration_number+=1
    BestNCost = 100000
    for VehIndexFrom in range(0,N_V):
      #RouteFrom = VR[VehIndexFrom][:]
      RouteFromLength = len(VR[VehIndexFrom])
      for i in range(1,RouteFromLength-1):
        for VehIndexTo in range(0,N_V):
          #RouteTo = VR[VehIndexTo][:]
          RouteToLength = len(VR[VehIndexTo])
          for j in range(0,RouteToLength-1):
            a=VehIndexFrom
            b=VehIndexTo
            Node_idx = VR[a][i]
            MovingNodeDemand=Node[Node_idx]["demand"]
            if((VehIndexFrom==VehIndexTo) or check_if_fits(VehIndexTo,MovingNodeDemand)):
              if(( (VehIndexFrom == VehIndexTo) and ((j==i)or(j==i-1))) == False):
                MinusCst1 = dist[VR[a][i-1]][VR[a][i]]
                MinusCst2 = dist[VR[a][i]][VR[a][i+1]]
                MinusCst3 = dist[VR[b][j]][VR[b][j+1]]
                AddCst1 = dist[VR[a][i-1]][VR[a][i+1]]
                AddCst2 = dist[VR[b][j]][VR[a][i]]
                AddCst3 = dist[VR[a][i]][VR[b][j+1]]
                S = AddCst1+AddCst2+AddCst3;
                M = MinusCst1+MinusCst2+MinusCst3
                #print(S,' ',M)
                NeightboorCost = (S)-(M)

                if(NeightboorCost<BestNCost):
                  #print(swapIndexA,' inf cond ',swapIndexB)
                  BestNCost = NeightboorCost
                  swapIndexA = i
                  swapIndexB = j
                  swapRouteFrom = VehIndexFrom
                  swapRouteTo = VehIndexTo
    
    #print("out of loop ", swapIndexA,' ',swapIndexB,' ', swapRouteFrom,' ',swapRouteTo)
      
    if(BestNCost<0):
      #print("in bestncost")
      RouteFrom.clear()
      RouteFrom = VR[swapRouteFrom].copy()
      #print(swapRouteFrom,' printing swap idx ',swapRouteTo)
      #print(swapIndexA,'print idx ',swapIndexB)
      RouteTo.clear()
      RouteTo = VR[swapRouteTo].copy()
      #print(VR[swapRouteFrom],' printing VR ',VR[swapRouteTo])
      VR[swapRouteFrom].clear()
      VR[swapRouteTo].clear()
      #print("in index ", swapIndexA,' ',RouteFrom)
      swapNode = RouteFrom[swapIndexA]
      #print(RouteFrom)
      del RouteFrom[swapIndexA]
      #print(RouteFrom)
      if(swapRouteFrom == swapRouteTo):
        del RouteTo[swapIndexA]
        #print("in equal")
        if(swapIndexA<swapIndexB):
          RouteTo.insert(swapIndexB,swapNode)
          #print(RouteTo)
        else:
          RouteTo.insert(swapIndexB+1,swapNode)
      else:
        RouteTo.insert(swapIndexB+1,swapNode)
      VR[swapRouteFrom] = RouteFrom.copy()
      V[swapRouteFrom]["load"] -= MovingNodeDemand
      VR[swapRouteTo] = RouteTo.copy()
      V[swapRouteTo]["load"] += MovingNodeDemand
      #ans=Cost+BestNCost
      RouteFrom.clear()
      RouteTo.clear()
    else:
      #print(iteration_number,' ',"end")
      Termination = True
    if iteration_number == MaxIteration:
      Termination = True
  #print("INTER",' ',ans)

      


def Calculate():
  Res = 0
  for i in range(N_V+1):
    if(len(VR[i])):
      for j in range(1,len(VR[i])):
        Res += dist[VR[i][j-1]][VR[i][j]]
  return Res
            
def Calculate1():
  Res = 0
  for i in range(N_V+1):
    if(len(VR1[i])):
      for j in range(1,len(VR1[i])):
        Res += dist[VR1[i][j-1]][VR1[i][j]]
  return Res

def Printans(s, x):
  print('\n=================================================================================')
  print('=================================================================================')
  print("\nUsing ",s, " Approach \n")

  for i in range(0,N_V):
    if(len(VR[i]) != 0):
      print("Nodes Traveled by vechile ",i, " are " , VR[i])
      
  print("\n")

  print("Total Distance travelled by all the Vechiles is ",  x, " metres")
  print('===================================================================================')
  print('===================================================================================\n')

def Printans1(s, x):
  print('\n=================================================================================')
  print('=================================================================================')
  print("\nUsing ",s, " Approach \n")

  for i in range(0,N_V):
    if(len(VR1[i]) != 0):
      print("Nodes Traveled by vechile ",i, " are " , VR1[i])
      
  print("\n")

  print("Total Distance travelled by all the Vechiles is ",  x, " metres")
  print('===================================================================================')
  print('===================================================================================\n')





def main():
  global Node     #initialisation of variables
  global dist    
  global V
  global best_V
  global VR        #vehical Route
  global D
  global VR1
  Node = []*(N_C+1)
  w, h = N_C+2, N_C+2;
  dist = [[0 for x in range(w)] for y in range(h)] 
  #dist = [[]for k in range(N_C+1)]
  VR = [[] for k in range(N_C+1)]
  VR1 = [[] for k in range(N_C+1)]
  V = []*(N_V+1)
  # Process of creating Node 
  D = {
      "id": 0,
      "x": D_X,
      "y": D_Y,
      "ID": True,
      "IR": False,
      "demand": 0
  }
  dcopy = D.copy()
  Node.append(dcopy)
  #cnt = 50
  #print(Node[0])  
  for i in range(1,N_C+1):
    x = int(random.random()*100)
    y = int(random.random()*100)
    demand = int(4+random.random()*7)
    # x = cnt+1
    # y = cnt-1
    # demand = 5
    # cnt+=1
    D = {}
    D = {
         "id": i,
        "x": x,
        "y": y,
        "ID": False,   
        "IR": False,
        "demand": demand
    }
    dcopy = D.copy()
    Node.append(dcopy)

  #print(Node)
  # end of process of creating Node

  # Calculating the distance matrix.
  for i in range(0,N_C+1):
    for j in range(i+1,N_C+1):
        #print(i,' ',j)
        X = (Node[i]["x"]-Node[j]["x"])
        Y = (Node[i]["y"]-Node[j]["y"])
        D = int(math.sqrt((X*X)+(Y*Y)))
        #print(X,' ',Y,' ',D)
        dist[i][j] = D
        dist[j][i] =D
        #print('Distance between node ',0 ,' and j ', 1 ,' is ' , dist[0][1])
  # end of creation of distance matrix.

  #creation of vehical.
  
  for i in range(N_V):
    vehical(i+1,V_C)
  #print(V)
  #print('Distance between node ',0 ,' and j ', 1 ,' is ' , dist[0][1])

  greedy_sol()
  Printans("greedy ",Calculate())
  #print("in the greedy",VR1)
  # IntraLocalSearch()
  # print("intra ", Calculate())
  # print(VR)
  #print(VR1)
  IntraLocalSearch()
  Printans1("IntraLocal",Calculate1())
  InterLocalSearch()
  Printans("InterLocal Search ",Calculate())
      
  



if _name_ == '_main_':
  main()
