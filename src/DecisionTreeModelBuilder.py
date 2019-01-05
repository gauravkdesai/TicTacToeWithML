import csv

import numpy as np
import pandas as pd
from joblib import dump, load
from  sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeRegressor


class DecisionTreeModelBuilder:
    def __init__(self, training_data_file, model_file):
        self.training_data_file = training_data_file
        self.model_file = model_file
        self.dt = None
        self.cv = None

    def get_data_from_file(self):
        print("Getting board data from {} file".format(self.training_data_file))
        board_data = []
        with open(self.training_data_file, "r") as file_to_read:
            file_reader = csv.reader(file_to_read)

            for row in file_reader:
                # print(",".join(row))
                if len(row) == 0:
                    continue

                row_data = {'board_state': row[0], 'next_move': row[1], 'score': row[2]}
                board_data.append(row_data)

        board_data_df = pd.DataFrame(board_data)
        print("Read {} records from file".format(board_data_df.size))
        return board_data_df


    def train_and_save_model(self):

        board_data_df = self.get_data_from_file()
        print("Training model for {} records".format(board_data_df.size))

        print("Glimpse at few records read from file")
        print(board_data_df.head())

        X = pd.DataFrame(data=board_data_df.loc[:, 'next_move'])
        Y = board_data_df.loc[:, 'score']

        # for each cell position, add +1 to X if it was current players move else add -1
        for cell_index in range(9):
            X.loc[:, str(cell_index)] =  board_data_df.loc[:, 'board_state'].apply(get_mov_info, args=(cell_index,))


        # self.cv = CountVectorizer(analyzer='char')
        # XCV = self.cv.fit_transform(board_data_df.loc[:, 'board_state'])
        #
        # for i, col in enumerate(self.cv.get_feature_names()):
        #     X.loc[:, col] = pd.SparseSeries(XCV[:, i].toarray().ravel(), fill_value=0)

        #print("Printing top X")
        #print(X.head())

        self.dt = DecisionTreeRegressor(max_depth=8)
        self.dt.fit(X, Y)

        dump((self.cv, self.dt), self.model_file)

        print("Model saved in file {}".format(self.model_file))

    def get_next_move_score(self, board_state, next_move):
        if self.dt is None:
            self.cv, self.dt = load(self.model_file)

        if self.dt is None:
            raise RuntimeError

        X = np.asarray(next_move)
        print(X)

        # XCV = self.cv.transform([board_state, ])
        # print(XCV.toarray())

        # X = np.append(X, XCV.toarray())
        # for each cell position, add +1 to X if it was current players move else add -1
        for cell_index in range(9):
            X=np.append(X,get_mov_info(board_state,cell_index))

        print("X,",X)

        #print(X.reshape(1, -1))

        predicted_score = self.dt.predict(X.reshape(1, -1))

        return predicted_score


def get_mov_info(board_state, cell_index):
    cell_already_marked = str(cell_index) in board_state

    if cell_already_marked:
        cell_sequence = board_state.index(str(cell_index))
        if cell_sequence%2 == len(board_state)%2:
            return 1  # current players move
        else:
            return -1  # opposite players moves
    else:
        return 0 # cell not marked



def main():
    model_builder = DecisionTreeModelBuilder("Board_Data.csv", "Decision_Tree_Model.txt")
    model_builder.train_and_save_model()
    # for i in range(9):
    #    print("Prediction:",model_builder.get_next_move_score(["0142",],[i,]))


if __name__ == "__main__":
    main()
