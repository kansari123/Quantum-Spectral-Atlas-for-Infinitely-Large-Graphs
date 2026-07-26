import numpy as np, json, time
from graphatlas import nnls_rung
from hypercube import level_masses_port, level_masses_dos, synth_moments, truths
t0=time.time(); K=24; C_REL=1e-3; G_CUT=5e-3; res={}
def lwp(models,grid,sigmas):
    lg=np.log10(grid); ls=np.log10(np.array(sigmas))
    band=np.argmin(np.abs(lg[:,None]-ls[None,:]),axis=1)
    R,C,_=models.shape; c=np.zeros((R,C))
    for d in range(R):
        m=band==d; c[d]=models[d][:,m]@(1.0/grid[m])
    tot=c.sum(0)
    return [[sigmas[d] for d in range(R) if c[d,col]>=C_REL*tot[col]] or [sigmas[-1]] for col in range(C)], c
def build(l,r,eb,sigmas,gridlo):
    Bt=l-r; alpha=2.0*(Bt+r*eb)
    ports={"d1":(1,0),"mid":(Bt//2,r//2),"anti":(Bt,r),"canary":(0,r)}
    names=list(ports)
    meas=[(level_masses_port(l,r,eb,*ports[nm])) for nm in names]
    grid=np.logspace(gridlo,np.log10(1.2*alpha),400)
    MU=np.zeros((len(sigmas),K,len(names)))
    for d,s in enumerate(sigmas):
        for c,(lam,m) in enumerate(meas):
            MU[d,:,c]=synth_moments(lam,m,s,K)
    NB2=np.full(len(names),2.0)
    models=np.stack([nnls_rung(MU[d],NB2,grid,sigmas[d],K) for d in range(len(sigmas))])
    tt=truths(l,r,eb,ports)
    Rt=np.array([tt[nm]["Reff"] for nm in names])
    return names,models,grid,MU,Rt,alpha
# --- A1/A2: l=14 ---
sig14=[1e-3,1e-2,1e-1,1,10,100]
names,mod,grid,MU,Rt,alpha=build(14,3,1e-3,sig14,-4)
aliveL,c=lwp(mod,grid,sig14)
inv=1.0/grid
def ev(alive,p):
    s0=sorted(alive)[0]; return float(mod[sig14.index(s0),p]@inv)
errF=np.array([abs(ev(sig14,p)-Rt[p])/Rt[p] for p in range(4)])
errL=np.array([abs(ev(aliveL[p],p)-Rt[p])/Rt[p] for p in range(4)])
ratio=errL/np.maximum(errF,1e-300)
A1=all(1e-3 in aliveL[p] for p in (1,2,3)) and bool(np.all(ratio[1:]<=2.0))
A1kill=bool(np.any(ratio>10.0))
A2=(len(aliveL[0])<=4) and (1e-3 not in aliveL[0]) and ratio[0]<=2.0
res["l14"]=dict(alive={names[p]:aliveL[p] for p in range(4)},
  err_full_pct=[100*float(e) for e in errF], err_LWP_pct=[100*float(e) for e in errL],
  ratio=[float(x) for x in ratio], A1=bool(A1), A1_kill=A1kill, A2=bool(A2),
  gprune_err_pct_from_expH=[0.00087,109.198,155.538,155.579])
print("l14 alive:",res["l14"]["alive"]); print("l14 err LWP:",res["l14"]["err_LWP_pct"],"ratio:",res["l14"]["ratio"],flush=True)
# --- A3: l=266 ---
sig266=[1e-3,1e-2,1e-1,1,10,100,1000]
l,r,eb=266,6,1e-3; Bt=l-r; alpha=2.0*(Bt+r*eb)
ports={"d1":(1,0),"mid":(Bt//2,r//2),"anti":(Bt,r),"canary":(0,r)}
names2=list(ports)
meas=[(level_masses_port(l,r,eb,*ports[nm])) for nm in names2]
lamD,mD=level_masses_dos(l,r,eb); meas.append((lamD,mD)); names2.append("dos")
grid2=np.logspace(-4,np.log10(1.2*alpha),400)
MU2=np.zeros((7,K,5))
for d,s in enumerate(sig266):
    for cc,(lam,m) in enumerate(meas): MU2[d,:,cc]=synth_moments(lam,m,s,K)
NB2=np.array([2.,2.,2.,2.,1.])
mod2=np.stack([nnls_rung(MU2[d],NB2,grid2,sig266[d],K) for d in range(7)])
aliveL2,c2=lwp(mod2,grid2,sig266)
A3=all(set(aliveL2[cc]).issubset({1e2,1e3}) for cc in range(5))
A3kill=any(any(s<=10 for s in aliveL2[cc]) for cc in range(5))
D266={s:int(np.ceil(4*np.sqrt(alpha/s))) for s in sig266}
res["l266"]=dict(alive={names2[cc]:aliveL2[cc] for cc in range(5)},A3=bool(A3),A3_kill=bool(A3kill),
  SumD_LWP_dos=int(sum(D266[s] for s in aliveL2[4])))
json.dump(res,open("res_G2_addendum.json","w"),indent=1)
print("l266 alive:",res["l266"]["alive"],"A3:",A3,"SumD dos:",res["l266"]["SumD_LWP_dos"])
print("ADDENDUM DONE %.0fs"%(time.time()-t0))
