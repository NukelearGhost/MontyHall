import multiprocessing
from os import path
from secrets import randbelow, randbits
import csv
import time
import argparse


class door:
    def __init__(self):
        self.open = False
        self.prize = False
        self.chosen = False
        self.switched = False

    def open_door(self):
        self.open = True

    def setprize(self):
        self.prize = True

    def togglechoice(self):
        if self.chosen:
            self.chosen = False
        else:
            self.chosen = True


def generate_doors():
    doors = []
    for i in range(0, 3):
        x = door()
        doors.append(x)

    # Pick which door hides the prize.
    i = randbelow(3)
    doors[i].setprize()

    return doors


def play_game():
    doors = generate_doors()

    # Pick first door
    firstchoice = randbelow(3)
    doors[firstchoice].togglechoice()

    # Find the door that has not been opened and does not contain the prize.
    for door in doors:
        if not door.chosen and not door.prize:
            door.open_door()

    # If switching doors, switch doors
    secondchoice = bool(randbits(1))

    if secondchoice:
        for door in doors:
            if door.chosen:
                door.togglechoice()
            elif not door.chosen and not door.open:
                door.togglechoice()

    results = []

    # Determine victory or defeat
    for door in doors:
        if door.chosen and door.prize:
            results.append('win')
        else:
            results.append('lose')

    for door in doors:
        results.append(door.open)
        results.append(door.chosen)
        results.append(door.prize)

    with open('results.csv', 'a', newline='') as output:
        writer = csv.writer(output,
                            delimiter=',',
                            quotechar='\'',
                            quoting=csv.QUOTE_MINIMAL)

        writer.writerow((results[0],
                         results[1],
                         results[2],
                         results[3],
                         results[4],
                         results[5],
                         results[6],
                         results[7],
                         results[8],
                         results[9],
                         firstchoice + 1,
                         secondchoice
                         ))


def speedtest(selection, runs):
    print(
        "--------------------\n",
        "        Results     \n",
        "--------------------\n",
        "Test: {}\n".format(selection),
    )

    one_run_start = time.time()
    if selection == 'play':
        if selection == 'play':
            play_game()
        elif selection == 'analyze':
            analyze_data(suppress=True)
    one_run_end = time.time()
    print("Single Run Result: {}\n".format(one_run_end - one_run_start))

    # Ten Run
    ten_run_tot = 0
    n = 10
    while n > 0:
        ten_run_start = time.time()
        if selection == 'play':
            play_game()
        elif selection == 'analyze':
            analyze_data(n, suppress=True)
        ten_run_end = time.time()
        ten_run_tot += (ten_run_end - ten_run_start)
        n -= 1

    print("Ten Run Avg: {}".format(ten_run_tot / 10))

    # Hundred Run
    hund_run_tot = 0
    n = 100
    while n > 0:
        hundred_run_start = time.time()
        if selection == 'play':
            play_game()
        elif selection == 'analyze':
            analyze_data(n, suppress=True)
        n -= 1
        hundred_run_end = time.time()
        hund_run_tot += (hundred_run_end - hundred_run_start)
    print("Hundred Run Avg: {}".format(hund_run_tot / 100))

    # Thousand Run
    thou_run_tot = 0
    n = 1000
    while n > 0:
        thousand_run_start = time.time()
        if selection == 'play':
            play_game()
        elif selection == 'analyze':
            analyze_data(n, suppress=True)
        n -= 1
        thousand_run_end = time.time()
        thou_run_tot += (thousand_run_end - thousand_run_start)
    print("Thousand Run Avg: {}".format(thou_run_tot / 1000))


def analyze_data(file='./results.csv', suppress=False):
    # Analyze results from output of simulation
    results = []
    with open(file, 'r') as input:
        reader = csv.reader(input,
                            delimiter=',',
                            quotechar='\''
                            )

        for line in reader:
            results.append(line)

    count_results = -1
    wins = 0
    losses = 0
    switches = 0
    nonswitches = 0
    win_switch = 0
    win_noswitch = 0

    for result in results:
        count_results += 1

        # Get win/loss stats
        if result[0] == 'win':
            wins += 1
        elif result[0] == 'lose':
            losses += 1

        # Get switch stats
        if result[11] == 'True':
            switches += 1
        elif result[11] == 'False':
            nonswitches += 1

        # Count wins because switch versus those because no switch
        if result[0] == 'win' and result[11] == 'True':
            win_switch += 1
        if result[0] == 'win' and result[11] == 'False':
            win_noswitch += 1

    win_prob = round((wins / losses) * 100, 2)
    win_sw_prob = round((wins / switches) * 100, 2)
    win_ns_prob = round((wins / nonswitches) * 100, 2)

    if not suppress:
        print(
            "--------------------\n",
            "        Results     \n",
            "--------------------\n",

            "Records Analyzed: {}\n\n".format(count_results),

            # Totals
            "+ Total Wins: {}\n".format(wins),
            "+ Total Losses: {}\n".format(losses),
            "+ Total Switches: {}\n".format(switches),
            "+ Total Non-Switches: {}\n\n".format(nonswitches),

            # Probabilities
            "+ Overall Win Probability: {}%\n\n".format(win_prob),

            # Other Stats
            "+ Games won where door switched: {}\t{}%\n".format(
                win_switch, round((win_switch / wins) * 100, 2)),
            "+ Games won where door not switched: {}\t{}%\n".format(
                win_noswitch, round((win_noswitch / wins) * 100, 2))
        )


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Simulate the Monty Hall Problem: '
        'https://www.wikiwand.com/en/Monty_Hall_problem\n\n'
        'Example: python MontyHall.py -s 10 -a',
        formatter_class=argparse.RawTextHelpFormatter)

    mode_group = parser.add_mutually_exclusive_group()

    mode_group.add_argument('-s', '--sim',
                            metavar='n',
                            type=int,
                            action='store',
                            nargs='?',
                            const=1000,
                            help="Run Montyhall Simulation"
                            " n times (default 1000)")
    mode_group.add_argument('-sps', '--speedsim',
                            action='store_true',
                            help="Test simulation speed without analysis")
    mode_group.add_argument('-spa', '--speedana',
                            action='store_true',
                            help="Test simulation speed with analysis")

    parser.add_argument('-a', '--analyze',
                        metavar='FILE',
                        type=str,
                        action='store',
                        nargs='?',
                        const='./results.csv',
                        help="Analyze results file (default ./results.csv)")

    args = parser.parse_args()

    if args.sim:
        # Set header of datafile
        header = "Result, Door1_open, Door1_chosen, Door1_prize," \
            "Door2_open, Door2_chosen,Door2_prize, Door3_open,"\
            "Door3_chosen, Door3_prize, first pick, switch\n"

        with open('results.csv', 'w') as results:
            results.write(header)

        # Gameplay
        n = args.sim  # Number of times to play the game (gets decremented)
        x = n  # Static number of times to play the game

        print("Running simulation, please wait...\n\n")

        while n > 0:
            play_game()
            n -= 1
    elif args.speedsim:
        speedtest('play', args.speedsim)
    elif args.speedana:
        speedtest('analyze', args.speedana)

    if args.analyze:
        if path.exists(args.analyze):
            analyze_data(args.analyze)
        elif not path.exists(args.analyze):
            raise Exception("Unable to find file {}".format(args.analyze))
