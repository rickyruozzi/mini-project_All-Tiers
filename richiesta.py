import requests
def aggiungi_elemento():
    while True:
        name=input("inserisci il nome dell'articolo: ")
        description=input("inserisci la descrizione dell'articolo: ")
        price=float(input("inserisci il prezzo dell'articolo: "))

        data = {'name': name, 'description' : description , 'price': price}
        headers = {'Content-Type': 'application/json'}
        richiesta = requests.post('http://127.0.0.1:8000/add_item', headers=headers, json=data) #json.dumps() per rendere l'oggetto in formato JSON
        risposta = richiesta.json()
        print(risposta)
        
        scelta=input(' Vuoi inserire un altro elemento? (Y/n)\n')
        if scelta=='n':
            break
        
        
def visualizza_elementi():
    while True:
        richiesta = requests.get('http://127.0.0.1:8000/items') 
        risposta = richiesta.text
        print(risposta)
        
        scelta=input(' Vuoi rivisualizzare gli elementi? (Y/n)\n')
        if scelta=='n':
            break
        
def elimina_elemento():
    while True:
        id=input("inserisci l'id dell'item da eliminare: ")
        data = {'id': id}
        headers = {'Content-Type': 'application/json'}
        richiesta = requests.post('http://127.0.0.1:8000/remove_item', headers=headers, json=data) #json.dumps() per rendere l'oggetto in formato JSON
        risposta = richiesta.json()
        print(risposta)
        
        scelta=input(' Vuoi eliminare un altro elemento? (Y/n)\n')
        if scelta=='n':
            break
        
def switch(s):
    if s==1 : aggiungi_elemento()
    if s==2 : visualizza_elementi()
    if s==3 : elimina_elemento()
    
if __name__ == '__main__':
    while True:
        scelta=int(input('selezionare\n1 - per aggiungere un nuovo elemento\n2 - per visualizzare gli elementi\n3 - per eliminare un elemento\n4 - per uscire\n'))
        switch(scelta)
        if scelta == 4 : break