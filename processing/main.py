import sys
import multiprocessing.shared_memory
import win32event
import procedures


if len(sys.argv) != 6:
    print('Usage: python main.py [mem][passport][recognized][result_taken][kill]')
    exit(0)


MEM_NAME = sys.argv[1]
PASSPORT_EVENT_NAME = sys.argv[2]
RECOGNIZED_EVENT_NAME = sys.argv[3]
RESULT_TAKEN_EVENT_NAME = sys.argv[4]
KILL_EVENT_NAME = sys.argv[5]
MEM = multiprocessing.shared_memory.SharedMemory(MEM_NAME, True, int(1e+7))
MEM_BUF = MEM.buf
PASSPORT_EVENT = win32event.OpenEvent(win32event.EVENT_ALL_ACCESS, False, PASSPORT_EVENT_NAME)
RECOGNIZED_EVENT = win32event.OpenEvent(win32event.EVENT_ALL_ACCESS, False, RECOGNIZED_EVENT_NAME)
RESULT_TAKEN_EVENT = win32event.OpenEvent(win32event.EVENT_ALL_ACCESS, False, RESULT_TAKEN_EVENT_NAME)
KILL_EVENT = win32event.OpenEvent(win32event.EVENT_ALL_ACCESS, False, KILL_EVENT_NAME)


while True:
    w = win32event.WaitForSingleObject(KILL_EVENT, 100)
    if w == win32event.WAIT_OBJECT_0:
        break
    img = procedures.get_webcam_image()  # exception
    if not procedures.is_passport(img):
        continue
    win32event.SetEvent(PASSPORT_EVENT)
    data = procedures.recognition(img)  # exception
    win32event.SetEvent(RECOGNIZED_EVENT)
    procedures.json_to_mem(data)
    w = win32event.WaitForSingleObject(RESULT_TAKEN_EVENT, 10000)
    if w == win32event.WAIT_TIMEOUT:
        print('Missing recognized passport, data:\n')  # TODO: recognized result


MEM.close()
PASSPORT_EVENT.close()
RECOGNIZED_EVENT.close()
RESULT_TAKEN_EVENT.close()
KILL_EVENT.close()









