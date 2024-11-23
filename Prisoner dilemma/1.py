import random

PAYOFF_MATRIX = {
    ('C', 'C'): (4, 4),
    ('C', 'D'): (0, 5),
    ('D', 'C'): (5, 0),
    ('D', 'D'): (2, 2)
}


def play_type_1(): 
    return 'C'

def play_type_2():  
    return 'D'

def play_type_3(): 
    return random.choice(['C', 'D'])

def play_type_4(opponent_last_move):  
    return opponent_last_move if opponent_last_move else 'C'

def play_single_game(strategy1, strategy2, rounds=10):
    score1, score2 = 0, 0
    move1, move2 = None, None
    
    for _ in range(rounds):
        if strategy1 == play_type_4:
            move1 = strategy1(move2)
        else:
            move1 = strategy1()  
        
        if strategy2 == play_type_4:
            move2 = strategy2(move1)
        else:
            move2 = strategy2()  

        payoff1, payoff2 = PAYOFF_MATRIX[(move1, move2)]
        score1 += payoff1
        score2 += payoff2

    return score1, score2

def run_tournament(players, rounds=10, simulations=10):
    total_scores = [0] * len(players)  
    num_players = sum(players)  

    for _ in range(simulations):
        player_strategies = (
            [play_type_1] * players[0] +
            [play_type_2] * players[1] +
            [play_type_3] * players[2] +
            [play_type_4] * players[3]
        )
        scores = [0] * num_players

        # Simulate matches
        for i in range(num_players):
            for j in range(i + 1, num_players):
                score1, score2 = play_single_game(player_strategies[i], player_strategies[j], rounds)
                scores[i] += score1
                scores[j] += score2

        idx = 0
        for t in range(len(players)):
            total_scores[t] += sum(scores[idx:idx + players[t]])
            idx += players[t]

    print("\nAverage scores per strategy:")
    for t, total in enumerate(total_scores):
        avg_score = total / (players[t] * simulations) if players[t] > 0 else 0
        print(f"Strategy TYPE {t + 1}: {avg_score:.2f}")

if __name__ == "__main__":
    print("Enter the number of players for each strategy (TYPE 1 to TYPE 4):")
    input_players = input("e.g., '30 0 0 0' -> ").split()
    players = list(map(int, input_players))

    if sum(players) < 2:
        print("At least 2 players are required to run the tournament.")
    else:
        run_tournament(players)
