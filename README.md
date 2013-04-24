README for Tat water resource network
=====================================

Wed Apr 24 19:11:37 BST 2013

## General information

- The model is defined as an AbstractModel(), which means the model is defined in the optim_quality.py and it calls values from the data_quality.dat file.
- The parameters and variables are named such that it should be self-explanatory what they represent.

## Sets
Parameters and variables are defined over the following sets:
- R indexes resources
- P indexes processes
- contam_P indexes processes which change the levels of contaminants in the water
- contam_R indexes resources going into a process which change levels of contamination
- head_P indexes processes which changes the head of the water
- head_R_out indexes the water resources whose head is change following various processes
- head_R_in indexes resources used in changing the head of water for a process

## Resources
1. Electricity
2. Source water
3. Pumped water
4. Treated water
5. Boiled water
6. Water to satisfy final demand for domestic use.
7. Water to satisfy final demand for livestock use.
8. Water to satisfy final demand for human use.
9. Heat
10. Waste water
11. Water that's had it's head raised (for electricity generation)
12. Water that's been used in electricity generation.

## Processes
1. Electricity generation (hydro-electric)
2. Water treatment
3. Pumping (to homes)
4. Boiling
5. Domestic processes (e.g. washing)
6. Transfer (a 'free' process to carry water from source to livestock)
7. Head raising (a 'free' process to raise head before using in electricity generation).

## Running the model
At the command prompt:

    pyomo optim_quality.py data_quality.dat --solver=glpk

## Constraints
- con_rule is a mass balance constraint for input and output resources at each process. It ensures that 

        INPUT + PRODUCTION = DEMAND + EXPORT. 
The production is given by 

        P=Pr*k*NP 
where NP is a decision variable.
- con_qual calculates the quality of treated water as

        f(treatment input quality, energy input). 
The quality of the outputted treated water increases linearly with energy input. Energy input is itself dependent on a decision variable. This constraint checks that the the water quality is at or above some minimum standard qCmin.
	- This kind of constraint has only been applied to the 'treatment' process, because this is the only process which depends on a decision variable (electricity).
- con_head checks that there is sufficient input of electricity to raise the water to the required head to pump water to houses (Mgh).
	- This kind of constraint hasn't yet been applied to 'electricity generation' and 'head raising' processes, because these aren't dependent on inputs of other resources whose quantities are affected by decision variables.

- When the con_qual and con_head constraints aren't satisfied, then running the model will result in there being no solution. 
- Note the negative signs in the con_qual and con_head constraints. This is because process inputs in the k-matrix are defined as negative. Thus we need to make this value positive if we are to compare it to (a positivley defined) required input quantity in an inequality.
- Not also the units for con_head. Whilst masses are given in [kg], energy inputs are in [MJ], thus the energy input on the RHS of the inequality has been multiplied by 1e6 to put it into J, for comparison with the 'Mgh' calculation on the left-hand side of the inequaility.
- Currently, the model will give a solution, if the water pumped is pumped to a house with 1m of head. However, this probably isn't realistic. But if required head is raised, then the model won't give a solution.
