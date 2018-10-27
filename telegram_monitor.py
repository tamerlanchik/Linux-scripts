import subprocess
import time
import os
def makeMessage(token, chat_id, text):
        text = text.replace(" ", "%20")
        return "curl -s -X POST https://api.telegram.org/bot" + token + "/sendMessage -d chat_id=" + chat_id + " -d text=\"" + text + "\" > /dev/null"
def getHostName(base, numb):
        p=str(numb)
        if numb<10: p = "0"+p
        return base+p
hostNumb=13
state0=[0]*hostNumb
httpState=[0]*hostNumb
WPState=[0]*hostNumb
TOKEN="792286212:AAHmjj2-NiVx02lwQ-uMDcCMFkTnNwvY6es"
ADMIN_ID="423430281"
CHK_TIMEOUT=1
NETWORK="192.168.142.1"
i=0
os.system(makeMessage(TOKEN, ADMIN_ID, "Monitoring Bot on 192.168.142.100 is turned on. Hello!"))
#os.system("curl http://192.168.142.101")
while True:
        for n in range(hostNumb):
                hostName=getHostName(NETWORK, n)
                #t=os.system("ping "+hostName + " -c 1 -w 0.1")
                t = os.system("fping -t 200 -Q 60 " +hostName + " > /dev/null")
                if t!=state0[n]:
                        mess = ": Host " + hostName + " unavailable by ping"
                        if t==0 and state0[n]!=0:
                                mess="OK"+mess
                        elif t!=0 and state0[n]==0:
                                mess="PROBLEM"+mess
                        comm=makeMessage(TOKEN, ADMIN_ID, mess)
                        os.system(comm)
                        state0[n]=t

                comm="curl -s -m 1 http://"+hostName
                pr = subprocess.Popen(comm.split(), stdout=subprocess.PIPE)
                out, e = pr.communicate()
                flag=len(out)<1
                if flag!=httpState[n]:
                        mess = ": HTTP connection to " + hostName
                        if flag:
                                mess="PROBLEM"+mess
                        else:
                                mess="OK" + mess
                        os.system(makeMessage(TOKEN, ADMIN_ID, mess))
                        httpState[n]=flag
                flag=not ("wp" in out)
                if flag!=WPState[n]:
                        mess = ": WP site available on " + hostName
                if flag!=WPState[n]:
                        mess = ": WP site available on " + hostName
                        if not flag:
                                mess="OK"+mess
                        else:
                                mess="PROBLEM"+mess
                        os.system(makeMessage(TOKEN, ADMIN_ID, mess))
                        WPState[n]=flag

        time.sleep(CHK_TIMEOUT)

