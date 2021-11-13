MIN_AXIS = 0
MAX_AXIS = 255


TOLERANCE  = 30
CENTER_POS = ((MAX_AXIS - MIN_AXIS) / 2) + MIN_AXIS

def is_center(x):
    return ((x >= (CENTER_POS-TOLERANCE)) and (x <= (CENTER_POS+TOLERANCE)))

def map(x,input_min,input_max,output_min,output_max):
    return (x-input_min)*(output_max-output_min)/(input_max-input_min)+output_min 


def moveMotor(xAxis, yAxis, speed):
    nJoyX = 0
    nJoyY = 0
    nMotMixL = 0           # Motor (left)  mixed output           (-128..+127)
    nMotMixR = 0           # Motor (right) mixed output           (-128..+127)

    # TEMP VARIABLES
    nMotPremixL    = 0     # Motor (left)  premixed output        (-128..+127)
    nMotPremixR    = 0     # Motor (right) premixed output        (-128..+127)
    nPivSpeed      = 0     # Pivot Speed                          (-128..+127)
    fPivScale      = 0     # Balance scale b/w drive and pivot    (   0..1   )

    fPivYLimit = 15.0
    # print('{} {}'.format(xAxis, yAxis))

    if is_center(xAxis):
        xAxis = CENTER_POS
    if is_center(yAxis):
        yAxis = CENTER_POS

    nJoyX = map(xAxis, MIN_AXIS, MAX_AXIS, -128, 127)
    nJoyY = map(yAxis, MIN_AXIS, MAX_AXIS, -128, 127)  
    # print('{} {}'.format(xAxis, yAxis))


    # Calculate Drive Turn output due to Joystick X input
    calcL = 0
    calcR = 0
    if nJoyY >= 0:
        # Forward
        if nJoyX >= 0:
            calcR = -nJoyX
        else:
            calcL = +nJoyX            
    else:
        # Reverse
        if nJoyX >= 0:
            calcL = -nJoyX            
        else:
            calcR = +nJoyX
            

    nMotPremixL = 127.0 + calcL
    nMotPremixR = 127.0 + calcR

    # Scale Drive output due to Joystick Y input (throttle)
    nMotPremixL = nMotPremixL * nJoyY/128.0
    nMotPremixR = nMotPremixR * nJoyY/128.0

    # Now calculate pivot amount
    # - Strength of pivot (nPivSpeed) based on Joystick X input
    # - Blending of pivot vs drive (fPivScale) based on Joystick Y input
    nPivSpeed = nJoyX
    
    if abs(nJoyY) > fPivYLimit:
        fPivScale = 0.0
    else:
        fPivScale = (1.0 - abs(nJoyY)/fPivYLimit)

    # Calculate final mix of Drive and Pivot
    nMotMixL = (1.0-fPivScale)*nMotPremixL + fPivScale*( nPivSpeed)
    nMotMixR = (1.0-fPivScale)*nMotPremixR + fPivScale*(-nPivSpeed)


    print('{} {}'.format(nMotMixL, nMotMixR))
    return nMotMixL, nMotMixR
    '''
    if nMotMixL < 0:
    back(CH1, map(abs(nMotMixL), 0, 127, 0, 255))
    else:  
    go(CH1, map(abs(nMotMixL), 0, 127, 0, 255))  

    if nMotMixR < 0:
    back(CH2, map(abs(nMotMixR), 0, 127, 0, 255))
    else:
    go(CH2, map(abs(nMotMixR), 0, 127, 0, 255))
    '''


if __name__ == '__main__':
    moveMotor(100, 0, 0)