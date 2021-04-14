# Инвестпроект представляет собой интернет-магазин по продаже компьютерных аксессуаров на площадке "Ozon"
# Первоначальные затарты составляют 200 000 руб.
# Срок реализации 4 года
# Планируемая сумма поступлений за период 110 000 руб
# Затраты за период 40 000 руб.
# Cтавка дисконтирования 1.4%

import itertools
import functools

try:
    # Первоначальные данные
    n = 4
    pz = 200000
    rd = 110000
    rz = 40000
    r = 0.014

    # Другие необходимые переменные
    sumNPV = 0
    L = [[1], [2], [3], [4]]
    mList = []
    NPVmas2m = []
    sumItog = {}
    NPVm1 = 0
    DPP = 0
    minNPV = 0
    aList = []


    # Расчет показателя NPV
    # --------------------------------------------------------------------------
    def findNPV(rd, rz, r, pz, L):
        NVP = list(itertools.starmap(lambda x: (rd - rz) / ((1 + r) ** x), L))
        NVP.insert(0, -pz)
        return NVP


    def sumNPV(rd, rz, r, pz, L):
        sNPVlist = findNPV(rd, rz, r, pz, L)
        sumNPV = functools.reduce(lambda x, y: x + y, sNPVlist)
        return sumNPV


    NPV1 = sumNPV(rd, rz, r, pz, L)
    print(f"NPV проекта: {round(NPV1, 2)}")

    # Расчет показателя DPP
    # --------------------------------------------------------------------------
    NVPmas2 = list(itertools.accumulate(findNPV(rd, rz, r, pz, L)))

    # Находим номер последнего отрицательного периода
    for i in NVPmas2:
        if i < 0:
            mList.append(i)
    m = len(mList)

    # Находим NPVm+1 по массиву 1
    for i in range(len(findNPV(rd, rz, r, pz, L))):
        if i == m + 1:
            NPVm1 = round(findNPV(rd, rz, r, pz, L)[i], 2)

    # Находим NPV за m периодов по массиву 2, т.е. тот самый последний отрицательный накопленный NPV
    for i in range(len(findNPV(rd, rz, r, pz, L))):
        if i <= m - 1:
            NPVmas2m.append(findNPV(rd, rz, r, pz, L)[i])
            if i == m - 1:
                NPVmas2mitog = NPVmas2m[i]

    NPVmas2m = list(itertools.accumulate(NPVmas2m))
    NPVmas2mitog = NPVmas2m[-1]

    try:
        DPP = round((m - 1) + (abs(NPVmas2mitog) / NPVm1))
    except (ZeroDivisionError):
        print("Неудается вычислить срок окупаемости!")

    print(f"DPP:{DPP} года")


    # Внутренняя норма доходности IRR
    # --------------------------------------------------------------------------
    def countdown():
        i = 0
        while i < 100:
            yield i
            i += 0.001


    for i in countdown():
        aList.append(i)

    for r in aList:
        NPV = sumNPV(rd, rz, r, pz, L)
        if NPV < 0:
            NPV = abs(NPV)
            sumItog[r] = NPV
        else:
            sumItog[r] = NPV

    minNPV = min(sumItog.values())
    r = list(sumItog.keys())[list(sumItog.values()).index(minNPV)]

    print(f"Внутренняя норма доходности IRR: NPV будет по модулю наиболее близок к нулю со значением {round(minNPV, 2)}"
          f" и ставка при этом будет {round(r * 100, 2)} %")

    if (NPV1>0):
        print("Инвестпроект эффективен")
    else:
        print("Инвестпроект не эффективен")

except(SyntaxError, NameError, ZeroDivisionError):
    print("Неверные значения!")
