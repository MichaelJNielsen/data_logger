filename = input("enter filename enclosed in quotation marks ")

file = open(filename,"w")
line = "Hello world 2 \n"

file.write(line)
file.close()
