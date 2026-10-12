from estimator.lwe_parameters import LWEParameters
from estimator.nd import UniformMod, DiscreteGaussian
from estimator import LWE, schemes #schemes are in estimator/schemes.py
from math import log2
from estimator.reduction import RC, ADPS16


#my_scheme = LWEParameters(n=1280, q=26045081, Xs=DiscreteGaussian(1.0), Xe=DiscreteGaussian(1.0)) #128 bit security
my_scheme = LWEParameters(n=1280, q=13462171, Xs=DiscreteGaussian(1.0), Xe=DiscreteGaussian(1.0)) #134 bit security
print("Running Estimator...")
my_estimate = LWE.estimate(my_scheme, red_cost_model=ADPS16(mode="quantum"))
best_my_scheme = min(my_estimate.values(), key=lambda x: x['rop'])
print("===========================")
print("My Security Estimate:", log2(best_my_scheme['rop']))
