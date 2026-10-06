def multiply(x, y):
    if x < 10 or y < 10: return x * y
    size=max(len(str(x)),len(str(y))); half=size//2; power=10**half
    high_x,low_x=divmod(x,power); high_y,low_y=divmod(y,power)
    return multiply(high_x,high_y)*power*power+(multiply(high_x+low_x,high_y+low_y)-multiply(high_x,high_y)-multiply(low_x,low_y))*power+multiply(low_x,low_y)
print(multiply(int(input()),int(input())))
