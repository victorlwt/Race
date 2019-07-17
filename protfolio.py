from itertools import permutations, combinations
import numpy as np
from torch import nn
import torch
import torch.nn.functional as F
from matplotlib import pyplot as plt


class Portfolio:

    def __init__(self, h, odds=None, single=True, place=True, double=True, place_q=True):
        size = 0
        if single:
            size += h
        if place:
            size += h
        if double:
            size += h*(h-1)/2
        if place_q:
            size += h*(h-1)/2

        self.single = single
        self.place = place
        self.double = double
        self.place_q = place_q

        w = np.random.normal(loc=1, scale=0.2, size=[1, int(size)])
        self.weights = torch.tensor(w, dtype=torch.float32, requires_grad=True)
        self.optim = torch.optim.SGD([self.weights], lr=0.0001, momentum=0.2)

        self.horse = [str(i + 1) for i in range(h)]
        self.horse_combination = [c for c in combinations(self.horse, 2)]
        self.odds = odds

    def forward(self, outcomes):
        amount = F.relu(self.weights.sum())
        r = outcomes * self.weights
        r = r.sum(dim=1) - amount
        return -r.sum()

    def plot(self):

        pays = [self._return(r) for r in permutations(self.horse, 3)]
        pays = np.stack(pays, axis=0)
        pays = torch.tensor(pays)

        w = F.relu(self.weights).detach()
        invest = float(w.sum())
        print('Total Investment: ', invest)
        w = pays * w
        w = w.sum(dim=1)
        w = w.numpy()
        print('Average return = ', np.mean(w) / invest)
        losses = 0
        for i in w:
            if i < invest:
                losses += 1
        print('Loss Probability = ', losses/len(w))
        plt.hist(w, bins='auto')
        plt.axvline(x=invest, color='Red')
        plt.show()

    def optimize(self):

        pays = [self._return(r) for r in permutations(self.horse, 3)]
        pays = np.stack(pays, axis=0)
        pays = torch.tensor(pays)
        for i in range(300):
            self.optim.zero_grad()
            loss = self.forward(pays)
            loss.backward()
            self.optim.step()

    def profit(self, winner):
        r = self._return(winner)
        r = r.view([210, 1])
        p = torch.matmul(F.relu(self.weights), r)
        return float(p)

    @property
    def amount(self):
        a = F.relu(self.weights).sum()
        return float(a)

    def _return(self, winner):

        r = []
        i = 0

        if self.single:
            for s in self.horse:
                if s == winner[0]:
                    r.append(self.odds[i])
                else:
                    r.append(0)
                i += 1

        if self.place:
            for p in self.horse:
                if p == winner[0] or p == winner[1] or p == winner[2]:
                    r.append(self.odds[i])
                else:
                    r.append(0)
                i += 1

        if self.double:
            for d in self.horse_combination:
                if winner[0] in d and winner[1] in d:
                    r.append(self.odds[i])
                else:
                    r.append(0)
                i += 1

        if self.place_q:
            for pq in self.horse_combination:
                if pq[0] in winner and pq[1] in winner:
                    r.append(self.odds[i])
                else:
                    r.append(0)
                i += 1

        return torch.tensor(r)


class Odds:

    def __init__(self, odd_dict):
        self.odd = odd_dict
        self.no_horse = len(odd_dict['win+place'])-1
        self.numbers = [str(i + 1) for i in range(self.no_horse)]

    @staticmethod
    def locate_odds(df, h1, h2=None, option=None):

        if h2 is None:
            h1 = int(h1)
            if option == 'win':
                y = h1
                x = 4
            else:
                y = h1
                x = 5
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

    @staticmethod
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


import pickle as pk
f = open('./Data/Odds/20190714_odd.dfdl', 'rb')
od = pk.load(f)
f.close()
odd = Odds(od[0])
o = odd.to_list()
port = Portfolio(14, o)
port.optimize()

port.plot()
p = port.profit(['6', '1', '4'])
print(p)




