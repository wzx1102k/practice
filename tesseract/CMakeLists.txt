cmake_minimum_required(VERSION 3.6)
project(tesseract)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    imagemagick/c_demo/convert.c
    imagemagick/c_demo/convert.h
    imagemagick/c_demo/demo_conv.c
    tesseract.cpp)

add_executable(tesseract ${SOURCE_FILES})