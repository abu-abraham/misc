#include<math.h>
#include<stdio.h>

//gcc -c libfoo.c -fPIC
//gcc -shared -o libfoo.so libfoo.o
//python Assignment1-AbuTrial2.py 2 2 .001 2
double distance(double a1,double b1,double c1, double a2, double b2, double c2){
    //printf("%f  %f  %f  and %f  %f  %f\n",a1,b1,c1,a2,b2,c2);
    return sqrt(((a1-a2)*(a1-a2))+((b1-b2)*(b1-b2))+((c1-c2)*(c1-c2))); 
}



//WORKING FINE
double findPotential(int count, int index, double** array){
    double rij,isum = 0;
    for (int i =0;i< count;i++){
        if (i!=index && i<index){
            rij = distance(array[i][0],array[i][1],array[i][2],array[index][0],array[index][1],array[index][2]);
            isum=isum+(1/pow(rij,12)-2/pow(rij,6));
        }
    }

    return isum;

}
//WORKING FINE
double potentialEnergy(int count, double** array)
{
   int ii = 0;
   double s,sum = 0;
   for (ii=0;ii<count;ii++){
        s=findPotential(count,ii,array);
        sum = sum+s;
   }
   //printf("%f\n",sum);
   return sum;

}

double* forceCoordinates(int count,int index,double ** array){
    int ii,jj;
    double rij,const_quantity= 0;
    double Fx,Fy,Fz = 0;
    static double F[3];
    for (ii=0;ii<count;ii++){
        if(ii!=index){
            rij = distance(array[ii][0],array[ii][1],array[ii][2],array[index][0],array[index][1],array[index][2]);
            const_quantity = (12/pow(rij,14))-(12/pow(rij,8));
            Fy+=const_quantity*(array[ii][1]-array[index][1]);
            Fz+=const_quantity*(array[ii][2]-array[index][2]);
            Fx+=(const_quantity*(array[ii][0]-array[index][0]));
            
      }  
    }
    F[0]=Fx;
    F[1]=Fy;
    F[2]=Fz;
    return F;

}

void updateCoordinates(int count, double** array, float tstep,double** velocity,double** acceleration){
    for(int i =0;i<count;i++){
        double* new_acceleration = forceCoordinates(count,i,array);
        array[i][0] = array[i][0]+tstep*(velocity[i][0]+(tstep*acceleration[i][0])/2);
        array[i][1] = array[i][1]+tstep*(velocity[i][1]+(tstep*acceleration[i][1])/2);
        array[i][2] = array[i][2]+tstep*(velocity[i][2]+(tstep*acceleration[i][2])/2);

        velocity[i][0] = velocity[i][0] + tstep*(acceleration[i][0]+new_acceleration[0])/2;
        velocity[i][1] = velocity[i][1] + tstep*(acceleration[i][1]+new_acceleration[1])/2;
        velocity[i][2] = velocity[i][2] + tstep*(acceleration[i][2]+new_acceleration[2])/2;
        acceleration[i] = new_acceleration;
    }
}