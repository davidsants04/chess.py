import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Definindo as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (235, 236, 208)
DARK_BROWN = (125, 135, 150)
HIGHLIGHT = (144, 238, 144)  # Verde claro para destacar casas válidas
CHECK_COLOR = (255, 0, 0)  # Vermelho para indicar Check

# Definindo o tamanho do tabuleiro
BOARD_SIZE = 8
SQUARE_SIZE = 80
WIDTH = HEIGHT = BOARD_SIZE * SQUARE_SIZE

# Definir a fonte para as letras
FONT = pygame.font.SysFont('Arial', 48)
SMALL_FONT = pygame.font.SysFont('Arial', 36)

# Função para desenhar o tabuleiro
def draw_board(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Função para desenhar as peças no tabuleiro
def draw_pieces(screen, board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece != "":
                color = WHITE if piece.isupper() else BLACK
                # Desenhar as peças como letras
                text = FONT.render(piece.upper(), True, color)
                screen.blit(text, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4))

# Função para destacar as casas válidas para o movimento
def highlight_valid_moves(screen, valid_moves):
    for move in valid_moves:
        row, col = move
        pygame.draw.rect(screen, HIGHLIGHT, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Função para verificar a validade de um movimento para as peças
def is_valid_move(piece, start_pos, end_pos, board, current_turn):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if (current_turn == 'white' and piece.islower()) or (current_turn == 'black' and piece.isupper()):
        return False  # Não é a vez do jogador para mover essa peça

    # Movimentos do peão
    if piece.lower() == 'p':
        direction = 1 if piece.islower() else -1
        if start_col == end_col and (end_row - start_row == direction or 
                                     (start_row == 1 and end_row - start_row == 2 and piece.islower()) or 
                                     (start_row == 6 and end_row - start_row == -2 and piece.isupper())):
            return True
        if abs(start_col - end_col) == 1 and (end_row - start_row == direction) and board[end_row][end_col] != "":
            return True

    # Movimentos da torre
    if piece.lower() == 'r':
        if start_row == end_row:  # Movimento horizontal
            for c in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                if board[start_row][c] != "":
                    return False
            return True
        if start_col == end_col:  # Movimento vertical
            for r in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                if board[r][start_col] != "":
                    return False
            return True

    # Movimentos do cavalo
    if piece.lower() == 'n':
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return True

    # Movimentos do bispo
    if piece.lower() == 'b':
        if abs(start_row - end_row) == abs(start_col - end_col):
            return True

    # Movimentos da rainha
    if piece.lower() == 'q':
        if start_row == end_row:  # Movimento horizontal
            for c in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                if board[start_row][c] != "":
                    return False
            return True
        if start_col == end_col:  # Movimento vertical
            for r in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                if board[r][start_col] != "":
                    return False
            return True
        if abs(start_row - end_row) == abs(start_col - end_col):  # Movimento diagonal
            return True

    # Movimentos do rei
    if piece.lower() == 'k':
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return True

    return False

# Função para verificar se o rei está em check
def is_king_in_check(board, king_pos, current_turn):
    # Verifique se alguma peça adversária pode atacar o rei
    king_row, king_col = king_pos
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece != "" and (piece.islower() if current_turn == 'white' else piece.isupper()):
                if is_valid_move(piece, (row, col), (king_row, king_col), board, current_turn):
                    return True
    return False

# Função para mostrar o status de check
def show_status(screen, status_text):
    status = SMALL_FONT.render(status_text, True, CHECK_COLOR)
    screen.blit(status, (WIDTH // 2 - status.get_width() // 2, HEIGHT // 2))

# Função principal do jogo
def main():
    # Criação da tela
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo de Xadrez")
    
    # Tabuleiro inicial (simplificado)
    board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    
    selected_piece = None
    start_pos = None
    current_turn = 'white'  # Começa com o jogador branco
    valid_moves = []
    check_status = ""
    
    # Loop principal do jogo
    running = True
    while running:
        screen.fill(WHITE)
        draw_board(screen)
        draw_pieces(screen, board)
        highlight_valid_moves(screen, valid_moves)
        
        # Mostrar o turno atual
        turn_text = SMALL_FONT.render(f"Turno: {current_turn.capitalize()}", True, BLACK)
        screen.blit(turn_text, (10, HEIGHT - 40))
        
        if check_status:
            show_status(screen, check_status)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                col, row = pygame.mouse.get_pos()
                col //= SQUARE_SIZE
                row //= SQUARE_SIZE
                
                # Seleção de uma peça
                if selected_piece is None:
                    if board[row][col] != "" and (board[row][col].isupper() if current_turn == 'white' else board[row][col].islower()):
                        selected_piece = board[row][col]
                        start_pos = (row, col)
                        valid_moves = []  # Limpar movimentos válidos anteriores
                        # Adicionar casas válidas dependendo da peça selecionada
                        for r in range(BOARD_SIZE):
                            for c in range(BOARD_SIZE):
                                if is_valid_move(selected_piece, start_pos, (r, c), board, current_turn):
                                    valid_moves.append((r, c))
                else:
                    # Tentar mover a peça
                    if (row, col) in valid_moves:
                        board[row][col] = selected_piece
                        board[start_pos[0]][start_pos[1]] = ""
                        # Troca de turno
                        current_turn = 'black' if current_turn == 'white' else 'white'
                        selected_piece = None
                        valid_moves = []  # Limpar movimentos válidos após a jogada
                        
                        # Verificar se o rei está em check
                        white_king_pos = None
                        black_king_pos = None
                        for r in range(BOARD_SIZE):
                            for c in range(BOARD_SIZE):
                                if board[r][c] == 'K':
                                    white_king_pos = (r, c)
                                if board[r][c] == 'k':
                                    black_king_pos = (r, c)
                        
                        # Verificar se o rei está em check
                        if current_turn == 'white' and is_king_in_check(board, black_king_pos, 'black'):
                            check_status = "Check"
                        elif current_turn == 'black' and is_king_in_check(board, white_king_pos, 'white'):
                            check_status = "Check"
                        else:
                            check_status = ""
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
