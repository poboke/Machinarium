#coding:utf-8

from tools import cost_time

L = 1   #左箭头
S = 0   #空格
R = -1  #右箭头

class Game:
    """箭头换位置游戏
    Attributes:
        values: 游戏状态列表
        length: 游戏状态列表长度
        ops: 操作步骤列表
    """

    def __init__(self, values):
        """初始化方法
        Args:
            values: 初始游戏状态列表
        """
        self.values = values
        self.length = len(self.values)
        self.ops = []

    def copy(self):
        """拷贝对象
        Returns: 新的游戏对象
        """
        game = Game(self.values[:])
        game.ops = self.ops[:]
        return game

    def show(self):
        """打印出所有箭头的值"""
        print(self.values)

    def move(self, index):
        """移动箭头
        Args:
            index: 箭头所在的下标
        Returns: 是否移动成功
        """
        value = self.values[index]
        new_index = index
        for _ in range(2):
            # 按箭头的方向移动下标
            new_index += value
            if new_index < 0 or new_index >= self.length:
                return False
            new_value = self.values[new_index]
            if new_value == S:
                # 如果遇到空格，就交换两个位置的值
                self.values[index], self.values[new_index] = \
                    self.values[new_index], self.values[index]
                return True
        return False

    def is_done(self):
        """判断是否完成游戏
        Returns: 是否完成
        """
        # 如果中间不是空格，肯定未完成
        middle = self.length / 2
        if self.values[middle] != S:
            return False
        # 判断左半部分是否全部是方向朝左的箭头
        for i in range(0, middle):
            if self.values[i] != R:
                return False
        return True
        
    def get_space_neighbors(self):
        """获取空格左右两边可移动的箭头下标
        Returns: 下标列表
        """
        neighbors = []
        index = self.values.index(S)
        # 获取空格左边方向朝右的箭头
        for i in range(max(0, index-2), index):
            if self.values[i] == L:
                neighbors.append(i)
        # 获取空格右边方向朝左的箭头
        for i in range(index+1, min(index+3, self.length)):
            if self.values[i] == R:
                neighbors.append(i)
        return neighbors

    def solve(self):
        """使用BFS求解答案"""
        queue = [self]
        while queue:
            pre_game = queue.pop(0)
            # 获取空格左右两边的箭头下标
            neighbors = pre_game.get_space_neighbors()
            for index in neighbors:
                cur_game = pre_game.copy()
                if not cur_game.move(index):
                    continue
                cur_game.ops += [index]
                if cur_game.is_done():
                    # 如果游戏完成，则打印操作步骤
                    cur_game.show()
                    print(cur_game.ops)
                    return
                # 将当前游戏加入队列
                queue.append(cur_game)

    def test(self):
        """验证操作步骤"""
        ops = [2, 4, 5, 3, 1, 0, 2, 4, 6, 5, 3, 1, 2, 4, 3]
        # ops = [4, 2, 1, 3, 5, 6, 4, 2, 0, 1, 3, 5, 4, 2, 3]
        for op in ops:
            print op, "=>",
            self.move(op)
            self.show()


@cost_time
def main():
    values = [L, L, L, S, R, R, R]
    game = Game(values)
    game.show()
    # game.test()
    game.solve()

if __name__ == "__main__":
    main()

