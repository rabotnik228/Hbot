#include <iostream>
#include <string>
#include "md5.h"
#include <fstream>

using namespace std;
bool finded = false;
std::string out = "";
int get_index(char symbol, std::string s){
    for(int i = 0; i < s.length(); i++){
        if(s[i] == symbol){
            return i + 1;
        }
    }
}
std::string wordlist(std::string hash){
    std::ifstream file("C:\\realhuman_phill.txt" , std::ios::binary | std::ios::in);
    std::string str;
    while(true){
        getline(file , str);
        if(file.fail())
            break;
        std::string hash_buffer = md5(str);
        if (hash_buffer.compare(hash) == 0){
            return str;
        }
        std::cout<<str<<endl;
    }
    return "Password isn't in this list";
}
void permute(string str, std::string out1, int n, int k, string hash) {
    if (k == 0) {
        string hash_buffer = md5(out1);
        int result = hash_buffer.compare(hash);
        if(result == 0){
            finded = true;
            return;
        }
        out = out1;
        cout << out1 << "\r";
        return;
    }

    for (int i = 0; i < n; i++) {
        string newOut = out1 + str[i];
        if (not finded){
            permute(str, newOut, n, k - 1, hash);
        }
    }
}

int main() {
    std::cout << "Pick type of crack:\n"<< endl;
    std::cout << "1 - dictionary search" << endl;
    std::cout << "2 - bruteforce" << endl;
    int num_of_crack;
    std::cin >> num_of_crack;
    std::string input_hash = "";
    std::cout << "Type hash" << endl;
    std::cin >> input_hash;
    std::cout << "Pick alphabet: 1 - ( !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~')\n"<< endl;
    std::cout << "2 - (ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789)\n" << endl;
    std::cout << "3 - (abcdefghijklmnopqrstuvwxyz0123456789)\n" << endl;
    std::cout << "4 - (0123456789)\n" << endl;
    int number_of_alpa;
    std::cin >> number_of_alpa;
    std::string str;
    if (num_of_crack == 1){
        wordlist(input_hash);
    }
    if (num_of_crack == 2){


    if (number_of_alpa == 1){
        str = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~'";
    }
    if (number_of_alpa == 2){
        str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    }if (number_of_alpa == 3){
        str = "abcdefghijklmnopqrstuvwxyz0123456789";
    }if (number_of_alpa == 4){
        str = "0123456789";
    }
    clock_t tStart = clock();
    for (int i=0; i < 8; i++){
        if (finded){
            break;
        }
        permute(str, std::string (""), str.length(), i, input_hash);}
    if (finded){
        int index = get_index(out.back(), str);
        out.back() = str[index];
        cout << "*** Pass found ***      ->      " << out.c_str() << endl;
    }
    printf("Time taken: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);}
    system("PAUSE");
    return 0;
}