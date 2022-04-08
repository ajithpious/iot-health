import time

MEAN_FILTER_SIZE=15
#Pulse detection parameters
PULSE_MIN_THRESHOLD=300 #300 is good for finger, but for wrist you need like 20, and there is shitloads of noise
PULSE_MAX_THRESHOLD=2000
PULSE_GO_DOWN_THRESHOLD=1
PULSE_BPM_SAMPLE_SIZE =10 #Moving average size
def enum(**enums):
    return type('Enum', (), enums)
PulseStateMachine = enum(PULSE_IDLE=0, PULSE_TRACE_UP=2, PULSE_TRACE_DOWN=3)



class meanDiffFilter_t(object):
    def __init__(self,values,index,sum,count):
        self.values=values
        self.index=index
        self.sum=sum
        self.count=count
class butterworthFilter_t(object):
    def __init__(self,v,result):
        self.v=v
        self.result=result
class dcFilter_t(object):
    def __init__(self):
        self.w=0
        self.result=0
class result(object):
    def __init__(self):
        self.pulseDetected=0
        self.heartBPM=0
        self.irCardiogram=0
        self.irDcValue=0
        self.redDcValue=0
        self.SaO2=0
        self.lastBeatThreshold=0
        self.dcFilteredIR=0
        self.dcFilteredRed=0


class HRSpo2(object):
    
    def __init__(self,debug):
        
        self.debug=debug
        
        self.valuesBPM = [0]*PULSE_BPM_SAMPLE_SIZE
        self.valuesBPMSum = 0
        self.valuesBPMCount = 0
        self.bpmIndex = 0
        self.irACValueSqSum = 0;
        self.redACValueSqSum = 0;
        self.samplesRecorded = 0;
        self.pulsesDetected = 0;
        self.currentSaO2Value = 0;
        
        self.currentPulseDetectorState=PulseStateMachine.PULSE_IDLE

        self.lastBeatThreshold = 0;
        self.meanDiffIR=meanDiffFilter_t([0]*MEAN_FILTER_SIZE,0,0,0)
        self.lpbFilterIR=butterworthFilter_t([0]*2,0)
        self.dcFilterIR=dcFilter_t()
        self.result=result()
        self.currentBPM=0
        
    def update(self,val):
        
        self.dcFilterIR=self.dcRemove(val,self.dcFilterIR.w)
        meanDiffResIR=self.meanDiff(self.dcFilterIR.result,self.meanDiffIR)
        self.lowPassButterworthFilter(meanDiffResIR,self.lpbFilterIR)
        self.irACValueSqSum +=  self.dcFilterIR.result* self.dcFilterIR.result
        self.samplesRecorded+=1
        if( self.detectPulse( self.lpbFilterIR.result ) and self.samplesRecorded > 0 ):
            self.result.pulseDetected=True;
            self.pulsesDetected+=1
            self.result.heartBPM = self.currentBPM;
            return self.result.heartBPM
        
        return "no beats"
        
        
    def dcRemove(self,val,prev):
        
        self.dcFilterIR.w=val+0.95*prev
        self.dcFilterIR.result=self.dcFilterIR.w-prev
        return self.dcFilterIR
        
        return y,new_prev
    def meanDiff(self,M,filterValues):
        avg=0
        filterValues.sum -= filterValues.values[filterValues.index];
        filterValues.values[filterValues.index] = M
        filterValues.sum += filterValues.values[filterValues.index];
        filterValues.index+=1;
        filterValues.index = filterValues.index % MEAN_FILTER_SIZE;
        if(filterValues.count < MEAN_FILTER_SIZE):
            filterValues.count+=1;

        avg = filterValues.sum / filterValues.count;
        return avg - M;
    def lowPassButterworthFilter(self,x,filterResult):
        filterResult.v[0] = filterResult.v[1];
        #Fs = 100Hz and Fc = 10Hz
        filterResult.v[1] = (2.452372752527856026e-1 * x) + (0.50952544949442879485 * filterResult.v[0]);
        #Fs = 100Hz and Fc = 4Hz
        #filterResult->v[1] = (1.367287359973195227e-1 * x) + (0.72654252800536101020 * filterResult->v[0]); //Very precise butterworth filter 
        filterResult.result = filterResult.v[0] + filterResult.v[1];
    def detectPulse(self,sensor_value):
        HRSpo2.prev_sensor_value = 0;
        HRSpo2.values_went_down = 0;
        HRSpo2.currentBeat = 0;
        HRSpo2.lastBeat = 0;
        if(sensor_value > PULSE_MAX_THRESHOLD):
            self.currentPulseDetectorState = PulseStateMachine.PULSE_IDLE
            HRSpo2.prev_sensor_value = 0
            HRSpo2.lastBeat = 0
            HRSpo2.currentBeat = 0
            HRSpo2.values_went_down = 0
            self.lastBeatThreshold = 0
            return False
        if(self.currentPulseDetectorState==PulseStateMachine.PULSE_IDLE):
            if(sensor_value >= PULSE_MIN_THRESHOLD):
                self.currentPulseDetectorState = PulseStateMachine.PULSE_TRACE_UP;
                HRSpo2.values_went_down = 0;
        elif(self.currentPulseDetectorState==PulseStateMachine.PULSE_TRACE_UP):
            if(sensor_value > HRSpo2.prev_sensor_value):
                HRSpo2.currentBeat = time.ticks_ms()
                self.lastBeatThreshold = sensor_value
            else:
                if(self.debug == True):
                    print("Peak reached: ",end=" ");
                    print(sensor_value);
                    print(HRSpo2.prev_sensor_value);
                    
                beatDuration = HRSpo2.currentBeat - HRSpo2.lastBeat;
                HRSpo2.lastBeat = HRSpo2.currentBeat;
                rawBPM = 0;
                if(beatDuration > 0):
                  rawBPM = 60000.0/float(beatDuration);
                if(self.debug == True):
                    print(rawBPM);
                self.valuesBPM[self.bpmIndex] = rawBPM;
                self.valuesBPMSum = 0;
                for i in range(PULSE_BPM_SAMPLE_SIZE):
                    self.valuesBPMSum += self.valuesBPM[i];
                if(self.debug == True):
                    print("CurrentMoving Avg: ");
                    for i in range(PULSE_BPM_SAMPLE_SIZE):
                        print(self.valuesBPM[i],end=" ");
                self.bpmIndex+=1;
                self.bpmIndex = self.bpmIndex % PULSE_BPM_SAMPLE_SIZE;
                if(self.valuesBPMCount < PULSE_BPM_SAMPLE_SIZE):
                    self.valuesBPMCount+=1
                self.currentBPM = self.valuesBPMSum / self.valuesBPMCount;
                if(self.debug == True):
                    print("AVg. BPM: ",end="");
                    print(self.currentBPM);
                self.currentPulseDetectorState = PulseStateMachine.PULSE_TRACE_DOWN;
                return True
        elif(self.currentPulseDetectorState==PulseStateMachine.PULSE_TRACE_DOWN):
            if(sensor_value < HRSpo2.prev_sensor_value):
                HRSpo2.values_went_down+=1;
            if(sensor_value < PULSE_MIN_THRESHOLD):
                PulseStateMachine.currentPulseDetectorState = PulseStateMachine.PULSE_IDLE
        HRSpo2.prev_sensor_value = sensor_value;
        return False;
        

                
                
                
                
      
        




    
    


    
    
