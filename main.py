import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# wczytanie pliku
wb = pd.read_excel('TRANSACTION_DATA_SAMPLE.XLSX')
woj = pd.read_excel('VOIVODESHIP.xlsx')

#################################################################
# ZADANIE 1
# unikatowi klienci u partnerów
wb_sort = wb.groupby(['PARTNER_ID', 'CUSTOMER_ID']).count().reset_index()
partner = 'partner'
unikat = {}
wszystkie_trans = {}
for i in range(wb_sort.shape[0]):
    wartosc = wb_sort.iloc[i]['PARTNER_ID']
    trans = wb_sort.iloc[i]['TRANSACTION_ID']
    nr = str(wartosc)

    variable_name = partner + "_" + nr

    if not variable_name in unikat.keys():
        wszystkie_trans[variable_name] = 0

    wszystkie_trans[variable_name] += 1
    if trans == 1:
        nr = str(wartosc)
        variable_name = partner + "_" + nr

        if not variable_name in unikat.keys():
            unikat[variable_name] = 0

        unikat[variable_name] += 1
print(unikat)
print(wszystkie_trans)
# ODPOWIEDŹ: Dla poszczególnych partnerów liczba unikalnych klientów wynosi odpowiedni {'partner_1': 534, 'partner_2': 1239, 'partner_3': 1602, 'partner_4': 4789}
# wzięty został pod uwagę klient który tylko raz zrobił zakupy u konkretnego partnera

###########################################################
# ZADANIE 2
# punkty wgl daty

x = datetime.datetime(2022, 5, 1)
y = datetime.datetime(2022, 5, 15)
suma_pkt = 0

for i in range(wb.shape[0]):
    data = wb.iloc[i]['TRANSACTION_DATE']
    punkty = wb.iloc[i]['POINTS']
    if data.date() >= x.date() and data.date() <= y.date():
        suma_pkt += punkty

print("Suma punktów w podanym okresie", suma_pkt)  # Odpowiedz: 80466

###########################################
# ZADANIE 3
# pierwsza transakcja

wb_daty = wb.groupby('SHOP_ID').agg({'TRANSACTION_DATE': ['min']})
print(wb_daty)  # Printujemy tabelę odpowiedzi

################################################
# ZADANIE 4
# transakcje kwoty
przedzial_1 = 0
przedzial_2 = 0
przedzial_3 = 0
for i in range(wb.shape[0]):
    kwota = wb.iloc[i]['TURNOVER']
    punkty = wb.iloc[i]['POINTS']
    if kwota <= 99.99:
        przedzial_1 += 1
    elif kwota >= 100.00 and kwota <= 199.99:
        przedzial_2 += 1
    elif kwota >= 200:
        przedzial_3 += 1
print('poniżej 99,99zl: ', przedzial_1)
print('pomiędzy 100-199,99zl: ', przedzial_2)
print('powyżej 200zl: ', przedzial_3)
# Odpowiedz:
# poniżej 99,99zl:  15396
# pomiędzy 100-199,99zl:  2612
# powyżej 200zl:  5024

###############################################################
# ZADANIE 5
# zmiana ID partnera
wb_edit = wb
for i in range(wb_edit.shape[0]):
    partner_id = wb_edit.iloc[i]['PARTNER_ID']
    if partner_id == 2:
        wb_edit.loc[i, 'PARTNER_ID'] = 4  # zapisane w zmiennej wb_edit

############################################################
# ZADANIE 6
# łączenie zbiorów

df = pd.merge(wb_edit, woj, on='SHOP_ID', how='outer')
df['VOIVODESHIP'] = df['VOIVODESHIP'].str.upper()
df.to_excel('C:/Users/majak/OneDrive/Pulpit/excel_edytowany.xlsx',
            sheet_name='DANE')  # zapisanie połączonych exceli razem ze zmianą nr partnera

#########################################################################


# CZĘŚĆ WŁASNA DO ZAPROPONOWANEJ ANALIZY

Partner = list(unikat.keys())
unikalni_klienci = list(unikat.values())
wszyscy_klienci = list(wszystkie_trans.values())

index = np.arange(len(Partner))
width = 0.30

plt.bar(index, unikalni_klienci, width, color='green', label="Unikatowi klienci")
plt.bar(index + width, wszyscy_klienci, width, color='red', label="Wszyscy klienci")
plt.title('Stosunek klientów u poszczególnych partnerów')
plt.ylabel('Klienci')
plt.xlabel('Partnerzy')
plt.xticks(index + width / 2, Partner)
plt.legend(loc="upper left")
plt.show()


# wykres kołowy
def wykres_kolowy(dane, col_dane, col_pro, tytul, argument='sum' or 'count'):
    if argument == 'sum':
        suma_pkt_1 = dane.groupby(col_dane)[col_pro].sum()
    elif argument == 'count':
        suma_pkt_1 = dane.groupby(col_dane)[col_pro].count()

    suma_pkt_1.plot.pie(autopct='%1.1f%%', startangle=140)

    plt.title(tytul)
    plt.show()


wykres_kolowy(wb, 'PARTNER_ID', 'POINTS', 'Procentowa suma punktów dla każdego partnera', 'sum')


# wykres_kolowy(df, 'VOIVODESHIP', 'SHOP_ID', 'Rozkład procentowy sklepów w województwach', 'count')
# wykres_kolowy(df, 'VOIVODESHIP', 'TRANSACTION_ID', 'Rozkład procentowy transakcji w województwach', 'count')
# wykresy wymagają dostosowania graficzngo dla ułatwienia czytelności ale pozwoliły wyciągnąć wnioski które można zawrzeć w analizie

def wykres_od_czasu(dane, col, tytul):
    wb_copy = dane.copy()
    wb_copy['TRANSACTION_DATE'] = pd.to_datetime(wb_copy['TRANSACTION_DATE'])
    wb_copy['TRANSACTION_DATE'] = wb_copy['TRANSACTION_DATE'].dt.strftime('%Y-%m')
    kalendarz1 = wb_copy[(wb_copy['PARTNER_ID'] == 1)].groupby(
        ['PARTNER_ID', 'TRANSACTION_DATE'])[col].sum().reset_index()
    kalendarz2 = wb_copy[(wb_copy['PARTNER_ID'] == 3)].groupby(
        ['PARTNER_ID', 'TRANSACTION_DATE'])[col].sum().reset_index()
    kalendarz3 = wb_copy[(wb_copy['PARTNER_ID'] == 4)].groupby(
        ['PARTNER_ID', 'TRANSACTION_DATE'])[col].sum().reset_index()

    plt.plot(kalendarz1['TRANSACTION_DATE'].tolist(), kalendarz1[col].tolist(), label='partner1')
    plt.plot(kalendarz2['TRANSACTION_DATE'].tolist(), kalendarz2[col].tolist(), label='partner3')
    plt.plot(kalendarz3['TRANSACTION_DATE'].tolist(), kalendarz3[col].tolist(), label='partner4')
    plt.title(tytul)
    plt.legend()
    plt.show()


wykres_od_czasu(wb, 'POINTS', 'Wykres sumy punktów w każdym miesiącu u poszczególnych partnerów')
wykres_od_czasu(wb, 'TURNOVER', 'Wykres sumy kwoty w każdym miesiącu u poszczególnych partnerów')
# możemy w kilka minut wykorzystać funkcję do stworzenia wykresu punktów w zależności od województwa na przestrzeni czasu
# czy ilości transakcji na przestrzeni czasu czy innych potrzebnych wykresów zależnych od czasu
