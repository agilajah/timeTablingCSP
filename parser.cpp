#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

vector<string> split(string data, string token)
{
    vector<string> output;
    size_t pos = string::npos; // size_t to avoid improbable overflow
    do
    {
        pos = data.find(token);
        output.push_back(data.substr(0, pos));
        if (string::npos != pos)
            data = data.substr(pos + token.size());
    } while (string::npos != pos);
    return output;
}

typedef vector<string> vectorstr;

int main () {

	ifstream prob("Testcase.txt");
	string buff;
	vector<vectorstr> hasilParse;

	if (prob.is_open()) {
		prob >> buff; //READ
		if (buff == "Ruangan") { //PARSE RUANGAN
			prob >> buff;
			while (buff.compare("Jadwal") != 0) {
				hasilParse.push_back(split(buff, ";"));
				prob >> buff;
			}
		}
		
		do { //PARSE JADWAL
				prob >> buff;
				// cout << buff << endl;
				hasilParse.push_back(split(buff, ";"));
		} while (!prob.eof());

	}

	for (int i = 0; i < hasilParse.size(); ++i)
	{
		for (int j = 0; j < hasilParse[i].size(); ++j)
		{
			cout << hasilParse[i][j] << endl;
		}
	}

	prob.close();

	return 0;
}