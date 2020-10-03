import sys
import multiprocessing.shared_memory
import win32event
from procedures import INVALID_PROCEDURE_RESPONSE, PROCEDURES


if len(sys.argv) != 5:
    print('Usage: python main.py [mem][main_event][response_event][kill_event]')
    exit(0)


def handle(index, buf):
    proc = PROCEDURES.get(index, None)
    if not proc:
        MEM_BUF[:len(INVALID_PROCEDURE_RESPONSE)] = INVALID_PROCEDURE_RESPONSE
        return
    proc(buf)


MEM_NAME = sys.argv[1]
MAIN_EVENT_NAME = sys.argv[2]
RESPONSE_EVENT_NAME = sys.argv[3]
KILL_EVENT_NAME = sys.argv[4]
MEM = multiprocessing.shared_memory.SharedMemory(MEM_NAME, False)
MEM_BUF = MEM.buf
MAIN_EVENT = win32event.OpenEvent(win32event.EVENT_ALL_ACCESS, False, MAIN_EVENT_NAME)
RESPONSE_EVENT = win32event.OpenEvent(win32event.EVENT_ALL_ACCESS, False, RESPONSE_EVENT_NAME)
KILL_EVENT = win32event.OpenEvent(win32event.EVENT_ALL_ACCESS, False, KILL_EVENT_NAME)


while True:
    waiting_result = win32event.WaitForSingleObject(MAIN_EVENT, 2000)
    if waiting_result == win32event.WAIT_TIMEOUT:
        waiting_result = win32event.WaitForSingleObject(KILL_EVENT, 500)
        if waiting_result == win32event.WAIT_OBJECT_0:
            print('Kill event has been received')
            break
        continue
    handle(MEM_BUF[0], MEM_BUF)
    win32event.SetEvent(RESPONSE_EVENT)


MEM.close()
MAIN_EVENT.close()
RESPONSE_EVENT.close()
KILL_EVENT.close()









