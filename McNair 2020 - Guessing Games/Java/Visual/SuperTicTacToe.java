package Visual;

import javax.swing.*;
import java.util.ArrayList;

public class SuperTicTacToe {

    private static int size;
    private static int[] secret = new int[2];
    private static int timeLimit;

    public static void main (String[] args)
    {
        JFrame frame = new JFrame ("Super TicTacToe");
        frame.setDefaultCloseOperation (JFrame.EXIT_ON_CLOSE);

        size = 3;
        boolean isError;
        String temp = "";
        do {
            isError = false;
            try {
                do {String s = JOptionPane.showInputDialog(null,
                        "Enter size of the board:");
                    if (s == null)
                            throw new NullPointerException();
                    size = Integer.parseInt(s);
                } while (size < 3 || size > 30);
            } catch (NumberFormatException e) {
                isError = true;
            } catch (NullPointerException n){
                System.exit(0);
            }
        } while(isError);

        do {
            isError = false;
            try {
                do {String s = JOptionPane.showInputDialog(null,
                        "Enter 2 secret numbers:");
                    if (s == null)
                        throw new NullPointerException();
                    String[] temp2 = s.split(",");
                    secret[0] = Integer.parseInt(temp2[0].trim());
                    secret[1] = Integer.parseInt(temp2[1].trim());
                } while (secret[0] <= 0 || secret[1] <= 0 || secret[0] > size || secret[1] > size);
            } catch (NumberFormatException e) {
                isError = true;
            } catch (NullPointerException n){
                System.exit(0);
            }
        } while(isError);


        Visual.SuperTicTacToePanel panel = new Visual.SuperTicTacToePanel(size, secret);
        frame.getContentPane().add(panel);

        frame.setSize((size+2)*70,(size+1)*70);
        frame.setVisible(true);
    }


}

