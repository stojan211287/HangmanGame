import os


class HighScoreTableConstructionError(Exception):
    pass


class TableSerializer:

    @staticmethod
    def serialize_entry(name, score):

        assert isinstance(name, str)
        assert isinstance(score, int)

        return "%s\t%d\n" % (name, score)

    @staticmethod
    def deserialize_entry(entry_string):

        name_string, score_string = tuple(entry_string.split("\t"))
        return name_string, int(score_string)


class HighScoreTable:

    def __init__(self, no_of_high_scores, game_scoring_function,
                 high_score_persist_path=os.path.join(".", ".hangman_scores")):

        self.no_of_high_scores = no_of_high_scores

        try:
            assert (callable(game_scoring_function))
        except AssertionError:
            raise HighScoreTableConstructionError("game_scoring_function must be a callable!")

        self.scoring_function = game_scoring_function

        self.serializer = TableSerializer

        self.high_score_persist_path = high_score_persist_path
        self.high_score_file_path = os.path.join(self.high_score_persist_path,
                                                 "high_scores.dat")

        self.high_scores = []
        self._load_or_init_high_scores()

    def _load_or_init_high_scores(self):

        self._ensure_high_score_dir()

        if os.path.exists(self.high_score_file_path):
            high_scores = []

            with open(self.high_score_file_path, "r") as high_score_file:

                for i, high_score_entry in enumerate(high_score_file.readlines()):

                    deserialized_entry = self.serializer.deserialize_entry(high_score_entry)
                    high_scores.append(deserialized_entry)
        else:
            high_scores = [("AAA", 1)]*self.no_of_high_scores

        self._update_high_scores(new_scores=high_scores)

    def _ensure_high_score_dir(self):
        if not os.path.isdir(self.high_score_persist_path):
            os.makedirs(self.high_score_persist_path)

    def _persist_high_scores(self):
        with open(self.high_score_file_path, "w") as high_score_file:
            for name, score in self.high_scores[:self.no_of_high_scores]:
                serialized_entry = self.serializer.serialize_entry(name, score)
                high_score_file.write(serialized_entry)

    def score_and_store(self, player_name, game_word, no_of_mistakes_made):

        current_player_score = self.scoring_function(game_word=game_word,
                                                     no_of_mistakes_made=no_of_mistakes_made)

        self._update_high_scores(new_scores=[(player_name, current_player_score)])
        self._persist_high_scores()

        return current_player_score

    def _update_high_scores(self, new_scores):

        interim_high_scores = self.high_scores+new_scores
        interim_high_scores = sorted(interim_high_scores,
                                     key=lambda entry: entry[1],
                                     reverse=True)

        self.high_scores = interim_high_scores[:self.no_of_high_scores]

    def print_high_scores(self):
        print("\t High Scores")
        print("\t ===========")
        for name, score in self.high_scores:
            print("\t %s: %d \t\n" % (name, score))
