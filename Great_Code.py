# -*- coding: utf-8 -*-
"""Submission1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ocbhszsEyaDw4oEfSilkzv-nCbjl1wJE
"""

! pip install CoolProp
import CoolProp.CoolProp as CP
from math import exp,pi
from matplotlib import pyplot
import matplotlib.pyplot as plt
import numpy as np

#Brayton

#Todo (submission 2): add component efficency, add mod

p1 = 101325.#pa
T1 = 25.+273.15#k
rp = 6.#compressor ratio
T3 = 1350.+273.15#k

#compressor
h1 = CP.PropsSI('H','T',T1, 'P',p1,'Air')
s1 = CP.PropsSI('S','T',T1, 'P',p1,'Air')
p2 = p1*rp
s2 = s1
h2 = CP.PropsSI('H','S',s2, 'P',p2,'Air')
w12 = h2 - h1
# print the mass specific compressor work
print('The mass specific compressor work is: '+str(round(w12/1000. ,2))+' kJ/kg')

#combuster
p3 = p2
h3 = CP.PropsSI('H','T',T3, 'P',p3,'Air')
s3 = CP.PropsSI('S','T',T3, 'P',p3,'Air')
q23 = h3 - h2
# print the mass specific heat addition in the combustor
print('The mass specific heat addition in the combustor is: '+str(round(q23/1000. ,2))+' kJ/kg')

#Turbine / exchanger
s4 = s3
p4 = p1
h4 = CP.PropsSI('H','S',s4, 'P',p4,'Air')
w34 = h3 - h4
q41 = h4 - h1
# print the mass specific turbine work
print('The mass specific turbine work is: '+str(round(w34/1000. ,2))+' kJ/kg')
# print the mass specific heat rejection in the heat exchanger
print('The mass specific heat rejection in the combustor is: '+str(round(q41/1000. ,2))+' kJ/kg')

#efficency / Back Work
eta_th = (w34 - w12)/q23
bwr = w12/w34
# print the thermal efficiency
print('The Braton cycle thermal efficiency is: '+str(round(eta_th*100. ,2))+' %')
# print the back work ratio
print('The back work ratio is: '+str(round(bwr ,3)))

# Rankine
print('// rankine cycle analysis');

#Todo Add Mod, Component Efficency, cycle

p1r = 6000 #pa
p3r = 10000000 #Todo
T1r = 30.+273.15#k
T3r = 440.+273.15#k
Treheatr = 440. + 273.15
prexit = 700000

#Quality (X) Min = 0.9

#Pump
pumpEfficency = 0.92;
v1r = CP.PropsSI('V','P', p1r, 'T', T1r, 'Water');
w12r = v1r * (p3r - p1r);
h1r = CP.PropsSI('H','P', p1r, 'T', T1r, 'Water');
h2r = w12r + h1r;
#efficency equation
h2r = -1. * (((h1r-h2r) / pumpEfficency) - h1r);
print('The mass specific pump work is: '+str(round(w12r/1000))+ ' kJ/kg');

#Boiler
#calculate qin todo: calculate q in when meshed with brayton cycle, use effectiveness
h3r = CP.PropsSI('H','P', p3r, 'T', T3r, 'Water');
q23r = h3r-h2r;
print('The mass specific heat addition in the boiler is: ' + str(round(q23r)/1000) + ' kJ/kg');

#Calculate Mass flow rate #todo
#first the brayton cycle would be solved for mass flow rate of the gas using Q in
#then Q dot out would be solved
#then using effectiveness Q dot out actual would be found
#So im just using a placeholder Qdotactual out until submission 2
QinRankineActual = 1000000. #J/s
massFlowRankine = 600 #Todo

#Pump Work
#print(massFlowRankine);
w12ractual = massFlowRankine * (h2r-h1r);
print('The actual pump work is: '+str(round(w12r/1000))+ ' kJ/s');

#Turbine
turbineEfficency = 0.93;
#temperature at which the steam enters reheat
#should be at the halfway point #todo iterate over this too?

s3r = CP.PropsSI('S','T',T3r, 'P',p3r,'Water');
s4exitr = s3r;
xExitr = CP.PropsSI('Q','P', prexit, 'S', s4exitr, 'Water');
h4exitr = CP.PropsSI('H','P', prexit, 'S', s4exitr, 'Water');
h4exitrIdeal = h4exitr;
#efficency equation
h4exitr = -1. * (((h3r-h4exitr) / turbineEfficency) - h3r);
wTurbine1r = h3r-h4exitr;
wTurbine1rActual = massFlowRankine * (wTurbine1r)
print('The mass specific steam turbine 1 work is: ' + str(round(wTurbine1r)/1000) + ' kJ/kg');

