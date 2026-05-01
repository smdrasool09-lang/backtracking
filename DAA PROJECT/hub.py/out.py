from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[r][col] for r in range(9)]:
        return False
    r0, c0 = 3 * (row // 3), 3 * (col // 3)
    for r in range(r0, r0 + 3):
        for c in range(c0, c0 + 3):
            if board[r][c] == num:
                return False
    return True

def solve(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for num in range(1, 10):
                    if is_valid(board, r, c, num):
                        board[r][c] = num
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True

@app.route("/solve", methods=["POST"])
def solve_sudoku():
    board = request.json["board"]
    if solve(board):
        return jsonify({"status": "solved", "board": board})
    return jsonify({"status": "no_solution"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)