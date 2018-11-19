import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.*;


public class Solution {

    // Complete the hourglassSum function below.
    static int hourglassSum(int[][] arr) {
        Integer maxSum = null;
        for (int i=0; i <= arr[0].length -3; i++){
            for (int j=0; j<= arr[1].length-3; j++){
                int groupSum = 0;
                for (int i1=i; i1<i+3;i1++){
                    for(int j1=j; j1<j+3;j1++){
                        if (!((i1-i)==1 && ((j1-j)==0 || (j1-j)==2))){
                             groupSum+=arr[i1][j1];
                        }                       
                    }
                }
                System.out.println(groupSum);
                if (maxSum == null || groupSum > maxSum) {
                    maxSum = groupSum;
                }
            }
        }
    return maxSum;
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException {
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        int[][] arr = new int[6][6];

        for (int i = 0; i < 6; i++) {
            String[] arrRowItems = scanner.nextLine().split(" ");
            scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

            for (int j = 0; j < 6; j++) {
                int arrItem = Integer.parseInt(arrRowItems[j]);
                arr[i][j] = arrItem;
            }
        }

        int result = hourglassSum(arr);

        bufferedWriter.write(String.valueOf(result));
        bufferedWriter.newLine();

        bufferedWriter.close();

        scanner.close();
    }
}

