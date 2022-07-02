import pandas as pd
from dataclasses import dataclass
from enum import Enum, auto
import random

from farwest.model.attitudes import Attitude
from .check import check_type


cooperate_functions = dict()


def coopere(a: Attitude):
    assert type(a) == Attitude

    def wrapper(func):
        cooperate_functions[a] = func
        return func

    return wrapper


@coopere(Attitude.rancuniers)
def f(histo):
    if False in histo:
        return False
    return True


@coopere(Attitude.copieurs)
def f(histo):
    if len(histo) == 0:
        return True
    else:
        return histo[-1]


@coopere(Attitude.pacificateurs)
def f(histo):
    if len(histo) < 2:
        return True
    two_last = histo[len(histo) - 2:len(histo)]
    assert (len(two_last) == 2)
    if False not in two_last:
        return True
    r = random.randint(0, 1)
    return r == 0


@coopere(Attitude.repliquants_prudents)
def f(histo):
    if len(histo) < 2:
        return True
    two_last = histo[len(histo) - 2:len(histo)]
    assert (len(two_last) == 2)
    if False not in two_last:
        return True
    return False

@coopere(Attitude.delateurs)
def f(histo):
    return False

@coopere(Attitude.oeil_pour_oeil)
def f(histo):
    if len(histo) < 1:
        return False
    return histo[-1]

# bug ? c'est la meme chose que oeil_pour_oeil
@coopere(Attitude.prudents)
def f(histo):
    if len(histo) < 1:
        return False
    return histo[-1]

@coopere(Attitude.charmeurs)
def f(histo):
    if len(histo) % 3 == 0:
        return True
    if len(histo) % 3 == 1:
        return True
    if len(histo) % 3 == 2:
        return False
    assert False

@coopere(Attitude.fair_plays)
def f(histo):
    return True

@coopere(Attitude.filous)
def f(histo):
    if len(histo) % 3 == 0:
        return False
    if len(histo) % 3 == 1:
        return False
    if len(histo) % 3 == 2:
        return True
    assert False


for a in Attitude:
    if cooperate_functions.get(a) is None:
        raise RuntimeError(f"no cooperate function for {a.name}")


def make_campagne(nombre_de_braquages, gain_seul, gain_a_deux, a1:Attitude, a2:Attitude):
    histo1=[]
    histo2=[]
    histo=[]
    check_type(a1,Attitude)
    check_type(a2,Attitude)
    for i in range(0, nombre_de_braquages):
        c1 = cooperate_functions[a1](histo2)
        c2 = cooperate_functions[a2](histo1)
        histo1.append(c1)
        histo2.append(c2)
        if c1 and c2:
            gains1 = gain_a_deux / 2
            gains2 = gain_a_deux / 2
        elif not c1 and c2:
            gains1 = gain_seul
            gains2 = 0
        elif c1 and not c2:
            gains1 = 0
            gains2 = gain_seul
        elif not c1 and not c2:
            gains1 = 0
            gains2 = 0
        else:
            assert False

        histo.append([c1,c2,gains1,gains2])
            
    df = pd.DataFrame(columns=["histo1","histo2","gains A","gains B"],data=histo)

    return df


        
    
        