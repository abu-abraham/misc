#include<stdio.h>
#include <stdlib.h>

struct randomNode{
    int a;
    int b;
};

void matrix(){
    printf("Inside function \n");
    int A [10][10];
    int i = 0, j =0;

    printf("Enter the value of n \n");
    int n;
    scanf("%d",&n); 
    for (i=0;i<n;i++){
        for(j =0; j< n; j++){
            A[i][j]=rand()%100;
        }
    }

    for (i=0;i<n;i++){
        for(j=0;j<n;j++){
            printf("%d  ",A[i][j]);
        }
        printf("\n");
    }


}

void main(){
    printf("Inside Main \n");
    //matrix();
    struct randomNode *n;
    n = malloc(sizeof(struct randomNode)); 
    n->a = 10;
    n->b= 20;
    printf("%d",n->a);

}