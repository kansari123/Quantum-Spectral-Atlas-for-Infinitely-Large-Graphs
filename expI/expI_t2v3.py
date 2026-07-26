import numpy as np, json, time
from itertools import product
from scipy.optimize import nnls
t0=time.time(); K=24; C_REL=1e-3; eps=3e-4; T=100
res=json.load(open("res_I_t1.json"))
def eps_modes(l,bc):
    S=np.zeros((l,l))
    for i in range(l-1): S[i,i+1]=1; S[i+1,i]=-1
    S[l-1,0]=bc; S[0,l-1]=-bc
    ev=np.linalg.eigvalsh(1j*S); return np.sort(ev[ev>1e-9])
def sector_dos_small(l,bc):
    ep=eps_modes(l,bc); m=len(ep)
    lev=np.array([float(l)-float((1-2*np.array(b))@ep) for b in product([0,1],repeat=m)])
    u,c=np.unique(np.round(lev,9),return_counts=True)
    return u, c/c.sum()
# gates at l=8,10: values AND weights of the 50/50 sector mixture vs dense
gate_ok=True
for l in (8,10):
    n=1<<l; xs=np.arange(n)
    Ld=np.zeros((n,n))
    for i in range(l):
        sgn=1-2*((xs>>((i+1)%l))&1)
        Ld[xs,xs^(1<<i)]-=sgn
    Ld+=np.diag(np.full(n,float(l)))
    evd=np.linalg.eigvalsh(Ld)
    uD,cD=np.unique(np.round(evd,9),return_counts=True); wD=cD/cD.sum()
    # mixture
    vals={} 
    for bc in (1,-1):
        u,w=sector_dos_small(l,bc)
        for v,ww in zip(u,w): vals[v]=vals.get(v,0.0)+0.5*ww
    uM=np.array(sorted(vals)); wM=np.array([vals[v] for v in uM])
    ok=len(uM)==len(uD) and np.max(np.abs(uM-uD))<1e-9 and np.max(np.abs(wM-wD))<1e-9
    print("l=%d gate: values&weights %s"%(l,ok),flush=True)
    gate_ok&=ok
res["t2_gate_v3"]=dict(construction="50/50 BC-sector mixture, all parities, zero modes as multiplicity",
                       gated_l=[8,10],status="PASS" if gate_ok else "FAIL")
