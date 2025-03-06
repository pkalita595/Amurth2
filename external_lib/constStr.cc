int* intcat(int* str1, int* str2){
    int * out = (int*) malloc(sizeof(int) * 20);
    int j = 1;
    out[0] = str1[0] || str2[0];
    for(int i=1; str1[i] != 0; i++){
        out[j++] = str1[i];
    }

    for(int i=1; str2[i] != 0; i++){
        out[j++] = str2[i];
    }
    
    out[j] = 0;
    return out;
}
