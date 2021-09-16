/**
 * Write a description of class Rules here.
 *
 * @author (your name)
 * @version (a version number or a date)
 */
public class Rules{
    MyTile[][] tiles;
    int numRows;
    int numColumns;
    final int screenPixels = 800;

    public Rules(int rows, int columns){
        numRows = rows;
        numColumns = columns;
        tiles = new MyTile[numRows][numColumns];
        for (int i = 0; i < numRows; i++){
            for (int j = 0; j < numColumns; j++){
                tiles[i][j] = new MyTile(screenPixels / rows);
            }
        }
    }

    public MyTile[][] getTiles(){
        return tiles;
    }

    public void removeAllPieces(){
        for (MyTile[] row : tiles){
            for (MyTile t : row){
                t.setHasQueen(false);
                t.setHasRook(false);
                t.setHasBishop(false);
            }
        }
    }

    public void resetAttackables(){
        for (int i = 0; i < numRows; i++){
            for (int j = 0; j < numColumns; j++){
                tiles[i][j].setAttackable(false);
            }
        }
    }

    public void setAttackables(){
        resetAttackables();
        for (int i = 0; i < numRows; i++){
            for (int j = 0; j < numColumns; j++){
                if(tiles[i][j].getHasQueen()){
                    setColumnAttackable(i, j);
                    setRowAttackable(i, j);
                    setDiagonalsAttackable(i, j);
                }

                if(tiles[i][j].getHasRook()){
                    setColumnAttackable(i, j);
                    setRowAttackable(i, j);
                }

                if(tiles[i][j].getHasBishop()){
                    setDiagonalsAttackable(i, j);
                }
            }
        }
    }

    public void setColumnAttackable(int row, int col){
        for (int r = 0; r < numRows; r++){
            if (r != row){
                tiles[r][col].setAttackable(true);
            }
        }
    }

    public void setRowAttackable(int row, int col){
        for (int c = 0; c < numColumns; c++){
            if (c != col){
                tiles[row][c].setAttackable(true);
            }
        }
    }

    public void setDiagonalsAttackable(int row, int col){
        setDescendingDiagonal(row, col);
        setAscendingDiagonal(row, col);
    }

    public void setDescendingDiagonal(int row, int col){
        for (int i = 1; row - i >= 0 && col - i >= 0 &&
                row - i < numRows && col - i < numColumns; i++){
            tiles[row - i][col - i].setAttackable(true);
        }
        for (int i = 1; row + i >= 0 && col + i >= 0 &&
                row + i < numRows && col + i < numColumns; i++){
            tiles[row + i][col + i].setAttackable(true);
        }
    }

    public void setAscendingDiagonal(int row, int col){
        for (int i = 1; row + i >= 0 && col - i >= 0 &&
                row + i < numRows && col - i < numColumns; i++){
            tiles[row + i][col - i].setAttackable(true);
        }
        for (int i = 1; row - i >= 0 && col + i >= 0 &&
                row - i < numRows && col + i < numColumns; i++){
            tiles[row - i][col + i].setAttackable(true);
        }
    }
}
