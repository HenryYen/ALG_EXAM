#include <iostream>
#include <cstring>
#include <fstream>
#include <sstream>
using namespace std;

string path = "../input";
string fn = path + "/KSP-";
string fn_end = ".txt";

const int MAX_W = 5000000;
const int MAX_N = 1000;
struct Item {int cost, weight;} items[MAX_N];
int dp[MAX_W + 1];

int ksp(int w, int n){
    for (int i = 0; i < n; ++i){
        int weight = items[i].weight;
        int cost = items[i].cost;
        for (int j = w; j - weight >= 0; --j)
            dp[j] = max(dp[j], dp[j - weight] + cost);
    }
    return dp[w];
}

string int2str(int &i) {
    string s;
    stringstream ss(s);
    ss << i;
    return ss.str();
}

int main()
{
    int w, n;

    for (int q = 0 ; q < 5 ; q++){
        string fn_all = fn;
        fn_all.append(int2str(q));
        fn_all.append(fn_end);
        ifstream myfile(fn_all.c_str());
        myfile >> w >> n ;
        for (int i=0 ; i<n ; i++)
            myfile >> items[i].cost >> items[i].weight;
        myfile.close();

        memset(dp, 0, sizeof(dp));
        cout << ksp(w, n) << endl;
    }
    return 0;
}

/*  107
50 7
70 31
20 10
39 20
37 19
7 4
5 3
10 6
*/

/*   1735
170 7
442 41
525 50
511 49
593 59
546 55
564 57
617 60
*/
