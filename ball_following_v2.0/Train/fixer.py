import re


def createTrainSet(index,dest):
    jnts = open("raw/"+dest+"/angle" + str(index) + ".dat")
    
    joints = jnts.readline().split()
    joiner = list()
    for s in joints:
        m = re.findall("[-+]?\d+[\.]?\d*", s) 
        if m :
            joiner.append(m[0])


    jnts = open("raw/"+dest+"/angle" + str(index) + ".dat", "w")

    for item in joiner:
        jnts.write(item + " ")

if __name__ == "__main__":
    index = 1
    dest = raw_input("Destination? : ")

    #createTrainSet("001","test")
    
    while True:
        try:
            createTrainSet("%03d" % index,dest)
            index += 1
        except:
            print "Number of samples: %03d" % (index-1)
            break
    
        