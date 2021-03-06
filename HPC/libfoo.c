#include<math.h>
#include<stdio.h>
#include <sys/time.h> 

//gcc -c libfoo.c -fPIC
//gcc -shared -o libfoo.so libfoo.o
//python Assignment1-AbuTrial2.py 2 2 .001 2

long micro_seconds_Update = 0;
long micro_seconds_Force = 0;
long micro_seconds_Velocity=0;

double distance(double a1,double b1,double c1, double a2, double b2, double c2){
    return sqrt(((a1-a2)*(a1-a2))+((b1-b2)*(b1-b2))+((c1-c2)*(c1-c2))); 
}

//WORKING FINE
double findPotential(int count, int index, double** array){
    double rij,isum = 0;
    for (int i =0;i< count;i++){
        if (i<index){
            rij = distance(array[index][0],array[index][1],array[index][2],array[i][0],array[i][1],array[i][2]);
            isum = isum+(1/pow(rij,12)-2/pow(rij,6));
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
   return sum;

}

double* forceCoordinates(int count,int index,double ** array){
    struct timeval start, end;
    long secs_used,micros_used;
    gettimeofday(&start, NULL);
    int ii,jj;
    long double rij,const_quantity;
    double Fx,Fy,Fz;
    //C doesnt initialize all variables to 0 when written double Fx,Fy,Fz=0.0 -- WHY?!!
    Fx=0.0;
    Fy=0.0;
    Fz=0.0;
    rij=0.0;
    const_quantity=0.0;
    static double F[3];
    for (ii=0;ii<count;ii++){
        if(ii!=index){
            rij = distance(array[index][0],array[index][1],array[index][2],array[ii][0],array[ii][1],array[ii][2]);
            const_quantity = 12/pow(rij,14)-12/pow(rij,8);
            Fx+=const_quantity*(array[index][0]-array[ii][0]);
            Fy+=const_quantity*(array[index][1]-array[ii][1]);
            Fz+=const_quantity*(array[index][2]- array[ii][2]);
            
      }  
    }
    F[0]=Fx;
    F[1]=Fy;
    F[2]=Fz;
    gettimeofday(&end, NULL);
    secs_used=(end.tv_sec - start.tv_sec); //avoid overflow by subtracting first
    micro_seconds_Force+=((secs_used*1000000) + end.tv_usec) - (start.tv_usec);
    return F;

}


void updateCoordinates(int count, double** array, float tstep,double** velocity,double** acceleration){
    double X[count][3];
    int i = 0;
    int j = 0;

    for(i=0;i<count;i++){
        X[i][0]=0;
        X[i][1]=0;
        X[i][2]=0;
    }

    for(i =0;i<count;i++){
        double* new_acceleration = forceCoordinates(count,i,array);
        X[i][0] = array[i][0]+tstep*(velocity[i][0]+(tstep*acceleration[i][0])/2);
        X[i][1] = array[i][1]+tstep*(velocity[i][1]+(tstep*acceleration[i][1])/2);
        X[i][2] = array[i][2]+tstep*(velocity[i][2]+(tstep*acceleration[i][2])/2);

        velocity[i][0] = velocity[i][0] + tstep*(acceleration[i][0]+new_acceleration[0])/2;
        velocity[i][1] = velocity[i][1] + tstep*(acceleration[i][1]+new_acceleration[1])/2;
        velocity[i][2] = velocity[i][2] + tstep*(acceleration[i][2]+new_acceleration[2])/2;
        acceleration[i] = new_acceleration;
    }

    for(i =0;i<count;i++){
        array[i][0]=X[i][0];
        array[i][1]=X[i][1];
        array[i][2]=X[i][2];
    }
}

        
void updateCoordinates_(int count, double** array, float tstep,double** velocity,double** acceleration){
    struct timeval start, end;
    long secs_used,micros_used;
    struct timeval start_vel, end_vel;
    long secs_used_vel,micros_used_vel;
    gettimeofday(&start, NULL);
    double X[count][3];
    int i = 0;
    int j = 0;
    for(i=0;i<count;i++){
        X[i][0]=0;
        X[i][1]=0;
        X[i][2]=0;
    }

    for(i =0;i<count;i++){
        double* new_acceleration = forceCoordinates(count,i,array);
        X[i][0] = (array[i][0]+tstep*(velocity[i][0]+(tstep*new_acceleration[0])/2));
        X[i][1] = (array[i][1]+tstep*(velocity[i][1]+(tstep*new_acceleration[1])/2));
        X[i][2] = (array[i][2]+tstep*(velocity[i][2]+(tstep*new_acceleration[2])/2));

        gettimeofday(&start_vel, NULL);
        velocity[i][0] = velocity[i][0] + tstep*(new_acceleration[0]);
        velocity[i][1] = velocity[i][1] + tstep*(new_acceleration[1]);
        velocity[i][2] = velocity[i][2] + tstep*(new_acceleration[2]);
        acceleration[i] = new_acceleration;
        gettimeofday(&end_vel, NULL);
        secs_used_vel=(end_vel.tv_sec - start_vel.tv_sec); //avoid overflow by subtracting first
        micro_seconds_Velocity+=((secs_used_vel*1000000) + end_vel.tv_usec) - (start_vel.tv_usec);

    }

    for(i =0;i<count;i++){
        array[i][0]=X[i][0];
        array[i][1]=X[i][1];
        array[i][2]=X[i][2];
    }


    gettimeofday(&end, NULL);
    secs_used=(end.tv_sec - start.tv_sec); //avoid overflow by subtracting first
    micro_seconds_Update+=((secs_used*1000000) + end.tv_usec) - (start.tv_usec);

    
}

void manual_profiling(){
    printf("Micro seconds taken for entire position update process in C                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              : %lu\n",micro_seconds_Update);
    printf("Micro seconds taken for finding force : %lu\n",micro_seconds_Force); 
    printf("Micro seconds taken for finding velocity : %lu\n",micro_seconds_Velocity); 
    printf("Micro seconds taken for updating arrays based on force computed: %lu\n",(micro_seconds_Update-micro_seconds_Force-micro_seconds_Velocity));
}