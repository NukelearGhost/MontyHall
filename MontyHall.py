import multiprocessing
from secrets import randbelow, randbits
import csv
import time

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
            self.chosen = True
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

    # Pick the first door.
    firstchoice = randbelow(3)

    # Decide whether to switch or stay.
    secondchoice = bool(randbits(1))

    # Select the first door.
    doors[firstchoice].togglechoice()
    doors[firstchoice].open_door()

    # Find the door that has not been opened and does not contain the prize.
    for door in doors:
        if not door.chosen and not door.prize:
            door.open_door()

    # If switching doors, switch doors
    if secondchoice:
        for door in doors:
            if door.chosen:
                door.togglechoice()
            elif not door.chosen and not door.open:
                door.togglechoice()

    # Determine victory or defeat
    for door in doors:
        if door.chosen and door.prize:
            result = 'win'
        else:
            result = 'lose'

    results = []

    for door in doors:
        results.append(door.open)
        results.append(door.chosen)
        results.append(door.prize)

    with open('results.csv', 'a', newline='') as output:
        writer = csv.writer(output,
                            delimiter=',',
                            quotechar='\'',
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow((result,
                         results[0],
                         results[1],
                         results[2],
                         results[3],
                         results[4],
                         results[5],
                         results[6],
                         results[7],
                         results[8],
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
        elif selection=='analyze':
            analyze_data(True)
    one_run_end = time.time()
    print("Single Run Result: {}\n".format(one_run_end - one_run_start))

    # Ten Run
    ten_run_tot = 0
    n = 10
    while n > 0:
        ten_run_start = time.time()
        if selection == 'play':
            play_game()
        elif selection=='analyze':
            analyze_data(True)
        ten_run_end = time.time()
        ten_run_tot += (ten_run_end - ten_run_start)
        n -= 1

    print("Ten Run Result: {}".format(ten_run_tot / 10))
    print("Ten Run Total: {}\n".format(ten_run_tot))

    # Hundred Run
    hund_run_tot = 0
    n = 100
    while n > 0:
        hundred_run_start = time.time()
        if selection == 'play':
            play_game()
        elif selection=='analyze':
            analyze_data(True)
        n -= 1
        hundred_run_end = time.time()
        hund_run_tot += (hundred_run_end - hundred_run_start)
    print("Hundred Run Avg: {}".format(hund_run_tot / 100))
    print("Hundred Run Total: {}\n".format(hund_run_tot))

    # Thousand Run
    thou_run_tot = 0
    n = 1000
    while n > 0:
        thousand_run_start = time.time()
        if selection == 'play':
            play_game()
        elif selection=='analyze':
            analyze_data(True)
        n -= 1
        thousand_run_end = time.time()
        thou_run_tot += (thousand_run_end - thousand_run_start)
    print("Thousand Run Avg: {}".format(thou_run_tot / 1000))
    print("Thousand Run Total: {}\n".format(thou_run_tot))

    # N Run
    n_tot = 0
    n = runs
    while n > 0:
        n_start = time.time()
        if selection == 'play':
            play_game()
        elif selection == 'analyze':
            analyze_data(True)
        n -= 1
        n_end = time.time()
        n_tot += (n_end - n_start)
    print("N Run Result: {}".format(n_tot / runs))
    print("N Run Total: {}\n".format(n_tot))


def analyze_data(runs=0, suppress=False):
    if runs:
        y = runs

        while y > 0:
            play_game()
            y -= 1

    results = []
    with open('results.csv', 'r') as input:
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


    win_prob = round((wins/losses) * 100, 2)
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
            "+ Games Won because Switch: {}\t{}%\n".format(win_switch, round((win_switch / wins) * 100, 2)),
            "+ Games Won because No Switch: {}\t{}%\n".format(win_noswitch, round((win_noswitch / wins) * 100, 2))
        )

if __name__ == '__main__':

    # Settings
    i = 1 # 1 = Main, 2 = analyze, 3 = speed test

    # Gameplay
    n = 1000000 # Number of times to play the game (gets decremented)
    x = n  # Static number of times to play the game
    z = 10000 # Main will print out a status update every z runs

    if i == 1:

        # Set header of datafile
        header = "Result, Door1_open, Door1_chosen,Door1_prize, Door2_open, Door2_chosen," \
                 "Door2_prize, Door3_open, Door3_chosen, Door3_prize, first pick, switch\n"

        with open('results.csv', 'w') as results:
            results.write(header)

        while n > 0:
            if n % z == 0:
                print(n)
            play_game()
            n -= 1

    elif i == 2:
        analyze_data()

    elif i == 3:
        speedtest('play', x)