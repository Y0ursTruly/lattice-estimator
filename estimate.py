from estimator.lwe_parameters import LWEParameters
from estimator.nd import UniformMod, DiscreteGaussian
from estimator import LWE, schemes #schemes are in estimator/schemes.py
from math import log2

N = 32768
q = (1<<60)*(1<<60) #approximate product of [60,60] primes

Xs = UniformMod(3)
Xe = DiscreteGaussian(stddev=3.19) #SEAL default sigma is 3.19
#according to https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/sealmanual_v2.2.pdf
#and previously: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/09/sealmanual.pdf

my_config = LWEParameters(n=N, q=q, Xs=Xs, Xe=Xe)
est = LWE.estimate(my_config) # I need to find a machine with enough RAM that this doesn't get terminated
#est = LWE.estimate(schemes.Kyber512) # example that doesn't get terminated on github codespaces
best = min(est.values(), key=lambda x: x['rop'])
print("===========================")
print(best)
print("===========================")
print("Classical bits:", log2(best['rop']))
print("Quantum bits:", log2(best.get('rop_q', best['rop'])))