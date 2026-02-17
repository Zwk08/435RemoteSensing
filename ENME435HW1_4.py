print("Please enter values for w, x, y, and z:")
w = int(input("Enter the value for w:"))
x = int(input("Enter the value for x:"))
y = int(input("Enter the value for y:"))
z = int(input("Enter the value for z:"))

def valueswapper(a,b,c,d):
    if a<b and c<d:
        a,c = c, a
        print("w swaps with y")
    elif b<a and d<c:
        b,d = d,b
        print("x swaps with z")
    elif a<b and d<c:
        a,d = d,a
        print("w swaps with z")
    elif b<a and c<d:
        b,c = c,b
        print("x swaps with y")
    return a, b, c, d
w,x,y,z= valueswapper(w,x,y,z)

print(f"w={w},x={x},y={y},z={z}")