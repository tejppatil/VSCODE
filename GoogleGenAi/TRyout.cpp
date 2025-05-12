#include <fstream>
#include <iostream>
using namespace std;

int main()
{
    // Create and open "data.csv" for writing
    ofstream output("data.csv");

     if (!output)
    {
        cerr << "Error opening file for writing." << endl;
        return 1;
    }
    output << "Sid, 001" << endl;
    output << "Sname, Ash" << endl;
    output << "grade, A+" << endl;
    output.close();
    system("start data.csv");
    return 0;
}
 

