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

    int GammaCheckOdd(int left, int right, int c){
        //checkVal(left);
        //checkVal(right);
        if(left % 2 == 0) exit(0);
        if(right % 2 == 0) exit(0);
        if(left>right) exit(0);
        //checkVal(c);
        if(left <= c && c <= right)
            return 1; //True
        return 0;
    }

    int GammaCheckEven(int left, int right, int c){
        //checkVal(left);
        //checkVal(right);
        if(left % 2 != 0) exit(0);
        if(right % 2 != 0) exit(0);
        if(left>right) exit(0);
        //checkVal(c);
        if(left <= c && c <= right)
            return 1; //True
        return 0;
    }


    int GammaCheck(int left, int right, int c){
        //checkVal(left);
        //checkVal(right);
        if(left>right) return 0;
        //checkVal(c);
        if(left <= c && c <= right)
            return 1; //True
        return 0;
    }

    void Beta(int c, int * beta){
        beta[0] = c;
        beta[1] = c;
    }

    int Gamma(int left, int right,int* conc){
        int j = 0;
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


    void Join(int left1, int right1, int left2, int right2, int* join){
        join[0] = min1(left1, left2);
        join[1] = max1(right1, right2);
    }
}
