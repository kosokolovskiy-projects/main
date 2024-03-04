#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <mpi.h>
#include <chrono>
#include <map>

#include "test_class/Test_class.h"
#include "exercise_25/class_25.h"
#include "exercise_26/class_26.h"
#include "exercise_27/class_27.h"

using namespace std;
using namespace std::chrono;

template <typename T>
void print_vector(vector<T>&);

template <typename T>
void print_vector_vector(vector<vector<T>>&);


int main(int argc, char** argv){

	map<string, int> numbers = {
		{"start_17", 293123456},
		{"end_17"  , 295123456},

		{"start_22", 45000000},
		{"end_22"  , 50000000}
	};

	map<string, string> paths_26 = {
		{"ex_26_1",  "exercise_26/files/26_demo_1.txt"},
		{"ex_26_2",  "exercise_26/files/26_demo_2.txt"},
		{"ex_26_16", "exercise_26/files/26_demo_16.txt"},
		{"ex_26_18", "exercise_26/files/26_demo_18.txt"},
		{"ex_26_27", "exercise_26/files/26_demo_27.txt"},
		{"ex_26_29", "exercise_26/files/26_demo_29.txt"}
	};

	vector<vector<string>> paths_27{
		{"1"},
		{"exercise_27/files/27-A_demo_1.txt", "exercise_27/files/27-B_demo_1.txt"}
	};




	Ex_25 sol;
	Ex_26 sol_26;
	Ex_27 sol_27;
	// sol.test_mpi(numbers["start_17"], numbers["end_17"] , argc, argv);
	// sol.ex_22_mpi(numbers["start_22"], numbers["end_22"], argc,  argv);

	// print_vector(paths_27[1]);
	sol_27.ex_1(paths_27[1]);


}

template <typename T>
void print_vector(vector<T>& vect){
	for (int i=0; i < vect.size(); ++i){
		cout << vect[i] << '\t';
	}
	cout << '\n';
}

template <typename T>
void print_vector_vector(vector<T>& vect){
	for (int i{0}; i < vect.size(); ++i){
		for (int j{0}; j<vect[i].size(); ++j){
			cout << vect[i][j] << '\t';
		}
	}
	cout << '\n';
}