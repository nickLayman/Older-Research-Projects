package Visual;

import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.LineBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;

public class SuperTicTacToePanel extends JPanel {

	private JButton[][] board;
	private Visual.Cell[][] iBoard;

	private JButton quitButton;
	private JButton enterButton;
//	private JButton undo;

	private JLabel guessLabel;
	private JTextField numberField;

	private ImageIcon maybeIcon;
	private ImageIcon noIcon;
	private ImageIcon yesIcon;

	private Visual.SuperTicTacToeGame game;

	private int size;

	public SuperTicTacToePanel() {
		this(3, new int[]{0, 0});
	}

	public SuperTicTacToePanel(int pSize, int[] pSecret) {
		setLayout(new BorderLayout());

		//resizes the image icons to the square size
		maybeIcon = new ImageIcon("./Visual/empty.jpg");
		Image imagem = maybeIcon.getImage();
		Image newimgm = imagem.getScaledInstance(90, 90,
				java.awt.Image.SCALE_SMOOTH);
		maybeIcon = new ImageIcon(newimgm);

		noIcon = new ImageIcon("./Visual/no.jpg");
		Image imagen = noIcon.getImage();
		Image newimgn = imagen.getScaledInstance(90, 90,
				java.awt.Image.SCALE_SMOOTH);
		noIcon = new ImageIcon(newimgn);

		yesIcon = new ImageIcon("./Visual/yes.jpg");
		Image imagey = yesIcon.getImage();
		Image newimgy = imagey.getScaledInstance(90, 90,
				java.awt.Image.SCALE_SMOOTH);
		yesIcon = new ImageIcon(newimgy);

		JPanel center = new JPanel();
		JPanel right = new JPanel();


		// create game, listeners
		ButtonListener listener = new ButtonListener();

		right.setLayout(new GridBagLayout());
		GridBagConstraints c = new GridBagConstraints();

		int totalHeight = (size+1)*66;

		guessLabel = new JLabel("Enter guesses:");
		c.gridy = 1;
		c.insets = new Insets(totalHeight/4,20,5,20);
		right.add (guessLabel, c);

		numberField = new JTextField(10);
		c.gridy = 2;
		c.insets = new Insets(0,20,10,20);
		right.add (numberField, c);

		enterButton = new JButton("Enter");
		c.gridy = 3;
		c.insets = new Insets(0,20,totalHeight/4,20);
		right.add (enterButton, c);
		enterButton.addActionListener(listener);

		quitButton = new JButton("quit");
		c.gridy = 4;
		c.insets = new Insets(80,20,0,20);
		right.add (quitButton, c);
		quitButton.addActionListener(listener);

//		undo = new JButton("undo");
//		add(undo);
//		undo.addActionListener(listener);

		size = pSize;
		game = new Visual.SuperTicTacToeGame(size, pSecret);

        center.setLayout(new GridLayout(size, size, 3,3));
        Dimension temp = new Dimension(60,60);
        board = new JButton[size][size];

        // add all the squares to the board
        for (int row = 0; row < size; row++)
            for (int col = 0; col < size; col++) {

                Border thickBorder = new LineBorder(Color.blue, 2);

                board[row][col] = new JButton ("", maybeIcon);
                board[row][col].setPreferredSize(temp);
                board[row][col].setBorder(thickBorder);

//                board[row][col].addActionListener(listener);
                center.add(board[row][col]);
            }

		displayBoard();

		// add all to contentPane
		add (new JLabel("Super TicTacToe"), BorderLayout.NORTH);
		add (center, BorderLayout.CENTER);
		add (right, BorderLayout.EAST);
	}

	private void displayBoard() {
		iBoard = game.getBoard ();

		for (int r = 0; r < size; r++)
			for (int c = 0; c < size; c++) {
				if (iBoard[r][c] == Visual.Cell.NO)
					board[r][c].setIcon(noIcon);
				else if (iBoard[r][c] == Visual.Cell.YES)
					board[r][c].setIcon(yesIcon);
				else
					board[r][c].setIcon(maybeIcon);
			}
	}

	private class ButtonListener implements ActionListener{

		public void actionPerformed(ActionEvent e) {
			if (e.getSource() == quitButton) {
				if (JOptionPane.showConfirmDialog(null,
						"Are you sure you want to quit?", "YES", 2) == 0)
					System.exit(0);
			}

//			if (e.getSource() == undo){
//				try {
//					game.undo();
//					displayBoard();
//				} catch(IndexOutOfBoundsException er){
//					return;
//				}
//			}

			if (e.getSource() == enterButton){
				game.guess(numberField.getText());
			}

			if (game.getGameStatus() == Visual.GameStatus.Q_WON) {
				JOptionPane.showMessageDialog(null,
						"The questioner won!");
			} else if (game.getGameStatus() == Visual.GameStatus.R_WON) {
				JOptionPane.showMessageDialog(null,
						"The responder won!");
			}
			displayBoard();
		}
	}
}
