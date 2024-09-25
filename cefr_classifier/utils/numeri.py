def scala_numero(x, i_min, i_max, o_min, o_max):
    """
    Scala un numero (Float) che rappresenta una proporzione su una differente scala (ad esempio 255, da usare in RGB)
    esempio: 0.5 può diventare 128 che è la metà di 255
    esempio: 0.5 può diventare 200 se desidero partire da un valore diverso da 0/255, perché con 0 non si legge niente

    x è il numero da scalare
    i_min, i_max valori minimo e massimo nella scala iniziale (Input)
    o_min, o_max valori minimo e massimo nella scala finale (Output)
    220
    """
    if i_max - i_min == 0:
        return o_min
        # raise Exception("Divisione fratto zero, i_max = " + str(i_max))
    porzione = (x - i_min) / (i_max - i_min)
    porzione_o = porzione * (o_max - o_min)
    return o_min + porzione_o


def dec_to_hex(dec, invertito=True):
    # in: numero normalmente 0-255, può anche essere float
    # out: stringa, max "ff"
    if invertito:
        reale = 256 - dec
    else:
        reale = dec
    return hex(int(reale)).split("x")[1]


def due_decimali(numero_float):
    numero_float = float(numero_float)
    return "{:.2f}".format(numero_float)