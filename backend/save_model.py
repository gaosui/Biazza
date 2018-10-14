from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format("./GoogleNews-vectors-negative300.bin", binary=True)
print("finish loading start saving")
fname = "vectors.kv"
model.save(fname)
print("reload")
word_vectors = KeyedVectors.load("vectors.kv", mmap='r')
print("end")