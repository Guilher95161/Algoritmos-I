def winner(play1,play2):
    if play1==play2:
        return "draw"
    elif (play1=='stone' and play2=='scissor') or (play1=='scissor' and play2=='paper') or (play1=='paper' and play2=='stone'):
        return "player1"
    else:
        return "player2"
