import signal
import sys

import inputs

""" keyboard except """
def signal_handler(signal, frame):
    print('byebye ^^')
    exit(0)


def map(x,input_min,input_max,output_min,output_max):
    return (x-input_min)*(output_max-output_min)/(input_max-input_min)+output_min 

def left_joystick_show():
    print('run left_joystick_show')
    # 센터 값으로 초기화
    x = 128 
    y = 128 
    while True:
        try:
            events = inputs.get_gamepad()
            for event in events:                
                if event.ev_type == 'Absolute':
                    changed = False
                    if event.code == 'ABS_X':                        
                        x = int(event.state)
                        changed = True
                    elif event.code == 'ABS_Y':
                        y = int(event.state)
                        changed = True
                    
                    if changed:
                        print('x: {} y: {}'.format(x, y))

                        cx = map(x, 0, 255, -100, 100)
                        cy = map(y, 0, 255, -100, 100)
                        print('x: {} y: {}, cx: {} cy: {} '.format(x, y, cx, cy))
        except:
            print('error ',sys.exc_info())
            break

    print('byebye!')

def just_show():
    print('run just_show')
    while True:
        try:
            events = inputs.get_gamepad()
            for event in events:
                print(event.ev_type, event.code, event.state)
        except:
            print('error ',sys.exc_info())
            break

    print('byebye!')

if __name__ == '__main__':
    # keyboard except signal handler
    signal.signal(signal.SIGINT, signal_handler)

    left_joystick_show()
    # just_show()