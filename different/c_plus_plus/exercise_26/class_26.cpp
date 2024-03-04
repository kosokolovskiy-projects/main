#include "class_26.h"
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
#include <cmath>

namespace fs = std::filesystem;

std::vector<int> divide_string(std::string);

void print_multimap(std::multimap<int, int>);

template <typename T>
void print_vector(std::vector<T>&);

void Ex_26::ex_1(std::string path){
	std::ifstream files;
	path = Ex_26::path_fun(path);
	files.open(path);
	std::string str;
	int number;
	int count {1};
	int people{0};
	int data{0};


	std::string S;
	getline(files, S);
	std::cout << S << "\n";
	std::vector<int> VecStr = divide_string(S);
	people = VecStr[1];
	data = VecStr[0];
	std::vector<int> vect;

	while (true){
		if (files.eof()){
			break;
		}
		if (count < people){
			getline(files, str);
			number = stoi(str);
			vect.push_back(number);
		}
		else {break;}
		count++;

	}
	sort(vect.begin(), vect.end());

	int sum = 0;
	count = 0;
	int max = 0;
	while (sum < data){
		sum += vect[count];
		count += 1;
		if (sum >= data){
			sum -= vect[count]+vect[count-1];
			count -= 1;
			max = vect[count];
			break;
		}
	}
	int size_vect = vect.size();
	int i = 1;
	sum += vect[size_vect - 1];
	while (sum > data){
		sum -= vect[size_vect - i];
		sum += vect[size_vect - i - 1];
		i++;
		if (sum < data){
			max = vect[size_vect - i - 1];
			break;
		}
	}
	std::cout << sum << "  " << count << "  " << max <<"\n";
	files.close();
};

void Ex_26::ex_2(std::string path){
	std::ifstream files;
	path = Ex_26::path_fun(path);
	files.open(path);
	std::string str;
	int number;
	int count {1};
	int people{0};
	int data{0};


	std::string S;
	getline(files, S);
	std::cout << S << "\n";
	std::vector<int> VecStr = divide_string(S);
	people = VecStr[1];
	data = VecStr[0];
	std::vector<int> vect;

	while (true){
		if (files.eof()){
			break;
		}
		if (count < people){
			getline(files, str);
			number = stoi(str);
			vect.push_back(number);
		}
		else {break;}
		count++;

	}
	sort(vect.begin(), vect.end());

	int sum = 0;
	count = 0;
	int max = 0;
	while (sum < data){
		sum += vect[count];
		count += 1;
		if (sum >= data){
			sum -= vect[count]+vect[count-1];
			count -= 1;
			max = vect[count];
			break;
		}
	}
	int size_vect = vect.size();
	int i = 1;
	sum += vect[size_vect - 1];
	while (sum > data){
		sum -= vect[size_vect - i];
		sum += vect[size_vect - i - 1];
		i++;
		if (sum < data){
			max = vect[size_vect - i - 1];
			break;
		}
	}
	std::cout << sum << "  " << count << "  " << max <<"\n";
	files.close();

};

void Ex_26::ex_16(std::string path){
	std::ifstream files;
	path = Ex_26::path_fun(path);
	files.open(path);
	std::string str;
	int number{0};
	getline(files, str);
	int quantity{stoi(str)};

	std::vector<int> under_50;
	std::vector<double> upper_50;

	int num;
	for (int i{0}; i< quantity; ++i){
		getline(files, str);
		num = stoi(str);
		if (num <= 50){
			under_50.push_back(num);
		}
		else {
			upper_50.push_back(num);
		}
	}
	sort(upper_50.begin(),upper_50.end());

	double sum = 0;
	double temp_var;
	int most_valued = 0;
	for (int i{0}; i < upper_50.size(); ++i){

		temp_var = 3*upper_50[i]/4;

		sum += temp_var;

		sum += upper_50[upper_50.size() - i - 1];

		if (i == upper_50.size()/2 - 1){
			std::cout << "MOST VALUED - " << upper_50[i] << "\n";
			break;
		}
	}
	std::cout << "SIZE:   " << upper_50.size() << "\n";
	for (int i {0}; i < under_50.size(); ++i){
		sum += under_50[i];
	}
	sum = ceil(sum);

	for (int i{0}; i < upper_50.size(); i++){
		std::cout << upper_50[i] << "\t";
	}

		std::cout << sum << "\n"; 

};


