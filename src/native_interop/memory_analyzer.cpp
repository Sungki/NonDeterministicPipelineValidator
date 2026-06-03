#include <iostream>
#include <cmath>

extern "C" {
    __declspec(dllexport) bool validate_memory_buffer(const double* data_buffer, int length) {
        if (data_buffer == nullptr || length <= 0) {
            return false;
        }

        for (int i = 0; i < length; i++) {
            if (std::isnan(data_buffer[i])) { 
                return false;
            }
        }
        return true;
    }
}