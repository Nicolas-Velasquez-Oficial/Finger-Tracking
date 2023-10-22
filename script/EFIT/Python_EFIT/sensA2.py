import random

def sens_a2():
    opts = {
        'thr': 0.1,
        'F0iidtol': 0.005,
        'maxFunEvals': 25000,
        'maxIter': 25000,
        'verbose': False,
    }

    Tmin = 10
    Tmax = 60

    Ts = round(random.uniform(Tmin, Tmax))

    return Ts

result = sens_a2()
print(result)