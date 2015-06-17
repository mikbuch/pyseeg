import numpy as np

def blink_det(data, thr):
    blink = np.zeros(len(data))
    blinks_num = 0 
    zero_crossed = True
    thr_crossed = False
    prev_val = 0.0
    for i in range(len(data)):
        if data[i] > thr and prev_val <= thr and zero_crossed == True:
            blinks_num += 1
            if i < len(data)-2:
                blink[i] = thr
                blink[i+1] = -thr
            zero_crossed = False
        if i!=0:
            prev_val = data[i-1]
            if prev_val > 0.0 and data[i] <= 0.0:
                zero_crossed = True
         
    return blink, blinks_num

