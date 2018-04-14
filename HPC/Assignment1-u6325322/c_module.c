#include<math.h>
#include<stdio.h>
#include <sys/time.h>
#include <papi.h>
#include <stdlib.h>

long micro_seconds_Update = 0;
long micro_seconds_Force = 0;
long micro_seconds_Velocity=0;

long long total_cycles=0;
long long total_instructions= 0;
long long L1_cache_miss =0;
long long L2_cache_miss = 0;
long long Brach_prediction_miss = 0;
long long Total_execution_time = 0;
int active = 1;
int num_events = 6;
int retval = 0;
long long StartTime;

int iter = 0;
int stopped_at =0;


//Function to intialize PAPI Modules 

void initialize(){
    int events[num_events];
    events[0] = PAPI_TOT_CYC;
    events[1] = PAPI_TOT_INS;
    events[2] = PAPI_L1_TCM;
    events[3] = PAPI_L2_TCM;
    events[4] = PAPI_BR_MSP;


    if(PAPI_library_init(PAPI_VER_CURRENT) != PAPI_VER_CURRENT){
		printf("PAPI Library initialization error\n");
		exit(1);
	}
	
	if ((retval = PAPI_start_counters(events, num_events)) != PAPI_OK){
		printf("PAPI Start counter error! %d\n", PAPI_start_counters(events, num_events));
		exit(1);
	}
}

//Function to compute the distance
double distance(double a1,double b1,double c1, double a2, double b2, double c2){
    return sqrt(((a1-a2)*(a1-a2))+((b1-b2)*(b1-b2))+((c1-c2)*(c1-c2)));
}

//Function to find the PE of each atom
double findPotential(int count, int index, double** array){
    double rij,isum = 0;
        int i = 0;
    for (i =0;i< count;i++){
        if (i<index){
            rij = distance(array[index][0],array[index][1],array[index][2],array[i][0],array[i][1],array[i][2]);
            isum = isum+(1/pow(rij,12)-2/pow(rij,6));
        }
    }
    return isum;
}

//Function to compute PE of the system
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

//Function to compute force Coordinates
double* forceCoordinates(int count,int index,double ** array){

    struct timeval start, end;
    long secs_used,micros_used;
    gettimeofday(&start, NULL);

    
    int ii,jj;
    long double rij,const_quantity;
    double Fx,Fy,Fz;
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
    secs_used=(end.tv_sec - start.tv_sec);
    micro_seconds_Force+=((secs_used*1000000) + end.tv_usec) - (start.tv_usec);
    return F;

}

//Function to call update coordinates , called from python module. Values are updated in shared array

void updateCoordinates(int count, double** array, float tstep,double** velocity,double** acceleration){
    float real_time, proc_time, total_proc_time;
    long long flpops;
    float mflops;



    double X[count][3];
    int i = 0;
    int j = 0;

    for(i =0;i<count;i++){
        X[i][0]=0;
        X[i][1]=0;
        X[i][2]=0;

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

//Function to call update coordinates , called from python module. Values are updated in shared array
void updateCoordinates_(int count, double** array, float tstep,double** velocity,double** acceleration){

    struct timeval start, end;
    long secs_used,micros_used;
    struct timeval start_vel, end_vel;
    long secs_used_vel,micros_used_vel;
    gettimeofday(&start, NULL);


    if(Total_execution_time==0){
        printf("Initializing PAPI\n");
        initialize();

        total_instructions = 0;
        total_cycles = 0;
        L1_cache_miss= 0;
        L2_cache_miss=0;
        Brach_prediction_miss=0;
        Total_execution_time=0;
    }


   	StartTime = PAPI_get_virt_usec();


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

    long long StopTime = PAPI_get_virt_usec();
    long long values[num_events];

	if (active==1 && (retval = PAPI_read_counters(values, num_events)) != PAPI_OK){
		printf("PAPI stop counters error ,%d \n",PAPI_stop_counters(values, num_events));
        active=0;
        stopped_at=iter;
	}else{
        iter+=1;
	    long long exec_time = StopTime - StartTime;
        total_cycles=total_cycles+values[0];
        total_instructions=total_instructions+values[1];
        L1_cache_miss=L1_cache_miss+values[2];
        L2_cache_miss=L2_cache_miss+values[3];
        Brach_prediction_miss=Brach_prediction_miss+values[4];
        Total_execution_time+=exec_time;
    }

    
}


void profiling(){

    printf("Manual Profiling results (in uS)\n");
    printf("Micro seconds taken for entire position update process in C : %lu\n",micro_seconds_Update);
    printf("Micro seconds taken for finding force : %lu\n",micro_seconds_Force);
    printf("Micro seconds taken for finding velocity : %lu\n",micro_seconds_Velocity);
    printf("Micro seconds taken for updating arrays based on force computed: %lu\n",(micro_seconds_Update-micro_seconds_Force-micro_seconds_Velocity));

    printf("===============================================================================================\n");
    printf("PAPI Counter worked for only %d iterations\n",stopped_at);
    printf("===============================================================================================\n");
    printf("Execution time         : %20lld\n", Total_execution_time);
    printf("Total cycles           : %20lld\n", total_cycles);
    printf("Total instructions     : %20lld\n", total_instructions);
	printf("L1 cache misses        : %20lld\n", L1_cache_miss);
	printf("L2 cache misses        : %20lld\n", L2_cache_miss);
	printf("Brach miss predictions : %20lld\n", Brach_prediction_miss);
    
}
