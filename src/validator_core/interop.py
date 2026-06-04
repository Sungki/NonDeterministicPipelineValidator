import ctypes
import os

lib_path = os.path.abspath("./native_interop/build/Release/matrix_validator.dll")
try:
    native_lib = ctypes.CDLL(lib_path)
    native_lib.validate_memory_buffer.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
    native_lib.validate_memory_buffer.restype = ctypes.c_bool
except OSError:
    native_lib = None

def call_native_validator(data_list_py) -> bool:
    if not native_lib:
        return True
    
    arr_type = ctypes.c_double * len(data_list_py)
    c_array = arr_type(*data_list_py)
    return native_lib.validate_memory_buffer(c_array, len(data_list_py))