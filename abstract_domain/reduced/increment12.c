#include <stdlib.h>
#include <stdio.h>
//extern "C"{


void reduction(int &l1, int &r1, int &l2, int &r2){
    int max = l1 > l2 ? l1 : l2;
    int min = r1 < r2 ? r1 : r2;

    if(max % 2 == 1 || (max % 2) == -1){
        l2 = max - 1;
    }
    else{
        l1 = max - 1;
    }
    if(min % 2 == 1 || (max % 2) == -1){
        r2 = min + 1;
    }
    else{
        r1 = min + 1;
    }

}


int isOdd(int x){
    return x % 2 == 1 || x % 2 == -1;
}

int isEven(int x){
    return x % 2 == 0;
}

///*
int GammaCheckoddIntv(int left1, int right1, int c){
    if(left1 % 2 == 0) 
        {printf("Ye nhi hona tha: Odd: %d, %d\n", left1, right1);exit(0);}
    if(right1 % 2 == 0) {printf("Ye nhi hona tha: Odd: %d, %d\n", left1, right1);exit(0);}

    if(left1 > right1) {printf("Ye nhi hona tha: Odd right is smaller: %d, %d\n", left1, right1);exit(0);}

    if(left1 <= c && c <= right1)
        return 1; 
    return 0;
}

int GammaCheckevenIntv(int left1, int right1, int c){
    if(left1 % 2 == 1 || left1 % 2 == -1) {printf("Ye nhi hona tha: Even: %d, %d\n", left1, right1);exit(0);}
    if(right1 % 2 == 1 || right1 % 2 == -1) {printf("Ye nhi hona tha: Even: %d, %d\n", left1, right1);exit(0);}

    if(left1 > right1) {printf("Ye nhi hona tha: even, right is smaller: %d, %d\n", left1, right1);exit(0);}


    if(left1 <= c && c <= right1)
        return 1; 
    return 0;
}
//*/

int GammaCheck(int leftO, int rightO, int leftE, int rightE, int c){
    printf("In domain.cc: %d, %d, %d, %d, %d\n", leftO, rightO, leftE, rightE, c );
    if(((leftO > rightO) || (leftE > rightE)) && !(leftE == leftO && leftE == -1 && rightE == rightO && rightE == 0)) exit(0);
    if(!isOdd(leftO)) exit(0);
    if(!isOdd(rightO)) exit(0);
    if(leftE % 2 != 0) exit(0);
    if(rightE % 2 != 0) exit(0);
    if(leftO <= c && c <= rightO && leftE <= c && c <= rightE)
        return 1; 
    return 0;
}

void Beta(int c, int * beta){
    if(isOdd(c)){ // odd
        beta[0] = c;
        beta[1] = c;
        beta[2] = c - 1;
        beta[3] = c + 1;
    }
    else{
        beta[0] = c - 1;
        beta[1] = c + 1;
        beta[2] = c;
        beta[3] = c;
    }
}

int min1(int a, int b){
    int _out;
    if (a<b) _out = a;
    else _out = b;
    return _out;
}

int max1(int a, int b){
    int _out;
    if (a>b) _out = a;
    else _out = b;
    return _out;
}
int Gamma(int left1, int right1, int left2, int right2, int* conc){
    int j = 0;
    /*
       int left = left1 < left2 ? left1 : left2;
       int right = right1 > right2 ? right1 : right2;
     */
    if(right1 < left2 || right2 < left1){
        conc[0] = -1;
        conc[1] = 0;
        return 0;
    }
    else{
        int left = max1(left1, left2);
        int right = min1(right1, right2);
        for(int i = left; i <= right; i++)
            conc[j++] = i;
        return j;
    }
}



void Join(int leftOdd1, int rightOdd1, int leftEven1, int rightEven1, int leftOdd2, int rightOdd2, int leftEven2, int rightEven2,int* join){
    join[0] = min1(leftOdd1, leftOdd2);
    join[1] = max1(rightOdd1, rightOdd2);
    join[2] = min1(leftEven1, leftEven2);
    join[3] = max1(rightEven1, rightEven2);
}
//}
