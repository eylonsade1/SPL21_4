import sys
import os
from _Repository import repo


def main(args):
    inputfilename = args[1]#config
    if os.path.isfile(inputfilename):
        lines = []
        with open(inputfilename) as inputfile:
            for line in inputfile:
                if "\n" in line:
                    line = line[:len(line)-1]
                lines.append(line)

        firstLine = lines[0].split(',') #find number of lines for each object
        numOfVaccines = int(firstLine[0])
        numOfSuppliers = int(firstLine[1])
        numOfClinics = int(firstLine[2])
        numOfLogistics = int(firstLine[3])
        vacList = []
        supList = []
        clinicList = []
        logList = []

        start = 1
        end = numOfVaccines+1
        for i in range(start,end):
            vacList.append(lines[i])
        start = end
        end = start + numOfSuppliers
        for i in range(start,end):
            supList.append(lines[i])
        start = end
        end = start + numOfClinics
        for i in range(start, end):
            clinicList.append(lines[i])
        start = end
        end = start + numOfLogistics
        for i in range(start, end):
            logList.append(lines[i])
        repo.create_tables()
        repo.insert(vacList, supList, clinicList, logList)

    else:
        print("file doesn't exist")

    inputfilename = args[2] #orders
    if os.path.isfile(inputfilename):
        lines = []
        with open(inputfilename) as inputfile:
            for line in inputfile:
                if "\n" in line:
                    line = line[:len(line) - 1]
                lines.append(line)
        f = open(args[3], "w")
        for line in lines:
            order = line.split(",")
            if len(order) == 3:
                repo.receive_shipment(order[0],int(order[1]),order[2])
            else:
                repo.send_shipment(order[0],int(order[1]))

            f.writelines(repo.summary())
        f.close()
    else:
        print("file doesn't exist")


if __name__ == '__main__':
    main(sys.argv)


