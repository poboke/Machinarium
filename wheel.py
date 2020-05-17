#coding:utf-8

from tools import cost_time

class Game:
    """红绿点转盘游戏
    Attributes:
        dots: 游戏状态列表
        wheel_poses: 转盘边上的点的下标列表
        ops: 操作步骤列表
    """

    def __init__(self, dots):
        """初始化游戏
        Args:
            dots: 存放12个点的数值
        """
        self.dots = dots
        self.wheel_poses = [
            [0, 1, 5, 8, 7, 3],
            [1, 2, 6, 9, 8, 4],
            [4, 5, 9, 11, 10, 7],
        ]
        self.ops = []

    def copy(self):
        """拷贝对象
        Returns: 新的游戏对象
        """
        game = Game(self.dots[:])
        game.ops = self.ops[:]
        return game

    def turn(self, index, clockwise):
        """转动轮盘
        Args:
            index: 转盘下标
            clockwise: 是否顺时针旋转
        """
        poses = self.wheel_poses[index]
        if clockwise:
            # 顺时针旋转
            temp = self.dots[poses[-1]]
            for i in range(len(poses)-1, -1, -1):
                self.dots[poses[i]] = self.dots[poses[i-1]]
            self.dots[poses[0]] = temp
        else:
            # 逆时针旋转
            temp = self.dots[poses[0]]
            for i in range(1, len(poses)):
                self.dots[poses[i-1]] = self.dots[poses[i]]
            self.dots[poses[-1]] = temp

    def is_done(self):
        """判断是否完成游戏
        Returns: 是否完成
        """
        return self.dots == [0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0]
        
    def show(self):
        """打印出点的位置"""
        text = '''
   %d   %d   %d

 %d   %d   %d   %d

   %d   %d   %d

     %d   %d
        '''%tuple(self.dots)
        print(text)
        
    def solve(self):
        """使用BFS求解答案"""
        # 将当前游戏加入队列
        queue = [self]
        while queue:
            pre_game = queue.pop(0)
            # 遍历3个转盘的下标
            for index in [0, 1, 2]:
                # 遍历两种旋转方向
                for clockwise in [True, False]:
                    # 拷贝上一个游戏状态来模拟游戏旋转
                    cur_game = pre_game.copy()
                    cur_game.turn(index, clockwise)
                    cur_game.ops += [(index, clockwise)]
                    if cur_game.is_done():
                        # 如果游戏完成，则打印操作步骤
                        cur_game.show()
                        print(cur_game.ops)
                        return
                    # 将当前游戏加入队列
                    queue.append(cur_game)

    def test(self):
        """验证操作步骤"""
        ops = [(0, True), (1, False), (2, True), (1, False)]
        # ops = [(0, True), (1, True), (2, False), (0, False), (0, False)]
        for op in ops:
            print(op)
            self.turn(*op)
            self.show()


@cost_time
def main():
    dots = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    # dots = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    game = Game(dots)
    game.show()
    # game.test()
    game.solve()


if __name__ == "__main__":
    main()

