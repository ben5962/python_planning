import constantes

import devpy.develop as log
log.setLevel('DEBUG')



# Autogenerated with DRAKON Editor 1.28

def ready_w(chaine):
    #item 213
    for r in xpld.xplode_ite(chaine):
        return repr_dico(r)


def repr_dico(dico_result):
    #item 206
    return str(dico_result['day'])  +" " + str(dico_result['month']) +  " " + str(dico_result['year'])   + " " + str(dico_result['poste'])

class xpld(object):



    def __init__(self):
        #item 16
        pass


    def _get_split_or_die(chaine, split_wanted=None):
        #item 97
        if split_wanted in ['jours','mois','annee','poste']:
            #item 101
            if xpld.valider_ligne(chaine):
                #item 91
                import re
                #item 92
                pat = re.compile(r"""
                (?P<jours>^(\d+,*)+)\s
                (?P<mois>\d{1,2})\s
                (?P<annee>\d{4,4})\s
                (?P<poste>\w{2,4})
                """,re.VERBOSE)
                #item 93
                match = re.search(pat, chaine)
                #item 94
                if match:
                    #item 104
                    return match.group(split_wanted)
                else:
                    #item 96
                    raise ValueError('bizarre: splitwanted ok ligne ok mais ok match',split_wanted, chaine)
            else:
                #item 108
                raise ValueError('ligne pas dans le bon format', chaine)
        else:
            #item 100
            raise ValueError('splitwanted doit etre dans jour mois annee poste',split_wanted)


    def _validate_int_between(chaine, mini, maxi):
        #item 41
        try:
            return int(chaine) >= mini and int(chaine) <= maxi
        except ValueError:
            return False


    def display_results(dico_result):
        for saisie in dico_result:
            #item 195
            print("{j} {m} {a} {p}".format(j=saisie['day'], 
                m=saisie['month'], 
                a=saisie['year'], 
                p=saisie['poste']))


    def file_operations(transfo_sur_ligne, filer, methode_lecture, filew, methode_ecriture, methode_fermeture):
        #item 215
        # s assurer que file r existe et que filew existe
        import os.path
        #item 216
        if os.path.isfile(filer):
            #item 220
            while methode_lecture_ligne(filer) is not '':
                lr = methode_lecture_ligne(filer)
                for result in methode_decomposition_ligne(lr):
                    methode_ecriture_ligne(filew,repr_dico(result))
            
            
            if isinstance(filer, 'File'):
                filer.close()
            if isinstance(filew, 'File'):
                filew.close()
        else:
            #item 219
            import fileDoesNotExist
            raise fileDoesNotExist.FileDoesNotExist


    def get_days(chaine):
        #item 81
        if xpld.valider_ligne(chaine):
            #item 80
            
            return chaine.split()[0]
        else:
            #item 84
            raise ValueError('le format de la ligne etait errone',ligne)


    def get_month(chaine):
        #item 114
        return int(xpld._get_split_or_die(chaine,'mois'))


    def get_poste(chaine):
        #item 126
        return xpld._get_split_or_die(chaine,'poste')


    def get_year(chaine):
        #item 120
        return int(xpld._get_split_or_die(chaine,'annee'))


    def main(liste_args, parsed=None):
        #item 177
        if parsed is None:
            #item 161
            import module_parse_xpld
            parsed = module_parse_xpld.parse(liste_args)
        else:
            pass
        #item 162
        if parsed.gui:
            #item 165
            raise NotImplementedYet("gui not implemented yet")
            #todo
        else:
            #item 166
            if parsed.file:
                #item 176
                #raise NotImplementedYet("operation from file not implemented yet")
                #todo
                #item 187
                xpld.file_operations(fn=None, filename=parsed.file)
            else:
                #item 171
                ligne = parsed.jours + ' ' + parsed.mois + ' ' + parsed.annee + ' ' + parsed.poste
                #item 172
                if xpld.valider_ligne(ligne):
                    #item 175
                    #print(resultat)
                    xpld.display_results(xpld.xplode(ligne))
                else:
                    pass


    def split_virg(chaine):
        #item 22
        return [int(i) for i in chaine.split(",")]

    def validate_day(day):
        log.debug("lancement de validate day avec chaine = {}".format(day))
        if int(day) > 0 and int(day) < 32:
            return True
        else:
            log.debug("jour ne peut prendre comme valeur que de 1 à 31 dans {}".format(day))
            return False


    def validate_days(days):
        #item 73
        #import functools
        #item 72
        #return functools.reduce((lambda x,y: xpld._validate_int_between(chaine=x,mini=1,maxi=31) and xpld._validate_int_between(chaine=y,mini=1,maxi=31)) ,xpld.split_virg(days))
        verite = True
        for jour in xpld.split_virg(days):
            if not xpld.validate_day(jour):
                verite = False
                break
        return verite

    def validate_month(chaine):
        #item 43
        #return xpld._validate_int_between(chaine=arg_chaine,mini=1,maxi=12)
        #item 35
        log.debug("lancement de validate month avec chaine = {}".format(chaine))
        if int(chaine) > 0 and int(chaine) < 13:
            return True
        else:
            log.debug("mois ne peut prendre comme valeur que de 1 à 12 dans {}".format(chaine))
            return False


    def validate_poste(chaine):
        #item 214
        valeurs_acceptees = constantes.postes.keys()
        if chaine in valeurs_acceptees:
            return True
        else:
            raise ValueError('validate poste: la chaine ne passe pas le cadre',chaine, valeurs_acceptees)


    def validate_year(arg_chaine):
        #item 50
        #return xpld._validate_int_between(chaine=arg_chaine,mini=2002,maxi=2017)
        #item 49
        log.debug("lancement de validate year avec chaine = {}".format(arg_chaine))
        if int(arg_chaine) > 2002 and int(arg_chaine) < 2018:
            return True
        else:
            log.debug("year ne peut prendre comme valeur que de 2002 à 2017 dans {}".format(arg_chaine))
            return False


    def valider_ligne(ligne):
        log.debug("valider ligne avec {}".format(ligne))
        #item 56
        import re
        #item 57
        pat = re.compile(r"""
        (?P<jours>^(\d+,*)+)\s
        (?P<mois>\d{1,2})\s
        (?P<annee>\d{4,4})\s
        (?P<poste>\w{2,2})
        """,re.VERBOSE)
        #item 58
        match = re.search(pat, ligne)
        #item 60
        if match:
            #item 63
            jours = match.group('jours')
            mois = match.group('mois')
            annee = match.group('annee')
            poste = match.group('poste')
            #item 71
            return xpld.validate_month(mois) and xpld.validate_poste(poste) and xpld.validate_year(annee) and xpld.validate_days(jours)
        else:
            #item 64
            return False


    def xplode(chaine):
        #item 132
        if xpld.valider_ligne(chaine):
            #item 135
            liste_resultat = []
            mois = xpld.get_month(chaine)
            poste = xpld.get_poste(chaine)
            annee = xpld.get_year(chaine)
            poste = xpld.get_poste(chaine)
            for jour in xpld.split_virg(xpld.get_days(chaine)):
                #item 138
                dico = { 'day': jour, 'month': mois, 'year': annee, 'poste' : poste }
                liste_resultat.append(dico)
            #item 139
            return liste_resultat
        else:
            #item 140
            raise ValueError('nope nope nope')


    def xplode_ite(chaine):
        #item 146
        if xpld.valider_ligne(chaine):
            #item 149
            liste_resultat = []
            mois = xpld.get_month(chaine)
            poste = xpld.get_poste(chaine)
            annee = xpld.get_year(chaine)
            poste = xpld.get_poste(chaine)
            for jour in xpld.split_virg(xpld.get_days(chaine)):
                #item 152
                dico = { 'day': jour, 'month': mois, 'year': annee, 'poste' : poste }
                yield dico
        else:
            #item 154
            raise ValueError('la chaine n a pas passe la validation', chaine)

    split_virg = staticmethod(split_virg)
    validate_poste = staticmethod(validate_poste)
    validate_month = staticmethod(validate_month)
    _validate_int_between = staticmethod(_validate_int_between)
    validate_year = staticmethod(validate_year)
    validate_days = staticmethod(validate_days)
    valider_ligne = staticmethod(valider_ligne)
    get_days = staticmethod(get_days)
    _get_split_or_die = staticmethod(_get_split_or_die)
    get_month = staticmethod(get_month)
    get_poste = staticmethod(get_poste)
    get_year = staticmethod(get_year)
    xplode = staticmethod(xplode)
    xplode_ite = staticmethod(xplode_ite)
    file_operations = staticmethod(file_operations)
    display_results = staticmethod(display_results)
    main = staticmethod(main)



if __name__ == '__main__':
    import sys
    xpld.main(sys.argv[1:])
