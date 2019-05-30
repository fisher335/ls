import subprocess
target = 1
up = 0
down = 0
li=[]
while (target < 255):
        ip = "192.168.31." +str(target)
        output = subprocess.getstatusoutput(["ping","-n","1",ip])
        print(output[1])
        if ('超时' in str(output[1])):
                print('Host ' + ip + " is offline or unavailable")
                down+= 1
        else:
                print("Host " + ip + " is online")
                up+= 1
                li.append(ip)
        target = target+1


print("A total of " + str(up+down) + " hosts were scanned.")
print(li)
print(str(up) + " hosts were alive, and " + str(down) + " hosts were unreachable. ")
