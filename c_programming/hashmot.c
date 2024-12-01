#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main() {
    double limit = pow(2, 32);
    int lines = 3;
    int i = 0;
    for (i = 0; i < lines; i++) {
        int hash, opp, diff;
        printf("\nEnter a number of Soldiers : ");
        scanf("%d %d", &hash, &opp);
        if (hash > limit || opp > limit) {
            printf("Soldiers cant't be bigger than 2^32\n");
            return 0;
        }
        diff = abs(hash - opp);
        printf("%d", diff);
    }
    


}
