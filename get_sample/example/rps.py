import random



def myRandom(start, end): return random.randint(start, end-1)
if __name__ == '__main__':
    c = myRandom(1, 3)
    p = int(input('가위(1), 바위(2), 보(3) 중 하나를 선택하세요: '))
    rps = ['가위', '바위', '보']
    if rps[p-1] == rps[c-1]:
        print(f'컴퓨터는 {rps[c-1]}를 냈고, 당신은 {rps[int(p)-1]}를 냈습니다. 비겼습니다.')
    elif rps[p-1] == rps[c % 3]:
        print(f'컴퓨터는 {rps[c-1]}를 냈고, 당신은 {rps[int(p)-1]}를 냈습니다. 당신이 이겼습니다.')
    else:
        print(f'컴퓨터는 {rps[c-1]}를 냈고, 당신은 {rps[int(p)-1]}를 냈습니다. 컴퓨터가 이겼습니다.')
