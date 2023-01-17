import sys
import json
import curses

class CarState:
    def __init__(self, balance, y, speed, shield):
        self.balance = balance
        self.y = y
        self.speed = speed
        self.shield = shield


def default_car_state():
    return CarState(17500, 0, 0, 0)

class GamePrinter:
    car_state = [default_car_state(), default_car_state(), default_car_state()]

    def __init__(self, window, game_data):
        self.window = window
        self.game_data = game_data

    def start(self):
        turn = 0
        num_turns = self.game_data["numTurns"]
        while turn <= num_turns:
            win = self.print_game(turn)
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

    def print_game(self, turn_idx):
        self.window.clear()
        self.print_static()

        header_display = curses.newwin(5, curses.COLS, 0, 0)
        header_display.clear()
        header_display.addstr(f"--------------- DISPLAYING GAME -- TURN {turn_idx} ---------------\n")
        if turn_idx == self.game_data["numTurns"] - 1:
            header_display.addstr(f"###-- GAME OVER --###")
        header_display.refresh()

        cars_display = curses.newwin(int(curses.LINES / 2), curses.COLS, 5, 25)
        cars_display.clear()

        [balance, y, speed, shield] = self.game_data["turns"][turn_idx]
        self.car_state[(turn_idx + 1) % 3] = CarState(balance, y, speed, shield)

        for state in self.car_state:
            cars_display.addstr(get_distance_str(state.y))
        cars_display.refresh()
        return cars_display

    def print_static(self):
        car_name_display = curses.newwin(int(curses.LINES / 4), 25, 5, 0)
        car_name_display.clear()

        for i, car in enumerate(self.game_data["cars"]):
            state = self.car_state[i]
            car_name_display.addstr(f"{car}\n")
            car_name_display.addstr(f"\ty: {state.y}\n")
            car_name_display.addstr(f"\tspeed: {state.speed}\n")
            car_name_display.addstr(f"\tbalance: {state.balance}\n")
            car_name_display.addstr(f"\tshield: {state.shield}\n")
        car_name_display.refresh()

        commands_display = curses.newwin(int(curses.LINES / 4), 25, int(curses.LINES / 4), 0)
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
    tick_space = int(y / 1000 * total_ticks)
    res = ""
    for _ in range(tick_space):
        res += "-"
    res += "x"
    for _ in range(total_ticks - tick_space - 1):
        res += "-"
    res += "\n\n\n\n\n\n\n"
    return res


    # print game with curses
    # for i,  in enumerate(game_data["turns"]):

if __name__ == '__main__':
    curses.wrapper(main)
