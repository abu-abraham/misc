
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.*;

class ParallelComputation implements Callable<Integer>{
    private int i;
    private int j;
    private int[][] arr;

    ParallelComputation(int i, int j, int[][] arr){
        this.i = i;
        this.j = j;
        this.arr = arr;
    }

    @Override
    public Integer call(){
        int groupSum = 0;
        for (int i1=i; i1<i+3;i1++){
            for(int j1=j; j1<j+3;j1++){
                if (!((i1-i)==1 && ((j1-j)==0 || (j1-j)==2))){
                    groupSum+=arr[i1][j1];
                }
            }
        }
        System.out.println("Thread: "+Thread.currentThread().getId()+" retuned "+groupSum);
        return groupSum;
    }

}


public class ThreadTrial {
    int value;

      public static void main(String args[]) {
        int[][] arr = new int[10][10];
        for (int i=0; i<10;i++){
            for (int j=0; j<10;j++){
                arr[i][j] = i+j;
            }

        }
        ExecutorService executor = Executors.newFixedThreadPool(100);
        //create a list to hold the Future object associated with Callable
        List<Future<Integer>> list = new ArrayList<Future<Integer>>();
        //Create MyCallable instance
        for (int i=0; i <= arr[0].length -3; i++){
            for (int j=0; j<= arr[1].length-3; j++){
                Future<Integer> future = executor.submit(new ParallelComputation(i,j,arr));
                //add Future to the list, we can get return value using Future
                list.add(future);
            }
        }
//        try{
//            executor.awaitTermination(1, TimeUnit.SECONDS);
//        }catch(InterruptedException e){
//            e.printStackTrace();
//        }
        int maxValue = 0;
        for(Future<Integer> fut : list){
            try {
                //print the return value of Future, notice the output delay in console
                // because Future.get() waits for task to get completed
                int value = fut.get();
                if (maxValue < value){
                    value = maxValue;
                }
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        }
        //shut down the executor service now
        executor.shutdown();
    }
}

