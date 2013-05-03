from coopr.pyomo import *

model = AbstractModel()

# Sets
model.R = Set()
model.P = Set()
model.contam_P = Set()
model.contam_R = Set()
model.head_P = Set()
model.head_R_in = Set()
model.head_R_out = Set()

# Parameters
model.imports_min = Param(model.R, initialize=0)
model.imports_max = Param(model.R, initialize=0)

model.demand = Param(model.R, initialize=0)
model.cost_resource = Param(model.R, initialize=0)

model.prod_coeff = Param(model.R, model.P, initialize=0)

model.process_number_min = Param(model.P, initialize=0)
model.process_number_max = Param(model.P, initialize=0)
model.process_rate = Param(model.P, initialize=0)

model.contam_min = Param(model.contam_P, initialize=0)
model.contam_in = Param(model.contam_P, initialize=0)

# Variables
def import_bounds(model, r):
	return (model.imports_min[r], model.imports_max[r])

def process_number_bounds(model, p):
	return (model.process_number_min[p], model.process_number_max[p])

model.imports = Var(model.R, bounds=import_bounds)
model.exports = Var(model.R, bounds=(0,None))
model.process_number = Var(model.P, bounds=process_number_bounds)

# Objective
def obj_rule(model):
	return sum((model.cost_resource[r]*model.imports[r]) for r in model.R)
model.obj = Objective(rule=obj_rule)

# Constraints
def resource_balance(model, r):
	return model.imports[r] + sum((model.prod_coeff[r,p]*model.process_rate[p]*model.process_number[p]) for p in model.P) == model.demand[r] + model.exports[r]

def process_contam(model, r, p):
	return  -0.2*model.process_rate[p]*model.prod_coeff[r,p]*model.process_number[p]  >= model.contam_min[p] - model.contam_in[p]

def process_head(model, r_in, r_out, p):
	return model.process_rate[p]*model.prod_coeff[r_out,p]*model.process_number[p] * 9.81 * 1 <= -model.process_rate[p]*model.prod_coeff[r_in,p]*model.process_number[p] * 1e6

model.quantity = Constraint(model.R, rule=resource_balance)
model.contamination = Constraint(model.contam_R, model.contam_P,  rule=process_contam)
model.con_head = Constraint(model.head_R_in, model.head_R_out, model.head_P, rule=process_head)
