#include<iostream>
#include<vector>
#include<string>
// #include <mpi.h>

class Ex_25{

	public:

		// Ex_25();

		

		// std::vector<std::vector<int>> ex_17_mpi(int n);

		void test_mpi(int, int, int argc, char** argv);

		
		void ex_22_mpi(int, int, int argc, char** argv);

	private:
		
		std::vector<std::vector<int> > ex_17(int, int, int);

		void ex_22(int, int);

		void test_private(std::string& );

		// int start, finish;

};