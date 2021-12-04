import time


def nombres_presences_et_messages_doubles(messages, indicateur):
    liste_de_doubles = []
    for message in messages:
        if message['subject'] == indicateur:
            liste_de_doubles.append(message)
    return liste_de_doubles


def dernier_message(listes_doubles):
    le_dernier_message = listes_doubles[0]
    for message in listes_doubles[1:]:
        if temps_1_plus_grand(message['date'], le_dernier_message['date']):
            le_dernier_message = message
    return le_dernier_message


def temps_1_plus_grand(temps_1, temps_2):
    jour_1 = int(temps_1[5] + temps_1[6])
    jour_2 = int(temps_2[5] + temps_2[6])
    if jour_1 != jour_2:
        return jour_1 > jour_2
    heure_1 = int(temps_1[14] + temps_1[15])
    heure_2 = int(temps_2[14] + temps_2[15])
    if heure_1 != heure_2:
        return heure_1 > heure_2
    minute_1 = int(temps_1[17] + temps_1[18])
    minute_2 = int(temps_2[17] + temps_2[18])
    if minute_1 != minute_2:
        return minute_1 > minute_2
    seconde_1 = int(temps_1[20] + temps_1[21])
    seconde_2 = int(temps_2[20] + temps_2[21])
    if seconde_1 != seconde_2:
        return seconde_1 > seconde_2
    raise Exception("Messages du même sujet envoyés simultanément !")


def chercheur_message(messages, indicateur):
    indicateur = "Alerte :" + indicateur
    liste_de_doubles = nombres_presences_et_messages_doubles(messages, indicateur)
    if len(liste_de_doubles) == 1:
        return liste_de_doubles[0]
    if len(liste_de_doubles) == 0:
        return
    return dernier_message(liste_de_doubles)


def sens_ichimoku(messages):
    indicateur = 'sens_nuage_ichimoku'
    message = chercheur_message(messages, indicateur)
    return message



def position_ichimoku(messages):
    indicateur = 'position_ichimoku'
    message = chercheur_message(messages, indicateur)
    return 'dessus', 'dessous', 'milieu', '4dessus', '4dessous', '4milieu'


def position_sar(messages):
    indicateur = 'position_sar'
    message = chercheur_message(messages, indicateur)
    pass


def position_ema(messages):
    indicateur = 'position_ema'
    message = chercheur_message(messages, indicateur)
    pass


def sens_macd(messages):
    indicateur = 'sens_macd'
    message = chercheur_message(messages, indicateur)
    pass


def heikin_ashi(messages):
    indicateur_rouge = 'heikin_rouge'
    indicateur_vert = 'heikin_vert'
    message_rouge = chercheur_message(messages, indicateur_rouge)
    message_vert = chercheur_message(messages, indicateur_vert)
    pass


def quatre_heure_sens_ichimoku(messages):
    indicateur = '4H_sens_nuage_ichimoku'
    message = chercheur_message(messages, indicateur)
    pass


def quatre_heure_position_ichimoku(messages):
    indicateur = '4H_position_ichimoku'
    message = chercheur_message(messages, indicateur)
    return 'dessus', 'dessous', 'milieu', '4dessus', '4dessous', '4milieu'


def quatre_heure_position_sar(messages):
    indicateur = '4H_position_sar'
    message = chercheur_message(messages, indicateur)
    pass


def quatre_heure_position_ema(messages):
    indicateur = '4H_position_ema'
    message = chercheur_message(messages, indicateur)
    pass


def quatre_heure_sens_macd(messages):
    indicateur = '4H_sens_macd'
    message = chercheur_message(messages, indicateur)
    pass


def quatre_heure_heikin_ashi(messages):
    indicateur_rouge = '4H_heikin_ashi_rouge'
    indicateur_vert = '4H_heikin_ashi_vert'
    message_rouge = chercheur_message(messages, indicateur_rouge)
    pass
