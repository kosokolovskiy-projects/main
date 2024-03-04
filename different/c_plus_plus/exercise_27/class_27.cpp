#include "class_27.h"
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <unistd.h>
#include <vector>
#include <typeinfo>
#include <cstring>
#include <sstream>
#include <iterator>
#include <map>

namespace fs = std::filesystem;

std::string path_create (std::string&);
std::vector<int> divide_line(std::string);
int max_fun(int, int );
int min_fun(int, int );

template <typename T>
void print_vector(std::vector<T>& vect){
	for (int i{0}; i < vect.size(); ++i){
		std::cout << vect[i] << "\t";
	}
}

void Ex_27::ex_1(std::vector<std::string> vect_init){
	std::string path_A = vect_init[0];
	std::string path_B = vect_init[1];

	for (int i{0}; i < vect_init.size(); ++i){
		ex_1_file_1(vect_init[i]);
	}

}

void Ex_27::ex_1_file_1 (std::string path){
	std::ifstream my_file_1;

	path_create(path);

	std::string str_temp;
	my_file_1.open(path);
	getline(my_file_1, str_temp);
	int rows{stoi(str_temp)};
	std::cout << "rows = " << rows << "\n";

	std::vector<int> numbers_in_line;
	int summ{0};
	int minn{1000000}, n_min, n_1, n_2, dn;
	for (size_t i{0}; i < rows; ++i){
		getline(my_file_1, str_temp);
		numbers_in_line = divide_line(str_temp);
		n_1 = numbers_in_line[0];
		n_2 = numbers_in_line[1];
		dn =  n_1 - n_2;
		if (n_1 > n_2){
			summ += n_1;
			if ((n_1 - n_2) % 3 != 0){
				minn = min_fun(minn, dn);
			}
		}
		else {
			summ += n_2;
			if (n_1 != n_2 and (n_2 - n_1) % 3 != 0){
				minn = min_fun(minn, -dn);
			}
		}

	}
	if (summ % 3 ==0){
		summ -= (minn);
	}


	std::cout << "MIN = " << minn << " and  SUMM = " << summ << "\n";
};

int max_fun(int& a_1, int& a_2){
	if (a_1 > a_2){
		return a_1;
	}
	else {return a_2;}
};

int min_fun(int a_1, int a_2){
	if (a_1 < a_2){
		return a_1;
	}
	else {return a_2;}
};

std::vector<int> divide_line(std::string str){
	std::vector<int> nums;
	std::stringstream ss{str};
	std::string num_str;
	while(ss >> num_str){
		nums.push_back(stoi(num_str));
	} 
	return nums;
};


std::string path_create (std::string& path){
	fs::path path_initial = fs::current_path();
	std::string path_string{path_initial.u8string()};
	std::size_t pos = path_string.find("build"); 
	path_string = path_string.substr (0,pos); 
	path = path_string + path;
	return path_string;
};