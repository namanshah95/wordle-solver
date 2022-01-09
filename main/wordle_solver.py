import string

class WordleSolver:
  remaining_words = set()
  score = 0
  
  def __init__(self, word_len):
    self.word_len = word_len
    self.read_dictionary()

  def read_dictionary(self):
    with open('/usr/share/dict/words') as f:
      for word in f.readlines():
        word = word.strip().lower()
        if len(word) != self.word_len:
          continue
        self.remaining_words.add(word)

  def suggest(self):
    alphabet_cardinality = self.create_alphabet_cardinality()
    max_word_value = 0
    suggestion = None
    for word in self.remaining_words:
      word_value = self.get_word_value(word, alphabet_cardinality)
      if word_value > max_word_value:
        max_word_value = word_value
        suggestion = word
    return suggestion

  def create_alphabet_cardinality(self):
    alphabet_cardinality = {}
    for letter in string.ascii_lowercase:
      alphabet_cardinality[letter] = 0
    for word in self.remaining_words:
      for letter in word:
        alphabet_cardinality[letter] += 1
    return alphabet_cardinality

  def get_word_value(self, word, alphabet_cardinality):
    word_value = 0
    for letter in set(word):
      word_value += alphabet_cardinality[letter]
    return word_value

  def play_round(self, guess, result):
    self.score += 1
    if all([x == 'g' for x in result]):
      return True

    remaining_words = set()
    for word in self.remaining_words:
      if self.verify_word(word, guess, result):
        remaining_words.add(word)
    self.remaining_words = remaining_words

  def verify_word(self, word, guess, result):
    unique_letters = set(word)
    for idx in range(len(result)):
      if result[idx] == 'b':
        if guess[idx] in unique_letters:
          return False
      if result[idx] == 'y':
        if guess[idx] not in unique_letters:
          return False
        if word[idx] == guess[idx]:
          return False
      if result[idx] == 'g':
        if word[idx] != guess[idx]:
          return False
    return True

  def get_score(self):
    return self.score
    
def main():
  word_len = int(input("Length of word: "))
  
  wordle_solver = WordleSolver(word_len);
  while True:
    suggestion = wordle_solver.suggest()
    print("WordleSolver suggests: " + wordle_solver.suggest())
    result = input("What was the result of the suggestion? ").strip().lower()
    if wordle_solver.play_round(suggestion, result):
      print("WordleSolver solved the wordle!")
      break;

  print("Score: " + str(wordle_solver.get_score()))
  
if __name__ == "__main__":
  main()