void Ex_26::ex_18(std::string path){

	std::ifstream my_file;
	path = path_fun(path);
	my_file.open(path);

	std::string first_line;

	getline(my_file, first_line);
	std::vector<int> vec_first_line = divide_string(first_line);
	int total_number =  vec_first_line[0];
	int total_mass = vec_first_line[1];

	std::string num_str;
	std::vector<int> vect_weight_total{};

	int del{0};

	while (true){
		getline(my_file, num_str);
		if (my_file.eof()){break;}
		del = stoi(num_str);
		vect_weight_total.push_back(del);
	}

	// print_vector(vect_weight_total);

	std::multimap<int, int> idx_num;
	std::multimap<int, int> idx_num_sorted;

	int mass_weight{0};
	int num_weights{0};

	for (int i{0}; i < vect_weight_total.size(); ++i){
		idx_num.insert(std::pair<int, int>(i, vect_weight_total[i]));
		idx_num_sorted.insert(std::pair<int, int>(vect_weight_total[i], i));
	}

    for (int i{0}; i < vect_weight_total.size(); ++i){
    	if (vect_weight_total[i] <= 210 && vect_weight_total[i] >= 200){
    		mass_weight += vect_weight_total[i];
    		num_weights++;
    	}
    }

    std::cout << "Current mass = " << mass_weight << " with the number of weights = " << num_weights << "\n";
    int mass_200 = mass_weight;

    std::vector<int> vect_123;
   	for (std::multimap<int,int>::iterator it = idx_num_sorted.begin(); it != idx_num_sorted.end(); ++it) {
   		mass_weight += it->first;
   		vect_123.push_back(it->first);
   		if (mass_weight > total_mass){
   			mass_weight -= it->first;
   			vect_123.pop_back();
   			break;
   		}
   		else{num_weights++;}
	
	}
	std::cout << "VECT SIZE = " << "    " << num_weights << "\n";

	std::cout << "New mass = " << mass_weight << " with the number of weights = " << num_weights << "\n";

	int mass_weight_last = mass_200;

	std::vector<int> mass_vector{mass_200};

	std::multimap<int,int>::iterator it = idx_num_sorted.end();

	sort(vect_weight_total.begin(),vect_weight_total.end());

	int vect_123_size = vect_123.size();
	bool flag = false;

	for (int i{0}; i < vect_123_size ; ++i){
		mass_weight -= vect_123[i];
		for (int k{num_weights-1}; k < vect_weight_total.size() - 1; ++k){
			if (mass_weight + vect_weight_total[k] <= total_mass && (mass_weight + vect_weight_total[k+1]) > total_mass){
					mass_weight += vect_weight_total[k];
					flag = true;
					break;}
		}
		if (!flag){
			mass_weight += vect_123[i];
			flag = false;
		}

		if (mass_weight == total_mass){break;}

	}
	std::cout << "Final mass: " << mass_weight << "   " << num_weights <<  "    " << vect_123_size <<"\n";
};


void Ex_26::ex_27(std::string path){

	std::ifstream my_file;
	path = path_fun(path);
	my_file.open(path);

	std::string temp_string;
	getline(my_file, temp_string);

	int places = stoi(temp_string);
	// std::cout << places << "\n" << typeid(places).name() << "\n";

	std::multimap<int, int> initial_data;
	std::multimap<int, int> initial_row;
	std::multimap<int, int> initial_place;
	for (size_t i{0}; i < places; ++i){
		getline(my_file, temp_string);
		std::vector<int> temp_vect;
		temp_vect = divide_string(temp_string);
		initial_data.insert(std::pair<int, int>(temp_vect[0], temp_vect[1]));
		initial_row.insert(std::pair<int, int>(i, temp_vect[0]));
		initial_place.insert(std::pair<int, int>(i, temp_vect[1]));
	}
	
	print_multimap(initial_data);

	std::multimap<int, int>::iterator it;
	std::multimap<int, int>::iterator it_temp;
	std::multimap<int, int>::iterator temp;
	int max_row = 0;
	int min_min{100000};
	int min_place = 1000000;
	for (it = initial_data.begin(); it != initial_data.end(); ++it ){
		temp = it;
		it_temp = it;
		++it;
		std::cout << "MIN_MIN = " << min_min << "\n"; 
		std::cout <<  it_temp->second << "   " << it->second << "\t" <<" MIN_MIN = " << it_temp->first << "    "<< it->first << "\n"; 
		while(it_temp->first == it->first ){
			if (abs(it_temp->second - it->second) <= min_min and abs(it_temp->second - it->second) >= 2){
				max_row = it_temp->first;
				if (it_temp->second - it->second > 0){
					min_place = it->second;
				}
				else{
					min_place = it_temp->second;
				}
				
				min_min = abs(it_temp->second - it->second);
				std::cout << "MIN_MIN = " << min_min << "\n"; 
			}
			// std::cout << min_place << "\n";
			it_temp++; it++;
		}
		it = temp;
	}
	std::cout << "ROW = " <<max_row << " PLACE = " << min_place + 1 << "  MIN_MIN "  << min_min<<"\n";



};

