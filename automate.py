import time
from datetime import datetime
import email
import imaplib
import ast
import aide_a_la_lecture
import lance_ordre

your_email = "" # put your email here

your_password = "" # put your password here

def espion(information, initialisation=False, saut_de_ligne=""):
    if initialisation:
        if input("Dois-je détruire les anciens rapports ?\n") == "oui":
            document_confidentiel = open('document_confidentiel.txt', "w")
        else:
            saut_de_ligne = "\n\n\n"
    document_confidentiel = open('document_confidentiel.txt', "a")
    document_confidentiel.write(f"{saut_de_ligne}Le {datetime.now()} {information}\n")


def etat(numero):
    etats = ['sommeil', 'lecture', 'écriture', 'analyse', "envoi d'un ordre", 'ordre en cours']
    espion(f"l'automate entre dans l'état {etats[numero]}.", saut_de_ligne='\n')


def validateur_reponses(demande, reponses_correctes):
    reponse, compteur = None, 0
    demande += '\n'
    while reponse not in reponses_correctes:
        if compteur > 0:
            print('Vous avez fait une faute de frappe.')
        reponse = input(demande)
        compteur += 1
    return reponse


def inbox():
    username = your_email
    password = your_password
    host = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    for numero in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(numero, '(RFC822)')
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            # print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == 'text/html':
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
    return my_message


def heure_actuelle():
    heures = int(datetime.now().strftime("%H"))
    minutes = round(int(datetime.now().strftime("%M")) / 60, 2)
    return heures + minutes


def checkout(dictionnaire, timeframe=''):
    heikin_sans_faille = dictionnaire[timeframe + 'heikin_ashi'][1][1] == 'oui' and (
                dictionnaire[timeframe + 'heikin_ashi'][0][1] == 'oui' or timeframe == '4h_')
    heikin_couleur_similaire = dictionnaire[timeframe + 'sens_macd'][1] == dictionnaire[timeframe + 'heikin_ashi'][1][
        0] and \
                               (dictionnaire[timeframe + 'heikin_ashi'][1][0] ==
                                dictionnaire[timeframe + 'heikin_ashi'][0][0] or timeframe == '4h_')
    return \
        heikin_sans_faille and \
        dictionnaire[timeframe + 'sens_ichimoku'][1] == dictionnaire[timeframe + 'position_ichimoku'][1] and \
        dictionnaire[timeframe + 'position_ichimoku'][1] == dictionnaire[timeframe + 'position_sar'][1] and \
        dictionnaire[timeframe + 'position_sar'][1] == dictionnaire[timeframe + 'position_ema'][1] and \
        dictionnaire[timeframe + 'position_ema'][1] == dictionnaire[timeframe + 'sens_macd'][1] and \
        heikin_couleur_similaire and \
        dictionnaire[timeframe + 'position_sar'][1] == dictionnaire['position_sar'][1]


def rondoudou():
    temps_actuelle = heure_actuelle()
    heures_valides = [0.5 + (0.75 * i) for i in range(32)]
    for indice in range(len(heures_valides)):
        if heures_valides[indice] >= temps_actuelle:
            temps_repos = round(heures_valides[indice] - temps_actuelle, 2) * 60
            espion("Rondoudou s'endort. Il ne se réveillera pas avant " + str(
                temps_repos + 2) + " bonnes minutes de repos.")
            # time.sleep(temps_repos * 60 + 120)
            espion('Rondoudou se réveille !')
            return


def lecteur():
    messages = inbox()
    return {'sens_ichimoku': aide_a_la_lecture.sens_ichimoku(messages),
            'position_ichimoku': aide_a_la_lecture.position_ichimoku(messages),
            'position_sar': aide_a_la_lecture.position_sar(messages),
            'position_ema': aide_a_la_lecture.position_ema(messages),
            'sens_macd': aide_a_la_lecture.sens_macd(messages),
            'heikin_ashi': aide_a_la_lecture.heikin_ashi(messages),
            '4h_sens_ichimoku': aide_a_la_lecture.quatre_heure_sens_ichimoku(messages),
            '4h_position_ichimoku': aide_a_la_lecture.quatre_heure_position_ichimoku(messages),
            '4h_position_sar': aide_a_la_lecture.quatre_heure_position_sar(messages),
            '4h_position_ema': aide_a_la_lecture.quatre_heure_position_ema(messages),
            '4h_sens_macd': aide_a_la_lecture.quatre_heure_sens_macd(messages),
            '4h_heikin_ashi': aide_a_la_lecture.quatre_heure_heikin_ashi(messages)
            }


