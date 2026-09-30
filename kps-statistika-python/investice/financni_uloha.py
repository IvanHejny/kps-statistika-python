import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 1. Vstupní data ze zadání (2004 - 2025)
roky = list(range(2004, 2026))
penzijni_fond = [3.50, 3.50, 3.00, 2.50, 0.50, 1.50, 1.50, 1.50, 1.50, 1.44, 1.35, 1.16, 0.66, 0.49, 0.51, 0.60, 0.35,
                 0.43, 0.00, 1.13, 1.80, 1.50]
globalni_fond = [14.72, 9.49, 20.07, 9.04, -40.71, 29.99, 11.76, -5.54, 15.83, 26.68, 4.94, -0.87, 7.51, 22.40, -8.71,
                 27.67, 15.90, 21.82, -18.14, 23.79, 18.67, 21.09]
inflace = [2.80, 1.90, 2.50, 2.80, 6.30, 1.00, 1.50, 1.90, 3.30, 1.40, 0.40, 0.30, 0.70, 2.50, 2.10, 2.80, 3.20, 3.80,
           15.10, 10.70, 2.40, 2.50]

# 2. Počáteční stavy investic na začátku roku 2004
vklad = 100000
hodnoty_sporici = [vklad]
hodnoty_penzijni = [130000]  # Vklad 100 000 + bonus 30 000
hodnoty_gf_drahy = [vklad * (1 - 0.03)]  # Po stržení vstupního poplatku 3 %
hodnoty_gf_levny = [vklad * (1 - 0.03)]  # Do roku 2008 vývoj stejný jako drahý

kumulovana_inflace = [1.0]

# 3. Výpočet vývoje rok po roce
for i in range(len(roky)):
    # Spořicí účet (fixně 1,5 % ročně)
    hodnoty_sporici.append(hodnoty_sporici[-1] * 1.015)

    # Penzijní připojištění
    zhodnoceni_pf = 1 + (penzijni_fond[i] / 100)
    hodnoty_penzijni.append(hodnoty_penzijni[-1] * zhodnoceni_pf)

    # Globální fond (hrubý výnos trhu)
    zhodnoceni_gf = 1 + (globalni_fond[i] / 100)

    # Globální fond - Drahá varianta (TER 2,0 % po celou dobu)
    nova_hodnota_drahy = hodnoty_gf_drahy[-1] * zhodnoceni_gf * (1 - 0.02)
    hodnoty_gf_drahy.append(nova_hodnota_drahy)

    # Globální fond - Levná varianta (TER 2,0 % do 2008, od 2009 TER 0,2 %)
    ter_levny = 0.02 if roky[i] < 2009 else 0.002
    nova_hodnota_levny = hodnoty_gf_levny[-1] * zhodnoceni_gf * (1 - ter_levny)
    hodnoty_gf_levny.append(nova_hodnota_levny)

    # Výpočet kumulované inflace (násobek cenové hladiny vůči 2004)
    kumulovana_inflace.append(kumulovana_inflace[-1] * (1 + inflace[i] / 100))

# 4. Vykreslení grafu
roky_osa = ["Zač. 2004"] + [str(r) for r in roky]  # Popisky osy X

plt.figure(figsize=(12, 7))

plt.plot(roky_osa, hodnoty_gf_levny, label='Globální fond (přechod na TER 0,2 %)', color='green', linewidth=2.5)
plt.plot(roky_osa, hodnoty_gf_drahy, label='Globální fond (TER 2,0 %)', color='orange', linewidth=2, linestyle='--')
plt.plot(roky_osa, hodnoty_penzijni, label='Penzijní připojištění (s bonusem)', color='blue', linewidth=2)
plt.plot(roky_osa, hodnoty_sporici, label='Spořicí účet (1,5 %)', color='red', linewidth=2)

# Formátování grafu
plt.title('Vývoj hodnoty investice (2004–2025)', fontsize=16)
plt.ylabel('Hodnota investice (Kč)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=11, loc='upper left')

# Úprava os
plt.xticks(rotation=45)
ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',').replace(',', ' ') + ' Kč'))

# Změna zde: Místo zobrazení na obrazovku uložíme graf jako vektorové PDF
plt.savefig('vyvoj_investice.pdf', format='pdf', bbox_inches='tight')
plt.close() # Uzavře instanci grafu a uvolní paměť

# Výpis konečných hodnot pro kontrolu řešení
print(f"Kumulovaná inflace: {(kumulovana_inflace[-1] - 1) * 100:.1f} %")
print(f"Hodnota spořicího účtu v roce 2025: {hodnoty_sporici[-1]:,.2f} Kč")
print(f"Hodnota penzijního připojištění v roce 2025: {hodnoty_penzijni[-1]:,.2f} Kč")
print(f"Hodnota globálního fondu (drahý) v roce 2025: {hodnoty_gf_drahy[-1]:,.2f} Kč")
print(f"Hodnota globálního fondu (levný) v roce 2025: {hodnoty_gf_levny[-1]:,.2f} Kč")
