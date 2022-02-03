# Tapahtumien suodattaminen ja lajittelu

Tämän viikon tehtävänä on harjoitella sanakirjoista ja listoista koostuvan aineiston suodattamista sekä järjestämistä annettujen ehtojen mukaan.

Aineistona käytämme [MyHelsinki Open API](https://open-api.myhelsinki.fi/) -REST-rajapinnan tarjoamia tapahtumatietoja, joissa vastaus koostuu sanakirjasta, jonka sisällä on lista sanakirjamuotoisista tapahtumista, joilla on sanakirjamuotoiset tiedot niiden ajankohdasta, nimistä ja muista tiedoista.

> <em>"So,<br/>
> I heard you guys like dictionaries,<br/>
> So we put a dictionary in a list within another dictionary within another list"</em>
>
> Anonymous Haaga-Helia student, 2021

## Harjoitusten kloonaaminen

Kun olet hyväksynyt tehtävän GitHub classroomissa ja saanut repositoriosta henkilökohtaisen kopion, kloonaa se itsellesi `git clone` -komennolla. Siirry sen jälkeen VS Codeen editoimaan tiedostoja.

Kloonatessasi repositoriota varmista, että Git-osoitteen lopussa on oma GitHub-käyttäjänimesi. Jos käyttäjänimesi puuttuu osoitteesta, kyseessä ei ole henkilökohtainen kopiosi tehtävästä. Luo tässä tapauksessa oma repositorio tämän linkin kautta: [https://classroom.github.com/a/hILfDCgY](https://classroom.github.com/a/hILfDCgY).


## Vastausten lähettäminen

Kun olet saanut toisen tai molemmat tehtävät ratkaistua, lisää tiedostoihin tekemäsi muutokset versionhallintaan `git add` ja `git commit` -komennoilla. Lähetä ratkaisut arvioitavaksi `git push`-komennolla. Git push käynnistää automaattisesti workflow:n, joka testaa kaikki komentosi ja antaa niistä joko hyväksytyn tai hylätyn tuloksen.

Kun GitHub Actions on saanut koodisi suoritettua, näet tuloksen GitHub-repositoriosi [Actions-välilehdellä](../../actions/workflows/classroom.yml). Arvioinnin valmistumiseen menee tyypillisesti noin pari minuuttia.

Klikkaamalla yllä olevan linkin takaa viimeisintä "GitHub Classroom Workflow" -suoritusta, saat tarkemmat tiedot tehtävän arvioinnista. Sivun alaosassa näkyy saamasi pisteet. Klikkaamalla "Autograding"-otsikkoa pääset katsomaan tarkemmin arvioinnissa suoritetut vaiheet ja niiden tulokset.


## Järjesteltävä aineisto

[MyHelsinki Open API](https://open-api.myhelsinki.fi/) on Helsinki Marketing:in tarjoama avoin REST-rajapinta kaupungin tapahtumien, paikkojen ja aktiviteettien tietoihin. 

Rajapinnan dokumentaatio löytyy interaktiivisessa [Swagger](https://swagger.io/)-muodossa osoitteesta [https://open-api.myhelsinki.fi/doc](https://open-api.myhelsinki.fi/doc). Kyseisessä osoitteessa on dokumentoituna esimerkkeineen niin resurssien osoitteet, niiden tukemat parametrit kuin palautettujen JSON-tietueiden rakenne.

Tässä tehtävässä hyödynnetään rajapinnan tarjoamaa tapahtuma-aineistoa osoitteesta [https://open-api.myhelsinki.fi/v1/events/](https://open-api.myhelsinki.fi/v1/events/).

Karkeasti supistettuna yhden tapahtuman pituinen vastaus rajapinnasta voi näyttää esimerkiksi seuraavalta:


```json
{
  "meta": {},
  "data": [
    {
      "id": "",
      "name": {
        "fi": "Suomenkielinen tapahtuman nimi",
        "en": null,
        "sv": null,
        "zh": null
      },
      "source_type": {},
      "info_url": null,
      "modified_at": "",
      "location": {
        "lat": 60,
        "lon": 24,
        "address": {}
      },
      "description": {
        "intro": "",
        "body": "",
        "images": []
      },
      "tags": [],
      "event_dates": {
        "starting_day": "2022-10-24T16:00:00.000Z",
        "ending_day": "2022-10-24T17:00:00.000Z",
        "additional_description": null
      }
    }
  ],
  "tags": {
  }
}
```

Tietorakenteen uloin tyyppi on sanakirja, jonka `"data"`-avaimelta löytyy lista sanakirjoista. 

Kukin sanakirja vastaa yhtä tapahtumaa, ja sisältää useita listoja ja sanakirjoja erinäisten tapahtuman tietojen tallentamiseksi.


## Osa 1: aineiston suodattaminen (2 pistettä)

Kirjoita Python-skriptiin `upcoming_events.py` koodi, joka hakee events-rajapinnasta kaikki tapahtumat. Skriptin tulee tulostaa saamastasi vastauksesta kaikki sellaiset tapahtumat, joiden alkamisaika on **seuraavan 30 vuorokauden aikana**.

Huomaa, että kaikilla rajapinnan palauttamilla tapahtumilla ei välttämättä ole alkamisaikaa. **Tuntemattoman ajankohdan tapahtumat tulee suodattaa pois aineistosta.**

Tulosteessa tulee käydä ilmi tapahtuman alkamisaika (`starting_day`) sekä tapahtuman nimi. Osalle tapahtumista on annettu nimet useilla eri kielillä, kun taas joiltain nimiä puuttuu. Skriptisi tulee ensisijaisesti käyttää suomenkielistä nimeä `'fi'`. Suomenkielisen nimen puuttuessa käytä tilalla kieliversioita `'en'`, `'sv'` tai `'zh'` tässä järjestyksessä.

Voit muodostaa Pythonissa aikaoliot sekä nykyhetkelle että 30 päivän päähän esimerkiksi seuraavasti:

```python
from datetime import datetime, timedelta

alku = datetime.utcnow()
loppu = alku + timedelta(days=30)
```

Yllä olevassa koodissa [utcnow-funktio](https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow) muodostaa ajanhetken UTC-aikavyöhykkeessä, joka vastaa myös tapahtuma-aineistossa käytettävää aikavyöhykettä. 

Voit muuttaa vastaavasti edellisessä esimerkissä esiintyvät `min`- ja `max`-oliot merkkijonoiksi `isoformat`-metodilla: 

```
alku_str = alku.isoformat()
loppu_str = loppu.isoformat()
```

Kun vertailtavat ajankohdat ovat merkkijonomuodossa, niitä voidaan vertailla tapahtumien ajankohtiin Pythonin `<`- ja `>`-operaattoreilla. 

Ohjelmasi tulee tehdä tarvittavat vertailut ja tulostaa kaikkien sellaisten tapahtumien nimet, joiden alkamisaika on seuraavien 30 vuorokauden aikana.

Skriptisi ei saa pyytää käyttäjältä lainkaan syötteitä, ja sen tulee olla normaalisti suoritettavissa komennolla `python3 upcoming_events.py`, olettaen että järjestelmässä löytyy `python3`-komento.


## Osa 2: tapahtumien lajittelu (3 pistettä)

Tässä osassa sinun tulee suodattamisen lisäksi **järjestää** tapahtumat niiden alkamisajan mukaan käyttäen **itse toteuttamaasi lajittelualgoritmia**.

> *"Some examples where you can find direct application of sorting techniques include: Sorting by price, popularity etc in e-commerce websites"*
>
> [The Ohio State University. 7 algorithms and data structures every programmer must know](https://u.osu.edu/cstutorials/2016/11/21/7-algorithms-and-data-structures-every-programmer-must-know/)

Koodisi tulee järjestellä kokonaisia tapahtumatietueita, eli älä poimi aineistosta järjesteltäväksi esimerkiksi pelkkiä nimiä ja alkamisaikoja.

🚨 **Tämän harjoituksen tavoitteena on opetella itse toteuttamaan jokin tunnettu järjestämisalgoritmi, joten Pythonin valmiin lajittelualgoritmin käyttämistä ei arvioida.** 🚨

Voit valita toteutettavan järjestämisalgoritmin esimerkiksi seuraavista:

**Lisäyslajittelu eli Insertion Sort**

[https://en.wikipedia.org/wiki/Insertion_sort](https://en.wikipedia.org/wiki/Insertion_sort)

<a title="Simpsons contributor / CC BY-SA (https://creativecommons.org/licenses/by-sa/3.0)" href="https://commons.wikimedia.org/wiki/File:Insertion_sort.gif"><img height="256" alt="Insertion sort" src="https://upload.wikimedia.org/wikipedia/commons/4/42/Insertion_sort.gif"></a>

Kuva: By Simpsons contributor - Own work, CC BY-SA 3.0, [https://commons.wikimedia.org/w/index.php?curid=17512147](https://commons.wikimedia.org/w/index.php?curid=17512147)

**Lomituslajittelu eli Merge Sort**

[https://en.wikipedia.org/wiki/Merge_sort](https://en.wikipedia.org/wiki/Merge_sort)

<a title="Swfung8 / CC BY-SA (https://creativecommons.org/licenses/by-sa/3.0)" href="https://commons.wikimedia.org/wiki/File:Merge-sort-example-300px.gif"><img width="256" alt="Merge-sort-example-300px" src="https://upload.wikimedia.org/wikipedia/commons/c/cc/Merge-sort-example-300px.gif" style="border solid silver 1px;"></a>

Kuva: By Swfung8 - Own work, CC BY-SA 3.0, [https://commons.wikimedia.org/w/index.php?curid=14961648](https://commons.wikimedia.org/w/index.php?curid=14961648)

**Kuplalajittelu eli Bubble Sort**

[https://en.wikipedia.org/wiki/Bubble_sort](https://en.wikipedia.org/wiki/Bubble_sort)

<a href="https://commons.wikimedia.org/wiki/File:Bubble-sort-example-300px.gif#/media/File:Bubble-sort-example-300px.gif" title="By Swfung8 - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=14953478"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c8/Bubble-sort-example-300px.gif" alt="Bubble-sort-example-300px.gif" width="256" style="border solid silver 1px;"></a>

Kuva: By Swfung8 - Own work, CC BY-SA 3.0, [https://commons.wikimedia.org/w/index.php?curid=14953478](https://commons.wikimedia.org/w/index.php?curid=14953478)

**Pikalajittelu eli Quicksort**

[https://en.wikipedia.org/wiki/Quicksort](https://en.wikipedia.org/wiki/Quicksort)
	
<a href="https://commons.wikimedia.org/wiki/File:Sorting_quicksort_anim.gif#/media/File:Sorting_quicksort_anim.gif" title="By en:User:RolandH, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1965827"><img src="https://upload.wikimedia.org/wikipedia/commons/6/6a/Sorting_quicksort_anim.gif" alt="Sorting quicksort anim.gif" width="256" style="border solid silver 1px;"></a>

Kuva: By en:User:RolandH, CC BY-SA 3.0, [https://commons.wikimedia.org/w/index.php?curid=1965827](https://commons.wikimedia.org/w/index.php?curid=1965827)


### Algoritmin valintaperusteet

Voit valita itsellesi mieluisen algoritmin esimerkiksi tutustumalla ensin niiden tehokkuuteen, tai valita sen, joka vaikuttaa toteutukseltaan sopivan yksinkertaiselta. Muista myös, että voit kysyä Teamsissa neuvoa mihin vain tehtävässä kohtaamaasi haasteeseen liittyen. Todennäköisesti samojen haasteiden parissa kamppailee myös moni muu kurssilainen.

Kun aineisto on järjestetty, tulosta tapahtumien nimet ja ajankohdat kronologisessa järjestyksessä. Tulosteen muodolla ei ole tehtävän arvioinnin kannalta isoa merkitystä, kunhan tulosteesta on todennettavissa ohjelman oikea toiminta.

Arvioi lopuksi tehtävää ratkaistessasi järjestämiseen kuluvaa aikaa. Miten esimerkiksi aineiston koon kaksinkertaistaminen vaikuttaisi ohjelmasi suoritusaikaan? Kirjoita yhden virkkeen pituinen arvio suorituskyvystä koodin kommentteihin.

**Huom!** Oikeassa ohjelmistoprojektissa käyttäisit Pythonin valmiita järjestämisfunktioita, joita esitellään esimerkiksi osoitteessa [https://docs.python.org/3/howto/sorting.html](https://docs.python.org/3/howto/sorting.html).


## Ohjelman esimerkkituloste

Halutessasi voit tulostaa tapahtumat skriptissäsi esimerkiksi seuraavaalla tavalla:

```
2022-01-14
 11:00 Bingo
 21:00 Maiju Hukkanen: Päiviä, jotka rytmittyvät päiväunien mukaan

2022-01-15
 08:00 Työpaja lapsiperheille
 09:00 Tarja Pitkänen-Walter: Maalauksellisia mietteitä
 10:00 Greta Hällfors-Sipilä & Sulho Sipilä -näyttelyn opastus ruotsiksi
 12:00 Taide ja aktivismi - keskustelu Palestiinasta
 12:00 Vain muutos on pysyvää -lukupiiri
 12:00 Katharina Grosse -näyttelyn opastus suomeksi
 13:00 Elannon Näyttämön 100-vuotisjuhlanäytelmä: Elämänmeno
 17:00 Det svarta fåret

2022-01-16
 17:00 Open Stage With Bryn And Ben
 22:01 Sibafest – Recovery Tour 2022

2022-01-17
 07:00 Valokuvanäyttely, kuvia Etiopiasta
 07:00 Kannelmäen kirjaston ekaluokkalaisstartti
 07:30 Leikkipuisto Ruoholahden ja Perhetalo Betanian yhteinen Perheaamu
 08:00 Luetaan yhdessä
 08:00 Lorurasti
 08:00 Vauva-aamu
 08:00 Vipinävarpaat: winter edition!
 08:00 Vauva-aamu
 08:00 Pihapuuhat
 08:30 Perheaamu
 09:00 Totta vai tarua?
 09:00 Runoryhmä
 10:30 Digirasti: Digitaitokurssi 2 (perusteiden kurssi) -TÄYNNÄ!
 12:00 Kielikahvila e-Ekstra Skypessä
...
```

Tapahtumien tulostaminen päivittäin ryhmiteltynä ei välttämättä vaadi erillistä tietorakennetta, vaan yksinkertainen tapahtumalista riittää. Vertaa vain aina tapahtuman päivämäärää edellisen päivämäärään, ja mikäli se on eri, tulosta uusi päivämäärän ennen tapahtuman kellonajan ja nimen tulostamista.


## Testit (valinnainen)

Ohjelmasi toiminta testataan GitHub classroomissa `.test`-piilohakemistossa sijaitsevilla testeillä. Testit eivät suorita ohjelmaasi, vaan ne tarkastavat ohjelmasi tulosteen tiedostosta nimeltä `student_output.txt`.

Mikäli haluat kokeilla testejä paikallisesti, ohjaa ohjelmasi tuloste ensin tiedostoon `student_output.txt` ja sen jälkeen aja Pytest-testit seuraavasti:

```
# Ohjataan tuloste tiedostoon
$ python3 upcoming_events.py > student_output.txt

# Suoritetaan testit
$ python3 -m pytest .test --verbose

======================== test session starts ========================
collected 3 items

.test/test_filtering.py::test_output_contains_all_events_in_range 
PASSED                                      [ 33%]

.test/test_filtering.py::test_output_does_not_contain_events_beyond_30_days 
PASSED                                      [ 66%]

.test/test_sorting.py::test_events_are_in_chronological_order 
PASSED                                      [100%]

======================== 3 passed in 5.32s ========================
```

Testien suorittaminen edellyttää `pytest`-työkalun asennusta, jonka voit tarvittaessa asentaa komennolla `python3 -m pip install pytest`.

----

# Lisenssit ja tekijänoikeudet

Tämän oppimateriaalin on kehittänyt Teemu Havulinna ja se on lisensoitu [Creative Commons BY-NC-SA -lisenssillä](https://creativecommons.org/licenses/by-nc-sa/4.0/).


## MyHelsinki Open API

> *"Note that all of the information provided over the API is open data with the exception of image files. When using images, please refer to the license terms included with each image.*"
> 
> MyHelsinki Open API. https://open-api.myhelsinki.fi/

MyHelsinki Open API:n aineisto on lisensoitu [Creative Commons BY 4.0](https://open-api.myhelsinki.fi/terms)-lisenssillä. Voit lukea tarkemmat käyttöehdot ositteesta https://open-api.myhelsinki.fi/terms.
