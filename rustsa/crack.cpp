#include <iostream>
#include <stdio.h>
//using uint128 = unsigned __int128;
typedef unsigned __int128 uint128;

#define UINT128(hi, lo) (((__uint128_t) ((__uint128_t)hi)) << 64 | ((__uint128_t)lo))
int main(int argc, char** argv) {
    uint128 exp = 65537;
    uint128 ciphertext = UINT128(10188453357494244660, 12826417249322753909);

    //pubmod = int(2**128 - 1)

    //for(uint128 i = 0xffffffffffffffff-1; i > 0; i -= 2) {
    for(uint128 i =1;i < 0xffffffffffffffff-1; i += 2) {
        if(UINT128(0xffffffffffffffff, 0xffffffffffffffff) % i == 0)
            printf("%llx\n", i);

    }


}