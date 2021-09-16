package Visual;

import java.awt.*;
import java.util.ArrayList;
import java.util.Random;

/************************************************************************
 * This program builds a GUI for SuperTicTacToe. SuperTicTacToe is a game
 * where the user chooses the size of the board and the number of
 * connections needed to win. It then allows the user to play with another
 * person or against an AI. The program will tell the user when either
 * side has won, lost, or tied.
 *
 * @author Justin Von Kulajta Winn & Nick Layman
 * @version 1.8
 ************************************************************************/

public class SuperTicTacToeGame {

    /** this is the board the that an X or O is 'placed' onto */
    private Visual.Cell[][] board;

    /** This is a variable that tells the program if one side has won or tied */
    private Visual.GameStatus status;

    private int remainingQuestions = -1;

    private int[] secret;

    /** This is the width of the board */
    private int size;

    /************************************************************************
     * This constructor is the basic constructor. It sets the board to it's
     * default settings
     ************************************************************************/
    public SuperTicTacToeGame() {
        this(3, new int[]{0, 0});
    }

    /************************************************************************
     * This constructor sets the width, height, and number of connections
     * needed to win for the current board. It also determines if X or O
     * is to go first
     * @param pSize is the height of the board
     ************************************************************************/
    public SuperTicTacToeGame(int pSize, int[] pSecret) {
        size = pSize;
        secret = pSecret;
        status = Visual.GameStatus.IN_PROGRESS;
        board = new Visual.Cell[size][size];

        for (int row = 0; row < size; row++)
            for (int col = 0; col < size; col++)
                if(size - 1 - row == col)
                    board[row][col] = Visual.Cell.NO;
                else
                    board[row][col] = Visual.Cell.MAYBE;
    }

    /************************************************************************
     * This function returns the current board
     * @return is the current board with the currently marked X's and O's
     ************************************************************************/
    public Visual.Cell[][] getBoard() {
        return board;
    }


    public void guess(String numbers){
        String[] temp = numbers.split(",");
        ArrayList<Integer> guesses = new ArrayList<Integer>();
        for (String s : temp){
            guesses.add(Integer.parseInt(s.trim()));
        }

        int answer = 0;
        for(int num : secret)
            if (guesses.contains(num))
                answer++;

        for(int r = 0; r < board.length; r++){
            for(int c = 0; c < board.length; c++){
                if(answer == 0)
                    if (guesses.contains(r + 1) || guesses.contains(c + 1))
                        board[size - 1 - r][c] = Cell.NO;
                if (answer == 1)
                    if (guesses.contains(r + 1) == guesses.contains(c + 1))
                        board[size - 1 - r][c] = Cell.NO;
                if (answer == 2)
                    if (!(guesses.contains(r + 1) && guesses.contains(c + 1)))
                        board[size - 1 - r][c] = Cell.NO;
            }
        }

        status = isWinner();
        if(status == GameStatus.Q_WON) {
            board[size - secret[0]][secret[1] - 1] = Cell.YES;
            board[size - secret[1]][secret[0] - 1] = Cell.YES;
        }
    }

    /************************************************************************
     * This function determines if there has been a winner or not of the
     * game. It checks if X or O has won vertically, horizontally, or
     * diagonally. If the board is completely full, it declares the game
     * a CATS game. IF none of these conditions are true, it returns the
     * game status 'IN_PROGRESS."
     * @return the current GameStatus of the board which will
     *         be either IN_PROGRESS, X_WON, O_WON, OR CATS
     ************************************************************************/
    private Visual.GameStatus isWinner() {
        int numRemaining = 0;
        for (int row = 0; row < size; row++)
            for (int col = 0; col < size; col++)
                if(board[row][col] == Cell.MAYBE)
                    numRemaining++;
        if (numRemaining == 2)
            return GameStatus.Q_WON;
        if (remainingQuestions == 0)
            return GameStatus.R_WON;
        return GameStatus.IN_PROGRESS;
    }

    /************************************************************************
     * This function returns the current status of the game. It will
     * either be IN_PROGRESS, X_WON, O_WON, OR CATS
     * @return the current status of the game
     ************************************************************************/
    public Visual.GameStatus getGameStatus() {
        return isWinner();
    }
}