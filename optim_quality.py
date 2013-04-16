from coopr.pyomo import *

model = AbstractModel()

model.N = Set()
model.M = Set()
model.qC = Set()
model.qH = Set()

model.I_l = Param(model.N)
model.I_u = Param(model.N)

model.D = Param(model.N)
model.a = Param(model.N)

model.k = Param(model.N, model.M)

model.NP_l = Param(model.M)
model.NP_u = Param(model.M)
model.Pr = Param(model.M)

model.qCmin = Param(model.qC)
model.qCIN = Param(model.qC)

def Ibounds(model, i):
	return (model.I_l[i], model.I_u[i])
model.I = Var(model.N, bounds=Ibounds)
model.E = Var(model.N, bounds=(0,None))

def NPBounds(model, p):
	return (model.NP_l[p], model.NP_u[p])
model.NP = Var(model.M, bounds=NPBounds)

def obj_rule(model):
	return sum((model.a[i]*model.I[i]) for i in model.N)
model.obj = Objective(rule=obj_rule)

def con_rule(model, i):
	return model.I[i] + sum((model.k[i,p]*model.Pr[p]*model.NP[p]) for p in model.M) == model.D[i] + model.E[i]
model.con = Constraint(model.N, rule=con_rule)

def con_qual(model, j):
	return  -model.Pr[j]*model.k[1,j]*model.NP[j]  >= model.qCmin[j] - model.qCIN[j]
model.con_qual = Constraint(model.qC, rule=con_qual)

def con_head(model, j):
	return model.Pr[j]*model.k[3,j]*model.NP[j] * 9.81 * 10 <= -model.Pr[j]*model.k[1,j]*model.NP[j] * 1e6
model.con_head = Constraint(model.qH, rule=con_head)