assert gate_ok, "T2 VOID"
# ---------- l=266 ----------
l=266
NB=1<<20
epP=eps_modes(l,+1); epM=eps_modes(l,-1)
E=max(epP.sum(),epM.sum())*1.0001
edges=np.linspace(-E,E,NB+1); ctr=0.5*(edges[:-1]+edges[1:]); db=edges[1]-edges[0]
def conv(epsk):
    d=np.zeros(NB); d[NB//2]=1.0
    for e in epsk:
        sh=int(round(e/db))
        up=np.zeros(NB); up[sh:]=d[:NB-sh]; dn=np.zeros(NB); dn[:NB-sh]=d[sh:]
        d=0.5*(up+dn)
    return d
dens=0.5*(conv(epP)+conv(epM)); dens/=dens.sum()
lam=float(l)-ctr; keep=dens>1e-300
lam=lam[keep]; mass=dens[keep]; mass/=mass.sum()
lam_min=float(lam.min()); lam_max=float(lam.max())
trinv_t=float((mass/lam).sum()); lndet_t=float((mass*np.log(lam)).sum())
rng=np.random.default_rng(777); tr2=[];ln2=[]
for _ in range(10):
    Nc=500000
    sP=rng.choice([-1.,1.],size=(Nc//2,len(epP))); sM=rng.choice([-1.,1.],size=(Nc//2,len(epM)))
    lv=np.concatenate([float(l)-sP@epP, float(l)-sM@epM])
    tr2.append(np.mean(1.0/lv)); ln2.append(np.mean(np.log(lv)))
tr_mc=float(np.mean(tr2)); tr_se=float(np.std(tr2)/np.sqrt(10))
ln_mc=float(np.mean(ln2)); ln_se=float(np.std(ln2)/np.sqrt(10))
okg=(abs(trinv_t-tr_mc)<=3*tr_se or abs(trinv_t-tr_mc)<=1e-4*trinv_t) and (abs(lndet_t-ln_mc)<=3*ln_se or abs(lndet_t-ln_mc)<=1e-4*abs(lndet_t))
res["t2_truthgate_v3"]=dict(lam_min=lam_min,lam_max=lam_max,trinv=trinv_t,trinv_mc=tr_mc,se=tr_se,
                            lndet=lndet_t,lndet_mc=ln_mc,se_ln=ln_se,gate_ok=bool(okg))
print("l=266 lam=[%.4f,%.2f] trinv %.6e (MC %.6e+-%.0e) lndet %.6f (MC %.6f+-%.0e) gate %s (%.0fs)"%(
  lam_min,lam_max,trinv_t,tr_mc,tr_se,lndet_t,ln_mc,ln_se,okg,time.time()-t0),flush=True)
assert okg
alpha=2.0*l; sigmas=[1e-1,1.0,10.0,100.0,1000.0]
grid=np.logspace(-2,np.log10(1.2*alpha),400)
def synth(sig):
    y=2.0*sig/(sig+lam)-1.0
    mu=np.zeros(K); Tm=np.ones_like(y); Tc=y.copy(); mu[0]=1.0; mu[1]=float(mass@Tc)
    for k in range(2,K):
        Tn=2*y*Tc-Tm; mu[k]=float(mass@Tn); Tm,Tc=Tc,Tn
    return mu
MU=np.array([synth(s) for s in sigmas])
def rungfit(mu,sig):
    y=2.0*sig/(sig+grid)-1.0; th=np.arccos(np.clip(y,-1,1))
    Am=np.cos(np.outer(np.arange(K),th)); A0=Am.copy(); A0[0]*=100.
    b=mu.copy(); b[0]*=100.
    wv,_=nnls(A0,b,maxiter=200*len(grid)); return wv
mods=np.array([rungfit(MU[d],sigmas[d]) for d in range(5)])
lg=np.log10(grid); ls=np.log10(np.array(sigmas))
band=np.argmin(np.abs(lg[:,None]-ls[None,:]),axis=1)
cv=np.array([mods[d][band==d]@(1.0/grid[band==d]) for d in range(5)])
alive=[sigmas[d] for d in range(5) if cv[d]>=C_REL*cv.sum()] or [sigmas[-1]]
def joint(mu_all):
    rows=[100.0*np.ones(len(grid))]; rhs=[100.0]
    for d,s in enumerate(sigmas):
        y=2.0*s/(s+grid)-1.0; th=np.arccos(np.clip(y,-1,1))
        rows.append(np.cos(np.outer(np.arange(1,K),th))); rhs.append(mu_all[d][1:])
    Aj=np.vstack([r if r.ndim==2 else r[None,:] for r in rows]); b=np.concatenate([np.atleast_1d(r) for r in rhs])
    wv,_=nnls(Aj,b,maxiter=200*Aj.shape[1]); return wv
wj=joint(MU); tr_h=float(wj@(1.0/grid)); ln_h=float(wj@np.log(grid))
rngN=np.random.default_rng(434343); fv=[(1.0+MU[d][1])/2.0 for d in range(5)]
tr_n=[];ln_n=[]
for t in range(T):
    mun=[MU[d].copy() for d in range(5)]
    for d in range(5):
        ee=eps/10 if fv[d]<0.51 else eps
        mun[d][1:]+=ee*rngN.standard_normal(K-1)
    wv=joint(mun)
    tr_n.append(abs(float(wv@(1.0/grid))-trinv_t)/trinv_t)
    ln_n.append(abs(float(wv@np.log(grid))-lndet_t))
D={s:int(np.ceil(4*np.sqrt(alpha/s))) for s in sigmas}
res["t2_l266_v3"]=dict(alive=alive,trinv_err_pct=100*abs(tr_h-trinv_t)/trinv_t,
  lndet_err_nats=abs(ln_h-lndet_t),noise_trinv_med_pct=100*float(np.median(tr_n)),
  noise_lndet_med=float(np.median(ln_n)),SumD_naive=int(sum(D.values())),SumD_LWP=int(sum(D[s] for s in alive)))
json.dump(res,open("res_I_t1.json","w"),indent=1)
r2=res["t2_l266_v3"]
print("l=266 SIGNED: alive %s trinv %.3e%% lndet %.3e nats noise %.3f%%/%.5f SumD %d->%d"%(
  str(alive),r2["trinv_err_pct"],r2["lndet_err_nats"],r2["noise_trinv_med_pct"],r2["noise_lndet_med"],
  r2["SumD_naive"],r2["SumD_LWP"]))
print("T2v3 DONE %.0fs"%(time.time()-t0))
