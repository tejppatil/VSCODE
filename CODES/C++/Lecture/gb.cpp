#include<iostream>
using namespace std;
class demo

{

int count;

public:

void getcount()

{

count = 0;

cout<<"count="<< ++count;

}

};

int main()

{

demo d1,d2,d3;

d1.getcount();

d2.getcount();

d3.getcount();

return 0;

}