def scribe(messages):
    fichier_original = open('indicateurs.txt', "r")
    print(messages)
    dico_en_str = fichier_original.readline()
    print(dico_en_str)
    dictionnaire_originel = ast.literal_eval(dico_en_str)
    for clef in dictionnaire_originel.keys():
        if len(dictionnaire_originel[clef]) == 1:
            dictionnaire_originel[clef].append(messages[clef])
            continue
        dictionnaire_originel[clef][0], dictionnaire_originel[clef][1] = dictionnaire_originel[clef][1], messages[clef]
    open('indicateurs.txt', 'w').write(str(dictionnaire_originel))


def analyste():
    fichier = open('indicateurs.txt', "r")
    dictionnaire = ast.literal_eval(fichier.readline())
    taille = 2
    if checkout(dictionnaire):
        espion("l'analyste a trouvé un signal d'entrée sur les 45 minutes.")
        if checkout(dictionnaire, '4h_'):
            espion("l'analyste a trouvé un signal d'entrée sur les 4 heures.")
            taille = 4
        return True, dictionnaire['sens_ichimoku'][1] == 'vert' * taille


def guet():
    pass


def automate():
    etat(0)
    rondoudou()
    etat(1)
    messages = lecteur()
    etat(2)
    scribe(messages)
    etat(3)
    signal = analyste()
    if not signal[0]:
        espion("pas encore de signal...")
        return
    etat(4)
    lance_ordre.ordre_strategique(signal[1])
    etat(5)
    guet()


def initialisateur():  # On suppose qu'il n'y a pas de signal sur la dernière bougie à avoir fermé
    espion("l'automate se remet en route.\n", initialisation=True)
    reponses_communes = ['vert', 'rouge', 'neutre']
    tableau_reponse = {
        'sens_ichimoku': None,
        'position_ichimoku': None,
        'position_sar': None,
        'position_ema': None,
        'sens_macd': None,
        'heikin_ashi': [None],
        '4h_sens_ichimoku': None,
        '4h_position_ichimoku': None,
        '4h_position_sar': None,
        '4h_position_ema': None,
        '4h_sens_macd': None,
        '4h_heikin_ashi': [None]
    }
    with open('indicateurs.txt', 'w') as fichier:
        if input('Indicateurs prédéfinis ?\n') == 'oui':
            tableau_reponse = {'sens_ichimoku': ['vert'], 'position_ichimoku': ['vert'], 'position_sar': ['vert'],
                               'position_ema': ['vert'],
                               'sens_macd': ['vert'], 'heikin_ashi': [('vert', 'oui')], '4h_sens_ichimoku': ['vert'],
                               '4h_position_ichimoku': ['vert'], '4h_position_sar': ['vert'],
                               '4h_position_ema': ['vert'],
                               '4h_sens_macd': ['vert'], '4h_heikin_ashi': [('vert', 'oui')]}
            print(
                "La base de donnée est bien set up.\nVous pouvez dès maintenant suivre les actions de l'automate en ouvrant le document confidentiel remis par l'espion.")
            fichier.write(str(tableau_reponse))
            return automate()
        print(
            "\nVeuillez indiquer la 'couleur' de ces indicateurs pour la dernière bougie à avoir fermer. (vert, rouge, neutre)\n")
        for key in tableau_reponse.keys():
            tableau_reponse[key] = [validateur_reponses(key, reponses_communes)]
            if key == 'heikin_ashi' or key == '4h_heikin_ashi':
                tableau_reponse[key][0] = (
                    tableau_reponse[key][0],
                    validateur_reponses(f"la bougie {key} est elle sans faille ?",
                                        ['oui', 'non']))
        if input(f"{tableau_reponse}\n\nTout est parfait Entrez non pour interrompre le programme et reprendre de zéro. \n") == 'non':
            raise Exception("Vous avez décidé d'interrompre le programme.")
        print("La base de donnée est bien set up.\nVous pouvez dès maintenant suivre les actions de l'automate en ouvrant le document confidentiel remis par l'espion.")
        fichier.write(str(tableau_reponse))
        automate()



# scribe({'sens_ichimoku': ['vert'], 'position_ichimoku': ['vert'], 'position_sar': ['vert'], 'position_ema': ['vert'], 'sens_macd': ['vert'], 'heikin_ashi': [('vert', 'oui')], '4h_sens_ichimoku': ['vert'], '4h_position_ichimoku': ['vert'], '4h_position_sar': ['vert'], '4h_position_ema': ['vert'], '4h_sens_macd': ['vert'], '4h_heikin_ashi': [('vert', 'oui')]})
print(inbox())
