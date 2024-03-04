cmake_minimum_required(VERSION 3.10.2)

project(test_1)

set (CMAKE_CXX_STANDARD 17)


find_package(MPI REQUIRED)


set(linkLibraries)
if (MPI_FOUND)
		include_directories(${MPI_INCLUDE_PATH})
		# Add mpi libraries:
		# Standard case: add cxx libraries
		if (MPI_CXX_LIBRARIES)
			set(linkLibraries ${linkLibraries} ${MPI_CXX_LIBRARIES})
		endif (MPI_CXX_LIBRARIES)				
	else (MPI_FOUND)
		message(FATAL_ERROR "MPI not found.")
	endif (MPI_FOUND)


# add library to linking

set(SOURCES
	test_class/Test_class.cpp
	exercise_25/class_25.cpp
	exercise_26/class_26.cpp
	exercise_27/class_27.cpp

)



add_library(hpclib ${SOURCES})
add_executable(hpc main.cpp)

message(STATUS "Run: ${MPIEXEC} ${MPIEXEC_NUMPROC_FLAG} ${MPIEXEC_MAX_NUMPROCS} ${MPIEXEC_PREFLAGS} EXECUTABLE ${MPIEXEC_POSTFLAGS} ARGS")



target_link_libraries(hpc hpclib ${linkLibraries})


if(MPI_COMPILE_FLAGS)
  set_target_properties(hpc PROPERTIES
    COMPILE_FLAGS "${MPI_COMPILE_FLAGS}")
endif()

if(MPI_LINK_FLAGS)
  set_target_properties(hpc PROPERTIES
    LINK_FLAGS "${MPI_LINK_FLAGS}")
endif()

######
