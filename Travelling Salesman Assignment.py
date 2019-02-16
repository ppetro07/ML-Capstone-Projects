#Pavlina Petrova
import pandas as pd
import numpy as np
import pytest
import math
import random

def read_cities(file_name):
    """
    Read in the cities from the given `file_name`, and return 
    them as a list of four-tuples: 

      [(state, city, latitude, longitude), ...] 
    """

    pd.options.display.float_format = '{:,.2f}'.format
    df = pd.read_csv('city-data.txt', sep="\t", header=None)
    city_data=[]
    for index, row in df.iterrows():
        city_data.append(tuple(row))
    return city_data
    
def print_cities(road_map):
    """
    Prints a list of cities, along with their locations. 
    Print only one or two digits after the decimal point.
    """
    print("first version of roadmap")
    for i,city in enumerate(road_map):
        print(road_map[i][1],round(road_map[i][2],2),round(road_map[i][3],2))

def compute_total_distance(road_map):
    """
    Returns, as a floating point number, the sum of the distances of all 
    the connections in the `road_map`. Remember that it's a cycle, so that 
    (for example) in the initial `road_map`, Wyoming connects to Alabama...
    

    Arguments:
    road_map -- list of 4-tuples

    Return:
    z -- a float, identifying csum of the distances of all the connections in the `road_map`
    """
    
    total_distance=[]
    for i in range(1,len(road_map)):
       total_distance.append(math.sqrt((road_map[i][2]-road_map[i-1][2])**2+(road_map[i][3]-road_map[i-1][3])**2))
    total_distance.append(math.sqrt((road_map[len(road_map)-1][2]-road_map[0][2])**2+(road_map[len(road_map)-1][3]-road_map[0][3])**2))
    
    return sum(total_distance)

def swap_adjacent_cities(road_map, index):
    """
    Take the city at location `index` in the `road_map`, and the city at 
    location `index+1` (or at `0`, if `index` refers to the last element 
    in the list), swap their positions in the `road_map`, compute the 
    new total distance, and return the tuple 

    Arguments:
    road_map -- list of 4-tuples
    index -- city location in the `road_map`

    Return:
    (new_road_map, new_total_distance) - a tuple of changed road_map and calculated total
                                         distanse
    """
    road_map[index],road_map[(index + 1) % len(road_map)]=road_map[(index + 1) % len(road_map)],road_map[index]    
    new_total_distance=compute_total_distance(road_map)
    return (road_map,new_total_distance)

def swap_cities(road_map, index1, index2):
    """
    Take the city at location `index1` and `index2` in the `road_map`,
    swap their positions in the `road_map`, 
    computes the new total distance, and return the tuple 

    Arguments:
    road_map -- list of 4-tuples
    index1, index2 -- city locations in the `road_map`

    Return:
    (new_road_map, new_total_distance) - a tuple of changed road_map and calculated total
                                         distanse
    """
    if index1==index2:
        pass
    else:
        road_map[index1], road_map[index2] = road_map[index2], road_map[index1]
    
    new_total_distance=compute_total_distance(road_map)
    
    return (road_map,new_total_distance)

def find_best_cycle(road_map):

    """
    Using a combination of `swap_cities` and `swap_adjacent_cities`, 
    makes `10000` swaps.
    After `10000` swaps, returns the best cycle found so far.

    Arguments:
    road_map -- list of 4-tuples

    Return:
    road_map - modified road_map so that distanse is minimal
    
    """
    
    swap=10000
    for i in range(len(road_map)):
        distance_min=math.sqrt((road_map[i][2]-road_map[(i + 1) % len(road_map)][2])**2+(road_map[i][3]-road_map[(i + 1) % len(road_map)][3])**2)
        for j in range(i+1,len(road_map)):
            total_distance=math.sqrt((road_map[i][2]-road_map[j][2])**2+(road_map[i][3]-road_map[j][3])**2)
            if total_distance<distance_min:
                m=j
                distance_min=total_distance
                swap_cities(road_map, i+1, m)
                swap=swap-1
    
    t=compute_total_distance(road_map)
    random.seed(0)
    while swap>0:
        random_state=0
        a,b,c=random.sample(range(len(road_map)), 3)
        r_rand,t_rand=swap_cities(road_map, a, b)
        if t_rand>t:
            r,t=swap_cities(road_map, b, a)
        swap=swap-1
        r_rand_c,t_rand_c=swap_adjacent_cities(road_map, c)
        if t_rand_c>min(t,t_rand):
            r,t=swap_adjacent_cities(road_map, c)
        swap=swap-1
    
    total=min(t,t_rand, t_rand_c)
    if total==t:
        return r
    elif total==t_rand_c:
        return r_rand_c
    else:
        return r_rand

def print_map(road_map):
    """
    Prints the cities and their connections, along with the cost
    for each connection and the total cost.

    Arguments:
    road_map -- list of 4-tuples
    """

    print("Most efficient route found")
    
    df=pd.DataFrame(road_map)
    df.columns=["State", "City", "d1", "d2"]
    df["Connection"]=df["City"].copy()
    df["dd1"]=df["d1"].copy()
    df["dd2"]=df["d2"].copy()

    df["Connection"] = df["Connection"].shift(-1)
    df["dd1"]=df["d1"].copy().shift(-1)
    df["dd2"]=df["d2"].copy().shift(-1)

    df.iloc[-1,4]=df.iloc[0,1]
    df.iloc[-1,5]=df.iloc[0,2]
    df.iloc[-1,6]=df.iloc[0,3]

    df["Distance"]=np.sqrt((df.iloc[:,2]-df.iloc[:,5])**2+(df.iloc[:,3]-df.iloc[:,6])**2)
    df.drop(['State', 'd1', 'd2', 'dd1', 'dd2'], axis=1, inplace=True)
    df.index.name = 'No.'
    total_dist=compute_total_distance(road_map)
    print (df,"Total distance = "+ str(round(total_dist,2))+ str(" miles"), sep="\n")


def main():
    """
    Reads in, and prints out, the city data, then creates the "best"
    cycle and prints it out.
    """
    road_map=read_cities('city-data.txt')
    print_cities(road_map)
    best_cycle=find_best_cycle(road_map)
    print_map(best_cycle)


if __name__ == "__main__":
    main()
