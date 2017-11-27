import os
import datetime
import time
import re
 
def getShmIds():
    comShm = "/proc/sysvipc/shm"
    fileShm = open(comShm)
    lineaShm = fileShm.read().split('\n')[1:-1]
    fileShm.close()
 
    shids = []
    for l in lineaShm:
        listaTemp = l.split()
        if int(listaTemp[1]) != 0:
            shids.append(int(listaTemp[1]))
    return shids
 
def getCountShm(shids,pid):
    maps = "/proc/%d/maps" % pid
    fileMaps = open(maps, 'r')
    lineaMaps = fileMaps.read()
    fileMaps.close()
    counter = 0
    for shid in shids:
        line = re.findall(r'%d' % shid, lineaMaps)
        counter += len(line)
    return counter
 
if __name__ == '__main__':
    arch = open("salida.csv","a")
    encabezado = "HORA,PID,NOMBRE,STATE,%CPU,MEMFISICA,MEMVIRTUAL,#OP.LECTURA,#OP.ESCRITURA,BYTESLETURA,BYTESESCRITURA,#SEMAFOROS,#MEMCOMPARTIDA,PRIORIEDAD,NICE,#HILOS\n"
    arch.write(encabezado)
 
    while True:
        timeIni = time.time()
        proc = os.listdir('/proc')
        pids = [int(s) for s in proc if s.isdigit()]
        listShids = getShmIds()
 
        for pid in pids:
            hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #HORA
 
            stat = "/proc/%d/stat" % pid
            fileStat = open(stat, 'r')
            lineaStat = fileStat.readline().split(' ')
            fileStat.close()
            name = lineaStat[1] #NAME
            name = name[1:-1]
            state = lineaStat[2] #STATE
            prioriedad = lineaStat[17]
            nice = lineaStat[18]
            # %CPU
            startTime = float(lineaStat[21])
            cpuUser = float(lineaStat[13])
            cpuSys = float(lineaStat[14])
            cpuTotal = cpuUser + cpuSys
            fileUpTime = open("/proc/uptime", 'r')
            lineaUpTime = fileUpTime.readline().split(' ')
            fileUpTime.close()
            upTime = float(lineaUpTime[0])
            secounds = upTime - (startTime / 100)
            cpuUsage = 100 * ((cpuTotal / 100) / secounds) #%CPU
 
            status = "/proc/%d/status" % pid
            fileStatus = open(status, 'r')
            lineaStatus = fileStatus.readlines()
            memVirtual = "0 kB"
            memFisica = "0 kB"
            if "VmSize:" in lineaStatus[17] and "VmRSS:" in lineaStatus[21]:
                lineaMemV = lineaStatus[17].split('\t')
                lineaMemF = lineaStatus[21].split('\t')
                memVirtual = lineaMemV[1].strip()
                memFisica = lineaMemF[1].strip()
 
            task = os.listdir("/proc/%d/task" % pid)
            threads = len(task)
 
            maps = "/proc/%d/maps" % pid
            fileMaps = open(maps, 'r')
            lineaMaps = fileMaps.read()
            count = lineaMaps.count("%d" % pid)
 
            io = "/proc/%d/io" % pid
            fileIO = open(io, 'r')
            lineaIO = fileIO.read().split('\n')
            fileIO.close()
            readOpDisk = lineaIO[2].split(': ')[1] #OPERACIONES LECTURA
            writeOpDisk = lineaIO[3].split(': ')[1] #OPERACIONES ESCRITURA
            readBytes = lineaIO[0].split(': ')[1] #BYTES LECTURA
            writeBytes = lineaIO[1].split(': ')[1] #BYTES ESCRITURA
 
            numShm = getCountShm(listShids,pid)
 
 
            proceso = "%s, %d, %s, %s, %f, %s, %s, %s, %s, %s, %s, %d ,%d, %s, %s,%d\n" \
                      % (hora, pid, name, state, cpuUsage, memFisica, memVirtual, readOpDisk, writeOpDisk, readBytes, writeBytes,0 , numShm, prioriedad, nice,threads)
            arch.write(proceso)
        timeFin = time.time() - timeIni
        print timeFin
        while timeFin < 1.0:
            timeFin = time.time() - timeIni
        print timeFi
