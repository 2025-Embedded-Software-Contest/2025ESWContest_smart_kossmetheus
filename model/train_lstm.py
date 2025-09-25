import numpy as np, tensorflow as tf
from sklearn.model_selection import train_test_split

np.random.seed(0); tf.random.set_seed(0)
WIN, D = 30, 9   # 3초 창, 9차원(기본6 + 파생3 예시)

def synth_segment(n=200, p_fall=0.15):
    # presence, movement(0/1/2), range, dwell, fallState
    X, y = [], []
    for _ in range(n):
        is_fall = np.random.rand() < p_fall
        pres = np.ones(WIN)
        mv = np.random.choice([0,1,2], size=WIN, p=[0.2,0.4,0.4])
        rng = np.clip(np.cumsum(np.random.randn(WIN)*0.5), -20, 80)+20
        dwl = (mv==1).astype(float)

        if is_fall:
            k = np.random.randint(8, 20)
            rng[k:k+3] += np.array([20, 30, 10])
            mv[k+2:] = 1
            dwl[k+3:] = 1

        # 원-핫
        mv_oh = np.eye(3)[mv]
        # 표준화 흉내
        r_z = (rng - 20)/20
        # 파생: diff, ewma, change
        diff = np.concatenate([[0], np.diff(rng)])/10
        ewma = np.zeros(WIN); a=0.2
        for t in range(1,WIN): ewma[t] = a*rng[t] + (1-a)*ewma[t-1]
        change = np.concatenate([[0],[mv[t]!=mv[t-1] for t in range(1,WIN)]]).astypㅇe(float)

        feats = np.c_[pres, mv_oh, r_z, diff, (ewma-20)/20, change]  # ~9D
        X.append(feats.astype(np.float32))
        y.append(1.0 if is_fall else 0.0)
    return np.array(X), np.array(y)

X, y = synth_segment(1500, p_fall=0.2)
Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

model = tf.keras.Sequential([
    tf.keras.layers.Input((WIN, X.shape[-1])),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32, return_sequences=True)),
    tf.keras.layers.LSTM(16),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=[tf.keras.metrics.AUC(name='auc'), 'accuracy'])
model.fit(Xtr, ytr, epochs=15, batch_size=128, validation_data=(Xva, yva))

model.save('model/c1001_lstm_corrector.h5')
with open('model/threshold.txt','w') as f: f.write('0.6')
print("Saved model & threshold")
