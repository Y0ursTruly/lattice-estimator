from estimator.lwe_parameters import LWEParameters
from estimator.nd import UniformMod, DiscreteGaussian
from estimator import LWE, schemes #schemes are in estimator/schemes.py
from math import log2

#N = int(32768/2)
#q = 1329227995775244468652735166391779329 #a sample product of 2 [60,60] primes
#these primes were: [1152921504598720513, 1152921504606584833]

N = int(32768/4)
q = 576460752302473217
#yes, 1152921504606584833, the 60 bit prime makes the construction weaker than the 59 bit one

Xs = UniformMod(3)
Xe = DiscreteGaussian(stddev=3.19) #SEAL default sigma is 3.19
#according to https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/sealmanual_v2.2.pdf
#and previously: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/09/sealmanual.pdf

my_config = LWEParameters(n=N, q=q, Xs=Xs, Xe=Xe)
print("Running Estimator...")
est = LWE.estimate.rough(my_config) # 512 bit secure configuration currently
#est = LWE.estimate(schemes.Kyber512) # normal configuration example (used to test that this code works properly)
best = min(est.values(), key=lambda x: x['rop'])
print("===========================")
print(best)
print("===========================")
print("Classical bits:", log2(best['rop']))
print("Quantum bits:", log2(best.get('rop_q', best['rop'])))
