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
        self.print_sidebar(turn_idx)

        self.window.clear()

        header_display = curses.newwin(5, curses.COLS, 0, 0)
        header_display.clear()
        header_display.addstr(f"--------------- DISPLAYING GAME -- TURN {turn_idx} ---------------\n")
        if turn_idx == len(self.turns) - 1:
            header_display.addstr(f"###-- GAME OVER --###", curses.A_STANDOUT)
        header_display.refresh()

        cars_display = curses.newwin(int(curses.LINES / 2), curses.COLS, 5, 25)
        cars_display.clear()

        for state in self.car_state:
            self.add_distance_str(cars_display, state.y)
        cars_display.refresh()

        return cars_display

    def print_sidebar(self, turn_idx):
        car_name_display = curses.newwin(int(curses.LINES / 2), 50, 5, 0)
        car_name_display.clear()


        for i, car in enumerate(self.game_data["cars"]):
            is_turn = (turn_idx + 1) % 3 == i
            state = self.car_state[i]
            car_name_display.addstr(f"{car if not is_turn else '> ' + car}\n", curses.A_BOLD if is_turn else 0)
            car_name_display.addstr(f"\ty: {state.y}\n")
            car_name_display.addstr(f"\tspeed: {state.speed}\n")
            car_name_display.addstr(f"\tbalance: {state.balance}\n")
            car_name_display.addstr(f"\tshield: {state.shield}\n\n")
            if not is_turn:
                car_name_display.addstr(f"\n\n\n\n\n")
            else:
                car_name_display.addstr(self.get_action_str(turn_idx))
        car_name_display.refresh()

        commands_display = curses.newwin(int(curses.LINES / 4), 25, int(curses.LINES / 2), 0)
        commands_display.addstr("Commands:\n")
        commands_display.addstr("l - forward a turn\n")
        commands_display.addstr("h - back a turn\n")
        commands_display.addstr("L - forward 5 turns\n")
        commands_display.addstr("H - back 5 turns\n")
        commands_display.addstr("q/ctrl+c - quit\n")

        [accel, shell, super, shield, banana] = self.game_data["prices"][turn_idx]
        commands_display.addstr("\n\n\n")
        commands_display.addstr("Prices:\n")
        commands_display.addstr(f"\tAccelerate: {accel}\n")
        commands_display.addstr(f"\tShell: {shell}\n")
        commands_display.addstr(f"\tSuper: {super}\n")
        commands_display.addstr(f"\tShield: {shield}\n")
        commands_display.addstr(f"\tBanana: {banana}\n")
        commands_display.refresh()

    def get_action_str(self, turn_idx):
        result = ""
        result += f"\tACTIONS:\n"

        lines_used = 0
        max_lines = 5
        [accel, shell, super, shield, banana] = self.game_data["actionsSold"][turn_idx]
        [prev_accel, prev_shell, prev_super, prev_shield, prev_banana] = self.game_data["actionsSold"][turn_idx - 1] if turn_idx > 0 else (0, 0, 0, 0, 0)
        if accel > prev_accel:
            result += f"\t- Accel {accel - prev_accel}\n"
            lines_used += 1

        if shell > prev_shell:
            result += f"\t- Shell {shell - prev_shell}\n"
            lines_used += 1

        if super > prev_super:
            result += f"\t- Super {super - prev_super}\n"
            lines_used += 1

        if banana > prev_banana:
            result += f"\t- Banana {banana - prev_banana}\n"
            lines_used += 1

        if shield > prev_shield:
            result += f"\t- Shield {shield - prev_shield}\n"
            lines_used += 1

        return result + "\n" * (max_lines - lines_used)

    def add_distance_str(self, win, y):
        total_ticks = curses.COLS - 50
        tick_space = min(total_ticks, int(y / 1000 * total_ticks))
        win.addstr("=" * (total_ticks + 2))
        win.addstr("\n\n")
        win.addstr("-" * tick_space)
        win.addstr("/x\\", curses.A_BOLD)
        win.addstr("-" * (total_ticks - tick_space - 1))
        win.addstr("\n\n")
        win.addstr("=" * (total_ticks + 2))
        win.addstr("\n\n\n\n\n\n\n")



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

if __name__ == '__main__':
    curses.wrapper(main)
