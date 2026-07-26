import numpy as np, scipy.linalg as sla, json, time
from scipy.optimize import nnls
t0=time.time(); K=24; C_REL=1e-3; G_CUT=5e-3; eps=3e-4; T=100
rngN=np.random.default_rng(434343)
def nnls_rung_c(mu_norm,nb2,grid,sigma):   # complex-safe local copy of the frozen fitter
    y=2.0*sigma/(sigma+grid)-1.0; th=np.arccos(np.clip(y,-1,1))
    A=np.cos(np.outer(np.arange(K),th)); A0=A.copy(); A0[0]*=100.0
    C=mu_norm.shape[1]; W=np.empty((C,len(grid)))
    for c in range(C):
        b=mu_norm[:,c].real.copy(); b[0]*=100.0
        w,_=nnls(A0,b,maxiter=200*len(grid)); W[c]=nb2[c]*w
    return W
def flags_c(mu):
    g=((1.0+mu[2].real)/2.0+2.0*mu[1].real+1.0)/4.0
    f=(1.0+mu[1].real)/2.0
    return g,f
def moments_dense(L,sigma,B):
    n=L.shape[0]; nb2=np.sum(np.abs(B)**2,0)
    lu=sla.lu_factor(L+sigma*np.eye(n,dtype=L.dtype))
    V=B/np.sqrt(nb2); mu=np.zeros((K,B.shape[1]),dtype=complex); mu[0]=1.0
    Y=lambda X: 2*sigma*sla.lu_solve(lu,X)-X
    tp=V; tc=Y(V); mu[1]=np.sum(np.conj(V)*tc,0)
    for k in range(2,K):
        tn=2*Y(tc)-tp; mu[k]=np.sum(np.conj(V)*tn,0); tp,tc=tc,tn
    assert np.max(np.abs(mu.imag))<1e-10, np.max(np.abs(mu.imag))
    return mu.real,nb2
def lwp_alive(models,grid,sigmas):
    lg=np.log10(grid); ls=np.log10(np.array(sigmas))
    band=np.argmin(np.abs(lg[:,None]-ls[None,:]),axis=1)
    R=len(sigmas); C=models[0].shape[0]; c=np.zeros((R,C))
    for d in range(R):
        m=band==d; c[d]=models[d][:,m]@(1.0/grid[m])
    tot=c.sum(0)
    return [[sigmas[d] for d in range(R) if c[d,col]>=C_REL*tot[col]] or [sigmas[-1]] for col in range(C)]
