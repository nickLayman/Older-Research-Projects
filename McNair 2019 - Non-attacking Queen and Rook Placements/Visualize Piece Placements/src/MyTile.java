import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.border.*;
/**
 * Write a description of class MyTile here.
 *
 * @author (your name)
 * @version (a version number or a date)
 */
public class MyTile extends JPanel implements MouseListener{
    boolean hasQueen;
    boolean hasRook;
    boolean hasBishop;
    boolean attackable;
    int size;
    int border;
    Color ATTACKABLE_COLOR = Color.gray;
    Color ATTACKABLE_PIECE_COLOR = Color.red;
    Color BACKGROUND_COLOR = Color.white;
    JLabel label;
    int currentPlacement;

    public MyTile(int pSize){
        size = pSize - 8;
        border = 4;
        hasQueen = false;
        attackable = false;
        setBackground(BACKGROUND_COLOR);
        setForeground(Color.black);
        setSize(size,size);
        setPreferredSize(new Dimension(size, size));
        setMinimumSize(new Dimension(size, size));
        setMaximumSize(new Dimension(size, size));
        currentPlacement = 1;

        setLayout(new FlowLayout(FlowLayout.CENTER, pSize/2, (int)(pSize/2.5)));
        label = new JLabel();
        label.setHorizontalTextPosition(JLabel.CENTER);
        label.setVerticalTextPosition(JLabel.CENTER);
        label.setFont(new Font(label.getFont().getName(), Font.PLAIN, 30));
        add(label);

        //create the fancy border
        Border raised = BorderFactory.createRaisedBevelBorder();
        Border lowered = BorderFactory.createLoweredBevelBorder();
        Border compound = BorderFactory.createCompoundBorder(raised, lowered);
        setBorder(compound);

        addMouseListener(this);
    }

    public MyTile(){
        this(100);
    }

    public boolean getHasQueen(){
        return hasQueen;
    }

    public boolean getHasRook(){
        return hasRook;
    }

    public boolean getHasBishop(){
        return hasBishop;
    }

    public boolean getHasPiece(){
        return hasQueen || hasRook || hasBishop;
    }

    public void setHasQueen(boolean b){
        hasQueen = b;

        if (b){
            label.setText("Q");
        }
        else{
            setBackground(BACKGROUND_COLOR);
            label.setText("");
        }
    }

    public void setHasRook(boolean b){
        hasRook = b;

        if (b){
            label.setText("R");
        }
        else{
            setBackground(BACKGROUND_COLOR);
            label.setText("");
        }
    }

    public void setHasBishop(boolean b){
        hasBishop = b;

        if (b){
            label.setText("B");
        }
        else{
            setBackground(BACKGROUND_COLOR);
            label.setText("");
        }
    }

    public void setCurrentPlacement(int i){
        currentPlacement = i;
    }

    public int getCurrentPlacement(){
        return currentPlacement;
    }

    public boolean getAttackable(){
        return attackable;
    }

    public void setAttackable(boolean b){
        attackable = b;
        if (b && getHasPiece()){
            setBackground(ATTACKABLE_PIECE_COLOR);
        }
        else if(b){
            setBackground(ATTACKABLE_COLOR);
            label.setText("");
        }
        else if(getHasQueen()){
            setBackground(BACKGROUND_COLOR);
            label.setText("Q");
        }
        else if(getHasRook()){
            setBackground(BACKGROUND_COLOR);
            label.setText("R");
        }
        else if (getHasBishop()){
            setBackground(BACKGROUND_COLOR);
            label.setText("B");
        }
        else{
            setBackground(BACKGROUND_COLOR);
            label.setText("");
        }
    }

    public void mouseClicked(MouseEvent e){
        if (getHasPiece()){
            setHasQueen(false);
            setHasRook(false);
            setHasBishop(false);
        }
        else if (currentPlacement == 1){
            setHasQueen(true);
        }
        else if (currentPlacement == 2){
            setHasRook(true);
        }
        else{
            setHasBishop(true);
        }
    }

    public void mousePressed(MouseEvent e){}

    public void mouseReleased(MouseEvent e){}

    public void mouseExited(MouseEvent e){}

    public void mouseEntered(MouseEvent e){}
}
