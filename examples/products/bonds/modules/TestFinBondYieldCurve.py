# -*- coding: utf-8 -*-
"""
Created on Fri Apr 08 09:26:27 2016

@author: Dominic O'Kane
"""

import datetime as dt

from financepy.finutils.FinFrequency import FinFrequencyTypes
from financepy.finutils.FinDayCount import FinDayCountTypes
from financepy.finutils.FinDate import FinDate, fromDatetime
from financepy.products.bonds.FinBond import FinBond
from financepy.market.curves.FinBondYieldCurve import FinBondYieldCurve
from financepy.market.curves.FinBondYieldCurveModel import FinCurveFitPolynomial
from financepy.market.curves.FinBondYieldCurveModel import FinCurveFitNelsonSiegel
from financepy.market.curves.FinBondYieldCurveModel import FinCurveFitNelsonSiegelSvensson
from financepy.market.curves.FinBondYieldCurveModel import FinCurveFitBSpline

##########################################################################

import os
root = (os.path.dirname(os.path.realpath(__file__)))

##########################################################################


def test_FinBondYieldCurve():

    ###########################################################################

    import pandas as pd
    bondDataFrame = pd.read_csv(root + '/data/giltbondprices.txt', sep='\t')
    bondDataFrame['mid'] = 0.5*(bondDataFrame['bid'] + bondDataFrame['ask'])

    frequencyType = FinFrequencyTypes.SEMI_ANNUAL
    accrualType = FinDayCountTypes.ACT_ACT_ICMA
    settlement = FinDate(2012, 9, 19)

    bonds = []
    ylds = []

    for index, bond in bondDataFrame.iterrows():

        dateString = bond['maturity']
        matDatetime = dt.datetime.strptime(dateString, '%d-%b-%y')
        maturityDt = fromDatetime(matDatetime)
        coupon = bond['coupon']/100.0
        cleanPrice = bond['mid']
        bond = FinBond(maturityDt, coupon, frequencyType, accrualType)
        yld = bond.yieldToMaturity(settlement, cleanPrice)
        bonds.append(bond)
        ylds.append(yld)

###############################################################################

    curveFitMethod = FinCurveFitPolynomial()
    fittedCurve1 = FinBondYieldCurve(settlement, bonds, ylds, curveFitMethod)
#    fittedCurve1.display("GBP Yield Curve")

    curveFitMethod = FinCurveFitPolynomial(5)
    fittedCurve2 = FinBondYieldCurve(settlement, bonds, ylds, curveFitMethod)
#    fittedCurve2.display("GBP Yield Curve")

    curveFitMethod = FinCurveFitNelsonSiegel()
    fittedCurve3 = FinBondYieldCurve(settlement, bonds, ylds, curveFitMethod)
#    fittedCurve3.display("GBP Yield Curve")

    curveFitMethod = FinCurveFitNelsonSiegelSvensson()
    fittedCurve4 = FinBondYieldCurve(settlement, bonds, ylds, curveFitMethod)
#    fittedCurve4.display("GBP Yield Curve")

    curveFitMethod = FinCurveFitBSpline()
    fittedCurve5 = FinBondYieldCurve(settlement, bonds, ylds, curveFitMethod)
#    fittedCurve5.display("GBP Yield Curve")

###############################################################################

    print("PARAMETER", "VALUE")
    print("beta1", fittedCurve3._curveFit._beta1)
    print("beta2", fittedCurve3._curveFit._beta2)
    print("beta3", fittedCurve3._curveFit._beta3)
    print("tau", fittedCurve3._curveFit._tau)

    print("PARAMETER", "VALUE")
    print("beta1", fittedCurve4._curveFit._beta1)
    print("beta2", fittedCurve4._curveFit._beta2)
    print("beta3", fittedCurve4._curveFit._beta3)
    print("beta4", fittedCurve4._curveFit._beta4)
    print("tau1", fittedCurve4._curveFit._tau1)
    print("tau2", fittedCurve4._curveFit._tau2)

###############################################################################

    maturityDate = FinDate(2030, 9, 19)
    interpolatedYield = fittedCurve5.interpolatedYield(maturityDate)
    print(maturityDate, interpolatedYield)

###############################################################################


test_FinBondYieldCurve()