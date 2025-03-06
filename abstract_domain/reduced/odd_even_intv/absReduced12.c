#include <stdlib.h>
extern "C"{
    void checkVal(int val){
        if(val < -200 || val > 200) exit(0);
    }


    int isOdd(int x){
        return x % 2 == 1;
    }

    int isEven(int x){
        return x % 2 == 0;
    }

    int modularMinus(int a, int b){
        int temp = a - b;
        int val = temp % 16;
        if(val < 0) return 16 + val;
        else return val;
    }
    int modularAdd(int a, int b){
        int temp = a + b;
        int val = temp % 16;
        if(val < 0) return 16 + val;
        else return val;
    }
    int modularMul(int a, int b){
        int temp = a * b;
        int val = temp % 16;
        if(val < 0) return 16 + val;
        else return val;
    }

    int GammaCheckOdd(int left1, int right1, int left2, int right2, int c){
        if(left1 % 2 == 0) exit(0);
        if(right1 % 2 == 0) exit(0);
        if(left2 % 2 == 0) exit(0);
        if(right2 % 2 == 0) exit(0);
        if(left1 > right1) exit(0);
        if(left2 > right2) exit(0);
        if(left1 <= c && c <= right1 && left2 <= c && c <= right2)
            return 1; 
        return 0;
    }

    int GammaCheckEven(int left1, int right1, int left2, int right2, int c){
        if(left1 % 2 == 1) exit(0);
        if(right1 % 2 == 1) exit(0);
        if(left2 % 2 == 1) exit(0);
        if(right2 % 2 == 1) exit(0);
        if(left1 > right1) exit(0);
        if(left2 > right2) exit(0);
        if(left1 <= c && c <= right1 && left2 <= c && c <= right2)
            return 1; 
        return 0;
    }


    int GammaCheck(int leftO, int rightO, int leftE, int rightE, int c){
        if(leftO > rightO && leftE > rightE) return 0;
        if(leftO % 2 != 1) exit(0);
        if(rightO % 2 != 1) exit(0);
        if(leftE % 2 != 0) exit(0);
        if(rightE % 2 != 0) exit(0);
        if(leftO <= c && c <= rightO && leftE <= c && c <= rightE)
            return 1; 
        return 0;
    }

    void Beta(int c, int * beta){
        beta[0] = c;
        beta[1] = c;
    }

    int Gamma(int left1, int right1, int left2, int right2, int* conc){
        int j = 0;
        int left = left1 < left2 ? left1 : left2;
        int right = right1 > right2 ? right1 : right2;
        for(int i = left; i <= right; i++)
            conc[j++] = i;
        return j;
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


    void Join(int leftOdd1, int rightOdd1, int leftEven1, int rightEven1, int leftOdd2, int rightOdd2, int leftEven2, int rightEven2,int* join){
        join[0] = min1(leftOdd1, leftOdd2);
        join[1] = max1(rightOdd1, rightOdd2);
        join[2] = min1(leftEven1, leftEven2);
        join[3] = max1(rightEven1, rightEven2);
    }
}
