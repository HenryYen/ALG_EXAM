#include <iostream>
#include <string>
#include <vector>
#define SIZE 110

using namespace std;

int dp[SIZE][SIZE];
vector< int* > link[SIZE][SIZE];
bool graph[SIZE][SIZE];
vector<string> allLCS;
string sA,sB;

void findAllLCS(char *path,int x,int y,int value);

int main(){
	
	cin >> sA >> sB;

	for(int i=0;i<=sA.size();i++){
		dp[0][i]=0;
	}
	for(int i=0;i<=sB.size();i++){
		dp[i][0]=0;
	}

	for(int i=1;i<=sA.size();i++){
		for(int j=1;j<=sB.size();j++){
			int matchedPlus=0;
			if(sA[i-1]==sB[j-1]){
				matchedPlus=1;
			}
			dp[i][j] = max( max(dp[i-1][j],dp[i][j-1]) , dp[i-1][j-1]+matchedPlus);
		}
	}
	int lcs_length =dp[sA.size()][sB.size()];

	for(int i=1;i<=sA.size();i++){
		for(int j=1;j<=sB.size();j++){
			if( sA[i-1]==sB[j-1] && dp[i][j]==lcs_length ){
				graph[i][j]=true;
			}else{
				graph[i][j]=false;
			}
		}
	}

	for(int i=sA.size();i>=1;i--){
		for(int j=sB.size();j>=1;j--){
			if(graph[i][j]){
				for(int s=1;s<i;s++){
					for(int t=1;t<j;t++){
						if(sA[s-1]==sB[t-1] && dp[s][t]==dp[i][j]-1){
							int *point = new int[2];
							point[0]=s; point[1]=t;
							link[i][j].push_back(point);
							graph[s][t] = true;
						}
					}
				}
			}
		}
	}


	char lcsString[SIZE];
	lcsString[lcs_length+1] = '\0';
	for (int i = 1; i <= sA.size(); i++) {
		for (int j = 1; j <= sB.size(); j++) {
			if (sA[i-1] == sB[j-1] && dp[i][j] == lcs_length){
				findAllLCS(lcsString,i,j,dp[i][j]);
			}
		}
	}
	

	int count = allLCS.size();

	cout << lcs_length << " " << count << endl;

	sort(allLCS.begin(),allLCS.end());
	for (string s : allLCS) { 
		cout << s << endl;
	}

	return 0;
}

void findAllLCS(char *lcsString,int x,int y,int value){
	lcsString[value] = sB[y-1]; 
	if (value == 1) {
		allLCS.push_back(string(lcsString+1));
		return;
	}
	for (int *node: link[x][y]) {
		findAllLCS(lcsString,node[0],node[1],value-1);
	}
}
