import numpy as np, json, time
t0=time.time()
res=json.load(open("res_I_t1.json"))
# ---------- T1b-R: declared repair — unbalanced signed SBM (5% sign disorder, seed 20261) ----------
import importlib.util
spec=importlib.util.spec_from_file_location("t1","expI_t1.py")
# reuse run_instance by exec of its function defs only
src=open("expI_t1.py").read().split("res={}")[0]
ns={}; exec(src,ns)
rg=np.random.default_rng(2026); n=1024; h=n//2
A=np.zeros((n,n))
for i in range(n):
    for j in range(i+1,n):
        same=(i<h)==(j<h)
        if same and rg.random()<0.02: A[i,j]=A[j,i]=1.0
        elif (not same) and rg.random()<0.01: A[i,j]=A[j,i]=-1.0
flip=np.random.default_rng(20261)
iu=np.triu_indices(n,1); mask=(A[iu]!=0)&(flip.random(len(iu[0]))<0.05)
A[iu[0][mask],iu[1][mask]]*=-1; A[iu[1][mask],iu[0][mask]]=A[iu[0][mask],iu[1][mask]]
Ls=np.diag(np.sum(np.abs(A),1))-A
r=ns["run_instance"](Ls.astype(complex),"signed_sbm_R",deflate=False)
res["signed_sbm_R"]=r
print("T1b-R lam_min=%.4g band %.4f%% endp %.4f%%/%.4f%% lndet %.2e trinv %.4f%% noise %.3f%%/%.4f/%.3f%% (%.0fs)"%(
  r["lam_min"],r["band_med_pct"],r["endpoint_med_pct"],r["endpoint_p90_pct"],r["lndet_err"],r["trinv_err_pct"],
  r["noise_endpoint_med_pct"],r["noise_lndet_med"],r["noise_trinv_med_pct"],time.time()-t0),flush=True)
json.dump(res,open("res_I_t1.json","w"),indent=1)
# ---------- P-I3: generic classical sampler breakdown on the torus ----------
Lx=Ly=32; n=Lx*Ly; alpha=8.5; sig_star=1e-2; tstar=int(np.ceil(alpha/sig_star))
Tmax=120; N=200000
out={}
for p in [0,1,2,4,8,16]:
    phi=2*np.pi*p/Lx
    # M = I - L/alpha: diag 1-4/alpha; 4 neighbor moves weight 1/alpha, y-moves carry phase exp(+-i phi x)
    d0=1-4/alpha; w=1/alpha
    S=d0+4*w   # uniform row |.|-sum
    probs=np.array([d0, w,w,w,w])/S     # stay, +x,-x,+y,-y
    cum=np.cumsum(probs)
    rng=np.random.default_rng(555+p)
    x=rng.integers(0,Lx,N); y=rng.integers(0,Ly,N)
    ph=np.zeros(N)          # accumulated phase (radians); real-signed at p in {0,16}
    logS=0.0; sbar=[]
    for t in range(1,Tmax+1):
        u=rng.random(N); mv=np.searchsorted(cum,u)
        dx=np.where(mv==1,1,0)-np.where(mv==2,1,0)
        dyp=(mv==3); dym=(mv==4)
        ph+= phi*x*(dyp.astype(float)) - phi*x*(dym.astype(float))
        x=(x+dx)%Lx; y=(y+dyp.astype(int)-dym.astype(int))%Ly
        s=np.abs(np.mean(np.exp(1j*ph)))
        sbar.append(s)
    sb=np.array(sbar)
    # fit decay rate on the measurable window (s > 5/sqrt(N))
    thr=5/np.sqrt(N); ok=np.where(sb>thr)[0]
    if p==0 or len(ok)<5: Ds=0.0 if p==0 else float('nan')
    if p>0:
        tt=np.arange(1,len(ok)+1) if len(ok)>=5 else None
        if len(ok)>=5:
            k=ok[:min(len(ok),60)]
            Ds=float(np.polyfit(k+1,np.log(sb[k]),1)[0]*-1)
        else: Ds=float(np.log(1/thr))  # lower bound: dead within 1 step-window
    mult=float(np.exp(2*Ds*tstar)) if p>0 else 1.0
    out["p%d"%p]=dict(Ds=Ds,avg_sign_at_t20=float(sb[19]),avg_sign_floor=float(thr),
                      dead_by_t=int(ok[-1]+2) if p>0 and len(ok)>0 else None,
                      mult_at_tstar=mult)
    print("p=%2d Ds=%.4f  <s>(t=20)=%.3e  dead_by_t=%s  mult(t*=%d)=%.3e"%(p,out["p%d"%p]["Ds"],sb[19],str(out["p%d"%p]["dead_by_t"]),tstar,mult),flush=True)
Dvals=[out["p%d"%p]["Ds"] for p in [1,2,4,8,16]]
from scipy.stats import spearmanr
rho=float(spearmanr([1,2,4,8,16],Dvals).statistic)
ratio=out["p16"]["mult_at_tstar"]/out["p0"]["mult_at_tstar"]
out["spearman_rho"]=rho; out["mult_ratio_pi_over_0"]=ratio; out["tstar"]=tstar
res["sampler"]=out
json.dump(res,open("res_I_t1.json","w"),indent=1)
print("P-I3: rho=%.3f  multiplier ratio (pi vs 0) = %.3e  [bar >=1e6, kill <1e2]"%(rho,ratio))
print("SAMPLER DONE %.0fs"%(time.time()-t0))
