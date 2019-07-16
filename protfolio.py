from itertools import permutations, combinations
import numpy as np
from torch import nn
import torch
import torch.nn.functional as F
from matplotlib import pyplot as plt


class Result:

    def __init__(self, winner, n):
        self.first = winner[0]
        self.second = winner[1]
        self.third = winner[2]
        self.horse = [str(i+1) for i in range(n)]

    def returns(self, odds, single=True, place=True, double=True, place_q=True):

        r = []
        i = 0

        if single:
            for s in self.horse:
                if s == self.first:
                    r.append(odds[i])
                else:
                    r.append(0)
                i += 1

        if place:
            for p in self.horse:
                if p == self.first or p == self.second or p == self.third:
                    r.append(odds[i])
                else:
                    r.append(0)
                i += 1

        if double:
            for d in combinations(self.horse, 2):
                if self.first in d and self.second in d:
                    r.append(odds[i])
                else:
                    r.append(0)
                i += 1

        if place_q:
            for pq in combinations(self.horse, 2):
                winners = (self.first, self.second, self.third)
                if pq[0] in winners and pq[1] in winners:
                    r.append(odds[i])
                else:
                    r.append(0)
                i += 1

        return np.array(r)


class Portfolio(nn.Module):

    def __init__(self, h, single=True, place=True, double=True, place_q=True):
        super(Portfolio, self).__init__()
        size = 0
        if single:
            size += h
        if place:
            size += h
        if double:
            size += h*(h-1)/2
        if place_q:
            size += h*(h-1)/2

        w = np.random.normal(loc=1, scale=0.2, size=[1, int(size)])
        w = torch.tensor(w)
        self.weights = nn.Parameter(w)

    def forward(self):
        pass

    def loss(self, outcomes):
        amount = F.relu(self.weights.sum())
        r = outcomes * self.weights
        r = r.sum(dim=1) - amount
        return -r.sum()

    def plot(self, outcomes):
        r = F.relu(self.weights).detach()
        invest = float(r.sum())
        print('Total Investment: ', invest)
        r = outcomes * r
        r = r.sum(dim=1)
        r = r.numpy()
        print('Average return = ', np.mean(r) / invest)
        losses = 0
        for i in r:
            if i < invest:
                losses += 1
        print('Loss Probability = ', losses/len(r))
        plt.hist(r, bins='auto')
        plt.axvline(x=invest, color='Red')
        plt.show()


def random_odds(h, factor=0.82, single=True, place=True, double=True, place_q=True):

    odds = []

    if single:
        mean = h * factor
        single_odd = np.random.normal(loc=mean, scale=h / 2, size=h)
        single_odd = np.abs(single_odd)
        odds.extend(single_odd.tolist())

    if place:
        mean = h / 3 * factor
        place_odd = np.random.normal(loc=mean, scale=h / 3, size=h)
        single_odd = np.abs(place_odd)
        odds.extend(place_odd.tolist())

    if double:
        mean = h * (h - 1) / 2 * factor
        double_odd = np.random.normal(loc=mean, scale=2 * h, size=int(h * (h - 1) / 2))
        double_odd = np.abs(double_odd)
        odds.extend(double_odd.tolist())

    if place_q:
        mean = h * (h - 1) / 6 * factor
        pq_odd = np.random.normal(loc=mean, scale=h, size=int(h * (h - 1) / 2))
        pq_odd = np.abs(pq_odd)
        odds.extend(pq_odd.tolist())

    return odds


class Odds:

    def __init__(self, odd_dict):
        self.odd = odd_dict
        self.no_horse = len(odd_dict['win+place'])
        self.numbers = [str(i + 1) for i in range(self.no_horse)]

    def locate_odds(self, df, h1, h2=None, option=None):

        if h2 is None:
            h1 = int(h1)
            if option == 'win':
                y = h1 + 1
                x = 4
            else:
                y = h1 + 1
                x = 4
        else:
            h1 = int(h1)
            h2 = int(h2)
            if h1 > h2:
                tmp = h1
                h1 = h2
                h2 = tmp
            if h1 < 8:
                y = h1
                x = h2 + 1
            else:
                y = h2 - 7
                x = h1 - 7
        return float(df.loc[y, x])

    def to_list(self, single=True, place=True, double=True, place_q=True):

        odds = []

        if single:
            for h in self.numbers:
                odd = self.locate_odds(self.odd['win+place'], h, option='win')
                odds.append(odd)

        if place:
            for h in self.numbers:
                odd = self.locate_odds(self.odd['win+place'], h, option='place')
                odds.append(odd)

        if double:
            for h in combinations(self.numbers, 2):
                odd = self.locate_odds(self.odd['quinella'], *h)
                odds.append(odd)

        if place_q:
            for h in combinations(self.numbers, 2):
                odd = self.locate_odds(self.odd['quinella_p'], *h)
                odds.append(odd)

        return odds


o = random_odds(14, factor=0.82, double=False)
s = [str(i+1) for i in range(14)]
results = [Result(r, 14) for r in permutations(s, 3)]
pays = [r.returns(o, double=False) for r in results]
out = np.stack(pays, axis=0)
out = torch.tensor(out)
port = Portfolio(14, double=False)
Optimizer = torch.optim.SGD([port.weights], lr=0.0001, momentum=0.3)
for i in range(500):
    Optimizer.zero_grad()
    l = port.loss(out)
    l.backward()
    Optimizer.step()
l = port.loss(out)
port.plot(out)



