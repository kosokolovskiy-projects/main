#include "class_25.h"
#include <iostream>
#include <vector>
#include <mpi.h>
#include <string>
#include <stdlib.h> 
#include <cmath>

template <typename T>
void print_vector(std::vector<T>& vect){
	for (int i=0; i < vect.size(); ++i){
		std::cout << vect[i] << '\t';
	}
	std::cout << '\n';
}



void Ex_25::test_mpi(int start, int finish, int argc, char** argv){

	MPI_Init(&argc, &argv);
	std::vector<int> test_vect;
	std::vector<int> recv_vect;
	std::vector<float> time_vect;
	int size_vect;

	int rank;
	int size;

	
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	time_vect.resize(size);
	const int main_rank = 0;


	int one_part = (finish - start +1) / size;
	MPI_Barrier(MPI_COMM_WORLD);
	double start_time = MPI_Wtime();

	if (rank == 0){
		ex_17(start, finish - one_part*(size-1)+1, rank);
	}
	else{
		int start_local = finish - one_part*(size - rank)+1;
		int end_local = finish - one_part*(size - rank - 1)+1;
		ex_17(start_local, end_local, rank);
	}

	double end_time = MPI_Wtime();

	float final_time = end_time - start_time;

	MPI_Gather(&final_time, 1, MPI_FLOAT, &time_vect[0], 1, MPI_FLOAT, main_rank, MPI_COMM_WORLD);
	if (rank == 0){
    	std::cout << "Time: "<< final_time << std::endl; 
    	print_vector(time_vect);
    }


	MPI_Finalize();
};

std::vector<std::vector<int>> Ex_25::ex_17(int start, int finish, int proc){
	const int num_div = 3;
	int n_curr = 0;

	std::vector<int> dividers;
	std::vector<std::vector<int>> final_vector;

	for (int i = start; i < finish; ++i){
		for (int k = 2; k < std::sqrt(i)+1; ++k){
			if (n_curr > num_div){
				break;
			}

			if (i % k == 0){
				n_curr++;
				dividers.push_back(k);
				if (i/k != k){
					n_curr++;
					dividers.push_back(i/k);
				}
			}
		}
		if (n_curr == num_div){
			std::sort(dividers.begin(),dividers.end());
			final_vector.push_back(dividers);
			print_vector(dividers);

		}
		n_curr = 0;
		dividers.clear();
	}
return final_vector;
};

void Ex_25::ex_22(int start, int finish){
	const int num_div = 5;
	int n_curr = 0;

	std::vector<int> dividers;

	for (int i{start}; i <= finish; ++i){
		for (int k{1}; k <= std::sqrt(i); ++k){
			if (i % k == 0){
				if (k % 2 != 0){
					dividers.push_back(k);
				}
				if (i / k % 2 != 0 and i / k != k){
					dividers.push_back(i/k);
				}
			}
			if (dividers.size() > num_div){
				break;
			}
		}
		if (dividers.size() == num_div){
			std::cout << "Number: " << i << "\n";
			std::sort(dividers.begin(), dividers.end());
			print_vector(dividers);
		}
		dividers.clear();
	}	
};


void Ex_25::ex_22_mpi(int start, int finish, int argc, char** argv){

	MPI_Init(&argc, &argv);
	 int rank, size;
	 int main_rank = 0;

	 MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	 MPI_Comm_size(MPI_COMM_WORLD, &size);
	 int one_part = (finish - start) / size;

	 double start_time = MPI_Wtime();
	 if (rank == 0){
	 	ex_22(start, finish - (size - 1)*one_part + 1 );
	 }
	 else{
		ex_22(finish - (size - rank)*one_part + 1 , finish - (size - rank - 1)*one_part + 1 );
	 }
	 double end_time = MPI_Wtime();

	 std::vector<float> time_vect;
	 time_vect.resize(4);
	 float time_result = end_time - start_time;
	 MPI_Gather(&time_result, 1, MPI_FLOAT, &time_vect[0], 1, MPI_FLOAT, main_rank, MPI_COMM_WORLD);

	 if (rank == 0){
	 	print_vector(time_vect);
	 }
	 MPI_Finalize();
};

void Ex_25::test_private(std::string& str){
	std::cout << "Before: " <<str << "\n";
	str = str + "QQQQ";
	std::cout << "After: " <<str << "\n";

};

