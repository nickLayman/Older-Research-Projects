import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
/**
 * Write a description of class GUI here.
 *
 * @author (your name)
 * @version (a version number or a date)
 */
public class GUI extends JFrame implements ActionListener, MouseListener{
    Rules rules;
    MyTile[][] tiles;
    JMenuItem resetAll, quit;
    JRadioButton pickQueen, pickRook, pickBishop;
    int currentPlacement;
    //Queen = 1, Rook = 2, Bishop = 3
    ButtonGroup pieceGroup;

    public GUI(){
        int rows = Integer.parseInt(JOptionPane.showInputDialog(this, "how many rows"));
        int columns = Integer.parseInt(JOptionPane.showInputDialog(this, "how many columns"));
        rules = new Rules(rows, columns);

        setUpMenu();

        setLayout(new GridBagLayout());
        GridBagConstraints position = new GridBagConstraints();

        tiles = rules.getTiles();

        position.gridy = 0;
        position.gridx = columns / 2 - 1;
        add(new JLabel("Piece"), position);
        position.gridy++;
        pickQueen = new JRadioButton("Q");
        pickQueen.setFont(new Font(pickQueen.getName(), Font.PLAIN, 15));
        add(pickQueen, position);
        position.gridy++;
        pickRook = new JRadioButton("R");
        pickRook.setFont(new Font(pickRook.getName(), Font.PLAIN, 15));
        add(pickRook, position);
        position.gridy++;
        pickBishop = new JRadioButton("B");
        pickBishop.setFont(new Font(pickBishop.getName(), Font.PLAIN, 15));
        add(pickBishop, position);

        pieceGroup = new ButtonGroup();
        pieceGroup.add(pickQueen);
        pieceGroup.add(pickRook);
        pieceGroup.add(pickBishop);

        pickQueen.addActionListener(this);
        pickQueen.setSelected(true);
        pickRook.addActionListener(this);
        pickBishop.addActionListener(this);


        for (int i = 4; i < rows + 4; i++){
            for (int j = 0; j < columns; j++){
                position.gridx = j;
                position.gridy = i;
                add(tiles[i - 4][j], position);
                tiles[i - 4][j].addMouseListener(this);
            }
        }
    }

    private void setUpMenu(){
        JMenuBar menuBar = new JMenuBar();
        setJMenuBar(menuBar);

        JMenu fileMenu = new JMenu("File");
        menuBar.add(fileMenu);

        resetAll = new JMenuItem("Reset All Pieces");
        fileMenu.add(resetAll);
        resetAll.addActionListener(this);

        quit = new JMenuItem("Quit");
        fileMenu.add(quit);
        quit.addActionListener(this);
    }

    public void actionPerformed(ActionEvent event){
        if (event.getSource() == resetAll){
            rules.removeAllPieces();
        }

        if (event.getSource() == quit){
            System.exit(0);
        }

        if (event.getSource() == pickQueen){
            for (MyTile[] r : tiles){
                for (MyTile t : r){
                    t.setCurrentPlacement(1);
                }
            }
        }

        if (event.getSource() == pickRook){
            for (MyTile[] r : tiles){
                for (MyTile t : r){
                    t.setCurrentPlacement(2);
                }
            }
        }

        if (event.getSource() == pickBishop){
            for (MyTile[] r : tiles){
                for (MyTile t : r){
                    t.setCurrentPlacement(3);
                }
            }
        }
    }

    public void mouseClicked(MouseEvent e){
        rules.setAttackables();
    }

    public void mousePressed(MouseEvent e){}

    public void mouseReleased(MouseEvent e){}

    public void mouseExited(MouseEvent e){}

    public void mouseEntered(MouseEvent e){}

    public static void main(String[] args){
        GUI frame = new GUI();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }
}
