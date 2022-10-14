import matplotlib.image as img
import matplotlib.pyplot as plt
import random
import numpy as np
from matplotlib.patches import Rectangle
from numpy.lib.function_base import average

#Intialization of Population
def Population(row,column, size):
    population = []
    for i in range(size):
        population.append((random.randint(0, row-29), random.randint(0, column-35)))
    return population
#Correlation Cofficient
def correlation_cofficient(A, B):
    return(np.mean(((A-A.mean())) * (B-B.mean())) /(A.std() * B.std()))


def fitness(image1, image2,pop):
    Fitness= []
    for i in pop:
        x = i[0]
        y = i[1]
        image3 = np.array([image1[y:y+35, x:x+29]])
        correlation= correlation_cofficient(image2, image3)
        Fitness.append(correlation)
    return Fitness

def selection(fitness,pop):
    rankedpopulation = []
    check = zip(fitness,pop)
    sort_check = sorted(check,reverse=True)
    for i in sort_check:
        rankedpopulation.append(i[1])
    return rankedpopulation

def crossover(rankedpopulation):
    for i in range(1,len(rankedpopulation)-1,2):
        coordinate1= rankedpopulation[i]
        coordinate2= rankedpopulation[i+1]
        x1coordinate=np.binary_repr(coordinate1[0],10)
        y1coordiate= np.binary_repr(coordinate1[1], 10)
        strngx= str(x1coordinate) 
        strngy=str(y1coordiate)
        x2coordinate= np.binary_repr(coordinate2[0], 10)
        y2coordinate= np.binary_repr(coordinate2[1],10)
        strngx2= str(x2coordinate)
        strngy2= str(y2coordinate)
        coordinate1= list(strngx+strngy)
        coordinate2=list(strngx2+strngy2)
        k = random.randint(0, 19)
        for j in range(k, len(coordinate1)):
            coordinate1[j], coordinate2[j] = coordinate2[j], coordinate1[j]
        coordinate1 = ''.join(coordinate1)
        coordinate2 = ''.join(coordinate2)
        rankedpopulation[i]= (int(coordinate1[0:10],2),int(coordinate1[10:],2))
        rankedpopulation[i+1]= (int(coordinate2[0:10],2),int(coordinate2[10:],2))
    return rankedpopulation

def mutation(crossover):
    nextgen= [] 
    for i in crossover:
        current = i
        while current[0] > 995:
            a= np.binary_repr(i[0],10)
            a1=str(a)
            a2=list(a1)
            k = random.randint(0,9) 
            if a2[k]=='0':
                a2[k]='1' 
            else:
                a2[k]='0'
            a2 =''.join(a2)
            a2 = int(a2,2) 
            current= (a2,current[1])
        while current[1] > 477:
            b =np.binary_repr(i[1],10)
            b1=str(b)
            b2=list(b1)
            k = random.randint(0,9)
            if b2[k]=='0':
                b2[k]='1'
            else:
                b2[k]='0'
            b2 =''.join(b2)
            b2 = int(b2,2)
            current= (current[0],b2)
        nextgen.append(current)
    return nextgen
# def terminat(Fitness,population):
#     list1 = []
#     for i in range(len(Fitness)):
#         if Fitness[i]>0.9:
#             list1.append()

image1 = np.array(img.imread("groupGray.jpg"))
image2 = np.array(img.imread("boothiGray.jpg"))
pop = Population(1024,512,100)
fit_pop = []
max_fit = []
avg_fit = []
for i in range(1000):
    fittest= fitness(image1, image2,pop)
    max_fit.append(max(fittest))
    avg_fit.append(average(fittest))
    select= selection(fittest,pop)
    if max(fittest)>0.8:
        fit_pop.append(select[0])
        break
    cross= crossover(select)
    pop= mutation(cross)
plt.imshow(image1)
plt.gray()
ax = plt.gca()
for i in fit_pop:
    rect = Rectangle(i, 29, 35, linewidth =1 ,edgecolor='r',facecolor='none')
    ax.add_patch(rect)
plt.show()
plt.figure(1)
plt.plot(max_fit,'r')
plt.plot(avg_fit,'b')
plt.show()