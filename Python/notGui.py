from datetime import  datetime
from algorithm import ACAlgo

a = datetime.now()
algo=ACAlgo();

"""
print ("Trazeni nizovi [C, T, G, A]: \n(nevaljali niz za izlaz)")
inp=input("->")
while(all(p in ['c','t','g','a'] for p in inp.lower())):
    algo.addWord(inp)
    inp=input("->")

algo.printFail()
algo.printTree()
algo.printContent()
"""
print ("Upisite trazene podnizove (\\ za prekid upisa)")
inp=input("->")
while(inp!="\\"):
    algo.addWord(inp);
    inp=input("->")
algo.addFails()

path=input("Putanja do datoteke: ")
try:
    algo.readFile(path)
except:
    print("Citanje nije uspjelo")
    exit()
b = datetime.now()
print(algo.foundWords)
for qw in algo.foundWords:
    print (qw,":" , len(algo.foundWords[qw]), "occurrences found")
print ((b-a).seconds, "seconds", (b-a).microseconds/1000, "miliseconds");