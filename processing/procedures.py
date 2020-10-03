import json


PROCEDURES = {}


def procedure(index):
    def decorator_result(f):
        assert not PROCEDURES.get(index, None), f'Procedure with index {index} already exists'
        PROCEDURES[index] = f
    return decorator_result


INVALID_PROCEDURE_RESPONSE = json.dumps({'status': 'INVALID_PROCEDURE_INDEX'}).encode('utf8')


LEN_INDEX = 0
IMAGE_INDEX = 4


@procedure(0)
def procedure_is_passport(buf):
    pass
    # data = json.dumps({'status': 'OK_PROC_IS_PASSPORT'}).encode('utf8')
    # buf[:4] = len(data).to_bytes(4, 'little', signed=False)
    # buf[4:4 + len(data)] = data


@procedure(1)
def procedure_recognition(buf):
    pass
    # data = json.dumps({'status': 'OK_PROC_RECOGNITION'}).encode('utf8')
    # buf[:4] = len(data).to_bytes(4, 'little', signed=False)
    # buf[4:4 + len(data)] = data



