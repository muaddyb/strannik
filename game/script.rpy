﻿# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
define narrator = nvl_narrator

init python:
    menu = nvl_menu

# Глобальные атрибуты

    class Gohan:
        round_count_default = 1 #Максимальное значение номера хода. У всех 1, у воина будет 2
        round_count = 1 #Текущее значение номера хода

# Общий класс всех персонажей

    class Character:
        # Инит всех объектов типа Персонаж.
        # По-умолчанию передаётся отсылка к классу глобальных атрибутов
        def __init__(self, globe=Gohan()):
            self.globe = globe

        # Броски кубика: принимает количество и доп. очки
        # Каждый даёт случайное число от 1 до 6
        # Возвращает сумму всех бросков и доп. очков
        @staticmethod
        def dice(n = 1, addition = 0):
            x = 0
            for i in range(n): 
                x += renpy.random.randint(1,6)
            return x + addition

# Вызов значений глобальных атрибутов

    # Даёт максимальное значение номера хода
        @property
        def round_count_default(self):
            return self.globe.round_count_default
        
    # Даёт текущее значение номера хода
        @property
        def round_count(self):
            return self.globe.round_count

    # В начале бой определяет, чей ход первый. Следует вызывать от объекта игрока
    # Первым ходит тот, чей бросок больше. Условно считаем бросок игрока x
    # Игрок ходит, когда round_count > 0, поэтому при его победе выставляем равным round_count_default
        def turn_define(self):
            x = 0
            y = 0
            while x == y:
                x = self.dice()
                y = self.dice()
            if x > y:
                self.globe.round_count = self.round_count_default
            else:
                self.globe.round_count = 0
    
    # После каждого раунда в бою вызывается эта функция, чтобы определить, чья очередь в следующем.
    # Значение номера хода снижается. Если 0 (ходил враг), возвращается максимальное значение
        def round(self):
            if self.round_count > 0:
                self.globe.round_count -= 1
            else:
                self.globe.round_count = self.round_count_default

