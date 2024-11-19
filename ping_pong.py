# Kidus Mengistu Gebremedhin - Mekelle University - MIT
# Africa Cybersecurity Bootcamp - Artificial intelligence
# Game Development Assignment - Ping Pong Game
# Python with PyQt6 library ChatGPT Generated Code

from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsTextItem, QMessageBox, QPushButton
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QBrush, QColor, QFont
import random
import sys

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 20
BLOCK_ROWS = 3  # Number of rows in the block layout
BLOCK_COLUMNS = 10  # Number of columns for small blocks

class Block(QGraphicsRectItem):
    def __init__(self, x, y, width, height, strength, points, color):
        super().__init__(0, 0, width, height)
        self.setBrush(QBrush(color))
        self.setPos(x, y)
        self.strength = strength  # Number of hits required to break
        self.points = points      # Score given for breaking this block

    def hit(self):
        """Reduces block's strength by 1. Returns True if destroyed."""
        self.strength -= 1
        if self.strength <= 0:
            return True  # Block is destroyed
        return False  # Block still has strength

class PingPongGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Set up the scene
        self.scene = QGraphicsScene(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setScene(self.scene)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Game state
        self.game_over = False
        self.game_started = False  # Flag to check if game has started

        # Create the paddle
        self.paddle1 = QGraphicsRectItem(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle1.setBrush(QBrush(QColor("blue")))
        self.paddle1.setPos(WINDOW_WIDTH / 2 - PADDLE_WIDTH / 2, WINDOW_HEIGHT - 30)
        self.scene.addItem(self.paddle1)

        # Create the ball
        self.ball = QGraphicsEllipseItem(0, 0, BALL_SIZE, BALL_SIZE)
        self.ball.setBrush(QBrush(QColor("red")))
        self.ball.setPos(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.scene.addItem(self.ball)

        # Scoring
        self.score = 0
        self.score_text = QGraphicsTextItem(f"Score: {self.score}")
        self.score_text.setFont(QFont("Arial", 16))
        self.score_text.setDefaultTextColor(QColor("black"))
        self.score_text.setPos(10, 10)
        self.scene.addItem(self.score_text)

        # Create blocks with varying strength, sizes, and arranged puzzle-like
        self.blocks = []
        self.create_blocks()

        # Ball movement direction
        self.ball_dx = 5
        self.ball_dy = -5

        # Timer for the game loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)

        # Countdown timer
        self.countdown = 3
        self.countdown_text = QGraphicsTextItem("")
        self.countdown_text.setFont(QFont("Comic Sans MS", 36, QFont.Weight.Bold))  # Stylish font and size
        self.countdown_text.setDefaultTextColor(QColor("black"))  # Black color
        self.scene.addItem(self.countdown_text)

        # Start button
        self.start_button = QPushButton("Start", self)
        # Corrected setGeometry line
        self.start_button.setGeometry(int(WINDOW_WIDTH / 2 - 50), int(WINDOW_HEIGHT / 2), 100, 50)
        self.start_button.clicked.connect(self.start_game)
        self.start_button.show()

    def create_blocks(self):
        # Arrange blocks with varying sizes and strength
        for row in range(BLOCK_ROWS):
            x_offset = 20  # Start position of blocks in each row
            for col in range(BLOCK_COLUMNS):
                strength = random.randint(1, 3)
                width = 40 + (strength - 1) * 20
                height = 30 if strength == 1 else 40
                points = strength * 10
                color = QColor(50 * strength, 255 - 50 * strength, 100)

                block = Block(x_offset, 50 + row * (height + 10), width, height, strength, points, color)
                self.scene.addItem(block)
                self.blocks.append(block)

                x_offset += width + 5

    def start_game(self):
        """Initiate countdown and prepare game start."""
        self.start_button.hide()  # Hide start button
        self.countdown = 3
        font = QFont("Comic Sans MS", 16)  # Choose a smaller font size
        font.setBold(True)  # Set the font to bold
        self.countdown_text.setFont(font)
        self.countdown_text.setPlainText("Buckle Up! This won't be a good Ping Pong game experience ¯\\_(ツ)_/¯")

        # Get the bounding rectangle of the text and center it
        text_rect = self.countdown_text.boundingRect()
        x_pos = (WINDOW_WIDTH - text_rect.width()) / 2  # Horizontal centering
        y_pos = (WINDOW_HEIGHT - text_rect.height()) / 2  # Vertical centering
        self.countdown_text.setPos(x_pos, y_pos)  # Set the position to center
        QTimer.singleShot(1000, self.update_countdown)  # Begin countdown

    def update_countdown(self):
        """Update countdown display and start game when countdown is over."""
        if self.countdown > 0:
            self.countdown_text.setPlainText(f"{self.countdown}")
            self.countdown_text.setFont(QFont("Comic Sans MS", 36, QFont.Weight.Bold))  # Larger size for countdown numbers
            # Center the countdown number on the screen
            text_rect = self.countdown_text.boundingRect()
            x_pos = (WINDOW_WIDTH - text_rect.width()) / 2
            y_pos = (WINDOW_HEIGHT - text_rect.height()) / 2
            self.countdown_text.setPos(x_pos, y_pos)
        
            self.countdown -= 1
            QTimer.singleShot(1000, self.update_countdown)  # Continue countdown
        else:
            # After countdown finishes, clear message and start the game
            self.countdown_text.setPlainText("")  # Clear countdown text
            self.game_started = True
            self.timer.start(30)  # Start game loop

    def game_loop(self):
        if not self.game_started or self.game_over:
            return

        # Move the ball
        self.ball.moveBy(self.ball_dx, self.ball_dy)

        # Ball collision with walls
        if self.ball.x() <= 0 or self.ball.x() + BALL_SIZE >= WINDOW_WIDTH:
            self.ball_dx *= -1  # Reverse x direction
        if self.ball.y() <= 0:
            self.ball_dy *= -1  # Reverse y direction

        # Ball missed by paddle (Game Over)
        if self.ball.y() + BALL_SIZE >= WINDOW_HEIGHT:
            self.end_game()  # Trigger game over

        # Ball collision with paddle1
        if self.ball.collidesWithItem(self.paddle1):
            self.ball_dy *= -1
            self.update_score(1)

        # Check collision with blocks
        for block in self.blocks:
            if self.ball.collidesWithItem(block):
                if block.hit():
                    self.scene.removeItem(block)
                    self.blocks.remove(block)
                    self.update_score(block.points)
                self.ball_dy *= -1
                break

    def update_score(self, value):
        self.score += value
        self.score_text.setPlainText(f"Score: {self.score}")

    def end_game(self):
        self.game_over = True
        self.timer.stop()

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(f"Game Over!\nYour Score: {self.score}\nWould you like to play again?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.reset_game()
        else:
            QApplication.instance().quit()

    def reset_game(self):
        self.score = 0
        self.score_text.setPlainText(f"Score: {self.score}")
        self.game_over = False
        self.game_started = False

        self.ball.setPos(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.ball_dx = 5
        self.ball_dy = -5

        for block in self.blocks:
            self.scene.removeItem(block)
        self.blocks.clear()
        self.create_blocks()

        self.start_button.show()  # Show start button again

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            new_x = max(self.paddle1.x() - 20, 0)
            self.paddle1.setPos(new_x, self.paddle1.y())
        elif event.key() == Qt.Key.Key_Right:
            new_x = min(self.paddle1.x() + 20, WINDOW_WIDTH - PADDLE_WIDTH)
            self.paddle1.setPos(new_x, self.paddle1.y())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = PingPongGame()
    game.show()
    sys.exit(app.exec())

def check_win(self):
    """Check if all blocks are destroyed and display 'YOU WIN' message."""
    if not self.blocks:  # If no blocks are left in the game
        self.timer.stop()  # Stop the game loop
        self.display_win_message()

def display_win_message(self):
    """Display 'YOU WIN' message in the center of the screen."""
    win_message = QGraphicsTextItem("YOU WIN!")
    font = QFont("Comic Sans MS", 36, QFont.Weight.Bold)
    win_message.setFont(font)
    win_message.setDefaultTextColor(Qt.black)  # Set message color
    
    # Center the message on the screen
    text_rect = win_message.boundingRect()
    x_pos = (WINDOW_WIDTH - text_rect.width()) / 2
    y_pos = (WINDOW_HEIGHT - text_rect.height()) / 2
    win_message.setPos(x_pos, y_pos)
    
    self.scene.addItem(win_message)  # Add the win message to the scene

