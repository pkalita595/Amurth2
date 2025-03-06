#include<stdlib.h>

int getLength(int* str1){
    int i;
    for(i = 0; str1[i] != 0 && i < 10; i++);
    return i;
}


int* stringTrim(int* str1){
    int N = 5;
    int* temp = (int*) calloc(2*N, sizeof(int));
    int i;
    int size = getLength(str1);

    //10 is the space

    //for leftTrim
    for(i = 0; str1[i] == 10 && i < 2 * N; i++);
    int start = i;
    int k = 0;

    //for rightTrim
    for(i = size - 1; str1[i] == 10 && i > 0; i--);
    int end = i;

    // update the new trimmed string
    for(i = start; i <= end; i++)
        temp[k++] = str1[i];


    temp[k] = 0;
    return temp;
}


int* trim(int* strSet){
    int K = 3;
    int N = 5;
    int* res = (int*)calloc(2 * N * (K + 1), sizeof(int));
    for(int i = 1; i < K+1; i++){
        int* temp = stringTrim(strSet + (i * 2 * N));
        for(int j = 0; j < 2 * N; j++){
            res[(i * 2 * N) + j] = temp[j];
        }
        free(temp);
    }
    return res;
}


int islower(int x) {
    return (x >= 5) && (x < 15);
}

int isupper(int x) {
    return (x >= 15) && (x <= 24);
}


int isEqual(int* string1, int*  string2){
    int s1 = getLength(string1);
    int s2 = getLength(string2);
    if(s1 != s2) return 0;
    for(int i = 0; string1[i] != 0 && i < 10; i++){
        if(string1[i] != string2[i])
            return 0;
    }

    return 1;
}

// checks whether string is in stringSet
int strContains(int* stringSet, int* string){
    for(int i = 0; i < 3 ; i++){
        if(isEqual(stringSet + (i + 1) * 10, string))
            return 1;
    }
    return 0;
}

int GammaCheck(int* aSet, int* str){
    return strContains(aSet, str);
}

//TOP -> 2
//BOT -> 3
int GammaCheckBool(int boolAbs, int boolConc) {
    if (boolAbs == 2) return 1;
    else if(boolAbs == 3) {std::cout << "BOT CAME IN GAMMACHECK\n"; return 0; }
    else return boolAbs == boolConc;
}

int getStrSetSize(int* strSet){
    int count = 0;
    for(int i = 1; i < 4; i++){
        if(strSet[i*10] != 0)
            count++;
    }
    return count;
}

int* intConcatStr(int* str1, int* str2) {
    int N = 5;
    int K = 3;
    int* result = (int*)calloc(2 * N, sizeof(int));

    int i = 0;
    for (; str1[i] != 0; i++) {
        result[i] = str1[i];
    }

    for (int j = 0; str2[j] != 0; j++) {
        result[i++] = str2[j];
    }
    result[i] = 0;


    return result;
}

int* concatStrSet(int* strSet1, int* strSet2) {
    // concat on concrete string set so flag values are all zero
    int K = 3;
    int N = 5;
    int* result = (int*) calloc(2 * N * 4, sizeof(int));
    int resid = 1;
    int idx = 0;
    int size = 1;
    for (int i = 1; i <= K; ++i){
        if (strSet1[i * 2 * N] == 0) continue;

        for (int j = 1; j <= K; ++j) {

            if (strSet2[j * 2 * N] == 0) continue;
            int* res = intConcatStr(&strSet1[i * 2 * N], &strSet2[j * 2 * N]);

            for(int x = 0; x < 2*N; x++){
                result[size * 2 * N + x] = res[x];
            }

            //memcpy(result + (size * 2 * N), res, 2 * N);
            size++;
            free(res);
        }
    }

    return result;
}

//whether subStr in str
int contains(int* str, int* subStr){
    int subLen = getLength(subStr);
    int strLen = getLength(str);
    int temp = 0;
    for(int i = 0; i <= strLen - subLen; i++){
        for(temp = 0; temp < subLen; temp++){
            if(subStr[temp] != str[i + temp]){
                temp = subLen + 1; // imitating break :p
            }
        }

        if(temp == subLen){
            return 1;
        }
    }
    return 0;
}
