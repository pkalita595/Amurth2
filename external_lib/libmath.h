#ifndef _LIB_MATH
#define _LIB_MATH
#include <inttypes.h>
extern "C"{
    int absSum(int , int );
    int add(int, int);
    int subtract(int, int);
    uint8_t subtractUnsigned(uint8_t, uint8_t);
    uint8_t multiplicationUnsigned(uint8_t, uint8_t);
    int multiplication(int , int);
    int divide(int, int);
    int uMinus(int);
    int increment(int);
    int bitAnd(int, int);
    int bitOr(int, int);
    int bitXor(int, int);
    int bitNot(int);
    int lshl(int, int);
    int lshr(int, int);
    int ashr(int8_t, int8_t);
}
#endif
