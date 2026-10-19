# STEP 3: Reset and New Puzzle buttons.
from flask import Flask, render_template, request

app = Flask(__name__)

# ---------- NEW: a list of puzzles instead of just one (0 = empty) ----------
PUZZLES = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ],
    [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ],
    [
        [0, 2, 0, 6, 0, 8, 0, 0, 0],
        [5, 8, 0, 0, 0, 9, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [3, 7, 0, 0, 0, 0, 5, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 8, 0, 0, 0, 0, 1, 3],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 9, 8, 0, 0, 0, 3, 6],
        [0, 0, 0, 3, 0, 6, 0, 9, 0],
    ],
]


def read_board(form):
    """Read the 81 cells from the submitted form into a 9x9 list."""
    board = []
    for r in range(9):
        row = []
        for c in range(9):
            value = form.get(f"c{r}{c}", "").strip()
            if len(value) == 1 and value in "123456789":
                row.append(int(value))
            else:
                row.append(0)
        board.append(row)
    return board


def find_conflicts(board):
    """Return a set of (row, col) cells that break a Sudoku rule."""
    conflicts = set()
    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num == 0:
                continue
            for i in range(9):
                if i != c and board[r][i] == num:
                    conflicts.add((r, c))
                if i != r and board[i][c] == num:
                    conflicts.add((r, c))
            br, bc = (r // 3) * 3, (c // 3) * 3
            for i in range(br, br + 3):
                for j in range(bc, bc + 3):
                    if (i, j) != (r, c) and board[i][j] == num:
                        conflicts.add((r, c))
    return conflicts


def is_full(board):
    return all(num != 0 for row in board for num in row)


def copy_board(board):
    """Make a fresh copy so we never change the original puzzle."""
    return [row[:] for row in board]


@app.route("/", methods=["GET", "POST"])
def home():
    puzzle_id = 0
    board = copy_board(PUZZLES[0])
    errors = set()
    message, msg_type = "", ""

    if request.method == "POST":
        # NEW: the page remembers which puzzle you are on (hidden field)
        puzzle_id = int(request.form.get("puzzle_id", 0)) % len(PUZZLES)
        board = read_board(request.form)
        action = request.form.get("action")

        if action == "check":
            errors = find_conflicts(board)
            if errors:
                message, msg_type = "Conflicts found. Check the red cells.", "error"
            elif not is_full(board):
                message, msg_type = "No conflicts so far. Keep solving!", "info"
            else:
                message, msg_type = "Solved! All rows, columns and boxes are valid!", "success"

        elif action == "reset":
            # NEW: go back to the starting numbers of the same puzzle
            board = copy_board(PUZZLES[puzzle_id])
            message, msg_type = "Board reset.", "info"

        elif action == "new":
            # NEW: move to the next puzzle (wraps back to the first)
            puzzle_id = (puzzle_id + 1) % len(PUZZLES)
            board = copy_board(PUZZLES[puzzle_id])
            message, msg_type = f"Puzzle {puzzle_id + 1} of {len(PUZZLES)}", "info"

    return render_template(
        "index.html",
        board=board,
        given=PUZZLES[puzzle_id],
        puzzle_id=puzzle_id,
        errors=errors,
        message=message,
        msg_type=msg_type,
    )


if __name__ == "__main__":
    app.run(debug=True)