#Boiler->Turbine 2
#for simplicity the working fluid is heated up to 3/4 tmax-tmin

hafterboilr = CP.PropsSI('H','P', prexit, 'T', Treheatr, 'Water');
safterBoilr = CP.PropsSI('S','P', prexit, 'T', Treheatr, 'Water');
sFinalr = CP.PropsSI('S','P', prexit, 'T', Treheatr, 'Water');
hfinalr = CP.PropsSI('H','S', sFinalr, 'P', p1r, 'Water');
hfinalrIdeal = hfinalr;
#effuicenety efficency efficceccy
hfinalr = -1. * (((hafterboilr-hfinalr) / turbineEfficency) - hafterboilr);
#Quality
Xfinalr = CP.PropsSI('Q','S', safterBoilr, 'P', p1r, 'Water');

wTurbine2r = hafterboilr - hfinalr;
wTurbine2rActual = massFlowRankine * wTurbine2r
print('The mass specific steam turbine work 2 is: ' + str(round(wTurbine2r)/1000) + ' kJ/kg');

#Condensor
q41r = hfinalr-h1r;
Q41rAcutal = massFlowRankine * q41r
print('The mass specific heat rejection from the condenser is: ' + str(round(q41r)/1000) + ' kJ/kg');

#todo fix
#Thermal Efficenecy
#netPowerR = wTurbine1rActual + wTurbine2rActual - w12ractual
#print('Net Power: ' + str(round(netPowerR)));
#print(w12ractual)
#backWorkRatio = w12ractual / (wTurbine1rActual + wTurbine2rActual);
#print('BWR: ' + str(backWorkRatio));
thermalEfficency = (wTurbine1r + wTurbine2r - w12r) / q23r;
print('TE: ' + str(thermalEfficency));

#Plot of my Data

#TS Diagram

s1r = CP.PropsSI('S','P', p1r, 'T', T1r, 'Water');
#iterate over boil stage 1
boiler1 = np.array([]);
sArray1 = np.arange(s1r,s3r,10);
for i in sArray1:
  j = CP.PropsSI('T','S', i, 'P', p3r, 'Water');
  boiler1 = np.append(boiler1, j);

boiler2 = np.array([]);
sArray2 = np.arange(s3r,sFinalr,10);
for i in sArray2:
  j = CP.PropsSI('T','S', i, 'P', prexit, 'Water');
  boiler2 = np.append(boiler2, j);

turbine1 = np.array([]);
sArray3 = np.array([]);
hArray1 = np.arange(h4exitrIdeal,h3r,5000);
for i in hArray1:
  j = CP.PropsSI('T','S', s3r, 'H', i, 'Water');
  turbine1 = np.append(turbine1, j);
  sArray3 = np.append(sArray3, s3r);

turbine2 = np.array([]);
sArray4 = np.array([]);
hArray2 = np.arange(hfinalrIdeal,hafterboilr,5000);
for i in hArray2:
  j = CP.PropsSI('T','S', sFinalr, 'H', i, 'Water');
  turbine2 = np.append(turbine2, j);
  sArray4 = np.append(sArray4, sFinalr);

condenser1 = np.array([]);
sArray5 = np.arange(s1r,sFinalr,100)
for i in sArray5:
  j = CP.PropsSI('T','S', i, 'P', p1r, 'Water');
  condenser1 = np.append(condenser1, j);

fig = plt.figure(32,figsize=(6,5))
plt.scatter(sArray1,boiler1, marker = '.');
plt.scatter(sArray2,boiler2, marker= '.');
plt.scatter(sArray3,turbine1, marker= '|');
plt.scatter(sArray4,turbine2, marker= '|');
plt.scatter(sArray5,condenser1, marker = '.');
plt.legend(loc=6)
plt.xlabel('S (J/kg')
plt.xlim([0, 10000])
plt.ylabel('T (kelvin)')

plt.show()

fig.savefig('Fig_test.eps')
# or output pdf file (just don't waste your time outputting jpg or png files)
fig.savefig('Fig_test.pdf')

plt.close()

s = []

for i in np.arange(0.1,11.,0.1):
  j = CP.PropsSI('V','P', 1000., 'Q', 0.5, 'Water');
  s = np.append(s,j)