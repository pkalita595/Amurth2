/// Integer array concatination same as string (char array) concat
int* intcat(int* str1, int* str2){
    int * out = (int*) calloc(2 * N, sizeof(int));
    int j = 0;
    for(int i = 0; str1[i] != 0; i++){
        out[j++] = str1[i];
    }

    for(int i = 0; str2[i] != 0; i++){
        out[j++] = str2[i];
    }

    out[j] = 0;
    return out;
}

