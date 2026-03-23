from estimator.lwe_parameters import LWEParameters
from estimator.nd import UniformMod, DiscreteGaussian
from estimator import LWE, schemes #schemes are in estimator/schemes.py
from math import log2

N = int(2048)
q = 268369921 #28 bit prime
#rough 229, but full estimate 251 bit security

Xs = UniformMod(3)
Xe = DiscreteGaussian(stddev=3.19) #SEAL default sigma is 3.19
#according to https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/sealmanual_v2.2.pdf
#and previously: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/09/sealmanual.pdf

my_config = LWEParameters(n=N, q=q, Xs=Xs, Xe=Xe)
print("Running Estimator...")
est = LWE.estimate(my_config) #251 bit security
#est = LWE.estimate(schemes.Kyber1024) # normal configuration example (used to test that this code works properly)
best = min(est.values(), key=lambda x: x['rop'])
print("===========================")
print(best)
print("===========================")
print("Classical bits:", log2(best['rop']))
print("Quantum bits:", log2(best.get('rop_q', best['rop'])))
