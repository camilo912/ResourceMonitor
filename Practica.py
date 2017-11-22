import os
import datetime
import time
import commands

def getShmSem(shmsem):
    com = commands.getoutput("ipcs -%s" % shmsem)

    lineas = com.split("\n")[3:-1]
    shmsemids = []
    for w in lineas:
        palabras = w.split(" ")
        if int(palabras[1]) != 0 :
            shmsemids.append(int(palabras[1]))
    #print shmsemids
    shmsem = {}
    for shmsemid in shmsemids:
        comGrep = commands.getoutput("grep %d /proc/*/maps" % shmsemid)
        lineaGrep = comGrep.split("\n")

        for proc in lineaGrep:
            #print proc.split("/")[2]
            process = int(proc.split("/")[2])
            if process in shmsem:
                shmsem[process] += 1
            else:
                shmsem[process] = 1
    return shmsem

def getShmSemByProcess(shmsem, pid):
    numShmSem = 0
    if pid in shmsem:
        numShmSem = shmsem[pid]
    return numShmSem

if __name__ == '__main__':
    arch = open("salidaLog.txt","a")
    arch.write("----------------------------------------------------------------------\n")
    encabezado = "HORA|PID|NOMBRE|STATE|%CPU|MEM FISICA|MEM VIRTUAL|#OP.LECTURA|#OP.ESCRITURA|BYTES LETURA|BYTES ESCRITURA|#SEMAFOROS|#MEM COMPARTIDA|#HILOS\n"
    arch.write(encabezado)

    while True:
        #print "CICLO"
        timeIni = time.time()
        proc = os.listdir('/proc')
        pids = [int(s) for s in proc if s.isdigit()]
        numShmDict = getShmSem("m")
        numSemDict = getShmSem("s")
        for pid in pids:
            hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #HORA

            stat = "/proc/%d/stat" % pid
            fileStat = open(stat, 'r')
            lineaStat = fileStat.readline().split(' ')
            name = lineaStat[1] #NAME
            name = name[1:-1]
            state = lineaStat[2] #STATE
            memFisica = lineaStat[22] #MEMORIA FISICA
            memVirtual = lineaStat[23] #MEMORIA VIRTUAL
            # %CPU
            startTime = float(lineaStat[21])
            cpuUser = float(lineaStat[13])
            cpuSys = float(lineaStat[14])
            cpuTotal = cpuUser + cpuSys
            fileUpTime = open("/proc/uptime", 'r')
            lineaUpTime = fileUpTime.readline().split(' ')
            upTime = float(lineaUpTime[0])
            secounds = upTime - (startTime / 100)
            cpuUsage = 100 * ((cpuTotal / 100) / secounds) #%CPU
            fileStat.close()

            task = os.listdir("/proc/%d/task" % pid)
            threads = len(task)

            io = "/proc/%d/io" % pid
            fileIO = open(io, 'r')
            lineaIO = fileIO.read().split('\n')
            readOpDisk = lineaIO[2].split(': ')[1] #OPERACIONES LECTURA
            writeOpDisk = lineaIO[3].split(': ')[1] #OPERACIONES ESCRITURA
            readBytes = lineaIO[0].split(': ')[1] #BYTES LECTURA
            writeBytes = lineaIO[1].split(': ')[1] #BYTES ESCRITURA
            #numShm = 0
            #numShmDict = getShmSem("m")
            numShm = getShmSemByProcess(numShmDict, pid)
            #numSem = 0
            #numSemDict = getShmSem("s")
            numSem = getShmSemByProcess(numSemDict, pid)

            proceso = "%s | %d | %s | %s | %f | %s | %s | %s | %s | %s | %s | %d | %d | %d \n" \
                      % (hora, pid, name, state, cpuUsage, memFisica, memVirtual, readOpDisk, writeOpDisk, readBytes, writeBytes,numSem, numShm, threads)
            arch.write(proceso)
        timeFin = time.time() - timeIni
        print timeFin
        while timeFin < 1.0:
            timeFin = time.time() - timeIni
        print timeFin
        
