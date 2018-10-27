import time
import os
def makeMessage(token, chat_id, text):
        text = text.replace(" ", "%20")
        return "curl -s -X POST https://api.telegram.org/bot" + token + "/sendMessage -d chat_id=" + chat_id + " -d text=\"" + text + "\" > /dev/null"
state0=[0]*10
TOKEN=" "
ADMIN_ID=" "
timeout = 1
i=0
os.system(makeMessage(TOKEN, ADMIN_ID, "Monitoring Bot on 192.168.142.100 is turned on. Hello!"))
while i<1:
        i+=1
        for n in range(7):
                #t=os.system("ping 192.168.142.10" + str(n) + " -c 1 -w 0.1")
                t = os.system("fping -t 200 -Q 60 192.168.142.10" + str(n) + " > /dev/null")
                if t!=state0[n]:
                        if t==0 and state0[n]!=0:
                                mess1="OK: Ping HOST 192.168.142.10"+str(n)
                        elif t!=0 and state0[n]==0:
                                mess1="Problem:Ping HOST 192.168.142.10"+str(n)
                        comm=makeMessage(TOKEN, ADMIN_ID, mess1)
                        os.system(comm)
                        state0[n]=t
                t = os.system("curl -s -m 1 http://192.168.142.10"+str(n)+" > /dev/null")
                if t!=0:
                        mess="No HTTP connection to 192.168.142.10"+str(n)
                        os.system(makeMessage(TOKEN, ADMIN_ID, mess))
                print t
