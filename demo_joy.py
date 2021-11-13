import sys
import signal

import inputs

import serial
from serial_prot import Protocol, ReaderThread

from time import sleep
from axis import moveMotor

# 포트 설정
PORT = '/dev/ttyACM0'

# 프로토콜
class odriveSerialProtocal(Protocol):
    # 연결 시작시 발생
    def connection_made(self, transport):
        self.transport = transport
        self.running = True
        self.l_ch = 0
        self.r_ch = 1

    # 연결 종료시 발생
    def connection_lost(self, exc):
        self.transport = None

    #데이터가 들어오면 이곳에서 처리함.
    def data_received(self, data):
        print('data_received', data)
        
    # 종료 체크
    def is_done(self):
        return self.running

    # 속도
    def velocity(self, l, r):        
        l_data = 'v {} {} 0\r\n'.format(self.l_ch, round(l, 2))
        r_data = 'v {} {} 0\r\n'.format(self.r_ch, round(r, 2))

        self.transport.write(l_data.encode())
        self.transport.write(r_data.encode())

""" keyboard except """
def signal_handler(signal, frame):
    print('byebye ^^')
    exit(0)


def map(x,input_min,input_max,output_min,output_max):
    return (x-input_min)*(output_max-output_min)/(input_max-input_min)+output_min 

def odrive_with_gamepad(): 
    try:
        MAX_VELOCITY_VALUE = 10.0
        MIN_VELOCITY_VALUE = -10.0
        x = 127
        y = 127
        step = 0.1
        velocity = 0.0
        # 연결
        with serial.serial_for_url(PORT, baudrate=9600, timeout=1) as ser:
            print('serial port opened')

            # 쓰레드 시작
            with ReaderThread(ser, odriveSerialProtocal) as p:
                while p.is_done():
                    sleep(0.001)
                    events = inputs.get_gamepad()
                    for event in events:
                        if event.ev_type == 'Absolute':
                            if event.code == 'ABS_X':
                                x = int(event.state)
                            elif event.code == 'ABS_Y':
                                y = int(event.state)
                            
                            cl, cr = moveMotor(x, y, 0)
                            print('x: {} y: {} cl: {}, cr: {}'.format(x, y, cl, cr))
                            if cl < 0:
                                # back
                                cl = -map(abs(cl), 0, 127, 0, 100) / 10.0
                            else:
                                # go
                                cl = (map(abs(cl), 0, 127, 0, 100) / 10.0)

                            if cr < 0:
                                # back
                                cr = -map(abs(cr), 0, 127, 0, 100) / 10.0
                            else:
                                # go
                                cr = (map(abs(cr), 0, 127, 0, 100) / 10.0)
                            # print('x: {} y: {}, cx: {} cy: {} '.format(x, y, cx, cy))
                            if cl <= 0.05 and cl >= -0.05:
                                cl = 0.0
                            if cr <= 0.05 and cr >= -0.05:
                                cr = 0.0
                            p.velocity(cl, -cr)
    finally:
        pass

if __name__ == '__main__':
    # keyboard except signal handler
    signal.signal(signal.SIGINT, signal_handler)
    odrive_with_gamepad()