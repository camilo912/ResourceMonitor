from time import sleep
import psutil
import datetime
import time
if __name__ == '__main__':

    arch = open("salidaLog.txt","a")
    arch.write("\n-----------------------------------------------------------------------------------------------\n")
    arch.write("Hora | PID | Nombre | CPU total | CPU User | CPU System | Memoria Fisica | Memoria Virtual | # Operaciones lectura en disco | # Operaciones escritura en disco\n")

    while True:
        timeIni = time.time()
        for p in psutil.process_iter():
            hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pid = p.pid
            name = p.name()
            # pCPU = p.cpu_percent() / psutil.cpu_count()
            pCPU = p.cpu_times().user + p.cpu_times().system
            cpu = p.cpu_times()
            cpuUser = cpu.user
            cpuSys = cpu.system


            memoria = p.memory_info()
            memFisica = memoria.wset
            memVirutal = memoria.vms

            disco = p.io_counters()
            numOpsLect = disco.read_count
            numOpsEscr = disco.write_count

            linea = "%s | %d | %s | %d | %d | %d | %d | %d | %d | %d \n" % (hora ,pid,name,pCPU, cpuUser, cpuSys,memFisica,memVirutal,numOpsLect,numOpsEscr)
            arch.write(linea)
        timeFin = time.time() - timeIni
        while timeFin < 1.0:
            timeFin = time.time() - timeIni