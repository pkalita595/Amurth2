#include <stdlib.h>
#include "libmath.h"
int absSum(int x, int y){
    return abs(x) + abs(y);
}
int add(int x, int y){
    return x + y;
}

int subtract(int x, int y){
    return x - y;
}

uint8_t subtractUnsigned(uint8_t x, uint8_t y){
    int a= (x - y);
    a = a % 16;
    if(a< 0) return  16 + a;
    return a;
}

uint8_t multiplicationUnsigned(uint8_t x, uint8_t y){
    int a= (x * y);
    a = a % 16;
    if(a< 0) return  16 + a;
    return a;
}
int multiplication(int a, int b){
    return a * b;
}
int divide(int a, int b){
    return a / b;
}

int increment(int a){
    return a + 1;
}

//unary minus
int uMinus(int a){
    return -a;
}
int bitAnd(int a, int b){
    return a & b;
}
int bitOr(int a, int b){
    return a | b;
}
int bitXor(int  a, int b){
    return a ^ b;
}
int bitNot(int a){
    unsigned char temp = a;
    unsigned char out = ~temp;
    return out;
}

int lshl(int op1, int shift){
    return op1 << shift;
}


int lshr(int op1, int shift){
    return op1 >> shift;
}

int ashr(int8_t n, int8_t sh)
{
    int8_t res = n;
    if(sh)
        res = (n & 0x80) | (n >> 1); //arhs1(n);
    for(int i = 0; i < sh - 1; i++){
        res = (res & 0x80) | (res >> 1); //arhs1(res);
    }
    return  (int)res;

  /*  
  uint8_t w = sizeof(uint8_t) << 3;
  uint8_t xsrl = (uint8_t) x >> k;
  uint8_t sign = x & 1 << (w - 1);
  uint8_t mask = ((1 << k) - 1) << (w - k);
  sign & (xsrl |= mask);
  return xsrl;
    */
}
