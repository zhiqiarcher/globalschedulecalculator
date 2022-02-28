
from logging import NullHandler
import gsMath
import os,sys
import copy



class Job(object):
    def __init__(self,Name, CycleNs, ReservedTimeSpanNs,Machine):
        self.Name = Name
        self.CycleNs = CycleNs    
        self.TimeSpan = ReservedTimeSpanNs
        self.offset = 0
        self.Machine = Machine  #consider to remove
        self.UpStreamJob = []
        self.DownStreamJob = []
        self.isScheduled = False
        self.layer = 0
        self.isLayered = False
    

    def isReadyForSchedule(self):
        #return true when upstreamjob list is empty or all upstream job is scheduled
        ret = True

        if self.UpStreamJob ==[]:
            pass
        else:
            for j in self.UpStreamJob:
                if j.isScheduled == False:
                    ret = False
                    break
        return ret

    def isAlreadyScheduled(self):
        return self.isScheduled

    def schedules(self):
        print(self.Name, 'is being scheduled')

        #Initializ
        PSs = [[0,self.CycleNs -self.TimeSpan]] #Possible Sets
        PSAJ=[] #PossibleSetAgainstJob

        latestboundary = 0
        for job in self.UpStreamJob:
            #find the time boundary of each upstream job, 
            #current job's start time must be after that
            if job.offset + job.TimeSpan > latestboundary:
                latestboundary = job.offset + job.TimeSpan
        
        # start scheduling
        for job in self.Machine.AssignedJobs:
            if not job == self and job.isAlreadyScheduled(): 
                print('check against ',job.Name)
                times = self.CycleNs / job.CycleNs

                #calculate possible set against this job
                if job.offset > self.TimeSpan:
                    PSAJ.append([0,job.offset - self.TimeSpan])
                
                if job.CycleNs - job.TimeSpan >self.TimeSpan:
                    while times > 0:
                        PSAJ.append([job.offset + job.TimeSpan + (times -1) * job.CycleNs ,job.offset + job.CycleNs - self.TimeSpan + (times -1) * job.CycleNs])
                        times = times -1
                #find cross set
                PSs = FindCrossSet(PSs,PSAJ)
                if PSs ==[]:
                    break
            i = 0

        if not PSs ==[]:        
            #check in the PSs, which set fits the latest boundary
            for set in PSs:
                if set[0]<=latestboundary and set[1]>= latestboundary:
                    if set[1]- latestboundary > self.TimeSpan:
                        self.offset = latestboundary
                        break
                elif set[0] > latestboundary:
                    if set[1] - set[0] > self.TimeSpan:
                        self.offset = set[0]
                        break
            self.isScheduled = True
            print(self.Name, ' has finish schedule, offset is',self.offset)
        else:
            print(self.Name," schedules fail")
        
        return self.isScheduled
        


class Task(Job):
    def __init__(self,Name, CycleNs, ReservedTimeSpanNs,Machine, BoolStartedWithNetoworkRx, BoolFollowedByNetworkTx):
        Job.__init__(self,Name, CycleNs,  ReservedTimeSpanNs,Machine)
        self.BoolStartedWithNetoworkRx = BoolStartedWithNetoworkRx 
        self.BoolFollowedByNetworkTx = BoolFollowedByNetworkTx

class QbvEvent(Job):
    def __init__(self,Name, CycleNs, ReservedTimeSpanNs,Machine):
        Job.__init__(self,Name, CycleNs, ReservedTimeSpanNs,Machine)

        
class Machine(object):
    def __init__(self, Name):
        self.Name = Name
        self.AssignedJobs = []

        
class Node(Machine):
    def __init__(self, Name,TxRxKernelDelayNs):
        Machine.__init__(self, Name)
        self.Name = Name
        self.Name = TxRxKernelDelayNs

class EthPort(Machine):
    def __init__(self, Name):
        Machine.__init__(self, Name)
        self.Name = Name

def FindCrossSet(PSs,PSAJ):
    #需要满足前提PSs，PSAJ内的各个集合之间没有交集
    tempsets = []
    for PS in PSs:
        for JS in PSAJ:
            PSLow = PS[0]
            PSUp = PS[1]
            JSLow = JS[0]
            JSUp = JS[1]
            if (PSLow >= JSLow and PSLow <= JSUp) or (PSUp >= JSLow and PSLow < JSUp) or (JSLow >= PSLow and JSLow <= PSUp) or (JSUp >= PSLow and JSUp <= PSUp):

                if PSLow >= JSLow:
                    Low = PSLow
                else:
                    Low = JSLow

                if PSUp <= JSUp:
                    Up = PSUp
                else:
                    Up = JSUp

                tempsets.append([Low, Up])
    if not tempsets == []:
        print('cross set found')
    else:
        print('not cross set found')

    return tempsets
