#include <iostream>
using namespace std;

int main()
{
 int arr[] = { 10, 20, 30, 40 };

 for (auto x : arr)
 ++x;
 for (auto x : arr)
 cout << x << endl;
 }