# 🎓 Wilma Kurssivalitsin

> Automaattinen kurssienvalintaohjelma Wilmaan — ei koodausosaamista tarvita!

---

## ⚡ Pikakäynnistys — lataa valmis EXE

Jos joku on jo paketoinut ohjelman `.exe`-tiedostoksi, tarvitset vain:

1. **Lataa `WilmaKurssivalitsin.exe`** Releases-osiosta (oikealla →)
2. **Tuplaklikkaa** tiedostoa — ohjelma käynnistyy suoraan
3. Täytä tietosi ja paina **▶ KÄYNNISTÄ VALINTA**

> ⚠️ **Google Chrome täytyy olla asennettuna koneellasi.** ChromeDriver latautuu automaattisesti ensimmäisellä käynnistyskerralla.

---

## ✨ Mitä tämä tekee?

Tämä ohjelma avaa Wilman automaattisesti, kirjautuu sisään puolestasi ja valitsee haluamasi kurssit kolmelta periodilta — muutamassa sekunnissa.

---


## 🖥️ Ohjelman käyttäminen

### Käynnistys

Tuplaklikkaa `WilmaKurssivalitsin.exe`. Ohjelma näyttää tältä:

```
┌──────────────────────────────────────────────────────┐
│  WILMA  kurssivalitsin                               │
├──────────────────────────────────────────────────────┤
│  🔐 Kirjautumistiedot    📅 Valittavat kurssit       │
│                                                      │
│  Sähköposti              1. Periodi                  │
│  [sinun@email.fi      ]  [BIO1.i, MAA05.1         ] │
│                                                      │
│  Salasana                2. Periodi                  │
│  [●●●●●●●●●●●●●●●●●●  ]  [FI02.1, ENA03.c        ] │
│                                                      │
│  Wilma-URL               3. Periodi                  │
│  [helsinki.inschool...  ] [MAT04.2, YH01.1         ] │
│                                                      │
│  [ ▶ KÄYNNISTÄ VALINTA ]                            │
│  [ 💾 Tallenna asetukset ]                           │
└──────────────────────────────────────────────────────┘
```

---

### Täytä tietosi

| Kenttä | Mitä kirjoitat |
|--------|---------------|
| **Sähköposti** | Wilma-tunnuksesi sähköpostiosoite |
| **Salasana** | Wilma-salasanasi |
| **Wilma-URL** | Liitä tähän oman kurssitarjottimesi linkki |

---

### Kurssikoodit

Kirjoita haluamasi kurssikoodit **täsmälleen niin kuin ne näkyvät Wilmassa.**

Voit erotella kurssit pilkulla tai laittaa jokaisen omalle rivilleen:

```
BIO1.i, MAA05.1, ENA01.+ENA02.g
```

tai

```
BIO1.i
MAA05.1
ENA01.+ENA02.g
```

> 💡 Kurssikoodit löydät Wilman kurssivalintasivulta — ne ovat pieniä tekstejä kurssinappeissa

---

### Käynnistä!

1. Klikkaa **💾 Tallenna asetukset** — tiedot muistetaan seuraavaa kertaa varten
2. Klikkaa **▶ KÄYNNISTÄ VALINTA**
3. Chrome avautuu automaattisesti — **älä sulje sitä!**
4. Seuraa lokin viestejä ohjelman alareunassa:
   - ✓ = kurssi valittu onnistuneesti
   - ✗ = kurssia ei löydetty (tarkista kurssikoodi)
   - ✅ Valmis! = kaikki tehty

---

## ❓ Usein kysytyt kysymykset

**Q: Windows varoittaa "Windows suojasi tietokoneesi"**
> Klikkaa **Lisätietoja** → **Suorita joka tapauksessa**. Tämä johtuu siitä että ohjelma ei ole allekirjoitettu — se on turvallista.

**Q: Ensimmäinen käynnistys on hidas**
> Ohjelma lataa automaattisesti ChromeDriverin — tämä tapahtuu vain kerran.

**Q: Tulee virhe "Chrome not found" tai "cannot find Chrome"**
> Asenna Google Chrome: https://www.google.com/chrome/

**Q: Kurssia ei löydy (✗ merkki)**
> Tarkista että kurssikoodi on kirjoitettu täsmälleen oikein — myös pisteet ja isot/pienet kirjaimet merkitsevät!

**Q: Ohjelma kirjautuu mutta mitään ei tapahdu**
> Koulusi Wilma-sivun rakenne saattaa erota oletuksesta. Lisää tästä Issues-osioon niin korjataan.

**Q: Halusin valita väärät kurssit**
> Mene Wilmaan normaalisti selaimella ja peru valinnat manuaalisesti.

---

## 🔒 Turvallisuus

- Salasanasi tallennetaan **vain omalle koneellesi** tiedostoon `wilma_settings.json`
- Tietoja ei lähetetä mihinkään — ohjelma kommunikoi suoraan Wilman kanssa
- **Älä jaa** `wilma_settings.json`-tiedostoa kenellekään

---

## 🐛 Ongelma?

Avaa uusi **Issue** tähän GitHub-repoon ja kuvaile mitä tapahtui. Liitä mukaan lokin teksti ohjelman alareunasta.

---

*Tehty helpottamaan kurssienvalintaa 🎒*




## 🛠️ EXE-tiedoston rakentaminen itse

Haluatko paketoida ohjelman itse tai jakaa sen kavereille? Seuraa näitä ohjeita.

### Mitä tarvitset

- Windows-tietokone
- Google Chrome asennettuna
- Python (ilmainen) — **vain rakentamiseen**

---

### Vaihe 1 — Lataa tiedostot

Lataa nämä kaksi tiedostoa **samaan kansioon** (esim. `C:\Wilma\`):

- `wilma_valitsin.py`
- `build_exe.bat`

---

### Vaihe 2 — Asenna Python

1. Mene osoitteeseen: https://www.python.org/downloads/
2. Klikkaa isoa **"Download Python"** -nappia
3. Avaa ladattu tiedosto
4. ⚠️ **TÄRKEÄÄ:** Laita ruksi kohtaan **"Add Python to PATH"**
5. Klikkaa **Install Now** ja odota

---

### Vaihe 3 — Rakenna EXE

1. Mene kansioon johon tallensit tiedostot
2. **Tuplaklikkaa `build_exe.bat`**
3. Musta ikkuna aukeaa ja teksti juoksee — odota rauhassa (voi kestää 1–3 min)
4. Kun se sulkeutuu tai lukee "Valmis!", löydät ohjelman kansiosta `dist\`

```
📁 C:\Wilma\
   ├── wilma_valitsin.py
   ├── build_exe.bat
   └── 📁 dist\
       └── ✅ WilmaKurssivalitsin.exe   ← tämä on valmis ohjelma!
```

5. Siirrä `WilmaKurssivalitsin.exe` haluamaasi paikkaan — voit jakaa sen kavereille!

---

