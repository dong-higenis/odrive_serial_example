from inputs import get_gamepad #inputs 패키지에서 get_gamepad만 임포트

def main():
    # 무한 루프!
    while 1:
        # gamepad 이벤트 받기
        events = get_gamepad()
        # 이벤트들을 루프로 돌림
        for event in events: 
            # type, code, state를 출력           
            print(event.ev_type, event.code, event.state)
if __name__ == "__main__":
    main()