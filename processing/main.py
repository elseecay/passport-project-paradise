import sys
import multiprocessing.shared_memory
import win32event
import procedures
import time


class SafeExecutionPack:

    def __init__(self, *args):
        self._items = args

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for i in self._items:
            if hasattr(i, 'unlink'):
                i.unlink()
            else:
                i.close()


if len(sys.argv) != 6:
    print('Usage: python main.py [mem][passport][recognized][result_taken][kill]')
    exit(0)


MEM_NAME = sys.argv[1]
PASSPORT_EVENT_NAME = sys.argv[2]
RECOGNIZED_EVENT_NAME = sys.argv[3]
RESULT_TAKEN_EVENT_NAME = sys.argv[4]
KILL_EVENT_NAME = sys.argv[5]


try:
    MEM = multiprocessing.shared_memory.SharedMemory(MEM_NAME, True, int(1e+7))
    MEM_BUF = MEM.buf
    PASSPORT_EVENT = win32event.CreateEvent(None, False, False, PASSPORT_EVENT_NAME)
    RECOGNIZED_EVENT = win32event.CreateEvent(None, False, False, RECOGNIZED_EVENT_NAME)
    RESULT_TAKEN_EVENT = win32event.CreateEvent(None, False, False, RESULT_TAKEN_EVENT_NAME)
    KILL_EVENT = win32event.CreateEvent(None, False, False, KILL_EVENT_NAME)
except Exception as e:
    print('Exception', e)
    if 'MEM' in globals():
        MEM.unlink()
    if 'PASSPORT_EVENT' in globals():
        PASSPORT_EVENT.close()
    if 'RECOGNIZED_EVENT' in globals():
        RECOGNIZED_EVENT.close()
    if 'RESULT_TAKEN_EVENT' in globals():
        RESULT_TAKEN_EVENT.close()
    if 'KILL_EVENT' in globals():
        KILL_EVENT.close()
    exit(1)


with SafeExecutionPack(MEM, PASSPORT_EVENT, RECOGNIZED_EVENT, RESULT_TAKEN_EVENT, KILL_EVENT):
    exception_counter = 0
    while True:
        try:
            w = win32event.WaitForSingleObject(KILL_EVENT, 100)
            if w == win32event.WAIT_OBJECT_0:
                print('Kill event accepted')
                break
            img = None # procedures.get_webcam_image()
            if not procedures.is_passport(img):
                continue
            win32event.SetEvent(PASSPORT_EVENT)
            data = procedures.recognition(img)
            procedures.json_to_mem(MEM_BUF, data)
            win32event.SetEvent(RECOGNIZED_EVENT)
            w = win32event.WaitForSingleObject(RESULT_TAKEN_EVENT, 10000)
            if w == win32event.WAIT_TIMEOUT:
                print('Missing recognized passport, data:\n')  # TODO: recognized result
        except Exception as e:
            print('Exception', e)
            exception_counter += 1
            if exception_counter == 5:
                print('TOO MUCH EXCEPTIONS')
                break








