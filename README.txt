1) po želji aktivramo virtual enviroment
    source .venv/bin/activate
2) prenesemo requirements.txt
3) potreben CORS addon drugače ne dela 

####################### Zagon spletne aplikacije ###################################
Zagon backenda:
    1) cd NUKSvaje/domaca_naloga3                   #premik v direktorij
    2) python3 -m uvicorn main:app --reload         #zagon fastapi (main.py)
    3) obiščemo localhost:8000/v2/docs

Zagon frontenda:
    1) cd NUKSvaje/domaca_naloga3/avto-net          #premik v direktorij
    2) npm run serve                                #zagon backenda
    3) obiščemo localhost:8080


################## DOCKER #####################################################################

sudo docker ps                                      #preverjanje delujočih kont.
sudo docker kill PID                                #ubijanje kont.
sudo docker run
sudo systemctl status docker                        #status dockerja

docker build -t "ime taga" .                        #naredi image (. išči dockerfile v trenutnem direktorjiju)
docker run -dp hostport:contport "ime tega" 	    #zaženi image in mapiraj porte
sudo docker image rm 19fef28777d4                   #delete image


Zagon mySQL docker image:
    1) 


v VS code odpro porte (forvording)

Zagon backend docker image:
    1) docker build -t fastapi_image .
    2) sudo docker run -dp 8000:8000 fastapi_image 
    3)obiščemo localhost:8000 oz. 212.101.137.121:8000  #pomembno da je 8000 zaradi fetchov v javaskriptu

Zagon frontenda docker image:
    1) docker build -t vue_image .
    2) sudo docker run -dp 5000:8080 vue_image     #8080 default vue.js port!
    3)obiščemo localhost:5000 oz. 212.101.137.121:5000