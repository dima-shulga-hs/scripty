import numpy as np
from sklearn.decomposition import PCA
x = np.random.normal(size=(10, 4))
pca = PCA(n_components=2)
res = pca.fit_transform(x)

print(res.shape)

