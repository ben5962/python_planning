import tempfile
# Autogenerated with DRAKON Editor 1.28

def getFichierTemporaire():
    #item 20
    a = tempfile.TemporaryFile(mode = 'w+')
    #item 21
    return a


def readFichierTemporaire(instance_fichier_temporaire):
    #item 34
    instance_fichier_temporaire.seek(0)
    #item 35
    return [l.strip() for l in instance_fichier_temporaire.readlines()]


def readLineFichierTemporaire(instance_fichier_temporaire):
    #item 42
    return instance_fichier_temporaire.readline().strip()


def writeFichierTemporaire(instance_de_fichier_temporaire, chaine):
    #item 27
    instance_de_fichier_temporaire.write(chaine + "\n")
    #item 28
    return instance_de_fichier_temporaire

    pass
