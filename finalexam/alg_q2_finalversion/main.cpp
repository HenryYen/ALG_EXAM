#include <cstdio>
#include <algorithm>
#include <cmath>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstring>
using namespace std;

struct Record {
    int idx1, idx2;
    Record(int idx1, int idx2){
        if (idx1 > idx2){
            this -> idx2 = idx1;
            this -> idx1 = idx2;
        }
        else{
            this -> idx1 = idx1;
            this -> idx2 = idx2;
        }
    }
};

struct Point{
    int x;
    int y;
};

const int MAX_P = 250000;
string path = "../input";
string fn = path + "/2DCP-";
string fn_end = ".txt";
vector<Record> result;
double minimum;
int N;

bool cmp(Point a,Point b)
{
    return a.x<b.x;
}
bool cmd(const Record & r1, const Record & r2)
{
   if (r1.idx1 != r2.idx1) return r1.idx1 < r2.idx1;
   return r1.idx2 < r2.idx2;
}
double distance(Point a,Point b);
double divide(Point a[],int low,int high);
double combine(Point a[],int low,int mid,int high,double min_left,double min_right);
int getIndex(Point a);
string int2str(int &i) ;
Point  point[MAX_P], duplicate[MAX_P];

int main()
{
    for (int q=0 ; q<5 ; q++){
        minimum = 99999;
        result.clear();
        string fn_all = fn;
        fn_all.append(int2str(q));
        fn_all.append(fn_end);
        ifstream myfile(fn_all.c_str());
        myfile >> N ;
        for(int i=0;i<N;i++){
            myfile >> point[i].x >> point[i].y;
            //scanf("%lf %lf",&point[i].x,&point[i].y);
            duplicate[i].x = point[i].x;
            duplicate[i].y = point[i].y;
        }
        sort(point,point+N,cmp);
        double dis=divide(point,0,N-1);
        if(dis>=20000.0) printf("INFINITY\n");
        else printf("%.2lf %d\n", dis, result.size());

        sort(result.begin(), result.end(), cmd);
        for (int i=0 ; i<result.size() ; i++)
            printf("%d %d\n", result[i].idx1, result[i].idx2);
        cout <<endl;
    }
    return 0;
}
double Distance(Point a,Point b)
{
    return (double)sqrt(pow(a.x-b.x,2)+pow(a.y-b.y,2));
}
double divide(Point a[],int low,int high)
{
    if(low>=high) return 99999;  //切到只剩1個點，return inf

    int mid=(low+high)/2;
    double min_left=divide(a,low,mid);
    double min_right=divide(a,mid+1,high);
    return combine(a,low,mid,high,min_left,min_right);
}
double combine(Point a[],int low,int mid,int high,double min_left,double min_right)
{
    double d=(min_left<min_right)?min_left:min_right;
    double line=(double)(a[mid].x+a[mid+1].x)*0.5; //line:左集合與右集合的中間線x座標
    double min_D=d;
    for(int i=mid+1;a[i].x<line+d && i<=high;i++){ //枚舉line+-d範圍內左右集合的點
        for(int j=mid;a[j].x>line-d && j>=low;j--){
            double temp=Distance(a[i],a[j]);
            if(temp<min_D) min_D=temp;

            if(temp < minimum){
                minimum = temp;
                result.clear();
                result.push_back(Record(getIndex(a[i]), getIndex(a[j])));
            }
            else if(temp == minimum){
                result.push_back(Record(getIndex(a[i]), getIndex(a[j])));
            }
        }
    }
    return min_D;
}
int getIndex(Point a){
    for(int i=0 ; i<N ; i++){
        if (a.x == duplicate[i].x && a.y == duplicate[i].y)
            return i + 1;
    }
    return -1;
}

string int2str(int &i) {
    string s;
    stringstream ss(s);
    ss << i;
    return ss.str();
}

/*
9
4630 3958
637 9585
4911 15241
8693 4792
11661 10667
10069 15094
15346 1347
14765 8063
13718 13376
*/
/*
9
1108 3991
1679 8588
3981 18409
12268 6050
9210 9969
8601 18191
18783 380
17297 9099
17173 13924
*/