# Атрибуты персонажа. Здесь указаны по-умолчанию. TO-DO: потом посмотреть, можно ли убрать

        name = 'Character'
        hp_default = 0
        hp = 0

        ghost_status = 0
        stone_skin_status = 0
        armor_spell_status = 0
        poison_status = 0
        noose_status = 0
        fire_skin_status = False
        resistance = []
        damage_type = 'normal'
        damage = 0

    # Защита по-умолчанию и защита текущая. TO-DO: потом посмотреть, можно ли убрать
        defence_default = 0
        defence = 0

        
    # Проверяет жив ли персонаж по хп больше 0. Да — возвращает True, Нет — False и сообщение
        def isalive(self):
            if self.hp > 0:
                return True
            else:
                renpy.say(narrator, self.name + " мёртв.")
                return False
        def isalive_silent(self):
            if self.hp > 0:
                return True
            else:
                return False

    # Определение, успешна ли атака: больше ли значение атаки, чем защита протиника
        def attack_success(self, enemy):
            if self.attack_rate() > enemy.defence:
                renpy.say(narrator, self.name + " атакует успешно.")
                return True
            else:
                renpy.say(narrator, self.name + " промахивается.")
                return False

    # Проверка на различные действия, которые проявляются в начале хода.    
        def status_attack_start_effect(self):
            if self.noose_status: # Заклинание Удавка наносит урон 1 ЖС
                self.hp -= 1
                renpy.say(narrator, self.name + " теряет 1 ЖС от невидимой удавки на шее.")
            if self.poison_status: # Яд наносит урон 3 ЖС
                self.hp -= 3
                renpy.say(narrator, self.name + " теряет 3 ЖС от яда.")
            return self.isalive() # Проверка, жив ли персонаж

    # Проверка действия заклинания Каменная кожа. Если есть, понижается его уровень.    
        def stone_skin_status_check(self):
            if self.stone_skin_status == 0:
                return True
            elif self.stone_skin_status > 1:
                self.stone_skin_status -= 1
                renpy.say(narrator, "Каменная кожа разрушается, поглощая весь урон. Осталось слоёв — " + str(self.stone_skin_status))
                return False
            else:
                self.stone_skin_status -= 1
                renpy.say(narrator, "Каменная кожа разрушается, поглощая весь урон.")
                return False

        # Проверка действия заклинания Призрак. Если да, противник не получит уровна от оружия
        # TO-DO: возможен урон не только обычным оружием
        def ghost_status_check(self, enemy):
            if enemy.ghost_status > 0 and self.damage_type == 'normal':
                renpy.say(narrator, self.name + " не получает урона, благодаря действию заклинания Привидение.")
                return False
            else:
                return True
        
        # Проверка действия заклинания энергетическая защита (силовое поле).
        # TO-DO: Проверить, прописано ли понижение защиты вслед за уровнем силового поля.
        def armor_spell_status_check(self):
            if self.armor_spell_status > 1:
                self.armor_spell_status -= 1
                renpy.say(narrator, "Силовое поле пробито. Защита снижена. Осталось слоёв — " + str(self.armor_spell_status))
            if self.armor_spell_status == 1:
                self.armor_spell_status -= 1
                renpy.say(narrator, "Силовое поле пробито. Защита снижена.")

        # Проверка действия заклинания Огненная Кожа. Если да, атакующий получит урон от огня.
        # TO-DO: проверить, не нужно ли поменять self на enemy    
        def fire_skin_status_check(self, enemy):
            if self.fire_skin_status == True:
                renpy.say(narrator, enemy.name + " испытывает жар огненной кожи.")
                if 'fire' not in enemy.resistance:
                    enemy.hp -= 5
                    renpy.with_statement(hpunch)
                    renpy.say(narrator, enemy.name + " получает урон 5 ЖС")
                    enemy.isalive()
                else:
                    renpy.say(narrator, enemy.name + " не получает урона от огня.")
        
        # Проверка иммунитета от типа урона.
        def resistance_check(self, enemy):
            if self.damage_type not in enemy.resistance:
                return True
            else:
                renpy.say(narrator, enemy.name + " не получает урона.")
                return False

        # Процесс атаки оружием
        def attack(self, enemy):
            if self.attack_success(enemy):
                if self.resistance_check(enemy):
                    if self.ghost_status_check(enemy):
                        return True
        
        def fight_weapon(self, enemy):
            if self.attack(enemy):
                enemy.hp -= self.damage
                enemy.armor_spell_status_check()
                enemy.fire_skin_status_check(self)

        




        
        def fight_magic(self, enemy, spell):
            if self.status_attack_start_effect():
                self.mana -= spell.mana_cost
                renpy.say(narrator, self.name + " применяет заклинание " + spell.name)
                if spell.resistance_check():
                    if enemy.stone_skin_status_check():
                        spell.cast(self, enemy)
                        if enemy.isalive():
                            enemy.armor_spell_status_check()
                
    class Player(Character):
        strength_default = 0
        strength = 0
        agility_default = 0
        agility = 0
        health_default = 0
        health = 0
        intellect_default = 0
        intellect = 0

        hp_default = 0
        mana_default = 0

        money = 0
        weapon_list = []
        armor_list = []
        item_list = []
        magic_item_list = []
        shield_list = []
        weapon_current = []
        shield_current = []
        armor_current = []
        weapon_banned = []
        spellbook = []

        belovedweapon = []

        def complete_creation(self):

            self.restore_stats()

            self.hp_default = self.hp_default_define()
            self.restore_hp()

            self.mana_default = self.mana_default_define()
            self.restore_mana()



        def hp_default_define(self):
            return (self.health_default * 4 + 4)

        def attack_rate(self):
            if self.strength == 1:
                i = int(self.dice(2))
            elif self.strength == 2:
                i = int(self.dice(2, 2))
            elif self.strength == 3:
                i = int(self.dice(2, 4))
            elif self.strength == 4:
                i = int(self.dice(3))
            elif self.strength == 5:
                i = int(self.dice(3, 2))
            elif self.strength == 6:
                i = int(self.dice(3, 4))
            elif self.strength == 7:
                i = int(self.dice(4))
            elif self.strength == 8:
                i = int(self.dice(4, 2))
            elif self.strength == 9:
                i = int(self.dice(4, 4))
            elif self.strength == 10:
                i = int(self.dice(5))
            elif self.strength == 11:
                i = int(self.dice(5, 2))
            elif self.strength == 12:
                i = int(self.dice(5, 4))
            elif self.strength == 13:
                i = int(self.dice(6))
            elif self.strength == 14:
                i = int(self.dice(6, 2))
            elif self.strength == 15:
                i = int(self.dice(6, 4))
            elif self.strength == 16:
                i = int(self.dice(7))
            elif self.strength == 17:
                i = int(self.dice(7, 2))
            elif self.strength == 18:
                i = int(self.dice(7, 4))
            return i

        def defence_calc(self):
            self.defence = self.agility + 7
            if len(self.armor_current):
                self.defence += self.armor_current[0].bonus
            if len(self.shield_current):
                self.defence += self.shield_current[0].bonus
        
        def learn_define(self, spell):
            return False

        def learn(self, spell):
            if self.learn_define():
                self.spellbook.append(spell)
                renpy.say(narrator, "Заклинание " + spell.name + " выучено!")
            else:
                renpy.say(narrator, "Заклинание " + spell.name + " не удалось выучить.")
        
        def restore_stats(self):
            self.strength = self.strength_default
            self.agility = self.agility_default
            self.health = self.health_default
            self.intellect = self.intellect_default
        
        def restore_hp(self):
            self.hp = self.hp_default
        
        def restore_mana(self):
            self.mana = self.mana_default

        def is_enough_mana():
            for i in self.spellbook:
                if self.mana >= i.mana_cost:
                    return True 
                    break
                else:
                    return False 
        def turn_start(self, band):
            if self.round_count > 0:
                self.player_turn(band)
            else:
                self.enemy_turn(band)

        def enemy_turn(self, band):
            for i in band:
                if i.isalive_silent():
                    if i.status_attack_start_effect():
                        i.fight_weapon(self)
            self.round()

        def player_turn(self, band):
            if self.isalive_silent():
                if self.status_attack_start_effect():
                    self.action_select(band)
            self.round()

        def action_select(self, band):
            selected = renpy.display_menu([('Атака оружием', 'weapon')])
            self.choose_enemy(band, selected)

        def choose_enemy(self, band, selected):
            chosen = renpy.display_menu([(i.name + ' / ' + str(i.hp), i) for i in band if i.isalive_silent()])
            if selected == 'weapon':
                self.fight_weapon(chosen)

        def add_item(self, item):
            if type(item).__name__ == 'Weapon':
                self.weapon_list.append(item)
            elif type(item).__name__ == 'Armor':
                self.armor_list.append(item)
            elif type(item).__name__ == 'Item':
                self.item_list.append(item)
            elif type(item).__name__ == 'MagicItem':
                self.magic_item_list.append(item)
            elif type(item).__name__ == 'Shield':
                self.shield_list.append(item)

        def buy_item(self, item):
            if self.money >= item.cost:
                self.add_item(item)
                renpy.say(narrator, self.name + " купил " + item.name)
            else:
                renpy.say(narrator, "Не хватает денег!")

        def remove_item(self, item):
            if item in self.weapon_list:
                self.weapon_list.remove(item)
            elif item in self.armor_list:
                self.armor_list.remove(item)
            elif item in self.item_list:
                self.item_list.remove(item)
            elif item in self.magic_item_list:
                self.magic_item_list.remove(item)
            elif item in self.shield_list:
                self.shield_list.remove(item)

        def sell_item(self, item):
            self.remove_item(item)
            self.money += item.cost
            renpy.say(narrator, self.name + " продал " + item.name)

        def equip_weapon(self, item):
            if item.type not in self.weapon_banned:
                if len(self.weapon_current):
                    self.weapon_list.append(self.weapon_current[0])
                    self.weapon_current.remove[0]
                self.weapon_current.append(item)
                self.weapon_list.remove(item)
                self.damage_type = item.damage_type
                self.damage = item.damage
            else:
                renpy.say(narrator, self.name + "не может пользоваться этим оружием!")
        
        def equip_armor(self, item):
            if item.type not in self.weapon_banned:
                if len(self.armor_current):
                    self.armor_list.append(self.armor_current[0])
                    self.armor_current.remove[0]
                self.armor_current.append(item)
                self.armor_list.remove(item)
                self.defence_calc()
            else:
                renpy.say(narrator, self.name + " не может пользоваться доспехами.")

        def equip_shield(self, item):
            if item.type not in self.weapon_banned:
                if len(self.shield_current):
                    self.shield_list.append(self.shield_current[0])
                    self.shield_current.remove[0]
                self.shield_current.append(item)
                self.shield_list.remove(item)
                self.defence_calc()
            else:
                renpy.say(narrator, self.name + " не может пользоваться щитами.")
        
        def steal_item_define(self):
            renpy.say(narrator, self.name + " никогда не опустится до воровства!")
            return 0

        def steal_item(self, item):
            if i > item.cost:
                self.add_item(item)
                renpy.say(narrator, self.name + " украл " + item.name)
                return True
            else:
                renpy.say(narrator, self.name + " не смог украсть " + item.name)
                return False
    
    class Warrior(Player):
        
        def mana_default_define(self):
            return self.intellect_default

        def defence_calc(self):
            super().defence_calc()
            if self.weapon_current[0].type in self.belovedweapon:
                self.defence += 2

        def attack_rate(self):
            i = super().attack_rate()
            if self.weapon_current[0].type in self.belovedweapon:
                i += self.dice()
            return i

        def learn_define(self, spell):
            if self.dice() > 4:
                return True
            else:
                return False

    class Thief(Player):
        weapon_banned = ['heavy_sword', 'spear']

        def mana_default_define(self):
            if self.intellect_default == 1:
                i = 2
            elif self.intellect_default == 2:
                i = 3
            elif self.intellect_default == 3:
                i = 5
            elif self.intellect_default == 4:
                i = 6
            elif self.intellect_default == 5:
                i = 8
            elif self.intellect_default == 6:
                i = 9
            elif self.intellect_default == 7:
                i = 11
            elif self.intellect_default == 8:
                i = 12
            elif self.intellect_default == 9:
                i = 14
            elif self.intellect_default == 10:
                i = 15
            elif self.intellect_default == 11:
                i = 17
            elif self.intellect_default == 12:
                i = 18
            elif self.intellect_default == 13:
                i = 20
            elif self.intellect_default == 14:
                i = 21
            elif self.intellect_default == 15:
                i = 23
            elif self.intellect_default == 16:
                i = 24
            elif self.intellect_default == 17:
                i = 26
            elif self.intellect_default == 18:
                i = 27
            return i
        
        def turn_define(self):
            global round_count
            round_count = 1

        def attack_rate(self):
            if self.agility > 9:
                return super().attack_rate() + super().attack_rate()
            else:
                return super().attack_rate()
        
        def steal_item_define(self, item):
            if self.agility == 1:
                i = int(self.dice())
            elif self.agility == 2:
                i = int(self.dice(1, 2))
            elif self.agility == 3:
                i = int(self.dice(1, 4))
            elif self.agility == 4:
                i = int(self.dice(2, 0))
            elif self.agility == 5:
                i = int(self.dice(2, 2))
            elif self.agility == 6:
                i = int(self.dice(2, 4))
            elif self.agility == 7:
                i = int(self.dice(3, 0))
            elif self.agility == 8:
                i = int(self.dice(3, 2))
            elif self.agility == 9:
                i = int(self.dice(3, 4))
            elif self.agility == 10:
                i = int(self.dice(4, 0))
            elif self.agility == 11:
                i = int(self.dice(4, 2))
            elif self.agility == 12:
                i = int(self.dice(4, 4))
            elif self.agility == 13:
                i = int(self.dice(5, 0))
            elif self.agility == 14:
                i = int(self.dice(5, 2))
            elif self.agility == 15:
                i = int(self.dice(5, 4))
            elif self.agility == 16:
                i = int(self.dice(6))
            elif self.agility == 17:
                i = int(self.dice(6, 2))
            elif self.agility == 18:
                i = int(self.dice(6, 4))
            return i
            
        def learn_define(self, spell):
            if self.dice() > 3:
                return True
            else:
                return False

    class Bard(Player):
        
        def mana_default_define(self):
            return self.intellect_default * 2
        
        def learn_define(self, spell):
            if self.dice() > 2:
                return True
            else:
                return False

        def steal_item_define(self, item):
            if self.agility < 4:
                renpy.say(narrator, self.name + " недостаточно ловок для воровства.")
                i = 0
            elif self.agility == 4:
                i = int(self.dice())
            elif self.agility == 5:
                i = int(self.dice(1, 2))
            elif self.agility == 6:
                i = int(self.dice(1, 4))
            elif self.agility == 7:
                i = int(self.dice(2, 0))
            elif self.agility == 8:
                i = int(self.dice(2, 2))
            elif self.agility == 9:
                i = int(self.dice(2, 4))
            elif self.agility == 10:
                i = int(self.dice(3, 0))
            elif self.agility == 11:
                i = int(self.dice(3, 2))
            elif self.agility == 12:
                i = int(self.dice(3, 4))
            elif self.agility == 13:
                i = int(self.dice(4, 0))
            elif self.agility == 14:
                i = int(self.dice(4, 2))
            elif self.agility == 15:
                i = int(self.dice(4, 4))
            elif self.agility == 16:
                i = int(self.dice(5, 0))
            elif self.agility == 17:
                i = int(self.dice(5, 2))
            elif self.agility == 18:
                i = int(self.dice(5, 4))
            return i
    
    class Shaman(Player):

        def mana_default_define(self):
            if self.intellect_default > 2:
                return ((self.intellect_default - 2) * 4)
            else:
                return 2

        def learn_define(self, spell):
            if spell.type == 'song':
                renpy.say(narrator, self.name + " испытывает отвращение, когда пытается выучить " + spell.name)
                return False
            else:
                return True
        
        def attack_rate(self):
            return (super().attack_rate() - self.dice())

    class Magic_Damaging():
        type = ''
        name = ''
        damage = 0
        def __init__(self, mana_cost):
            self.mana_cost = mana_cost
        
        def resistance_check(self, enemy):
            if self.type not in enemy.resistance:
                return True
            else:
                renpy.say(narrator, "Заклинание " + self.name + " не подействовало")

    class Fire_Fingers(Magic_Damaging):
        type = 'fire'
        name = 'Огненные Пальцы'
        damage = 5

        def cast(self, player, enemy):
            if self.resistance_check(enemy):
                renpy.say(narrator, player.name + " касается противника пальцами, которые вспыхивают огнём.\n" + enemy.name + " получает урон 5 ЖС")
                enemy.hp -= self.damage
    
    fire_fingers_spell = Fire_Fingers(5)

    class Energy(Magic_Damaging):
        type = 'energy'
        name = 'Сгусток Энергии'
        damage = 3
        selected = []

        def select(self, player, enemy):
            player.mana -= self.mana_cost
            self.selected.append(enemy)
        
        def cast(self):
            for i in self.selected:
                if i.resistance_check():
                    i.hp -= self.damage
                    renpy.say(narrator, i.name + " получил урон " + str(self.damage) + " ЖС")
            self.selected.clear()
        



    energy_spell = Energy(3)

    class Magic_StatChanging():
        type = ''
        name = ''

        def __init__(self, mana_cost):
            self.mana_cost = mana_cost

    class Size_Change(Magic_StatChanging):
        type = 'transformation'
        name = 'Изменение Роста'

        def cast(self, player, direction):
            if direction == 'up':
                player.strength = player.strength * 2
                player.agility = player.agility // 2
                player.defence_calc()
                renpy.say(narrator, player.name + " увеличил свой рост. Сила выросла, а ловкость снизилась в 2 раза.")
            else:
                player.strengh = player.strengh // 2
                player.agility = player.agility * 2
                player.defence_calc()
                renpy.say(narrator, player.name + " уменьшил свой рост. Ловкость увеличилась, а сила уменьшилась в 2 раза.")

    size_change_spell = Size_Change(8)

    class Armor(Magic_StatChanging):
        type = 'transformation'
        name = 'Волшебные Доспехи'
        amount = 0
        max_amount = 0

        def cast(self, player):
            self.max_amount = player.mana // self.mana_cost
            string = "Сколько уровней поля создать?\nВведи число не более " + str(self.max_amount)
            self.amount = renpy.input()
            chck = True
            try:
                self.amount = int(self.amount)
            except ValueError:
                chck = False
            if chck == True and self.amount <= self.max_amount and self.amount > 0:
                player.mana -= self.mana_cost
                player.defence += self.amount
                player.armor_spell_status = self.amount
                renpy.say(narrator, player.name + " создал вокруг себя силовое поле. Уровней — " + str(self.amount))
            else:
                renpy.say(narrator, "Неправильное значение")
    
    armor_spell = Armor(3)


        

    class Enemy(Character):
        damage_type = 'normal'
        bonus = 0
        size = 'normal'
        damage = 0
        
        def attack_rate(self):
            return 0
        
    
    class Zombie(Enemy):
        name = 'Зомби'
        defence = 8
        hp = 6
        damage = 4
        bonus = 5
        resistance = ['song', 'death', 'illusion', 'poison', 'trans']
        noose_status = 1

        def attack_rate(self):
            return self.dice(2, 1) + 10

