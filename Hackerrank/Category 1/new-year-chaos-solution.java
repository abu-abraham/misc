import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.*;

public class Solution {

    // Complete the minimumBribes function below.
    static void minimumBribes(int[] q) {
        int i = q.length;
        int op =0;
        while (i>0) {
            if (q[i-1]==i) {
                i=i-1;
            } else {
                int j = 0;
                Stack<Integer> stack = new Stack<Integer>();
                while (j < 3 && i-j>0){
                    if (q[i-j-1]!=i){
                        stack.push(q[i-j-1]);
                    }
                    else {
                        int j1=0;
                        while (!stack.empty()) {
                            q[i-j+j1-1]= stack.pop();
                            j1++;
                            op++;
                        }
                        q[i-1]=i;
                        break;
                    }
                    j+=1;
                }
                if(q[i-1]!=i){
                    System.out.println("Too chaotic");
                    return;
                }
                    
                
            }             
        }
        System.out.println(op);
    }

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        int t = scanner.nextInt();
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

        for (int tItr = 0; tItr < t; tItr++) {
            int n = scanner.nextInt();
            scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

            int[] q = new int[n];

            String[] qItems = scanner.nextLine().split(" ");
            scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");

            for (int i = 0; i < n; i++) {
                int qItem = Integer.parseInt(qItems[i]);
                q[i] = qItem;
            }

            minimumBribes(q);
        }

        scanner.close();
    }
}

