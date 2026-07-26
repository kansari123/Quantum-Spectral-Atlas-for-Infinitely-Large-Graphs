# ==================== Q-PVL RUN-2 REANALYSIS (self-contained, zero QPU) ====================
# Paste as ONE new cell at the END of your notebook and run it. Reads the existing
# qpvl_hw_results_lite.json cache; no hardware, no credentials, no qiskit needed.
import json, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import nnls

CACHE="qpvl_hw_results_lite.json"; K_MAX=8; MODELS=["signed","unsigned"]
R=json.load(open(CACHE)); print("data from:",R["_meta"])
assert R["_meta"].get("instance")=="lite", "this block reanalyzes the lite-instance cache"
SHOTS=R["_meta"].get("shots",8192); sig=1/np.sqrt(SHOTS)

# ---- exact lite model + truth (verbatim from the validated notebook; numpy only) ----
I2=np.eye(2); PX=np.array([[0,1],[1,0]],dtype=complex); PZ=np.diag([1,-1]).astype(complex)
SP=dict(n_sys=2, nT=2, terms={"signed":[[("X",0)],[("Z",0),("X",1)]],
                              "unsigned":[[("X",0)],[("X",1)]]})
L_SITES=SP["n_sys"]; N_TERMS=SP["nT"]; PORT="plus0"
def pauli_matrix(term):
    ops=[I2]*L_SITES
    for p,q in term: ops[q]=PX if p=="X" else PZ
    out=np.array([[1]],dtype=complex)
    for o in ops[::-1]: out=np.kron(o,out)
    return out
def A_matrix(model): return sum(pauli_matrix(t) for t in SP["terms"][model])/N_TERMS
def port_vec(n):
    b=np.zeros(n,dtype=complex)
    if PORT=="plus0": b[0]=b[1]=1/np.sqrt(2)
    else: b[0]=1
    return b
def cheb_truth(model,K):
    A=A_matrix(model); n=A.shape[0]
    b=port_vec(n)
    out=[1.0]; Tm=np.eye(n,dtype=complex); Tc=A.copy()
    for k in range(1,K):
        out.append(float(np.real(b.conj()@Tc@b))); Tm,Tc=Tc,2*A@Tc-Tm
    return np.array(out)
GEN2Q={0:0,1:17,2:34,3:51,4:68,5:85,6:102,7:119,8:136}
N2Q=R.get("_n2q",{m:{str(k):GEN2Q[k] for k in range(K_MAX+1)} for m in MODELS})

# ---- self-normalization + alpha calibration ----
# Self-normalization: mu_0 is EXACTLY 1 by construction (the k=0 circuit applies no walk
# steps), so any deviation of the measured mu_0 from 1 is a global multiplicative artifact
# (e.g. over-corrected readout mitigation). Dividing every moment by the measured mu_0 removes
# it exactly, truth-free.
MU0={m: R[m]["0"] for m in MODELS}
for m in MODELS:
    dev=100*(MU0[m]-1)
    print(f"{m}: measured mu_0 = {MU0[m]:.4f} (mathematical value 1) -> "
          f"global scale artifact {dev:+.1f}% removed by self-normalization")
def get_mu(m):
    return [R[m][str(k)]/MU0[m] for k in range(K_MAX+1)]
def fit_alpha(m):
    truth=cheb_truth(m,K_MAX+1); mu=get_mu(m); xs=[]; ys=[]
    for k in range(1,K_MAX+1):
        t=truth[k]
        if abs(t)<0.05: continue
        if abs(mu[k])<3*sig: continue          # moment at the noise floor: no alpha information
        r=mu[k]/t
        if r<=0.01: continue
        xs.append(N2Q[m][str(k)]); ys.append(np.log(r))
    if len(xs)<2: return None
    a=np.exp(np.polyfit(xs,ys,1)[0]); return a
ALPHA={m:fit_alpha(m) for m in MODELS}
print("fitted per-2Q-gate signal retention alpha:",{m:(f"{a:.4f}" if a else "n/a") for m,a in ALPHA.items()})
def mu_corr(m):
    a=ALPHA[m]; mu=get_mu(m)
    return [mu[k]/(a**N2Q[m][str(k)]) if (a and k>0) else mu[k] for k in range(K_MAX+1)]

# ---- bias vs true circuit volume (normalized moments) ----
R=json.load(open(CACHE)); print("data from:",R["_meta"])
N2Q=R.get("_n2q",{m:{str(k):GEN2Q[k] for k in range(K_MAX+1)} for m in MODELS})
sig=1/np.sqrt(R["_meta"]["shots"])
fig,ax=plt.subplots(1,2,figsize=(11,4))
for m,c in zip(MODELS,["#1f77b4","#2ca02c"]):
    truth=cheb_truth(m,K_MAX+1)
    mu=np.array([R[m][str(k)] for k in range(K_MAX+1)]); bias=mu-truth
    ax[0].errorbar(range(K_MAX+1),bias,yerr=sig,fmt="o-",color=c,label=m,capsize=3)
    xs=[N2Q[m][str(k)] for k in range(1,K_MAX+1)]
    ax[1].semilogy(xs,np.abs(bias[1:])+1e-6,"o-",color=c,label=m)
ax[0].axhline(0,color="gray",lw=.7); ax[0].set_xlabel("Chebyshev order k"); ax[0].set_ylabel("measured bias"); ax[0].legend()
ax[1].set_xlabel("ISA 2Q gates"); ax[1].set_ylabel("|bias|"); ax[1].set_title("moment bias vs circuit volume"); ax[1].legend()
plt.tight_layout(); plt.show()

