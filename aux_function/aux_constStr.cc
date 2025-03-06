#include<stdlib.h>

typedef struct intCP{
        bool isTop;
        bool isBot;
        int value;
} intCP;

class bitStruct;

class bitStruct{
  public:
  bool  isTop;
  bool  isBot;
  bool  flag;
  bitStruct(){}
  static bitStruct* create(  bool  isTop_,   bool  isBot_,   bool  flag_);
  ~bitStruct(){
  }
  void operator delete(void* p){ free(p); }
};

/*
typedef struct bitStruct{
        bool isTop;
        bool isBot;
        bool flag;
} bitStruct;
*/

bitStruct* bitStruct::create(bool  isTop_, bool  isBot_, bool  flag_){
  void* temp= malloc( sizeof(bitStruct) );
  bitStruct* rv = new bitStruct();
  rv->isTop =  isTop_;
  rv->isBot =  isBot_;
  rv->flag =  flag_;
  return rv;
}


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
        int* temp = (int*) calloc(2*10,sizeof(int));
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
/*:
int* contains(int* subStr, int* str){
     int subLen = getLength(subStr);
     int strLen = getLength(str);
     int temp = 0;
     int * out = (int*) calloc(2 * 10 + 1, sizeof(int));
     for(int i = 1; i < strLen - subLen; i++){
         for(temp = 1; temp < subLen; temp++){
             if(subStr[temp] != str[i + temp]){
                 temp = subLen + 1;
             }
         }

         if(temp == subLen){
             out[1] = 1;
             return out;
         }
     }
     return out;
 }
*/

