import gsSystem
import os,sys

#this package calculate by layer
#- no, by layer is not correct
#make some change

def Calculate(NodeSet,PortSet,DAGSet):
    print('*********************************Start of cyclic DAG scheduling process********************************************************')
    
    #Get path of current director
    if getattr(sys, 'frozen', False):
        FP = os.path.dirname(sys.executable)
    elif __file__:
        FP = os.path.dirname(__file__)

    ScheduleTablePath = os.path.join(FP,"Accessory","ScheduleTable.txt")
    StreamPathLogPath = os.path.join(FP,"Accessory","StreamPathLog.txt")

    depthfirst = True
    
    for DAG in DAGSet:
        DAGlen = len(DAG)
        # initialize 
        #CreateDAGLayer(DAG)
        targetjobindex = 0
        i = 1
        while notalljobscheduled(DAG):

            for job in DAG:
                if not job.isAlreadyScheduled():
                    if job.isReadyForSchedule():
                        #job is not scheduled but is ready for schedule, then simple schedule this job
                        #print(job.Name)
                        job.schedules()  #TODO:Need to consider when schedules error

                        if depthfirst == True:

                            targetjobindex = DAG.index(job)
                            depthfirstseach(DAG,targetjobindex)                            

                    else:
                        #the job is not scheduled and is not ready for schedule, 
                        # find proper upstream job to be scheduled
                        targetjobindex = DAG.index(job)
                        depthfirstseach(DAG,targetjobindex)
                #else, the schedule is scheduled, then just skip, no code

def depthfirstseach(DAG,startindex):

    targetjobindex = startindex

    while not DAG[targetjobindex].isAlreadyScheduled() and not DAG[targetjobindex].DownStreamJob == []:
        if DAG[targetjobindex].isReadyForSchedule():
            if DAG[targetjobindex].isAlreadyScheduled():
                #this job is ready for schedule and also already scheduled, so find a next job that need to be scheduled
                for j in DAG[targetjobindex].DownStreamJob:
                    if not j.isAlreadyScheduled():
                        targetjobindex = DAG.index(j)
                            

            else:
                #print(DAG[targetjobindex].Name)
                DAG[targetjobindex].schedules() #TODO:Need to consider when schedules error
                for dwnjob in DAG[targetjobindex].DownStreamJob:
                    if not dwnjob.isAlreadyScheduled():
                        targetjobindex = DAG.index(dwnjob)                                        
                    break
        else:
            # means this job is not ready for schedule
            # so look for upstream job which is not scheduled
            for j in DAG[targetjobindex].UpStreamJob:
                if not j.isAlreadyScheduled():
                    targetjobindex = DAG.index(j)                                        
                    break

                


def CreateDAGLayer(DAG):
    #initialize DAG
    for job in DAG:
        job.isLayered = False

    #create layer for DAG
    DAG[0].layer = 0
    DAG[0].isLayered = True
    minilayer = 0
    maxlayer = 0
    while notalljoblayered(DAG):
        for job in DAG:
            if job.isLayered == False:
                for upjob in job.UpStreamJob:
                    if upjob.isLayered == True:
                        job.layer = upjob.layer + 1
                        job.isLayered = True
                        break
                if job.isLayered == False:
                    for dwnjob in job.DownStreamJob:
                        if dwnjob.isLayered == True:
                            job.layer = dwnjob.layer - 1
                            job.isLayered = True
                            break
    
    for job in DAG:
        if job.layer > maxlayer:
            maxlayer = job.layer

        if job.layer < minilayer:
            minilayer = job.layer
        
        d = maxlayer - minilayer
    
    for job in DAG:
        job.layer = job.layer - minilayer

        #print(job.Name, " is layer ", job.layer)

    return



def notalljoblayered(DAG):
    ret = False
    for job in DAG:
        if job.isLayered == False:
            ret = True
    return ret 

def notalljobscheduled(DAG):
    result = False
    for Job in DAG:
        if Job.isScheduled == False:
            result = True

    

    return result



def WriteScheduleTable():
    pass

def WriteFramePath():
    pass


   
    
   

    



