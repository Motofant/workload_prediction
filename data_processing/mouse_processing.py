import json
import pandas as pd


class MouseProcess:
    def __init__(self, data, mode) -> None:
        self.mode = mode
        self.data = data
        self.total_elements = len(self.data["0"].keys())-1 # remove endtime 
        self.res, self.nan, self.move = self.get_tasks()
        self.task_res = [x.count(True) for x in self.res]
        self.task_nan = [x.count(True) for x in self.nan]
        self.task_move = [sum(x) for x in self.move]

        self.total_res = sum(self.task_res)
        self.total_nan = sum(self.task_nan)
        self.total_move = sum(self.task_move)
    
    def get_tasks(self):
        total_result = []
        total_nan = []
        total_moves = []
        for task, result in self.data.items():
            task_result = []
            task_nan = [] 
            task_moves = []
            for movable, res in result.items():
                if movable == "time_end":
                    continue
                if res[-1]['overlap']:
                    task_result.append(movable[0]==res[-1]['overlap'][-1])
                else:
                    task_result.append(False)
                task_nan.append(not res[-1]['overlap'])

                task_moves.append(len(res)-1)
            total_result.append(task_result)
            total_moves.append(task_moves)
            total_nan.append(task_nan)
        print(total_result)
        print(total_nan)
        print(total_moves)
        return total_result, total_nan, total_nan
    
    def output_dict(self):
        return{
            self.mode+"total_el":self.total_elements,
            self.mode+"task_res":self.task_res,
            self.mode+"task_nan":self.task_nan,
            self.mode+"task_move":self.task_move,

            self.mode+"total_res":self.total_res,
            self.mode+"total_nan":self.total_nan,
            self.mode+"total_move":self.total_move,
        }

if __name__ == "__main__":
    with open("./logging/Sensor_test_1_dragging_user_entered.json",mode = "r") as file:
        #data = file.read().splitlines()
        data = json.load(file)
    print(json.dumps(data, indent=2))

    #print(data)
    x = MouseProcess(data=data)
    x.get_tasks()
    print(json.dumps(x.output_dict(), indent=2))