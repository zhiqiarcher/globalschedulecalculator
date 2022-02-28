import os
import gsCalculator as CDC
import gsSystem as sys


def run():
    
    #this main function serves as a interface to the user

    #any other used GUI shall also call the calculator as shown in this main function
    os.system('cls')


    #Define the system
    node0 = sys.Node('node0',200000)
    node1 = sys.Node('node1',200000)
    node2 = sys.Node('node2',200000)
    node3 = sys.Node('node3',200000)
    NodeSet= [node0,node1,node2,node3]

    port0 =sys.EthPort('port0')
    port1 =sys.EthPort('port1')
    port2 =sys.EthPort('port2')
    port3 =sys.EthPort('port3')
    port4 =sys.EthPort('port4')
    port5 =sys.EthPort('port4')
    port6 =sys.EthPort('port4')
    port7 =sys.EthPort('port4')
   
    PortSet = [port0,port1,port2,port3,port4,port5,port6,port7]

    #DAG0
    DAG0CycleNs = 10000000  #10ms

    #tasks
    uc0t0 = sys.Task('uc0t0',DAG0CycleNs,800000,node0,False,True,) # reserve 800us
    uc0t1 = sys.Task('uc0t1',DAG0CycleNs,800000,node0,False,True,) # reserve 800us
    uc0t2 = sys.Task('uc0t2',DAG0CycleNs,800000,node1,False,True,) # reserve 800us
    uc0t3 = sys.Task('uc0t3',DAG0CycleNs,800000,node2,False,True,) # reserve 800us
    uc0t4 = sys.Task('uc0t4',DAG0CycleNs,800000,node3,False,True,) # reserve 800us

    #QbvEvents

    uc0s0p0 = sys.QbvEvent('uc0s0p0',DAG0CycleNs,200000,port0) # reserve 200us
    uc0s0p2 = sys.QbvEvent('uc0s0p2',DAG0CycleNs,200000,port2) # reserve 200us

    uc0s1p0 = sys.QbvEvent('uc0s1p0',DAG0CycleNs,200000,port0) # reserve 200us
    uc0s1p2 = sys.QbvEvent('uc0s1p2',DAG0CycleNs,200000,port2) # reserve 200us

    uc0s2p3 = sys.QbvEvent('uc0s2p3',DAG0CycleNs,200000,port3) # reserve 200us
    uc0s2p4 = sys.QbvEvent('uc0s2p4',DAG0CycleNs,200000,port4) # reserve 200us

    uc0s3p3 = sys.QbvEvent('uc0s3p3',DAG0CycleNs,200000,port3) # reserve 200us
    uc0s3p6 = sys.QbvEvent('uc0s3p6',DAG0CycleNs,200000,port6) # reserve 200us


    #add Jobs to machines
    node0.AssignedJobs = [uc0t0,uc0t1]
    node1.AssignedJobs = [uc0t2]
    node2.AssignedJobs = [uc0t3]
    node3.AssignedJobs = [uc0t4]
  

    port0.AssignedJobs = [uc0s0p0,uc0s1p0]
    port1.AssignedJobs = []
    port2.AssignedJobs = [uc0s0p2,uc0s1p2]
    port3.AssignedJobs = [uc0s2p3]
    port4.AssignedJobs = [uc0s2p4]
    port5.AssignedJobs = []
    port6.AssignedJobs = [uc0s3p3]
    port7.AssignedJobs = [uc0s3p6]

    #Link task and Qbv events
    uc0t0.DownStreamJob = [uc0s0p0]
    uc0t0.UpStreamJob = []

    uc0t1.DownStreamJob = [uc0s1p0]
    uc0t1.UpStreamJob = []

    uc0t2.DownStreamJob = [uc0s2p3,uc0s3p3]
    uc0t2.UpStreamJob = [uc0s0p2,uc0s1p2]

    uc0t3.DownStreamJob = []
    uc0t3.UpStreamJob = [uc0s2p4]

    uc0t4.DownStreamJob = []
    uc0t4.UpStreamJob = [uc0s3p6]


    uc0s0p0.DownStreamJob = [uc0s0p2]
    uc0s0p0.UpStreamJob = [uc0t0]

    uc0s0p2.DownStreamJob = [uc0t2]
    uc0s0p2.UpStreamJob = [uc0s0p0]

    uc0s1p0.DownStreamJob = [uc0s1p2]
    uc0s1p0.UpStreamJob = [uc0t1]
 
    uc0s1p2.DownStreamJob = [uc0t2]
    uc0s1p2.UpStreamJob = [uc0s1p0]

    uc0s2p3.DownStreamJob = [uc0s2p4]
    uc0s2p3.UpStreamJob =[uc0t2]

    uc0s2p4.DownStreamJob =[uc0t3]
    uc0s2p4.UpStreamJob =[uc0s2p3]

    uc0s3p3.DownStreamJob = [uc0s3p6]
    uc0s3p3.UpStreamJob = [uc0t2]

    uc0s3p6.DownStreamJob = [uc0t4]
    uc0s3p6.UpStreamJob = [uc0s3p3]


    DAG1 = [uc0t2,uc0t0,uc0t1,uc0t3,uc0t4,uc0s0p0,uc0s0p2,uc0s1p0,uc0s1p2,uc0s2p3,uc0s2p4,uc0s3p3,uc0s3p6]

    DAGSet = [DAG1]
  

    CDC.Calculate(NodeSet,PortSet,DAGSet)
    
    while True:
        pass     
    
if __name__ == "__main__":


    run()
    


   
    
   

    



