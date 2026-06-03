cmake_minimum_required(VERSION 3.15)
project(NativeInterop CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(matrix_validator SHARED memory_analyzer.cpp)

set_target_properties(matrix_validator PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON
)

if(MSVC)
    target_compile_options(matrix_validator PRIVATE /W4 /WX)
else()
    target_compile_options(matrix_validator PRIVATE -Wall -Wextra -Werror)
endif()
