from datetime import datetime, timedelta

from random import randint
import requests

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.hp = randint(50, 100)
        self.power = randint(20, 50)
        self.last_feed_time = datetime.now()

        Pokemon.pokemons[pokemon_trainer] = self
    
    
    def feed(self, feed_interval = 20, hp_increase = 10 ):
        now = datetime.now()  
        delta_time = timedelta(seconds=feed_interval)  
        if (now - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = now
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {now + delta_time}"  
        
    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "https://static.wikia.nocookie.net/pokemon/images/0/0d/025Pikachu.png/revision/latest/scale-to-width-down/1000?cb=20181020165701&path-prefix=ru"
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"
    
    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance==1:
                return f'противник пременил щит'
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f'наше сражение @{self.name}, @{enemy.name}'
        else:
            enemy.hp = 0
            return f'Победа @{self.name} над @{enemy.name}'
        
    # Метод класса для получения информации
    def info(self):
        return f"""Имя твоего покеомона: {self.name}
        Здоровье твоего покемона: {self.hp}
        Сила твоего покемона: {self.power}
        """

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img


class Wizard(Pokemon):
    def info(self):
        return f'Ваш покемон волшебник'
    def feed(self):
        return super().feed(hp_increase = 10)
class Fighter(Pokemon):
    def info(self):
        return f'Ваш покемон боец'
    def attack(self, enemy):
        super_power = randint(1,5)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой:{super_power} "
    def feed(self):
        return super().feed(hp_increase = 7)
if __name__ == '__main__':
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    print(wizard.info())
    print()
    print(fighter.info())
    print()
    print(fighter.attack(wizard))
