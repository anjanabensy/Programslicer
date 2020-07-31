def myfunc(z):
    print(z)
def main():
    a = 3
    b = 4
    x = 5
    y = 9
    c = a + b
    z = x + y
    myfunc(z)
    if(x > z):
        z = z - 2
        myfunc(z)
    else:
        a += 2