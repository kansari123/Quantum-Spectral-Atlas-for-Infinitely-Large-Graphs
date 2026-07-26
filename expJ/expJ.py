import numpy as np, json, time, itertools
t0=time.time()
l=12; n=1<<l
# terms as (xmask, zmask)
terms=[]
for i in range(l): terms.append(((1<<i), (1<<((i+1)%l)), "C%d"%i))
for i in (0,4,8): terms.append(((1<<i)|(1<<((i+2)%l)), 0, "E%d"%i))
def anticomm(a,b):
    # Pauli strings anticommute iff sum over qubits of (x1z2 - z1x2) parity is odd
    return (bin(a[0]&b[1]).count("1")+bin(a[1]&b[0]).count("1"))%2==1
m=len(terms)
adj=[[anticomm(terms[a],terms[b]) for b in range(m)] for a in range(m)]
# J1: find induced claw K_{1,3}
claw=None
for c in range(m):
    nb=[v for v in range(m) if adj[c][v]]
    for trio in itertools.combinations(nb,3):
        if not adj[trio[0]][trio[1]] and not adj[trio[0]][trio[2]] and not adj[trio[1]][trio[2]]:
            claw=(terms[c][2],terms[trio[0]][2],terms[trio[1]][2],terms[trio[2]][2]); break
    if claw: break
# J2: non-commuting pair exists
ncpair=any(any(row) for row in adj)
print("J1 claw certificate:", claw, " J2 non-commuting pair:", ncpair, flush=True)
# build dense L_J
xs=np.arange(n)
L=np.zeros((n,n))
for (xm,zm,_) in terms:
    sgn=1-2*(np.array([bin(x&zm).count("1") for x in xs])%2) if zm else np.ones(n)
    L[xs, xs^xm]-=sgn
L+=np.diag(np.full(n,float(m)))
assert np.max(np.abs(L-L.T))==0
# engine via EXP I machinery
src=open("expI_t1.py").read().split("res={}")[0]
ns={}; exec(src,ns)
r=ns["run_instance"](L.astype(complex),"expJ_l12",deflate=False)
print("J3 l=12 lam_min=%.4f band %.4f%% endp %.4f%%/%.4f%% lndet %.2e trinv %.4f%% noise %.3f%%/%.4f/%.3f%% gate %.1e (%.0fs)"%(
  r["lam_min"],r["band_med_pct"],r["endpoint_med_pct"],r["endpoint_p90_pct"],r["lndet_err"],r["trinv_err_pct"],
  r["noise_endpoint_med_pct"],r["noise_lndet_med"],r["noise_trinv_med_pct"],r["truth_gate"],time.time()-t0),flush=True)
# J4 sampler on implicit rules
alpha=r["alpha"]; sig=1e-2; tstar=int(np.ceil(alpha/sig))
d0=1-m/alpha; w=1/alpha; S=d0+m*w
probs=np.array([d0]+[w]*m)/S; cum=np.cumsum(probs)
rng=np.random.default_rng(606); N=200000
x=rng.integers(0,n,N); sgn=np.ones(N); sb=[]
zms=np.array([t[1] for t in terms]); xms=np.array([t[0] for t in terms])
pop=np.array([bin(v).count("1")%2 for v in range(n)])  # parity table
for t in range(150):
    u=rng.random(N); mv=np.searchsorted(cum,u)
    act=mv>0
    ti=np.where(act, mv-1, 0)
    zm=zms[ti]; xm=xms[ti]
    s_step=np.where(act & (zm>0), 1-2*pop[x & zm], 1)
    sgn=sgn*s_step
    x=np.where(act, x ^ xm, x)
    sb.append(abs(float(np.mean(sgn))))
sb=np.array(sb); thr=5/np.sqrt(N)
ok=np.where(sb>thr)[0]
k=ok[:min(len(ok),60)]
Ds=float(-np.polyfit(k+1,np.log(sb[k]),1)[0])
mult=float(np.exp(2*Ds*tstar))
print("J4 Ds=%.4f dead_by_t=%d t*=%d mult=%.3e (bar 1e6, kill 1e2)"%(Ds,int(ok[-1]+2),tstar,mult))
res=json.load(open("res_I_t1.json"))
res["expJ"]=dict(claw=claw,noncommuting=bool(ncpair),l12=r,sampler=dict(Ds=Ds,tstar=tstar,mult=mult,dead_by=int(ok[-1]+2)),
                 terms=[t[2] for t in terms])
json.dump(res,open("res_I_t1.json","w"),indent=1)
print("EXPJ DONE %.0fs"%(time.time()-t0))
