import argparse
import sys
import os

sys.path.append('/Users/naman.shah/wordle-solver/main')
from wordle_solver import WordleSolver

def test_word(word):
  wordle_solver = WordleSolver(len(word))
  while True:
    suggestion = wordle_solver.suggest()
    result = get_result(suggestion, word)
    if wordle_solver.play_round(suggestion, result):
      break
  return wordle_solver.get_score()

def get_result(guess, target):
  unique_letters = set(target)
  result = ''
  for idx in range(len(target)):
    if guess[idx] == target[idx]:
      result += 'g'
    elif guess[idx] in unique_letters:
      result += 'y'
    else:
      result += 'b'
  return result

def test_file(file):
  scores = {}
  with open(file) as f:
    for word in f.readlines():
      word = word.strip().lower()
      scores[word] = test_word(word)
  bmrk_file = file + ".bmrk"
  replace_bmrk = True
  if os.path.exists(bmrk_file):
    benchmark = {}
    with open(bmrk_file) as f:
      for line in f.readlines():
        word, score = line.split()
        word = word.strip().lower()
        score = int(score.strip())
        benchmark[word] = score
    improved = 0
    unchanged = 0
    regressed = 0
    for word in scores.keys():
      if scores[word] < benchmark[word]:
        improved += 1
      elif scores[word] > benchmark[word]:
        regressed += 1
      else:
        unchanged += 1
    print("Summary: ")
    print(str(improved) + " words had better scores than the benchmark.")
    print(str(unchanged) + " words had the same score as the benchmark.")
    print(str(regressed) + " words had worse scores than the benchmark.")
    replace_bmrk = input("Overwrite the existing benchmark? (y/n) ").strip().lower() == 'y'
  if replace_bmrk:
    with open(bmrk_file, 'w') as f:
      for word in scores.keys():
        f.write(word + " " + str(scores[word]) + "\n")
    print("Wrote scores to " + bmrk_file)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--word')
  parser.add_argument('--file')
  args = parser.parse_args()
  if args.word:
    print("Score: " + str(test_word(args.word)))
  if args.file:
    test_file(args.file)

if __name__ == "__main__":
  main()
