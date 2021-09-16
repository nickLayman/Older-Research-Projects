import java.util.ArrayList;
import java.util.stream.Collectors;

public class QueenStream {
    ArrayList<int[]> rookPlacements;
    ArrayList<int[]> queenPlacements;
    int boardSize;
    Permutation permutation = new Permutation();

    public QueenStream(int pBoardSize){
        boardSize = pBoardSize;
        makeQueenPlacements();
    }

    public void makeRookPlacements(){
        int[] nums = new int[boardSize];
        for (int i = 0; i < boardSize; i++){
            nums[i] = i+1;
        }
        permutation.permute(nums, 0, boardSize - 1);

        rookPlacements = permutation.PERMS;
    }

    public void makeQueenPlacements(){
        makeRookPlacements();

        queenPlacements = (ArrayList<int[]>) rookPlacements.stream()
                .filter(arg -> isValidPlacement(arg))
                .collect(Collectors.toList());
    }

    public boolean isValidPlacement(int[] placement){
        boolean valid = true;
        for (int pos1 = 0; pos1 < placement.length - 1; pos1++){
            int val1 = placement[pos1];
            for (int pos2 = pos1 + 1; pos2 < placement.length; pos2++){
                int val2 = placement[pos2];
                if (Math.abs(pos1 - pos2) == Math.abs(val1 - val2)){
                    valid = false;
                }
            }
        }

        return valid;
    }

    public static void main(String[] args){
        QueenStream test = new QueenStream(10);
        System.out.println("Placements: " + test.queenPlacements.size());
    }
}