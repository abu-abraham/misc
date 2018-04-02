#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

int main(int argc, char *argv[]){
    int i = 0;
    int val;
    int a[6];
    for (i=0;i<argc;i++){
        a[i] = atoi(argv[i]);
    }
    double ans = sqrt(((a[1]-a[4])*(a[1]-a[4]))+((a[2]-a[5])*(a[2]-a[5]))+((a[3]-a[6])*(a[3]-a[6])));
    printf("%f",ans);
    return 0;
}