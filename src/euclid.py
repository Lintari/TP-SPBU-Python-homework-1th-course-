a = int(input())
b = int(input())

a0, a1 = 1, 0 
b0, b1 = 0, 1
    
while b != 0:
    q = a // b  
    a, b = b, a % b 
    a0, a1 = a1, a0 - q * a1 
    b0, b1 = b1, b0 - q * b1
    
print(a0, b0)