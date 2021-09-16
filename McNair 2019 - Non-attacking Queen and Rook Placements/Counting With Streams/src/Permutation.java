import java.util.ArrayList;
import java.util.Arrays;

public class Permutation {

    public ArrayList<int[]> PERMS = new ArrayList<>();;

    public static void main(String[] args) {
        int[] list = new int[4];
        for(int i = 0; i < 4; i++){
            list[i] = i+1;
        }
        int n = list.length;
        Permutation permutation = new Permutation();
        permutation.permute(list, 0, n - 1);
        permutation.printPerm();
    }

    /**
     * permutation function
     * @param list array to calculate permutation for
     * @param l starting index
     * @param r end index
     */
    public void permute(int[] list, int l, int r)
    {
        if (l == r) {
            int[] temp = new int[list.length];
            for (int i = 0; i < list.length; i++)
                temp[i] = list[i];
            PERMS.add(temp);
        }
        else {
            for (int i = l; i <= r; i++) {
                list = swap(list, l, i);
                permute(list, l + 1, r);
                list = swap(list, l, i);
            }
        }
    }

    /**
     * Swap Characters at position
     * @param a string value
     * @param i position 1
     * @param j position 2
     * @return swapped string
     */
    public int[] swap(int[] a, int i, int j)
    {
        int temp;
        temp = a[i];
        a[i] = a[j];
        a[j] = temp;
        return a;
    }

    public void printPerm(){
        for (int[] ints : PERMS)
            System.out.println(Arrays.toString(ints));
    }
}