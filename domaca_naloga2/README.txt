main.py
CRUD operacije izvedene z API klici. 

GET klici za:
-pridobivanje vseh avtomobilov
-pridobivanje določene zname avtomobilov (se lahko ustvari get klice še za druge parametre)
-pridobivanje avta po ID

POST klici:
-ustvarjanje novega avta
-ustvarjanje novega uporabnika

PUT klici:
-posodobitev:
    -vsega
    -znamke
    -leta
    -kilometrov
    -...

DELETE:
-izbris avta
-izbris uporabnika

--------------------------------------------------------------------------------------------------
database.py
Vsebuje dve tabeli: Car in User.
Car tabela:
ID, znamka, model, leto, kilometri, cena, ...

User tabela:
ID, ime, priimek, email

--------------------------------------------------------------------------------------------------
shemas.py
vsebuje klase za avto in uporabnika

--------------------------------------------------------------------------------------------------
knjižnice, ki jih potrebujemo se nahajajo v datoteki requerments.txt in jih lahko naložimo z 
"pip install -r "requirments""

če želimo knjižnice namestiti v virtualno okolje pred tem kličemo:
python3 -m venv .venv --> da ustvarimo .venv virtualno kolje
source .venv/bin/activate --> vklop virtualke
deactivate --> ugašanje

kodo main.py zaženo z:
uvicorn main:app --reload
na 127.0.0.1:8000/docs lahko testiramo API klice

--------------------------------------------------------------------------------------------------
fastAPI & sqlite tutorial
https://www.youtube.com/watch?v=eltKL8kC160