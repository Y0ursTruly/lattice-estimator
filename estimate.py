from estimator.lwe_parameters import LWEParameters
from estimator.nd import UniformMod, DiscreteGaussian
from estimator import LWE, schemes #schemes are in estimator/schemes.py
from math import log2
from estimator.reduction import RC, ADPS16

N = int(2048)
q = 268369921 #28 bit prime
#rough 229, but full estimate 251 bit security

Xs = UniformMod(3)
Xe = DiscreteGaussian(stddev=3.19) #SEAL default sigma is 3.19
#according to https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/sealmanual_v2.2.pdf
#and previously: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/09/sealmanual.pdf

bfv_scheme = LWEParameters(n=N, q=q, Xs=Xs, Xe=Xe)
print("Running Estimator...")
bfv_estimate = LWE.estimate(bfv_scheme, red_cost_model=ADPS16(mode="quantum"))
kyber_estimate = LWE.estimate(schemes.Kyber1024, red_cost_model=ADPS16(mode="quantum"))
best_bfv = min(bfv_estimate.values(), key=lambda x: x['rop'])
best_kyber = min(kyber_estimate.values(), key=lambda x: x['rop'])
print("===========================")
print("BFV Security Estimate:", log2(best_bfv['rop']))
print("Kyber Security Estimate:", log2(best_kyber['rop']))
