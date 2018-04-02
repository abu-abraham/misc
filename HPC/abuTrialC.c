#include<stdio.h>

void square_array(int n, double* ina, double* outa)
{
    int i;
    for (i=0; i<n; i++){
        printf("%f\n",ina[i]);
        outa[i] = ina[i];
    }
}