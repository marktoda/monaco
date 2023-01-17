import sys
import json
import curses
from monaco import ActionType

class CarState:
    def __init__(self, balance, y, speed, shield):
        self.balance = balance
        self.y = y
        self.speed = speed
        self.shield = shield


def default_car_state():
    return CarState(17500, 0, 0, 0)

def group_turns(all_turns):
    turns = []
    # group in chunks of 3
    for i in range(0, len(all_turns), 3):
        turns.append(all_turns[i:i+3])
    return turns


class GamePrinter:
    def __init__(self, window, game_data):
        self.window = window
        self.game_data = game_data
        self.turns = group_turns(self.game_data["turns"])
        self.car_state = [default_car_state(), default_car_state(), default_car_state()]
        self.actionsSold = {
            ActionType.ACCELERATE: 0,
            ActionType.SHELL: 0,
            ActionType.SUPER_SHELL: 0,
            ActionType.BANANA: 0,
            ActionType.SHIELD: 0,
        }

    def start(self):
        turn = 0
        num_turns = len(self.turns)
        win = self.print_game(0)
        while turn <= num_turns:
            k = win.getkey()
            if k == "l":
                turn = min(num_turns - 1, turn + 1)
            elif k == "L":
                turn = min(num_turns - 1, turn + 5)
            elif k == "h":
                turn = max(0, turn - 1)
            elif k == "H":
                turn = max(0, turn - 5)
            else:
                break
            win = self.print_game(turn)

    def set_car_states(self, idx):
        for i, state in enumerate(self.turns[idx]):
            [balance, y, speed, shield] = state
            self.car_state[i] = CarState(balance, y, speed, shield)

    def print_game(self, turn_idx):
        self.set_car_states(turn_idx)

        self.window.clear()
        self.print_sidebar(turn_idx)

        header_display = curses.newwin(5, curses.COLS, 0, 0)
        header_display.clear()
        header_display.addstr(f"--------------- DISPLAYING GAME -- TURN {turn_idx} ---------------\n")
        if turn_idx == len(self.turns) - 1:
            header_display.addstr(f"###-- GAME OVER --###")
        header_display.refresh()

        cars_display = curses.newwin(int(curses.LINES / 2), curses.COLS, 5, 25)
        cars_display.clear()

        for state in self.car_state:
            cars_display.addstr(get_distance_str(state.y))
        cars_display.refresh()
        return cars_display

    def print_sidebar(self, turn_idx):
        car_name_display = curses.newwin(int(curses.LINES / 2), 50, 5, 0)
        car_name_display.clear()

        for i, car in enumerate(self.game_data["cars"]):
            is_turn = (turn_idx + 1) % 3 == i
            state = self.car_state[i]
            car_name_display.addstr(f"{car if not is_turn else '> ' + car}\n")
            car_name_display.addstr(f"\ty: {state.y}\n")
            car_name_display.addstr(f"\tspeed: {state.speed}\n")
            car_name_display.addstr(f"\tbalance: {state.balance}\n")
            car_name_display.addstr(f"\tshield: {state.shield}\n\n")
            car_name_display.addstr(f"\tACTIONS:\n")
            car_name_display.addstr(f"\t- accelerate")
            car_name_display.addstr(f"\n\n\n\n")
        car_name_display.refresh()

        commands_display = curses.newwin(int(curses.LINES / 4), 25, int(curses.LINES / 2), 0)
        commands_display.addstr("Commands:\n")
        commands_display.addstr("l - forward a turn\n")
        commands_display.addstr("h - back a turn\n")
        commands_display.addstr("L - forward 5 turns\n")
        commands_display.addstr("H - back 5 turns\n")
        commands_display.addstr("q/ctrl+c - quit\n")
        commands_display.refresh()


def main(window):
    # read file name from command line
    if len(sys.argv) != 2:
        print("Usage: show_game.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        data = json.loads(f.read())

    printer = GamePrinter(window, data)
    printer.start()

def get_distance_str(y):
    total_ticks = curses.COLS - 50
    tick_space = min(total_ticks, int(y / 1000 * total_ticks))
    res = ""
    for _ in range(tick_space):
        res += "-"
    res += "x"
    for _ in range(total_ticks - tick_space - 1):
        res += "-"
    res += "\n\n\n\n\n\n\n\n\n\n\n"
    return res

if __name__ == '__main__':
    curses.wrapper(main)