# ---- two-regime usable-depth selection ----
GRID=np.linspace(-0.9999,0.9999,241); TH=np.arccos(GRID)
def fit_measure(mu,grid=None):
    g=GRID if grid is None else grid; th=np.arccos(g)
    K=len(mu); Adm=np.cos(np.outer(np.arange(K),th)); A0=Adm.copy(); A0[0]*=100.
    b=np.array(mu,float); b[0]*=100.
    w,_=nnls(A0,b,maxiter=200*len(g)); return w,g
def kstar_select(mu_all,sig_k):
    # Two regimes, truth-free. (1) SNR gate: moments below 5x their own noise floor carry
    # no usable signal; fewer than three informative orders => noise-characterization
    # regime (functional table suppressed downstream). (2) Within the SNR-passing prefix,
    # prune TOP-DOWN on in-sample consistency: the fit of the retained prefix must
    # reproduce every retained moment within tolerance. Small-K forward holdout is NOT
    # used: an ambiguous short prefix (e.g. an operator with A^2 proportional to I)
    # resolves only once the informative higher moments are included.
    usable=[k for k in range(1,len(mu_all)) if abs(mu_all[k])>5*sig_k[k]]
    K_snr=min((max(usable)+1) if usable else 1, len(mu_all))
    if K_snr<4: return K_snr
    for K in range(K_snr,3,-1):
        w,g=fit_measure(mu_all[:K]); th=np.arccos(g)
        if all(abs(float(w@np.cos(k*th))-mu_all[k])<=5*sig_k[k] for k in range(1,K)):
            return K
    return 3
def support_refit(mu,s):
    w,g=fit_measure(mu); nb_=24; edges=np.linspace(-1,1,nb_+1)
    keep=np.zeros(nb_,bool)
    for j in range(nb_):
        msk=(g>=edges[j])&(g<edges[j+1])
        if w[msk].sum()>1e-3: keep[j]=True
    keep=keep|np.roll(keep,1)|np.roll(keep,-1)
    mask=np.zeros_like(g,bool)
    for j in range(nb_):
        if keep[j]: mask|=(g>=edges[j])&(g<=edges[j+1])
    return fit_measure(mu,grid=g[mask])
SIGK={"raw":{m:[sig/abs(MU0[m])]*(K_MAX+1) for m in MODELS},
      "calibrated":{m:[sig/abs(MU0[m])/(ALPHA[m]**N2Q[m][str(k)]) if (ALPHA[m] and k>0) else sig/abs(MU0[m])
                       for k in range(K_MAX+1)] for m in MODELS}}
ARMS={"raw":{m:get_mu(m) for m in MODELS},          # self-normalized by measured mu_0
      "calibrated":{m:mu_corr(m) for m in MODELS}}
KS={arm:{m:kstar_select(ARMS[arm][m],SIGK[arm][m]) for m in MODELS} for arm in ARMS}
print("usable orders (truth-free; <4 = noise-characterization regime):",KS)

# ---- functional atlas, raw & calibrated ----
S_GRID=np.exp(np.linspace(np.log(0.3),np.log(10),20))
import pandas as pd
rows=[]
for arm in ("raw","calibrated"):
    for m in MODELS:
        if KS[arm][m]<4:
            print(f"[{arm}/{m}] only {KS[arm][m]} usable moment(s) above the noise floor -> "
                  f"functional table SUPPRESSED; this dataset is informative for noise "
                  f"characterization (alpha fit, bias-vs-volume), not spectroscopy.")
            continue
        w,g=support_refit(ARMS[arm][m][:KS[arm][m]],sig)
        lam_g=N_TERMS*(1-g)
        Am=A_matrix(m); ev,U=np.linalg.eigh(Am); lam=N_TERMS*(1-ev)
        b=port_vec(Am.shape[0]); pj=np.abs(U.conj().T@b)**2
        for s_ in S_GRID:
            hw=float(w@(1/(lam_g+s_))); ex=float(np.sum(pj/(lam+s_)))
            rows.append((arm,m,f"R({s_:.3g})",hw,ex,100*abs(hw-ex)/ex))
        if m=="signed" and lam_g.min()>0.05:
            hw=float(w@np.log(lam_g)); ex=float(np.sum(pj*np.log(lam)))
            rows.append((arm,m,"port lndet",hw,ex,100*abs(hw-ex)/abs(ex)))
            hw=float(w@(1/lam_g)); ex=float(np.sum(pj/lam))
            rows.append((arm,m,"port tr-inv",hw,ex,100*abs(hw-ex)/ex))
df=pd.DataFrame(rows,columns=["arm","model","functional","hardware","exact","rel err %"])
for arm in ("raw","calibrated"):
    med={m:df[(df.arm==arm)&(df.model==m)]["rel err %"].median() for m in MODELS}
    print(arm,"median functional error:",{k:f"{v:.3g}%" for k,v in med.items()})
print("\n(calibrated arm divides by fitted alpha^n2q using KNOWN truth - validation-only;",
      "a deployment would calibrate from reference circuits instead)")
print(df.to_string(index=False,float_format=lambda x:f"{x:.5g}"))

# ---- empirical noise model (if repeats present) ----
if "_repeats" in R:
    print("shot-noise prediction 1/sqrt(shots) =",f"{sig:.4f}")
    for m in MODELS:
        for k,vals in sorted(R["_repeats"].get(m,{}).items(),key=lambda kv:int(kv[0])):
            if len(vals)>=3: print(f"  {m} k={k}: sigma_emp={np.std(vals,ddof=1):.4f} (n={len(vals)})")
else: print("local mode: run on hardware for the noise-model check.")