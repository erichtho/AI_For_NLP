import itertools

def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    candidates1 = [] 
    candidates2 = []
    bjoke = ''.join(hand).find('?B')>0
    rjoke = ''.join(hand).find('?R')>0
    ncards = []
    for card in hand:
        if card[0]!='?':
            ncards.append(card)

            if bjoke:
                candidates1.append(card_sum(card, 1) + (card[1] if card[1] in set(['S','C']) else 'S'))
                candidates1.append(card_sum(card, -1) + (card[1] if card[1] in set(['S','C']) else 'S'))
                candidates1.append(card[0] + list(set(['S','C']).difference(set(card[1])))[0])
            if rjoke:
                candidates2.append(card_sum(card, 1) + (card[1] if card[1] in set(['H','D']) else 'H'))
                candidates2.append(card_sum(card, -1) + (card[1] if card[1] in set(['H','D']) else 'H'))
                candidates2.append(card[0] + list(set(['H','D']).difference(set(card[1])))[0])
    
    if len(candidates2)==0 and len(candidates1)==0:
        return max([c5 for c5 in itertools.combinations(ncards,5)], key=hand_rank)
    else:
        return max([max([c5 for c5 in itertools.combinations(ncards+(list(s) if len(s[1])==2 else [s]), 5)], key=hand_rank) for s in list(itertools.product(candidates1, candidates2))+candidates1+candidates2], key=hand_rank)

def card_sum(card, num):
    return '--23456789TJQKA'['--23456789TJQKA'.find(card[0])+num]

def test_best_wild_hand():
    # assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
    #         == ['7C', 'TC', 'TD', 'TH', 'TS'])
    # assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
    #         == ['7C', '8C', '9C', 'JC', 'TC'])
    
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_wild_hand passes'


# help functions

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand) 
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)
    
def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    """Return True if the ordered 
    ranks form a 5-card straight."""
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has 
    exactly n-of-a-kind of. Return None if there 
    is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair here, return the two 
    ranks of the two pairs, else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None 
if __name__=='__main__':
    print(test_best_wild_hand())