void Ex_26::ex_29(std::string path){
	std::ifstream my_file;
	path = Ex_26::path_fun(path);
	my_file.open(path);

	std::string initial_data;
	getline(my_file, initial_data);
	std::vector<int> vect_initial_data = divide_string(initial_data);
	int volume{vect_initial_data[1]}, items{vect_initial_data[0]};

	std::string data_line;
	std::vector<int>vect_A;
	std::vector<int>vect_B;
	std::vector<std::string>vect_lett_AB;
	std::vector<int>vect_AB;
	while(true){
		getline(my_file, data_line);

		if (my_file.eof()){
			break;
		}

		std::stringstream ss(data_line);
		std::string word;
		int number_temp;

		while(ss >> word){
			number_temp = stoi(word);
			ss >> word;
			if (word == "A"){
				vect_A.push_back(number_temp);
				vect_lett_AB.push_back("A");
			}
			else{
				vect_B.push_back(number_temp);
				vect_lett_AB.push_back("B");
			}
			vect_AB.push_back(number_temp);
		}
	}

	sort(vect_A.begin(), vect_A.end());
	sort(vect_B.begin(), vect_B.end());
	sort(vect_AB.begin(), vect_AB.end());

	// std::cout << "Size of A: " << vect_A.size() << "\n";
	// std::cout << "Size of B: " << vect_B.size() << "\n";
	// std::cout << "Size of AB: " << vect_AB.size() << "\n";

	int current_sum{0};
	int i_A{0}, i_B{0};
	int idx{0};
	
	while(current_sum < volume){
		current_sum += vect_AB[idx];
		idx++;
	}
	idx--;
	current_sum -= vect_AB[idx];
	std::cout << "First summ: " << current_sum << " with difference: " << volume - current_sum << "\n";

	current_sum = 0;

	int count{0};
	for (int k_total{1}; k_total <= idx+1; k_total++){

		for (int k_A{0}; k_A < k_total; k_A++){
			current_sum += vect_A[k_A];
			count++;
		}
		// std::cout << "count A = " << count << "\n";
		for (int k_B{0}; k_B < idx - k_total; k_B++){
			current_sum += vect_B[k_B];
			i_B++;
			count++;
		}
		if (current_sum < volume){
			std::cout << "B: " <<i_B <<" WITH RESIDUUM: " <<volume - current_sum << "\n";
		}
		i_B = 0;
		count = 0;
		current_sum = 0;
	}


	std::cout << "SIZE TOTAL: " << idx << "\n";
	std::cout << "LAST A:  " << i_A << "\n";
	std::cout << "B number: " << i_B << "\n";


	std::cout << "Number of B: " << i_B << "\n";

	int i_2{0};


	std::cout << "New summ: " << current_sum << " with residuum: " << volume - current_sum << "\n";
	std::cout << "New Number of B: " << i_B + 1 << "\n";
	std::cout << "ANSWER: " << i_B + 1 << volume - current_sum << "\n";

};

	






std::string Ex_26::path_fun(std::string& path){
	fs::path path_initial = fs::current_path();
	std::string path_string{path_initial.u8string()};
	std::size_t pos = path_string.find("build"); 
	path_string= path_string.substr (0,pos); 
	path_string += path;
	return path_string;
};


std::vector<int> divide_string(std::string s){

	std::vector<int> numbers;
    std::stringstream ss{s};
    std::string word;
    while (ss >> word) {
        numbers.push_back(stoi(word));
    }

    return numbers;
};

void print_multimap(std::multimap<int, int> mp){
		std::multimap<int, int>::iterator itr;
	for (itr = mp.begin(); itr != mp.end(); ++itr) {
        std::cout << '\t' << itr->first << '\t' << itr->second
             << '\n';
    }

}

template <typename T>
void print_vector(std::vector<T>& vect){
	for (int i=0; i < vect.size(); ++i){
		std::cout << vect[i] << '\t';
	}
	std::cout << '\n';
}




