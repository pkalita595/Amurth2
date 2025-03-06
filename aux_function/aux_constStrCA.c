int min(int a, int b){
    int _out;
    if (a<b) _out = a;
    else _out = b;
    return _out;
}

int max(int a, int b){
    int _out;
    if (a>b) _out = a;
    else _out = b;
    return _out;
}

//concatenate
int* concate(int* str1, int* str2){
        int* temp = (int*) malloc(sizeof(int)*2*10);
        int i;
        for(i=0; str1[i] != 0; i++){
                temp[i] = str1[i];
        }
        int j = i;
        for(i=0; str2[i] != 0; i++){
                temp[j] = str2[i];
                j++;
        }
        temp[j] = 0;
        return temp;
}

void copyArray(int* dest, int* src){
    for(int i=0; i<10; i++)
        dest[i] = src[i];

}

void getLength(int* str, int& length){
    for(int i = 1; i < 10; i++){
        if(str[i] == 0) return;
        length++; 
    }
}
