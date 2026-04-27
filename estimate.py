from estimator.lwe_parameters import LWEParameters
from estimator.nd import UniformMod, DiscreteGaussian
from estimator import LWE, schemes #schemes are in estimator/schemes.py
from math import log2
from estimator.reduction import RC, ADPS16

#N = 2048
#q = 268369921 #28 bit prime

#Xs = UniformMod(3)
#Xe = DiscreteGaussian(stddev=3.19) #SEAL default sigma is 3.19
#according to https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/sealmanual_v2.2.pdf
#and previously: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/09/sealmanual.pdf
# this was for microsoft SEAL BFV stuff of a standard deviation 3.19 for Xe and UniformMod(3)
# but we're moving on from SEAL onto a module-lwe configuration for speed

N = 1024
q = 8191

Xs = DiscreteGaussian(stddev=3.937) #KYBER_ETA1=31 in params.h
Xe = DiscreteGaussian(stddev=3.937) #KYBER_ETA2=31 in params.h
# module learning with errors scheme intended to be adopted from the ind-cpa parts of Kyber1024


my_mlwe_scheme = LWEParameters(n=N, q=q, Xs=Xs, Xe=Xe)
print("Running Estimator...")
my_mlwe_estimate = LWE.estimate(my_mlwe_scheme, red_cost_model=ADPS16(mode="quantum"))
kyber_estimate = LWE.estimate(schemes.Kyber1024, red_cost_model=ADPS16(mode="quantum"))
best_my_mlwe = min(my_mlwe_estimate.values(), key=lambda x: x['rop'])
best_kyber = min(kyber_estimate.values(), key=lambda x: x['rop'])
print("===========================")
print("My MLWE Security Estimate:", log2(best_my_mlwe['rop']))
print("Kyber Security Estimate:", log2(best_kyber['rop']))
