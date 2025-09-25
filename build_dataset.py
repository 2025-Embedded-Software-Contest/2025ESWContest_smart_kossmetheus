# build_dataset.py
import pandas as pd
import numpy as np

CSV = 'c1001_raw_log.csv'
WIN = 30   
STRIDE = 3 

df = pd.read_csv(CSV)
df = df.sort_values('ts').reset_index(drop=True)

df = df.dropna(subset=['presence','movement','movingRange','dwell','fallState'])

mu = df['movingRange'].mean()
std = df['movingRange'].std() + 1e-6

def one_hot_mv(m):
    oh = np.zeros(3, dtype=np.float32)
    if m in [0,1,2]: oh[m] = 1.0
    return oh

X, y = [], []
vals = df[['presence','movement','movingRange','dwell','fallState']].values.astype(float)

for i in range(0, len(vals)-WIN, STRIDE):
    win = vals[i:i+WIN]
    pres = win[:,0:1]
    mv_oh = np.stack([one_hot_mv(int(m)) for m in win[:,1]], axis=0)  # (WIN,3)
    rng = ((win[:,2:3]-mu)/std)                                       # (WIN,1)
    dwl = win[:,3:4]
    feats = np.concatenate([pres, mv_oh, rng, dwl], axis=1)           # (WIN,6)
    X.append(feats)

    fall_win = win[:,4]
    y.append(1.0 if fall_win.max()>0.5 else 0.0)

X = np.array(X, dtype=np.float32)   
y = np.array(y, dtype=np.float32)   
np.savez('dataset_win30.npz', X=X, y=y, mu=mu, std=std)
print(X.shape, y.mean())
