# Gomoku

A simple Gomoku project with:
- local 2-player gameplay (Pygame)
- AI-vs-player gameplay using a trained model
- a training script to generate `.h5` models from game records

## Project Structure

- `gomoku.py` - Human vs Human game and record saving to `data.txt`
- `gomoku_with_ai.py` - Human vs AI game using a pre-trained model
- `train_model.py` - Training pipeline from `data.txt` game records
- `data/` - Sample record files
- `models/` - Saved model files (`.h5`)

## Requirements

- Python 3.9+
- `pygame`
- `numpy`
- `tensorflow`
- `keras`

You can install dependencies with:

```bash
pip install -r requirements.txt
#### This command runs a program where you can play gomoku with a friend.
```
python gomoku.py

### 1) Human vs Human

Controls:
- Left click: place a stone
- `Space`: undo last move
- After a win, `Enter`: save record and start a new board

### 2) Human vs AI

```bash
python gomoku_with_ai.py
```

## Train a Model

```bash
python train_model.py
```

What it does:
- Reads records from `data.txt`
- Builds training data with board augmentation (flip/rotate)
- Saves the trained model as `gomoku(<data_count>).h5`

## Current Repository Notes

- `gomoku_with_ai.py` currently loads `models/gomoku(22)_(acc56%).h5`, but this filename does not exist in the current `models/` folder.
- `gomoku_board.png` is required at runtime by both game scripts, but the file is currently not present in this repository.

## GitHub Page / README Improvement Suggestions

- Add a gameplay GIF in this README.
- Add badges (Python version, license, etc.).
- Add a short “Known Issues” section and keep it updated.
- Add issue/PR templates under `.github/` for collaboration.

## License

This project is licensed under the MIT License.
See [`LICENSE`](LICENSE) for details.
Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