def run_instance(L, tag, deflate):
    n=L.shape[0]; alpha=8.5 if n==1024 and tag.startswith("torus") else None
    if alpha is None:
        alpha=2.0*float(np.max(np.sum(np.abs(L-np.diag(np.diag(L))),1)))  # frozen procedure T1b
    ev,U=np.linalg.eigh(L)
    lam_min=float(ev[0] if not deflate else ev[1])
    sigmas=[1e-3,1e-2,1e-1,1.0,10.0]
    grid=np.logspace(-4,np.log10(1.2*alpha),400)
    rng=np.random.default_rng(2026)
    ports=[]
    for _ in range(3):
        u,v=rng.choice(n,2,replace=False); ports.append((int(u),int(v)))
    dg=np.sum(np.abs(L-np.diag(np.diag(L))),1); hubs=np.argsort(dg)[-2:]
    for h in hubs:
        v=int(rng.integers(n)); v=v if v!=h else (v+1)%n; ports.append((int(h),v))
    ports.append((0,n//2+ (16 if n==1024 else 0)))
    Z=np.random.default_rng(31337).choice([-1.,1.],size=(n,8))
    B=np.zeros((n,14)); 
    for p,(u,v) in enumerate(ports): B[u,p]=1.; B[v,p]=-1.
    B[:,6:]=Z
    if deflate:
        one=np.ones(n)/np.sqrt(n); B=B-np.outer(one,one@B)
    Bc=B.astype(L.dtype)
    mus={};mods=[]
    for s in sigmas:
        mu,nb2=moments_dense(L,s,Bc); mus[s]=mu
        mods.append(nnls_rung_c(mu,nb2,grid,s))
    aliveL=lwp_alive(mods,grid,sigmas)
    inv=1.0/grid
    # truths via eigendecomposition (generator 1) + direct solves gate (generator 2)
    lam_t=ev.copy()
    if deflate: lam_t=lam_t[1:]; Ut=U[:,1:]
    else: Ut=U
    proj=np.abs(Ut.conj().T@Bc)**2
    Reff_t=np.array([float(np.sum(proj[:,p]/lam_t)) for p in range(6)])
    sv=np.logspace(-3,np.log10(alpha),25)
    Rs_t=np.array([[float(np.sum(proj[:,p]/(lam_t+s))) for s in sv] for p in range(6)])
    x=np.linalg.solve(L+ (1e-9 if not deflate else 1e-9)*np.eye(n,dtype=L.dtype),Bc[:,0])
    gate=abs(float(np.real(np.vdot(Bc[:,0],x)))-(Reff_t[0] if not deflate else float(np.sum(proj[:,0]/(lam_t+1e-9)))))/Reff_t[0]
    lndet_t=float(np.sum(np.log(lam_t)))/n
    trinv_t=float(np.sum(1.0/lam_t))/n
    def ev_at(alive,c,s):
        sg=np.array(sorted(alive)); d=sg[0] if s<=0 else sg[int(np.argmin(np.abs(np.log10(sg)-np.log10(s))))]
        return float(mods[sigmas.index(d)][c]@(1.0/(grid+s)))
    band=np.array([[abs(ev_at(aliveL[p],p,s)-Rs_t[p,i])/Rs_t[p,i] for i,s in enumerate(sv)] for p in range(6)])
    endp=np.array([abs(ev_at(aliveL[p],p,0)-Reff_t[p])/Reff_t[p] for p in range(6)])
    # joint fit on probes for lndet + trinv
    def joint(mu_all):
        rows=[100.0*np.ones(len(grid))]; rhs=[100.0]
        for d,s in enumerate(sigmas):
            y=2.0*s/(s+grid)-1.0; th=np.arccos(np.clip(y,-1,1))
            rows.append(np.cos(np.outer(np.arange(1,K),th))); rhs.append(mu_all[d][1:])
        A=np.vstack([r if r.ndim==2 else r[None,:] for r in rows]); b=np.concatenate([np.atleast_1d(r) for r in rhs])
        w,_=nnls(A,b,maxiter=200*A.shape[1]); return w
    le=[];te=[]
    for c in range(6,14):
        w=joint([mus[s][:,c] for s in sigmas])
        le.append(float(w@np.log(grid))); te.append(float(w@inv))
    lndet_h=float(np.mean(le)); trinv_h=float(np.mean(te))
    # noise
    pe=np.empty((T,6)); ln_e=np.empty(T); tr_e=np.empty(T)
    for t in range(T):
        for p in range(6):
            s0=sorted(aliveL[p])[0]; d0=sigmas.index(s0)
            g,f=flags_c(mus[s0]); ee=eps/10 if f[p]<0.51 else eps
            mu_n=mus[s0][:,p].copy(); mu_n[1:]+=ee*rngN.standard_normal(K-1)
            wfit=nnls_rung_c(mu_n[:,None],np.array([np.sum(np.abs(Bc[:,p])**2)]),grid,s0)
            pe[t,p]=abs(float(wfit[0]@inv)-Reff_t[p])/Reff_t[p]
        c=6+t%8
        mun=[mus[s][:,c].copy() for s in sigmas]
        for d,s in enumerate(sigmas):
            g,f=flags_c(mus[s]); ee=eps/10 if f[c]<0.51 else eps
            mun[d][1:]+=ee*rngN.standard_normal(K-1)
        w=joint(mun)
        ln_e[t]=abs(float(w@np.log(grid))-lndet_t); tr_e[t]=abs(float(w@inv)-trinv_t)/trinv_t
    return dict(tag=tag,alpha=alpha,lam_min=lam_min,truth_gate=gate,
        band_med_pct=100*float(np.median(band)),endpoint_med_pct=100*float(np.median(endp)),
        endpoint_p90_pct=100*float(np.quantile(endp,0.9)),
        lndet_true=lndet_t,lndet_err=abs(lndet_h-lndet_t),trinv_err_pct=100*abs(trinv_h-trinv_t)/trinv_t,
        noise_endpoint_med_pct=100*float(np.median(np.median(pe,0))),
        noise_lndet_med=float(np.median(ln_e)),noise_trinv_med_pct=100*float(np.median(tr_e)),
        aliveLWP={("port%d"%c if c<6 else "probe%d"%(c-6)):aliveL[c] for c in range(14)})
res={}
# T1a magnetic torus across fluxes
Lx=Ly=32; n=Lx*Ly
def torus_L(p):
    phi=2*np.pi*p/Lx
    L=np.zeros((n,n),dtype=complex)
    idx=lambda x,y:(x%Lx)*Ly+(y%Ly)
    for x in range(Lx):
        for y in range(Ly):
            i=idx(x,y)
            for (dx,dy,ph) in [(1,0,1.0),(0,1,np.exp(1j*phi*x))]:
                j=idx(x+dx,y+dy)
                L[i,j]-=ph; L[j,i]-=np.conj(ph)
                L[i,i]+=1; L[j,j]+=1
    return L
for p in [0,1,2,4,8,16]:
    L=torus_L(p)
    r=run_instance(L,"torus_p%d"%p,deflate=(p==0))
    res["torus_p%d"%p]=r
    print("p=%d lam_min=%.4g band %.4f%% endp %.4f%%/%.4f%% lndet %.2e trinv %.4f%% noise %.3f%%/%.4f/%.3f%% gate %.1e (%.0fs)"%(
      p,r["lam_min"],r["band_med_pct"],r["endpoint_med_pct"],r["endpoint_p90_pct"],r["lndet_err"],r["trinv_err_pct"],
      r["noise_endpoint_med_pct"],r["noise_lndet_med"],r["noise_trinv_med_pct"],r["truth_gate"],time.time()-t0),flush=True)
    json.dump(res,open("res_I_t1.json","w"),indent=1)
# T1b signed SBM
rg=np.random.default_rng(2026); nS=1024; h=nS//2
A=np.zeros((nS,nS))
for i in range(nS):
    for j in range(i+1,nS):
        same=(i<h)==(j<h)
        if same and rg.random()<0.02: A[i,j]=A[j,i]=1.0
        elif (not same) and rg.random()<0.01: A[i,j]=A[j,i]=-1.0
Ls=np.diag(np.sum(np.abs(A),1))-A
r=run_instance(Ls.astype(complex),"signed_sbm",deflate=False)
res["signed_sbm"]=r
print("SBM lam_min=%.4g band %.4f%% endp %.4f%% lndet %.2e trinv %.4f%%"%(r["lam_min"],r["band_med_pct"],r["endpoint_med_pct"],r["lndet_err"],r["trinv_err_pct"]),flush=True)
json.dump(res,open("res_I_t1.json","w"),indent=1)
print("T1 DONE %.0fs"%(time.time()-t0))
