import tarfile

tf = tarfile.open("kdelibs-4.7.3.tar.bz2", "r")
print(len(tf.getnames()))
