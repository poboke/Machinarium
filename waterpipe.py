#coding:utf-8

from tools import cost_time


class Valve:
    """阀门类
    Attributes:
        name: 阀门名字
        closed: 是否关闭
        outlets: 连接的阀门对象列表
    """

    def __init__(self, name):
        """使用阀门名字初始化阀门
        Args:
            name: 阀门名字
        """
        self.name = name
        self.closed = False
        self.outlets = []

    def link(self, valve):
        """连接某个阀门
        Args:
            valve: 阀门对象
        """
        self.outlets.append(valve)

    def show(self):
        """打印阀门名和连接的阀门
        Print: "阀门名(是否关闭) : [连接的阀门名列表]"
        """
        outlet_names = [x.name for x in self.outlets]
        print("%s(%d) : %s"%(self.name, self.closed, outlet_names))


class Game:
    """扳手关水管游戏
    Attributes:
        valve_dict: 存放阀门的字典{阀门名:阀门对象}
        water_inlet: 入水口
        water_outlet: 出水口
        ops: 操作步骤列表
    """

    def __init__(self, link_valves):
        """使用连接的阀门列表初始化游戏
        Args:
            link_valves: 相连的阀门列表
        """
        self.valve_dict = {}
        for link_valve in link_valves:
            from_name, to_name = link_valve
            self.add_link_valve(from_name, to_name)
        self.water_inlet = self.valve_dict['X']
        self.water_outlet = self.valve_dict['Y']
        self.ops = []

    def add_link_valve(self, from_name, to_name):
        """添加相连的阀门
        Args:
            from_name: 起始阀门名
            to_name: 目的阀门名
        """
        from_valve = self.valve_dict.get(from_name)
        if not from_valve:
            from_valve = Valve(from_name)
            self.valve_dict[from_name] = from_valve

        to_valve = self.valve_dict.get(to_name)
        if not to_valve:
            to_valve = Valve(to_name)
            self.valve_dict[to_name] = to_valve

        from_valve.link(to_valve)
        to_valve.link(from_valve)

    def show(self):
        """打印出所有阀门的值"""
        for key in self.valve_dict:
            valve = self.valve_dict[key]
            valve.show()

    def is_done(self):
        """判断是否完成游戏
        Returns: 是否完成游戏
        """
        return not self.is_connected(self.water_inlet, self.water_outlet)

    def is_connected(self, from_valve, to_valve):
        """判断两个阀门是否相通
        Args:
            from_valve: 起始阀门
            to_valve: 目的阀门
        Returns: 是否相通
        """
        visited = set()
        def dfs(valve):
            """使用DFS判断
            Args:
                valve: 阀门对象
            Returns: 是否相通
            """
            # 如果阀门关闭，肯定不相通
            if valve.closed:
                return False
            # 如果阀门和目的阀门是同一个阀门，说明相通
            if valve == to_valve:
                return True
            # 如果阀门已经访问过了，说明不相通
            if valve.name in visited:
                return False
            visited.add(valve.name)
            # 遍历目的阀门的所有连接阀门，递归判断是否相通
            for valve in valve.outlets:
                if dfs(valve):
                    return True
        # 如果任意一个阀门关闭了，肯定不相通
        if from_valve.closed or to_valve.closed:
            return False
        return dfs(from_valve)
        
    def backtrack(self):
        """使用回溯求解答案
        Returns: 是否找到了答案
        """
        # 如果关掉了3个阀门，就验证游戏结果
        if len(self.ops) == 3:
            return self.is_done()

        valve_names = [
            'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I',      'J', 'K',
        ]
        for valve_name in valve_names:
            valve = self.valve_dict[valve_name]
            if valve.closed:
                continue
            # 关闭当前阀门
            valve.closed = True
            self.ops.append(valve.name)
            # 递归验证其它阀门
            if self.backtrack():
                return True
            # 打开当前阀门进行回溯
            valve.closed = False
            self.ops.pop()

    def solve(self):
        """调用回溯算法求解答案"""
        if self.backtrack():
            print('')
            print(self.ops)

    def test(self):
        """验证操作步骤"""
        ops = ['A', 'B', 'H']
        for op in ops:
            print(op)
            valve = self.valve_dict[op]
            valve.closed = True
        print(self.is_done())


@cost_time
def main():
    link_valves = [
        ('X', 'G'), ('X', 'H'), ('X', 'K'), ('X', 'B'),
        ('Y', 'C'), ('Y', 'D'), ('Y', 'E'), ('Y', 'J'), 
        ('Y', 'B'), ('Y', 'H'), ('Y', 'I'),
        ('A', 'D'), ('A', 'C'), ('A', 'I'), ('A', 'J'),
        ('A', 'F'), ('A', 'G'),
        ('B', 'I'), ('F', 'K'),
    ]
    game = Game(link_valves)
    game.show()
    # game.test()
    game.solve()

if __name__ == "__main__":
    main()

