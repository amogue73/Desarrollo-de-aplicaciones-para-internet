max = 100

primo = [True for i in range(max+1)]

p = 2
while (p*p <= max):

    if (primo[p] == True):
        for i in range(p * p, max+1, p):
            primo[i] = False
    
    p += 1

numeros = []
for p in range(2, max+1):
    if primo[p]:
        numeros.append(p)

print(numeros)