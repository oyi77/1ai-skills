
class TetrisLogic:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0

    def check_collision(self, piece, x, y):
        for r, row in enumerate(piece):
            for c, val in enumerate(row):
                if val:
                    if (x + c < 0 or x + c >= self.width or 
                        y + r >= self.height or 
                        (y + r >= 0 and self.grid[y + r][x + c])):
                        return True
        return False

    def merge_piece(self, piece, x, y):
        for r, row in enumerate(piece):
            for c, val in enumerate(row):
                if val and y + r >= 0:
                    self.grid[y + r][x + c] = val

    def clear_lines(self):
        lines_cleared = 0
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = self.height - len(new_grid)
        
        # Add empty rows to top
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.width)])
            
        self.grid = new_grid
        self.score += lines_cleared * 100
        return lines_cleared

# Simple test suite
def test_tetris():
    game = TetrisLogic()
    
    # Test collision with boundary
    piece = [[1, 1], [1, 1]]
    assert game.check_collision(piece, -1, 0) == True, "Should collide with left wall"
    assert game.check_collision(piece, 10, 0) == True, "Should collide with right wall"
    assert game.check_collision(piece, 0, 20) == True, "Should collide with bottom"
    
    # Test line clearing
    game.grid[19] = [1] * 10 # Full bottom row
    cleared = game.clear_lines()
    assert cleared == 1, "Should clear one line"
    assert game.score == 100, "Score should increase"
    assert sum(game.grid[19]) == 0, "Bottom row should now be empty"

    print("TDD: Logic tests passed")

if __name__ == "__main__":
    test_tetris()
