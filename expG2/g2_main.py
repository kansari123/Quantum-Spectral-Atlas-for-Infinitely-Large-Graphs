import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla, json, time
from graphatlas import GraphOp, nnls_rung, flags
t0=time.time(); K=24; G_CUT=5e-3; C_REL=1e-3
res={}
def lwp_alive(models_dsg, grid, sigmas):
    """models_dsg: (R, C, Ngrid). Returns aliveL: list per column of kept sigma values, and c matrix."""
    lg=np.log10(grid); ls=np.log10(np.array(sigmas))
    band=np.argmin(np.abs(lg[:,None]-ls[None,:]),axis=1)   # full-ladder band map (stitcher-identical)
    R,C,_=models_dsg.shape
    c=np.zeros((R,C))
    for d in range(R):
        m=band==d
        c[d]= models_dsg[d][:,m]@(1.0/grid[m])
    tot=c.sum(0)
    aliveL=[[sigmas[d] for d in range(R) if c[d,col]>=C_REL*tot[col]] or [sigmas[-1]] for col in range(C)]
    return aliveL, c
# ---------------- LastFM regression (P-G2R3): archived models, zero new shots ----------------
d=np.load("stage2a.npz",allow_pickle=True)
models=d["models"]; grid=d["grid"]; sigmas=[float(s) for s in d["sigmas"]]
gmask=d["alive_mask"]   # (20, 6) g-rule alive
tr=np.load("stage2truth_solves.npz"); Reff_true=tr["Reff_true"]
aliveL,cmat=lwp_alive(models,grid,sigmas)
aliveG=[[sigmas[j] for j in range(len(sigmas)) if gmask[col,j]] for col in range(20)]
changed=[col for col in range(20) if set(aliveL[col])!=set(aliveG[col])]
inv_g=1.0/grid
def reff_eval(alive,col):
    s0=sorted(alive)[0]; ri=sigmas.index(s0)
    return float(models[ri,col]@inv_g)
errL=np.array([abs(reff_eval(aliveL[p],p)-Reff_true[p])/Reff_true[p] for p in range(12)])
errG=np.array([abs(reff_eval(aliveG[p],p)-Reff_true[p])/Reff_true[p] for p in range(12)])
res["lastfm"]=dict(cols_changed=len(changed),changed_cols=changed,
    changes={str(c):{"g":aliveG[c],"lwp":aliveL[c]} for c in changed},
    reff_med_LWP_pct=100*float(np.median(errL)), reff_med_g_pct=100*float(np.median(errG)),
    bar_med_pct=0.0017, kill_med_pct=0.5)
print("LastFM: cols changed %d, med LWP %.5f%% (g: %.5f%%)  %.0fs"%(len(changed),res["lastfm"]["reff_med_LWP_pct"],res["lastfm"]["reff_med_g_pct"],time.time()-t0),flush=True)
# ---------------- SBM (P-G2R1/R2): deterministic rebuild + authenticity gates ----------------
Ws=sp.load_npz("sbm_W.npz"); n=Ws.shape[0]
deg=np.asarray(Ws.sum(1)).ravel(); L=sp.diags(deg)-Ws
op=GraphOp(L); alpha=33.361
sigS=[1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1.0,1e1,1e2]
gridS=np.logspace(-7,np.log10(1.2*alpha),400)
rng=np.random.default_rng(2026); csz=512
ports=[(0*csz+int(rng.integers(csz)),7*csz+int(rng.integers(csz))),
       (0*csz+int(rng.integers(csz)),1*csz+int(rng.integers(csz))),
       (3*csz+int(rng.integers(csz)),3*csz+int(rng.integers(csz)))]
hub=int(np.argmax(deg)); v=int(rng.integers(n)); ports.append((hub,v))
names=["far-inter","adj-inter","intra","hub+rand"]
B=np.zeros((n,4))
for p,(u,vv) in enumerate(ports): B[u,p]=1.; B[vv,p]=-1.
musS={};modS=np.zeros((9,4,400))
for i,s in enumerate(sigS):
    mu,nb2=op.moments_block(s,K,B); musS[s]=mu
    modS[i]=nnls_rung(mu,nb2,gridS,s,K)
gmatS=np.array([flags(musS[s])[0] for s in sigS])
one=np.ones(n)/np.sqrt(n); Bp=B-np.outer(one,one@B)
lu=spla.splu((L+1e-13*sp.identity(n)).tocsc()); X=lu.solve(Bp)
Reff_S=np.sum(Bp*X,0)
rec=json.load(open("res_sbm.json"))
g_rec=np.array([rec["g_by_rung"][k] for k in rec["names"]]).T   # (9,4)
gate_g=float(np.max(np.abs(gmatS-g_rec)/np.maximum(g_rec,1e-300)))
gate_R=float(np.max(np.abs(Reff_S-np.array(rec["Reff_true"]))/np.array(rec["Reff_true"])))
invS=1.0/gridS
def reff_S(alive,p):
    s0=sorted(alive)[0]; ri=sigS.index(s0)
    return float(modS[ri,p]@invS)
err_full=np.array([abs(reff_S(sigS,p)-Reff_S[p])/Reff_S[p] for p in range(4)])
gate_full=float(np.max(np.abs(100*err_full-np.array(rec["err_full_pct"]))))
print("AUTH gates: g %.2e  Reff %.2e  errfull(abs pct) %.2e"%(gate_g,gate_R,gate_full),flush=True)
aliveLS,cS=lwp_alive(modS,gridS,sigS)
aliveGS=[[sigS[dd] for dd in range(9) if gmatS[dd,p]>=G_CUT] or [sigS[-1]] for p in range(4)]
errL_S=np.array([abs(reff_S(aliveLS[p],p)-Reff_S[p])/Reff_S[p] for p in range(4)])
ratio=errL_S/np.maximum(err_full,1e-300)
empty={1e-4,1e-3,1e-2,1e-1}
R1a=all(len(empty.intersection(aliveLS[p]))==0 for p in range(4))
R1b=all((1e-6 in aliveLS[p]) and (1e-5 in aliveLS[p]) for p in (0,1,3))
R1c=bool(np.all(ratio<=2.0)); R1kill=bool(np.any(ratio>10.0))
R2=(len(aliveLS[2])<=3) and (1e-6 not in aliveLS[2]) and (1e-5 not in aliveLS[2])
D=[int(np.ceil(4*np.sqrt(alpha/s))) for s in sigS]
res["sbm"]=dict(auth_gates=dict(g_rel=gate_g,Reff_rel=gate_R,errfull_abs_pct=gate_full),
  aliveLWP={names[p]:aliveLS[p] for p in range(4)}, aliveG={names[p]:aliveGS[p] for p in range(4)},
  c_over_tot={names[p]:[float(cS[dd,p]/cS[:,p].sum()) for dd in range(9)] for p in range(4)},
  err_full_pct=[100*float(e) for e in err_full], err_LWP_pct=[100*float(e) for e in errL_S],
  ratio=[float(r) for r in ratio],
  P_G2R1a=R1a,P_G2R1b=R1b,P_G2R1c=R1c,R1_kill=R1kill,P_G2R2=R2,
  SumD_full=int(np.sum(D)),
  SumD_LWP={names[p]:int(np.sum([D[sigS.index(s)] for s in aliveLS[p]])) for p in range(4)},
  SumD_g={names[p]:int(np.sum([D[sigS.index(s)] for s in aliveGS[p]])) for p in range(4)})
json.dump(res,open("res_G2.json","w"),indent=1)
print(json.dumps(res["sbm"],indent=1)[:2200])
print("MAIN G2 DONE %.0fs"%(time.time()-t0))
