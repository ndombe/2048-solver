import sys
sys.path.append('../APIs')
import numpy as np

class FeatureExtractor():
    def __init__(self, board):
        self.board = board

    def getfeatures(self):
        return self.combinefeatures([
            self.emptyTiles(),
            self.hasMerge(),
            self.maxTile(),
            self.gravityFactor(),
            self.accumulativeTiles()
        ])

    def combinefeatures(self, features):
        feat = {}
        for f in features:
            feat.update(f)
        return feat

    def hasMerge(self):
        '''
        Returns a dictionary with keys of the format <has_merge_axis_a_ij>, where
            * <axis> is either 'row' or 'col'
            * <a> takes values from [0,1,2,3] and represents a particular row or column
            * <i> and <j> denote the position of the two tiles respectively
        The value for each entry is the value of the 2 tiles that could be merged.

        Ex: The board
        [[2  0  0  0]
         [2  8  4  0]
         [2  0  0  0]
         [8  4  4  0]]

         Would generate the features:
         {'has_merge_row_3_12': 4,
          'has_merge_col_0_01': 2,
          'has_merge_col_0_12': 2,
          'has_merge_col_2_13': 4}
        '''
        feat = {}
        name = 'has_merge_{}_{}_{}{}'
        for axis in range(2):
            for index in range(4):
                line = self.board[index,
                                  :] if axis == 0 else self.board[:, index]
                for i in range(0, len(line)-1):
                    n = line[i]
                    if n == 0:
                        continue
                    for j in range(i+1, len(line)):
                        m = line[j]
                        if n != m and m != 0:
                            break
                        if n == m:
                            feat[name.format(
                                'row' if axis is 0 else 'col', index, i, j)] = n
                            break
        return feat
    
    def emptyTiles(self):
        '''
        Returns a single entry dictionary with the number of tiles that are still empty.
        '''
        return {'empty_tiles': len([1 for i in range(4) for j in range(4) if self.board[i,j]==0])}

    def maxTile(self):
        return {'max_tile': np.amax(self.board)}

    def gravityFactor(self):
        factor = 0
        for i in range(4):
            row = 0
            col = 0
            for j in reversed(range(3)):
                row += min(self.board[i, j+1] - self.board[i,j], 0)
                col += min(self.board[j+1, i] - self.board[j,i], 0)
            factor += row + col
        return {'gravity': factor}

    def accumulativeTiles(self):
        return {'accumulativeTiles': sum(sum(np.square(self.board)))}


# # Simulation Test
# g = Game()
# for _ in range(30):
#     import random
#     g.move(random.randint(0, 3))
# f = FeatureExtractor(g.board)
# print(g.board)
# print(f.getfeatures())
# #print(calculate_score(f.getfeatures()))
