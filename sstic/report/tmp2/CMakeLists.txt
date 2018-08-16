cmake_minimum_required(VERSION 2.8.12)

set(PROJ video_inject)
project(${PROJ} CXX)
include (GenerateExportHeader)
find_package(DDraw)
add_definitions(-std=c++11)

set(LIB_SRC 
    ./lib/lib.cpp
    ./lib/lib.h
    ./lib/ddraw.h
    ./lib/lib.def
	./lib/lodepng.cpp
	./lib/lodepng.h
    )

set(MAIN_SRC
    ./main/main.cpp
    )


add_library(ddraw SHARED
    ${LIB_SRC}
    )

GENERATE_EXPORT_HEADER( ddraw
    BASE_NAME ddraw
    EXPORT_MACRO_NAME test_EXPORT
    EXPORT_FILE_NAME test_Export.h
    STATIC_DEFINE test_BUILT_AS_STATIC
    )

target_include_directories(ddraw
    PUBLIC
    ./lib
    ${PROJECT_BINARY_DIR}
    "C:/Program Files (x86)/Windows Kits/8.1/Include/um"
    )

add_executable(test_main
    ${MAIN_SRC}
    )

target_link_libraries(test_main
    ddraw
    )


