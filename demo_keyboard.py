from time import sleep

# 시리얼 
import serial
from serial_prot import Protocol, ReaderThread

# 포트 설정
PORT = '/dev/ttyACM0'

# 키 입력 관련
import sys
import select
import tty
import termios


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

# 키 체크
def is_keydown():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

old_settings = termios.tcgetattr(sys.stdin)
try:
    MAX_VELOCITY_VALUE = 10.0
    MIN_VELOCITY_VALUE = -10.0
    step = 0.1
    velocity = 0.0
    tty.setcbreak(sys.stdin.fileno())
    # 연결
    with serial.serial_for_url(PORT, baudrate=9600, timeout=1) as ser:
        print('serial port opened')

        # 쓰레드 시작
        with ReaderThread(ser, odriveSerialProtocal) as p:
            while p.is_done():
                sleep(0.01)
                if is_keydown():
                    c = sys.stdin.read(1)
                    if c == 'a':
                        print('left')
                        velocity = velocity + step
                        if velocity > MAX_VELOCITY_VALUE:
                            velocity = MAX_VELOCITY_VALUE
                        p.velocity(velocity, -velocity)
                        
                    elif c == 'd':
                        print('right')
                        velocity = velocity - step
                        if velocity < MIN_VELOCITY_VALUE:
                            velocity = MIN_VELOCITY_VALUE

                        p.velocity(velocity, -velocity)
                    elif c == 'w':
                        print('up')
                    elif c == 's':
                        print('stop')
                        velocity = 0
                        p.velocity(velocity, -velocity)
                    elif c == 'q':         # x1b is ESC
                        print('byebye')
                        break

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
