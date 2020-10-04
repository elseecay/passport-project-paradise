import multiprocessing.shared_memory
import win32event
import event_generator_proc


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


MEM_NAME = 'pppmem'
MUTEX_NAME = 'pppmutex'
RECOGNITION_EVENT_NAME = 'ppprecognition'
RESULT_TAKEN_EVENT_NAME = 'pppresulttaken'
KILL_EVENT_NAME = 'pppkill'


try:
    MEM = multiprocessing.shared_memory.SharedMemory(MEM_NAME, True, int(1e+7))
    MEM_BUF = MEM.buf
    MUTEX = win32event.CreateMutex(None, False, MUTEX_NAME)
    RECOGNITION_EVENT = win32event.CreateEvent(None, False, False, RECOGNITION_EVENT_NAME)
    RESULT_TAKEN_EVENT = win32event.CreateEvent(None, False, False, RESULT_TAKEN_EVENT_NAME)
    KILL_EVENT = win32event.CreateEvent(None, False, False, KILL_EVENT_NAME)
except Exception as e:
    print('Exception', e)
    if 'MEM' in globals():
        MEM.unlink()
    if 'MUTEX' in globals():
        MUTEX.close()
    if 'RECOGNITION_EVENT' in globals():
        RECOGNITION_EVENT.close()
    if 'RESULT_TAKEN_EVENT' in globals():
        RESULT_TAKEN_EVENT.close()
    if 'KILL_EVENT' in globals():
        KILL_EVENT.close()
    exit(1)


with SafeExecutionPack(MEM, MUTEX, RECOGNITION_EVENT, RESULT_TAKEN_EVENT, KILL_EVENT):
    exception_counter = 0
    while True:
        try:
            w = win32event.WaitForSingleObject(KILL_EVENT, 100)
            if w == win32event.WAIT_OBJECT_0:
                print('Kill event accepted')
                break
            img = event_generator_proc.get_webcam_image()
            if not event_generator_proc.is_passport(img):
                continue
            w = win32event.WaitForSingleObject(MUTEX, 0)
            if w == win32event.WAIT_TIMEOUT:
                continue
            data = event_generator_proc.recognition(img)
            event_generator_proc.json_to_mem(MEM_BUF, data)
            win32event.ReleaseMutex(MUTEX)
            win32event.SetEvent(RECOGNITION_EVENT)
            w = win32event.WaitForSingleObject(RESULT_TAKEN_EVENT, 10000)
            if w == win32event.WAIT_TIMEOUT:
                print('Missing recognized passport, data:\n')
        except Exception as e:
            print('Exception', e)
            exception_counter += 1
            if exception_counter == 5:
                print('TOO MUCH EXCEPTIONS')
                break