######## Вещи ########

#Оружие

    class Weapon():
        def __init__(self, name, cost, damage, damage_type, type):
            self.name = name
            self.cost = cost
            self.damage = damage
            self.damage_type = damage_type
            self.type = type

    dagger = Weapon('кинжал', 3, 3, 'normal', 'dagger')
    sword = Weapon('меч', 5, 4, 'normal', 'sword')
    heavy_sword = Weapon('тяжёлый меч', 10, 5, 'normal', 'heavy_sword')
    axe = Weapon('секира', 15, 6, 'normal', 'axe')
    magic_sword = Weapon('волшебный меч', 20, 6, 'energy', 'magic_sword')

#Доспехи

    class Armor:
        def __init__(self, name, cost, defencebonus, ident):
            self.name = name
            self.cost = cost
            self.defencebonus = defencebonus
            self.ident = type

    knight_armor = Armor('рыцарские доспехи', 30, 3, 'knight_armor')

# Щиты

    class Shield:
        def __init__(self, name, cost, defencebonus, ident):
            self.name = name
            self.cost = cost
            self.defencebonus = defencebonus
            self.ident = type

# Магические предметы

    class MagicItem:
        def __init__(self, name, cost, bonus, ident):
            self.name = name
            self.cost = cost
            self.bonus = bonus
            self.ident = type

# The game starts here.

label start:
    hide main_menu
    $ hero = Warrior()
    $ hero.strength_default = 5
    $ hero.agility_default = 4
    $ hero.intellect_default =2
    $ hero.health_default = 6
    $ hero.complete_creation()
    $ hero.weapon_list.append(sword)
    $ hero.equip_weapon(sword)
    $ hero.defence_calc()
    $ hero.fire_skin_status = True

    $ enemy1 = Zombie()
    $ enemy2 = Zombie()
    $ enemy3 = Zombie()
    $ band = []
    $ band.append(enemy1)
    $ band.append(enemy2)
    $ band.append(enemy3)
    show screen character_screen
    $ hero.turn_define()
    python:
        while len(band):
            hero.turn_start(band)

