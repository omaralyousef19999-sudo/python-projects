import time
print("in order to calculate the area of a circle, enter the length of the radius:")
R=int(input("R:"))
p=3.14
if R > 0:
    S=p*R
    print(S)
elif R == 0:
    print("this is a point (.) ")
else:
    print("sory, ther is no negative radius x")
time.sleep(5)