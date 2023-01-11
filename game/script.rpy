# The script of the game goes in this file.

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
                self.round_count = 0
    
    # После каждого раунда в бою вызывается эта функция, чтобы определить, чья очередь в следующем.
    # Значение номера хода снижается. Если 0 (ходил враг), возвращается максимальное значение
        def turn(self):
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
        
        def attack_rate(self):
            return 0

        def attack(self, enemy):
            if self.attack_rate() > enemy.defence:
                renpy.say(narrator, self.name + " атакует успешно.")
                return True
            else:
                renpy.say(narrator, self.name + " промахивается.")
                return False
        
        def status_attack_start_effect(self):
            if self.noose_status:
                self.hp -= 1
                renpy.say(narrator, self.name + " теряет 1 ЖС от невидимой удавки на шее.")
            if self.poison_status:
                self.hp -= 3
                renpy.say(narrator, self.name + " теряет 3 ЖС от яда.")
            return self.isalive()
        
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
        
        def ghost_status_check(self):
            if self.ghost_status > 0:
                renpy.say(narrator, self.name + " не получает урона, благодаря действию заклинания Привидение.")
                return False
            else:
                return True
        
        def armor_spell_status_check(self):
            if self.armor_spell_status > 1:
                self.armor_spell_status -= 1
                renpy.say(narrator, "Силовое поле пробито. Защита снижена. Осталось слоёв — " + str(self.armor_spell_status))
            if self.armor_spell_status == 1:
                self.armor_spell_status -= 1
                renpy.say(narrator, "Силовое поле пробито. Защита снижена.")
            
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
        
        def resistance_check(self, enemy):
            if self.damage_type not in enemy.resistance:
                return True
            else:
                renpy.say(narrator, enemy.name + " не получает урона.")
                return False

        def fight_weapon(self, enemy):
            if self.status_attack_start_effect():
                renpy.say(narrator, self.name + " атакует.")
                if self.attack(enemy):
                    if enemy.ghost_status_check():
                        if enemy.stone_skin_status_check():
                            if self.resistance_check(enemy):
                                enemy.hp -= self.damage
                                renpy.say(narrator, enemy.name + " получает урон " + str(self.damage) + " ЖС.")
                                if enemy.isalive():
                                    enemy.armor_spell_status_check()
                                    enemy.fire_skin_status_check(self)
        
        def fight_magic(self, enemy, spell):
            if self.status_attack_start_effect():
                self.mana -= spell.mana_cost
                renpy.say(narrator, self.name + " применяет заклинание " spell.name)
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
                    return(True)
                    break
                else:
                    return(False)
        
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
        def __init__(self, name, strength_default, agility_default, health_default, intellect_default):
            global round_count
            global round_count_default

            round_count = 2
            round_count_default = 2

            self.name = str(name)

            self.strength_default = strength_default
            self.agility_default = agility_default
            self.health_default = health_default
            self.intellect_default = intellect_default

            self.restore_stats()

            self.hp_default = self.hp_default_define()
            self.restore_hp()

            self.mana_default = self.mana_default_define()
            self.restore_mana()
        
        def mana_default_define(self):
            return self.intellect_default

        def defence_calc(self):
            super().defence_calc()
            if self.weapon_current[0] in self.belovedweapon:
                self.defence += 2

        def attack_rate(self):
            i = super().attack_rate()
            if self.weapon_current[0] in self.belovedweapon:
                i += self.dice()
            return i

        def learn_define(self, spell):
            if self.dice() > 4:
                return True
            else:
                return False

    class Thief(Player):
        def __init__(self, name, strength_default, agility_default, health_default, intellect_default):
            self.name = str(name)

            self.strength_default = strength_default
            self.agility_default = agility_default
            self.health_default = health_default
            self.intellect_default = intellect_default

            self.restore_stats()

            self.hp_default = self.health_default * 4 + 4
            self.restore_hp()

            self.mana_default_define()
            self.restore_mana()

            self.weapon_banned = ['heavy_sword', 'spear']

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
        def __init__(self, name, strength_default, agility_default, health_default, intellect_default):
            self.name = str(name)

            self.strength_default = strength_default
            self.agility_default = agility_default
            self.health_default = health_default
            self.intellect_default = intellect_default

            self.restore_stats()

            self.hp_default = self.hp_default_define()
            self.restore_hp()

            self.mana_default = mana_default_define()
            self.restore_mana()
        
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
        def __init__(self, name, strength_default, agility_default, health_default, intellect_default):
            self.name = str(name)

            self.strength_default = strength_default
            self.agility_default = agility_default
            self.health_default = health_default
            self.intellect_default = intellect_default

            self.restore_stats()

            self.hp_default = self.hp_default_define()
            self.restore_hp()

            self.mana_default = mana_default_define()
            self.restore_mana()

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

        def selection_display(self, band):
            for i in band:
                if i.hp > 0

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
        def __init__(self, name):
            self.name = name
            self.defence = 8
            self.hp = 6
            self.damage = 4
            self.bonus = 5
            self.resistance = ['song', 'death', 'illusion', 'poison', 'trans']

        def attack_rate(self):
            return self.dice(2, 1)

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

#

    class Shield:
        def __init__(self, name, cost, defencebonus, ident):
            self.name = name
            self.cost = cost
            self.defencebonus = defencebonus
            self.ident = type

    class MagicItem:
        def __init__(self, name, cost, bonus, ident):
            self.name = name
            self.cost = cost
            self.bonus = bonus
            self.ident = type

# The game starts here.
# screen simple_example_inventory:
#     frame xalign 1 ypos 0.01:
#         vbox:
#             text "Строка вот такая длинная"
#             text "Cnhjrf djn nfrfz lkbyyfz"
label start:
    hide main_menu
    $ backpack.currentweapon.append(sword)
    "Выбери своего странника"
    show screen character_screen
    jump choose_class
#     $ backpack.addweapon(sword)
#     $ backpack.addweapon(axe)
#     "Выбери странника"
#     call screen simple_example_inventory
# screen simple_example_inventory:
#     frame xalign 0.5 ypos 0.1:
#         vbox:
#             for w in backpack.weaponset:
#                 textbutton "[w.name]: [w.cost]" action Jump(w.ident+'_label')
# label sword_label:
#     $ backpack.sellweapon(sword)
#     "Вы продали меч. Ваши деньги: [backpack.money]"
#     call screen simple_example_inventory
    
# label axe_label:
#     $ backpack.sellweapon(axe)
#     "Вы продали секиру. Ваши деньги: [backpack.money]"
#     call screen simple_example_inventory

label choose_class:            
default menuset = set()
menu:
    "Воин":
        $ character_class = 'warrior'
        $ character_class_rus = 'странник-воин'
        $ strengthcost = 70
        jump warrior_choose_beloved_weapon
    "Вор":
        $ character_class = 'thief'
        $ character_class_rus = 'странник-вор'
        $ bannedweapon.append(heavy_sword)
        $ bannedweapon.append(axe)
        $ agilitycost = 80
        jump choose_name
    "Бард":
        $ character_class = 'bard'
        $ character_class_rus = 'странник-бард'
        $ spellbook.addspell(peace_song_spell)
        $ spellbook.addspell(lullaby_song_spell)
        $ spellbook.addspell(dead_fear_song_spell)
        $ spellbook.addspell(pain_song_spell)
        jump choose_name
    "Шаман":
        $ character_class = 'shaman'
        $ character_class_rus = 'странник-шаман'
        $ spellbook.addspell(fire_fingers_spell)
        $ spellbook.addspell(size_change_spell)
        $ spellbook.addspell(armor_spell)
        $ spellbook.addspell(energy_spell)
        $ spellbook.addspell(noose_spell)
        $ spellbook.addspell(poisoned_spear_spell)
        $ spellbook.addspell(ghost_spell)
        $ spellbook.addspell(fireball_spell)
        $ spellbook.addspell(vampire_spell)
        $ spellbook.addspell(lightning_spell)
        $ spellbook.addspell(lightning_chain_spell)
        $ spellbook.addspell(stone_skin_spell)
        $ spellbook.addspell(ice_storm_spell)
        $ spellbook.addspell(transmutation_spell)
        $ spellbook.addspell(fire_skin_spell)
        $ spellbook.addspell(healing_spell)
        $ spellbook.addspell(elementary_resistance_spell)
        $ spellbook.addspell(healing_acceleration_spell)
        $ spellbook.addspell(false_death_spell)
        $ spellbook.addspell(death_spell)
        jump choose_name
nvl clear
label warrior_choose_beloved_weapon:
menu:
    "Выберите любимое оружие"
    "Кинжал":
        jump warrior_cosen_dagger
    "Меч":
        jump warrior_cosen_sword
    "Секира":
        jump warrior_cosen_axe
    "Копьё":
        jump choose_name
label warrior_cosen_dagger:
    "Теперь, кода у вас в руках кинжал, вы будете лучше атаковать и защищаться"
    $ belovedweapon.append(dagger)
    jump choose_name
label warrior_cosen_sword:
    "Теперь, кода у вас в руках меч, вы будете лучше атаковать и защищаться"
    $ belovedweapon.append(sword)
    $ belovedweapon.append(heavy_sword)
    $ belovedweapon.append(magic_sword)
    jump choose_name
label warrior_cosen_axe:
    "Теперь, кода у вас в руках секира, вы будете лучше атаковать и защищаться"
    $ belovedweapon.append(axe)
    jump choose_name
nvl clear
label choose_name:
    python:
        name = renpy.input("Как зовут вашего персонажа?")
    jump choosing_stats

label choosing_stats:
    nvl clear
    python:
        stata1 = dice()
        stata2 = dice()
        stata3 = dice()
        stata4 = dice()
    "Это твои характеристики:\n[stata1], [stata2], [stata3], [stata4]"
menu:
    set menuset
    "Что характеризует число [stata1]?"
    "Сила" if strength == 0:
        $ strength = stata1
    "Ловкость" if agility == 0:
        $ agility = stata1
    "Здоровье" if health == 0:
        $ health = stata1
    "Интеллект" if intellect == 0:
        $ intellect = stata1
nvl clear
menu:
    set menuset
    "Что характеризует число [stata2]?"
    "Сила" if strength == 0:
        $ strength = stata2
    "Ловкость" if agility == 0:
        $ agility = stata2
    "Здоровье" if health == 0:
        $ health = stata2
    "Интеллект" if intellect == 0:
        $ intellect = stata2
nvl clear
menu:
    set menuset
    "Что характеризует число [stata3]?"
    "Сила" if strength == 0:
        $ strength = stata3
    "Ловкость" if agility == 0:
        $ agility = stata3
    "Здоровье" if health == 0:
        $ health = stata3
    "Интеллект" if intellect == 0:
        $ intellect = stata3
nvl clear
menu:
    set menuset
    "Что характеризует число [stata4]?"
    "Сила" if strength == 0:
        $ strength = stata4
    "Ловкость" if agility == 0:
        $ agility = stata4
    "Здоровье" if health == 0:
        $ health = stata4
    "Интеллект" if intellect == 0:
        $ intellect = stata4
nvl clear
jump character_creation_final

label character_creation_final:
    python:
        defaultstats()
        defence_calc()
        mana_max_def()
        hp_max_def()
        mana = mana_max
        hp = hp_max
        damage = backpack.currentweapon[0].damage
    if character_class == 'warrior':
        "Ты — странник-воин по имени [name]"
    elif character_class == 'thief':
        "Ты — странник-вор по имени [name]"
    elif character_class == 'bard':
        "Ты — странник-бард по имени [name]"
    elif character_class == 'shaman':
        "Ты — странник-шаман по имени [name]"
    "Настало время приключений!"
    nvl clear
    call choose_path

label choose_path:
    nvl clear
    hide screen character_screen
    call screen worldmap()


label goto_south_castle:
    $ territory = 'south_castle'
menu choose_way:
    "Прямой путь":
        jump direct_path

label direct_path:
    $ currentpath = territory + '_direct_path'
    "Путешествие началось"
    $ adventure = dice()
    if adventure == 1:
        jump green_breeze_peninsula_1
    else:
        jump green_breeze_peninsula_1


label green_breeze_peninsula_1:
    "Тебе повстречались три безмозглых зомби"
    python:
        enemy0 = Enemy('Первый Зомби', zombie_attack(), 8, 6, 4, 'normal', 5, ['song', 'death', 'illusion', 'poison', 'trans'], [], 'normal','0')
        enemy1 = Enemy('Второй Зомби', zombie_attack(), 8, 6, 4, 'normal', 5, ['song', 'death', 'illusion', 'poison', 'trans'], [], 'normal', '1')
        enemy2 = Enemy('Третий Зомби', zombie_attack(), 8, 6, 4, 'normal', 5, ['song', 'death', 'illusion', 'poison', 'trans'], [], 'normal', '2')
        enemyband = EnemyGroup()
        enemyband.addenemy(enemy0)
        enemyband.addenemy(enemy1)
        enemyband.addenemy(enemy2)
        turn_def()
    if rnd == 0:
        $ fight_defend()
        $ turn()
    else:
        jump green_breeze_peninsula_1_fight

label green_breeze_peninsula_1_fight:
    if enemy1.hp <= 0 and enemy0.hp <= 0 and enemy2.hp <= 0:
        jump green_breeze_peninsula_1_win
    if rnd == 0:
        $ fight_defend()
        $ turn()
        jump green_breeze_peninsula_1_fight
menu:
    "[enemy0.name] / [enemy0.hp]" if enemy0.hp > 0:
        $ currentenemy = enemy0
        call fight_menu
        call green_breeze_peninsula_1_fight
    "[enemy1.name] / [enemy1.hp]" if enemy1.hp > 0:
        $ currentenemy = enemy1
        call fight_menu
        call green_breeze_peninsula_1_fight
    "[enemy2.name] / [enemy2.hp]" if enemy2.hp > 0:
        $ currentenemy = enemy2
        call fight_menu
        call green_breeze_peninsula_1_fight



label green_breeze_peninsula_1_win:
    nvl clear
    "Ты победил"

label fight_menu:
    nvl clear
menu:
    "Атаковать оружием":
        call fight_attack
        return
    "Использовать заклинание" if len(spellbook.spells):
        call fight_magic
        return

label fight_attack:
    nvl clear
    "[name] атакует [currentenemy.name]"
    $ atk = attack(currentenemy)
    $ return_fight()
    $ turn()
    return

label fight_magic:
    nvl clear
    if enoughmana() == False:
        "У вас закончилась магическая энергия."
        return
    else:
        "Выберите заклинание"
        call fight_cast
        return
label fight_cast:
    nvl clear
menu:
    "Назад":
        return
    "[fire_fingers_spell.name] ([fire_fingers_spell.manacost] МЭ)" if (fire_fingers_spell in spellbook.spells) and mana >= fire_fingers_spell.manacost:
        call fire_fingers_cast
        $ turn()
        $ return_fight()
        return
    "[size_change_spell.name] ([size_change_spell.manacost] МЭ)" if (size_change_spell in spellbook.spells) and mana >= size_change_spell.manacost:
        call size_change_spell_cast
        $ turn()
        $ return_fight()
        return
    "[armor_spell.name] ([armor_spell.manacost] МЭ)" if (armor_spell in spellbook.spells) and mana >= armor_spell.manacost and armor_spell_count == 0:
        call armor_spell_cast
        return
    "[energy_spell.name] ([energy_spell.manacost] МЭ)" if (energy_spell in spellbook.spells) and mana >= energy_spell.manacost:
        call energy_spell_cast
        $ turn()
        return
    "[noose_spell.name] ([noose_spell.manacost] МЭ)" if (noose_spell in spellbook.spells) and mana >= noose_spell.manacost:
        call noose_spell_cast
        $ turn()
        $ return_fight()
        return
    "[poisoned_spear_spell.name] ([poisoned_spear_spell.manacost] МЭ)" if (poisoned_spear_spell in spellbook.spells) and mana >= poisoned_spear_spell.manacost:
        call poisoned_spear_spell_cast
        $ turn()
        $ return_fight()
        return
    "[ghost_spell.name] ([ghost_spell.manacost] МЭ)" if (ghost_spell in spellbook.spells) and mana >= ghost_spell.manacost and ghost_status == 0:
        call ghost_spell_cast
        $ turn()
        return
    "[fireball_spell.name] ([fireball_spell.manacost] МЭ)" if (fireball_spell in spellbook.spells) and mana >= fireball_spell.manacost:
        call fireball_spell_cast
        $ return_fight()
        return
    "[vampire_spell.name] ([vampire_spell.manacost] МЭ)" if vampire_spell in spellbook.spells and mana >= vampire_spell.manacost and hp < currenthpmax:
        call vampire_spell_cast
        $ return_fight()
        return
    "[lightning_spell.name] ([lightning_spell.manacost] МЭ)" if lightning_spell in spellbook.spells and mana >= lightning_spell.manacost:
        call lightning_spell_cast
        $ return_fight()
        return
    "[lightning_chain_spell.name] ([lightning_chain_spell.manacost] МЭ)" if lightning_chain_spell in spellbook.spells and mana >= lightning_chain_spell.manacost:
        call lightning_chain_spell_cast
        $ return_fight()
        return
    "[stone_skin_spell.name] ([stone_skin_spell.manacost] МЭ)" if stone_skin_spell in spellbook.spells and mana >= stone_skin_spell.manacost and stone_skin_spell_count == 0:
        call stone_skin_spell_cast
        return
    "[ice_storm_spell.name] ([ice_storm_spell.manacost] МЭ)" if ice_storm_spell in spellbook.spells and mana >= ice_storm_spell.manacost:
        call ice_storm_spell_cast
        $ turn()
        return
    "[transmutation_spell.name] ([transmutation_spell.manacost] МЭ)" if transmutation_spell in spellbook.spells and mana >= transmutation_spell.manacost:
        call transmutation_spell_cast
        $ turn()
        $ return_fight()
        return
    "[fire_skin_spell.name] ([fire_skin_spell.manacost] МЭ)" if fire_skin_spell in spellbook.spells and mana >= fire_skin_spell.manacost:
        call fire_skin_spell_cast
        $ turn()
        return
    "[healing_spell.name] ([healing_spell.manacost] МЭ)" if healing_spell in spellbook.spells and mana >= healing_spell.manacost and hp < currenthpmax:
        call healing_spell_cast
        return
    "[elementary_resistance_spell.name] ([elementary_resistance_spell.manacost] МЭ)" if elementary_resistance_spell in spellbook.spells and mana >= elementary_resistance_spell.manacost and len(elementary_resistance_status) == 0:
        call elementary_resistance_spell_cast
        $ turn()
        return
    "[healing_acceleration_spell.name] ([healing_acceleration_spell.manacost] МЭ)" if healing_acceleration_spell in spellbook.spells and mana >= healing_acceleration_spell.manacost and hp < hp_max:
        call healing_acceleration_spell_cast
        return

label fire_fingers_cast:
    "[name] применяет заклинание [fire_fingers_spell.name]"
    $ mana -= fire_fingers_spell.manacost
    if 'fire' in currentenemy.resistance:
        "Заклинание не подействовало. [currentenemy.name] не боится огня."
        return
    else:
        "[currentenemy.name] теряет 5 ЖС от урона огнём" with hpunch
        $ currentenemy.hp -= 5
        if currentenemy.hp > 0:
            return
        else:
            "[currentenemy.name] убит!"
            return

label size_change_spell_cast:
    nvl clear
menu:
    "Увеличить свой рост":
        $ mana -= size_change_spell.manacost
        $ currentstr = currentstr * 2
        $ currentagi = currentagi // 2
        $ defence_calc()
        "[name] увеличил свой рост. Сила выросла, а ловкость снизилась в 2 раза." with blinds
        return
    "Уменьшить свой рост":
        $ mana -= size_change_spell.manacost
        $ currentstr = currentstr // 2
        $ currentagi = currentagi * 2
        $ defence_calc()
        "[name] уменьшил свой рост. Ловкость увелиилась, а сила снизилась в 2 раза." with blinds
        return

label armor_spell_cast:
    nvl clear
    "Сколько создать уровней силового поля?"
    python:
        armor_spell_amount_max = mana // 3
        armor_spell_amount = renpy.input("Введи количество не более [armor_spell_amount_max]")
        chck = True
        try:
            armor_spell_amount = int(armor_spell_amount)
        except ValueError:
            chck = False
    if chck == True and armor_spell_amount <= armor_spell_amount_max and armor_spell_amount > 0:
        $ mana -= armor_spell.manacost * armor_spell_amount
        $ defence += armor_spell_amount
        $ armor_spell_count = armor_spell_amount
        "[name] создал вокруг себя силовое поле [armor_spell_count] уровня" with blinds
        $ turn()
        return
    else:
        "Неправильное значение"
        return

label energy_spell_cast:
    nvl clear
    if mana >= energy_spell.manacost:
        $ energy_spell_select_show = True
        call energy_spell_cast_select
        return
    else:
        "Энергия закончилась"
        return
label energy_spell_cast_select:
    if energy_spell_select_show == True:
        "Каждый выстрел тратит [energy_spell.manacost] МЭ.\nВ кого направить сгусток энергии?"
    $ enemy_count = len(enemyband.band) - 1
menu:
    "Ни в кого, вернуться":
        $ energy_spell_select_show = False
        return
    "[enemy0.name] ([enemy0.hp] ЖС)" if enemy_count >= 0 and enemy0.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy0.resistance:
            "Заклинание не подействовало. [enemy0] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy0.hp -= 3
            "Сгусток энергии поразил врага. [enemy0.name] теряет 3 ЖС." with hpunch
            if enemy0.hp <= 0:
                "[enemy0.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy1.name] ([enemy1.hp] ЖС)" if enemy_count >= 1 and enemy1.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy1.resistance:
            "Заклинание не подействовало. [enemy1] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy1.hp -= 3
            "Сгусток энергии поразил врага. [enemy1.name] теряет 3 ЖС." with hpunch
            if enemy1.hp <= 0:
                "[enemy1.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy2.name] ([enemy2.hp] ЖС)" if enemy_count >= 2 and enemy2.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy2.resistance:
            "Заклинание не подействовало. [enemy2] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy2.hp -= 3
            "Сгусток энергии поразил врага. [enemy2.name] теряет 3 ЖС." with hpunch
            if enemy2.hp <= 0:
                "[enemy2.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy3.name] ([enemy3.hp] ЖС)" if enemy_count >= 3 and enemy3.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy3.resistance:
            "Заклинание не подействовало. [enemy3] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy3.hp -= 3
            "Сгусток энергии поразил врага. [enemy3.name] теряет 3 ЖС." with hpunch
            if enemy3.hp <= 0:
                "[enemy3.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy4.name] ([enemy4.hp] ЖС)" if enemy_count >= 4 and enemy4.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy4.resistance:
            "Заклинание не подействовало. [enemy4] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy4.hp -= 3
            "Сгусток энергии поразил врага. [enemy4.name] теряет 3 ЖС." with hpunch
            if enemy4.hp <= 0:
                "[enemy4.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy5.name] ([enemy5.hp] ЖС)" if enemy_count >= 5 and enemy5.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy5.resistance:
            "Заклинание не подействовало. [enemy5] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy5.hp -= 3
            "Сгусток энергии поразил врага. [enemy5.name] теряет 3 ЖС." with hpunch
            if enemy5.hp <= 0:
                "[enemy5.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy6.name] ([enemy6.hp] ЖС)" if enemy_count >= 6 and enemy6.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy6.resistance:
            "Заклинание не подействовало. [enemy6] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy6.hp -= 3
            "Сгусток энергии поразил врага. [enemy6.name] теряет 3 ЖС." with hpunch
            if enemy6.hp <= 0:
                "[enemy6.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy7.name] ([enemy7.hp] ЖС)" if enemy_count >= 7 and enemy7.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy7.resistance:
            "Заклинание не подействовало. [enemy7] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy7.hp -= 3
            "Сгусток энергии поразил врага. [enemy7.name] теряет 3 ЖС." with hpunch
            if enemy7.hp <= 0:
                "[enemy7.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy8.name] ([enemy8.hp] ЖС)" if enemy_count >= 8 and enemy8.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy8.resistance:
            "Заклинание не подействовало. [enemy8] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy8.hp -= 3
            "Сгусток энергии поразил врага. [enemy8.name] теряет 3 ЖС." with hpunch
            if enemy8.hp <= 0:
                "[enemy8.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy9.name] ([enemy9.hp] ЖС)" if enemy_count >= 9 and enemy9.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy9.resistance:
            "Заклинание не подействовало. [enemy9] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy9.hp -= 3
            "Сгусток энергии поразил врага. [enemy9.name] теряет 3 ЖС." with hpunch
            if enemy9.hp <= 0:
                "[enemy9.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy10.name] ([enemy10.hp] ЖС)" if enemy_count >= 10 and enemy10.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy10.resistance:
            "Заклинание не подействовало. [enemy10] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy10.hp -= 3
            "Сгусток энергии поразил врага. [enemy10.name] теряет 3 ЖС." with hpunch
            if enemy10.hp <= 0:
                "[enemy10.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy11.name] ([enemy11.hp] ЖС)" if enemy_count >= 11 and enemy11.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy11.resistance:
            "Заклинание не подействовало. [enemy11] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy11.hp -= 3
            "Сгусток энергии поразил врага. [enemy11.name] теряет 3 ЖС." with hpunch
            if enemy11.hp <= 0:
                "[enemy11.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy12.name] ([enemy12.hp] ЖС)" if enemy_count >= 12 and enemy12.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy12.resistance:
            "Заклинание не подействовало. [enemy12] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy12.hp -= 3
            "Сгусток энергии поразил врага. [enemy12.name] теряет 3 ЖС." with hpunch
            if enemy12.hp <= 0:
                "[enemy12.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy13.name] ([enemy13.hp] ЖС)" if enemy_count >= 13 and enemy13.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy13.resistance:
            "Заклинание не подействовало. [enemy13] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy13.hp -= 3
            "Сгусток энергии поразил врага. [enemy13.name] теряет 3 ЖС." with hpunch
            if enemy13.hp <= 0:
                "[enemy13.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy14.name] ([enemy14.hp] ЖС)" if enemy_count >= 14 and enemy14.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy14.resistance:
            "Заклинание не подействовало. [enemy14] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy14.hp -= 3
            "Сгусток энергии поразил врага. [enemy14.name] теряет 3 ЖС." with hpunch
            if enemy14.hp <= 0:
                "[enemy14.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy15.name] ([enemy15.hp] ЖС)" if enemy_count >= 15 and enemy15.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy15.resistance:
            "Заклинание не подействовало. [enemy15] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy15.hp -= 3
            "Сгусток энергии поразил врага. [enemy15.name] теряет 3 ЖС." with hpunch
            if enemy15.hp <= 0:
                "[enemy15.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy16.name] ([enemy16.hp] ЖС)" if enemy_count >= 16 and enemy16.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy16.resistance:
            "Заклинание не подействовало. [enemy16] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy16.hp -= 3
            "Сгусток энергии поразил врага. [enemy16.name] теряет 3 ЖС." with hpunch
            if enemy16.hp <= 0:
                "[enemy16.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy17.name] ([enemy17.hp] ЖС)" if enemy_count >= 17 and enemy17.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy17.resistance:
            "Заклинание не подействовало. [enemy17] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy17.hp -= 3
            "Сгусток энергии поразил врага. [enemy17.name] теряет 3 ЖС." with hpunch
            if enemy17.hp <= 0:
                "[enemy17.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy18.name] ([enemy18.hp] ЖС)" if enemy_count >= 18 and enemy18.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy18.resistance:
            "Заклинание не подействовало. [enemy18] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy18.hp -= 3
            "Сгусток энергии поразил врага. [enemy18.name] теряет 3 ЖС." with hpunch
            if enemy18.hp <= 0:
                "[enemy18.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy19.name] ([enemy19.hp] ЖС)" if enemy_count >= 19 and enemy19.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy19.resistance:
            "Заклинание не подействовало. [enemy19] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy19.hp -= 3
            "Сгусток энергии поразил врага. [enemy19.name] теряет 3 ЖС." with hpunch
            if enemy19.hp <= 0:
                "[enemy19.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy20.name] ([enemy20.hp] ЖС)" if enemy_count >= 20 and enemy20.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy20.resistance:
            "Заклинание не подействовало. [enemy20] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy20.hp -= 3
            "Сгусток энергии поразил врага. [enemy20.name] теряет 3 ЖС." with hpunch
            if enemy20.hp <= 0:
                "[enemy20.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy21.name] ([enemy21.hp] ЖС)" if enemy_count >= 21 and enemy21.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy21.resistance:
            "Заклинание не подействовало. [enemy21] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy21.hp -= 3
            "Сгусток энергии поразил врага. [enemy21.name] теряет 3 ЖС." with hpunch
            if enemy21.hp <= 0:
                "[enemy21.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy22.name] ([enemy22.hp] ЖС)" if enemy_count >= 22 and enemy22.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy22.resistance:
            "Заклинание не подействовало. [enemy22] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy22.hp -= 3
            "Сгусток энергии поразил врага. [enemy22.name] теряет 3 ЖС." with hpunch
            if enemy22.hp <= 0:
                "[enemy22.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy23.name] ([enemy23.hp] ЖС)" if enemy_count >= 23 and enemy23.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy23.resistance:
            "Заклинание не подействовало. [enemy23] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy23.hp -= 3
            "Сгусток энергии поразил врага. [enemy23.name] теряет 3 ЖС." with hpunch
            if enemy23.hp <= 0:
                "[enemy23.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
    "[enemy24.name] ([enemy24.hp] ЖС)" if enemy_count >= 24 and enemy24.hp > 0:
        $ mana -= energy_spell.manacost
        if energy_spell.type in enemy24.resistance:
            "Заклинание не подействовало. [enemy24] не боится воздействия энергии."
            call energy_spell_cast
            $ energy_spell_select_show = False
            return
        else:
            $ enemy24.hp -= 3
            "Сгусток энергии поразил врага. [enemy24.name] теряет 3 ЖС." with hpunch
            if enemy24.hp <= 0:
                "[enemy24.name] убит!"
            call energy_spell_cast
            $ energy_spell_select_show = False
            return

label noose_spell_cast:
    nvl clear
    "[name] применяет заклинание [noose_spell.name]"
    $ mana -= noose_spell.manacost
    if noose_spell.type in currentenemy.resistance:
        "Заклинание не действует. [currentenemy.name] не боится воздействий энергии."
        return
    else:
        $ currentenemy.status.append(['noose'])
        "[currentenemy.name] ощущает на своей шее невидимую удавку, которая причиняет в каждм кругу ущерб в 1 ЖС, и мешает применять магиню." with hpunch
        return    

label poisoned_spear_spell_cast:
    nvl clear
    "[name] применяет заклинание [poisoned_spear_spell.name]"
    $ mana -= poisoned_spear_spell.manacost
    if poisoned_spear_spell.type in currentenemy.resistance:
        "Заклинание не действует. [currentenemy.name] не боится яда."
        return
    else:
        $ currentenemy.status.append(['poison'])
        $ currentenemy.hp -= 4
        "[currentenemy.name] теряет 4 ЖС. Яд попадает в кровь, отнимая 3 ЖС каждый круг и мешая применять магию." with hpunch
        return

label ghost_spell_cast:
    $ mana -= ghost_spell.manacost
    $ ghost_status = 5
    "[name] применяет заклинание [ghost_spell.name]. В течение 5 кругов ему не страшны атаки обычным оружием." with fade
    return

label fireball_spell_cast:
    nvl clear
    "Огненный шар какого уровня создать?"
    python:
        fireball_did_damage = False
        fireball_line = ''
        fireball_spell_amount_max = mana // 3
        if fireball_spell_amount_max > 4:
            fireball_spell_amount_max = 4
        fireball_spell_amount = renpy.input("Введи количество не более [fireball_spell_amount_max]")
        chck = True
        try:
            fireball_spell_amount = int(fireball_spell_amount)
        except ValueError:
            chck = False
        if chck == True and fireball_spell_amount <= fireball_spell_amount_max and fireball_spell_amount_max > 0:
            mana -= fireball_spell.manacost * fireball_spell_amount
            fireball_damage = fireball_spell_amount * 5
            if 'fire' in currentenemy.resistance:
                fireball_line += "Огненный шар взрывается, но " + currentenemy.name + " не боится огня.\n"
            else:
                currentenemy.hp -= fireball_damage
                fireball_line += "Огненный шар взрывается, и " + currentenemy.name + " получает урон " + str(fireball_damage) + " ЖС.\n"
                fireball_did_damage = True
                if currentenemy.hp <= 0:
                    fireball_line += currentenemy.name + " убит!\n"
            fireball_count = 0
            for i in enemyband.band:
                if i.ident != currentenemy.ident and i.hp > 0:
                    fireball_count += 1
            fireball_list = []
            fireball_range = len(enemyband.band) - 1
            if fireball_range > 0:
                if fireball_count <= 3:
                    for i in enemyband.band:
                        if i.ident != currentenemy.ident and i.hp > 0:
                            if 'fire' in i.resistance:
                                fireball_line += i.name + " в области взрыва, но огонь не причиняет урон.\n"
                            else:
                                i.hp -= fireball_damage
                                fireball_line += i.name + " получает урон " + str(fireball_damage) + " ЖС от взрыва.\n"
                                fireball_did_damage = True
                                if i.hp < 0:
                                    fireball_line += i.name + " убит!\n"
                else:
                    while fireball_count > 0:
                        if fireball_count > 3:
                            fireball_count = 3
                        fireball_random = renpy.random.randint(0, fireball_range)
                        if enemyband.band[fireball_random].hp > 0 and enemyband.band[fireball_random].ident != currentenemy.ident and fireball_random not in fireball_list:
                            fireball_list.append(fireball_random)
                            fireball_count -= 1
                    for i in fireball_list:
                        if 'fire' in enemyband.band[i]:
                            fireball_line += enemyband.band[i].name + " в области взрыва, но огонь не причиняет урон.\n"
                        else:
                            enemyband.band[i].hp -= fireball_damage
                            fireball_line += enemyband.band[i].name + " получает урон " + str(fireball_damage) + " ЖС от взрыва.\n"
                            fireball_did_damage = True
                            if enemyband.band[i].hp < 0:
                                fireball_line += enemyband.band[i].name + " убит!\n"
        else:
            renpy.say(narrator, "Неправильное значение")
    if chck == True and fireball_spell_amount <= fireball_spell_amount_max and fireball_spell_amount_max > 0:
        if fireball_did_damage == True:
            "[fireball_line]" with hpunch
        else:
            "[fieball_line]"
        $ turn()
    return

label vampire_spell_cast:
    nvl clear
    "Сколько жизненной силы отнять?"
    python:
        vampire_spell_amount_max = mana // vampire_spell.manacost
        if vampire_spell_amount_max > currentenemy.hp:
            vampire_spell_amount_max = currentenemy.hp
        if vampire_spell_amount_max > (currenthpmax - hp):
            vampire_spell_amount_max = (currenthpmax - hp)
        vampire_spell_amount = renpy.input("Введи количество не более [vampire_spell_amount_max]")
        chck = True
        try:
            vampire_spell_amount = int(vampire_spell_amount)
        except ValueError:
            chck = False
    if chck == True and vampire_spell_amount <= vampire_spell_amount_max and vampire_spell_amount_max > 0:
        "[name] использует заклинание [vampire_spell.name]"
        $ mana -= vampire_spell_amount * vampire_spell.manacost
        if 'death' not in currentenemy.resistance:
            $ currentenemy.hp -= vampire_spell_amount
            $ hp += vampire_spell_amount
            "[currentenemy.name] теряет [vampire_spell_amount] ЖС" with blinds
            if currentenemy.hp <= 0:
                "[currentenemy.name] убит!"
        else:
            "Заклинание не действует. Из этого врага нельзя вытянуть жизненную энергию, потому что он уже по сути мёртв."
        $ turn()
    else:
        "Неправильное значение"
    return

label lightning_spell_cast:
    nvl clear
    "Молнию какого уровня создать?"
    python:
        lightning_spell_amount_max = mana // lightning_spell.manacost
        if lightning_spell_amount_max > 4:
            lightning_spell_amount_max = 4
        lightning_spell_amount = renpy.input("Введи количество не более [lightning_spell_amount_max]")
        chck = True
        try:
            lightning_spell_amount = int(lightning_spell_amount)
        except ValueError:
            chck = False    
    if chck == True and lightning_spell_amount > 0 and lightning_spell_amount <= lightning_spell_amount_max:
        "[name] выпускает из рук молнию, которая поражает противника."
        $ mana -= lightning_spell.manacost * lightning_spell_amount
        if 'lightning' in currentenemy.resistance:
            "Заклинание не действует. [currentenemy.name] не боится электричества."
        else:
            $ lightning_spell_damage = lightning_spell_amount * 5
            $ currentenemy.hp -= lightning_spell_damage
            "[currentenemy.name] теряет [lightning_spell_damage] ЖС" with hpunch
            if currentenemy.hp <= 0:
                "[currentenemy.name] убит!"
        $ turn()
    else:
        "Неправильное значение"
    return

label lightning_chain_spell_cast:
    nvl clear
    "Молнию какого уровня создать?"
    python:
        lightning_chain_line = ''
        lightning_chain_did_damage = False
        lightning_chain_damage = [5, 12, 18, 24]
        lightning_chain_spell_amount_max = mana // lightning_chain_spell.manacost
        if lightning_chain_spell_amount_max > 4:
            lightning_chain_spell_amount_max = 4
        lightning_chain_spell_amount = renpy.input("Введи количество не более [lightning_chain_spell_amount_max]")
        chck = True
        try:
            lightning_chain_spell_amount = int(lightning_chain_spell_amount)
        except ValueError:
            chck = False    
        if chck == True and lightning_chain_spell_amount > 0 and lightning_chain_spell_amount <= lightning_chain_spell_amount_max:
            lightning_chain_line += name + ' выпускает из рук молнию.\n'
            mana -= lightning_chain_spell.manacost * lightning_chain_spell_amount
            lightning_chain_spell_index = lightning_chain_spell_amount - 1
            if 'lightning' in currentenemy.resistance:
                lightning_chain_line += currentenemy.name + ' не получает урона, так как не боится воздействия электричества.\n'
            else:
                currentenemy.hp -= lightning_chain_damage[lightning_chain_spell_index]
                lightning_chain_line += currentenemy.name + ' получает урон ' + str(lightning_chain_damage[lightning_chain_spell_index]) + ' ЖС.\n'
                lightning_chain_did_damage = True
                if currentenemy.hp <= 0:
                    lightning_chain_line += currentenemy.name + ' убит!\n'
            lightning_chain_spell_index -= 1
            if lightning_chain_spell_index >= 0:
                lightning_chain_list = []
                lightning_chain_count = 0
                for i in enemyband.band:
                    if i.hp > 0 and i.ident != currentenemy.ident:
                        lightning_chain_count += 1
                if lightning_chain_count > 0:
                    if lightning_chain_count <= (lightning_chain_spell_index + 1):
                        for i in enemyband.band:
                            if i.hp > 0 and i.ident != currentenemy.ident:
                                if 'lightning' not in i.resistance:
                                    i.hp -= lightning_chain_damage[lightning_chain_spell_index]
                                    lightning_chain_line += i.name + ' получает урон ' + str(lightning_chain_damage[lightning_chain_spell_index]) + ' ЖС от молнии.\n'
                                    lightning_chain_did_damage = True
                                    lightning_chain_spell_index -= 1
                                    if i.hp <= 0:
                                        lightning_chain_line += i.name + ' убит!\n'
                                else:
                                    lightning_chain_line += i.name + ' не получает урона, так как не боится воздействия электричества.\n'
                                    lightning_chain_spell_index -= 1
                    else:
                        lightning_chain_range = len(enemyband.band) - 1
                        while lightning_chain_spell_index >= 0:
                            lightning_chain_random = renpy.random.randint(0, lightning_chain_range)
                            if enemyband.band[lightning_chain_random].ident != currentenemy.ident and enemyband.band[lightning_chain_random].hp > 0 and enemyband.band[lightning_chain_random].ident not in lightning_chain_list:
                                if 'lightning' not in enemyband.band[lightning_chain_random].resistance:
                                    enemyband.band[lightning_chain_random].hp -= lightning_chain_damage[lightning_chain_spell_index]
                                    lightning_chain_line += enemyband.band[lightning_chain_random].name + ' получает урон ' + str(lightning_chain_damage[lightning_chain_spell_index]) + ' ЖС от молнии.\n'
                                    lightning_chain_spell_index -= 1
                                    lightning_chain_did_damage = True
                                    if enemyband.band[lightning_chain_random].hp <= 0:
                                        lightning_chain_line += enemyband.band[lightning_chain_random].name + ' убит!\n'
                                else:
                                    lightning_chain_line += enemyband.band[lightning_chain_random].name + ' не получает урона, так как не боится воздействия электричества.\n'
                                    lightning_chain_spell_index -= 1
            turn()
        else:
            lightning_chain_line += 'Неправильное значение'
    if lightning_chain_did_damage == True:
        "[lightning_chain_line]" with hpunch
    else:
        "[lightning_chain_line]"
    return

label stone_skin_spell_cast:
    nvl clear
    "Создание каждого слоя каменой кожи требует [stone_skin_spell.manacost] МЭ.\nСколько слоёв создать?"
    python:
        stone_skin_line = ''
        stone_skin_spell_amount_max = mana // 5
        stone_skin_spell_amount = renpy.input("Введи количество не более [stone_skin_spell_amount_max]")
        chck = True
        try:
            stone_skin_spell_amount = int(stone_skin_spell_amount)
        except ValueError:
            chck = False
    if chck == True and stone_skin_spell_amount <= stone_skin_spell_amount_max and stone_skin_spell_amount > 0:
        $ mana -= stone_skin_spell_amount * stone_skin_spell.manacost
        $ stone_skin_spell_count += stone_skin_spell_amount
        "[name] применяет [stone_skin_spell.name]. Количество слоёв —  [stone_skin_spell_amount]." with bilnds
        $ turn()
    else:
        "Неправильное значение"
    return

label ice_storm_spell_cast:
    nvl clear
    "[name] использует заклинание [ice_storm_spell.name]. Тонкие и острые, как иглы, льдинки вращаются с бешеной скоростью вокруг центра бури."
    $ mana -= ice_storm_spell.manacost
    python:
        ice_storm_line = ''
        ice_storm_did_damage = False
        for i in enemyband.band:
            if i.hp > 0:
                if 'ice' not in i.resistance:
                    i.hp -= 10
                    ice_storm_line += i.name + " получает урон 10 ЖС.\n"
                    ice_storm_did_damage = True
                    if i.hp <= 0:
                        ice_storm_line += i.name + " убит!\n"
                else:
                    ice_storm_line += i.name + " не получает урона благодаря защите от холода."
    if ice_storm_did_damage == True:
        "[ice_storm_line]" with hpunch
    else:
        "[ice_storm_line]"
    return

label transmutation_spell_cast:
    nvl clear
    "[name] использует заклинание [transmutation_spell.name]"
    $ mana -= transmutation_spell.manacost
    if 'trans' in currentenemy.resistance:
        "[currentenemy.name] имеет иммунитет от магии превращения. Заклинание не действует."
    else:
        $ transmutation_spell_random = dice()
        if currentenemy.size == 'normal':
            $ transmutation_spell_chance = 3
        elif currentenemy.size == 'big':
            $ transmutation_spell_chance = 4
        elif currentenemy.size == 'huge':
            $ transmutation_spell_chance = 5
        if transmutation_spell_random <= transmutation_spell_chance:
            "[currentenemy.name] избегает превращения."
        else:
            $ currentenemy.hp = 0
            "[currentenemy.name] превращается в мышь. Он больше не может сражаться и спасается бегством." with blinds
    return

label fire_skin_spell_cast:
    nvl clear
    "[name] использует заклинание [fire_skin_spell.name]."
    $ mana -= fire_skin_spell.manacost
    $ fire_skin_spell_status = True
    return

label healing_spell_cast:
    nvl clear
    "Восстановление каждого очка жизненной силы требует [healing_spell.manacost]. Сколько жизненных сил восстановить?"
    python:
        healing_spell_amount_max = mana // 5
        if healing_spell_amount_max > (currenthpmax - hp):
            healing_spell_amount_max = currenthpmax - hp
        healing_spell_amount = renpy.input("Введи количество не более [healing_spell_amount_max]")
        chck = True
        try:
            healing_spell_amount = int(healing_spell_amount)
        except ValueError:
            chck = False
    if chck == True and healing_spell_amount <= healing_spell_amount_max and healing_spell_amount > 0:
        $ mana -= healing_spell_amount * healing_spell.manacost
        $ hp += healing_spell_amount
        "[name] восстанавливает [healing_spell_amount] ЖС." with blinds
        $ turn()
    else:
        "Неправильное значение"
    return

label elementary_resistance_spell_cast:
    "Сколько времени будет длиться защита? Каждый круг требует [elementary_resistance_spell.manacost] МЭ."
    python:
        elementary_resistance_spell_amount = renpy.input("Введи количество не более [mana]")
        chck = True
        try:
            elementary_resistance_spell_amount = int(elementary_resistance_spell_amount)
        except ValueError:
            chck = False
    if chck == True and elementary_resistance_spell_amount <= mana and elementary_resistance_spell_amount > 0:
        $ elementary_resistance_status.append(['', elementary_resistance_spell_amount])
    else:
        "Неправильное значение"
        return
    "От какой стихии будет защищать заклинание?"
menu:
    "Огонь":
        $ elementary_resistance_status[0][0] = 'fire'
        "[name] получает защиту от огня"
        return
    "Холод":
        $ elementary_resistance_status[0][0] = 'ice'
        "[name] получает защиту от холода"
        return
    "Электричество":
        $ elementary_resistance_status[0][0] = 'lightning'
        "[name] получает защиту от электричества"
        return
    "Яд":
        $ elementary_resistance_status[0][0] = 'poison'
        "[name] получает защиту от яда"
        return
    "Кислота":
        $ elementary_resistance_status[0][0] = 'acid'
        "[name] получает защиту от кислоты"
        return
        
label healing_acceleration_spell_cast:
    "Ускорение заживления ран требует 2 МЭ за каждый день. На сколкьо дней ускорить заживление?"
    python:
        healing_acceleration_spell_amount_max = mana // healing_acceleration_spell.manacost
        healing_acceleration_spell_amount = renpy.input("Введи количество не более [healing_acceleration_spell_amount_max]")
        chck = True
        try:
            healing_acceleration_spell_amount = int(healing_acceleration_spell_amount)
        except ValueError:
            chck = False
    if chck == True and healing_acceleration_spell_amount <= healing_acceleration_spell_amount_max and healing_acceleration_spell_amount > 0:
        $ mana -= healing_acceleration_spell_amount * healing_acceleration_spell.manacost
        $ healing_bonus = healing_acceleration_spell_amount
        "Восстановление жизненных сил ускорено. Количество дней — [healing_acceleration_spell_amount]." with blinds
    else:
        "Неправильное значение"
    return
    




            
            


label game_over:
    nvl clear
    "Game over"

#(self, name, attack, defence, hp, damage, damagetype, bonus, resistance, status, ident)
#screen simple_example_inventory:
#     frame xalign 0.5 ypos 0.1:
#         vbox:
#             for w in backpack.weaponset:
#                 textbutton "[w.name]: [w.cost]" action Jump(w.ident+'_label')
# label sword_label:
#     $ backpack.sellweapon(sword)
#     "Вы продали меч. Ваши деньги: [backpack.money]"
#     call screen simple_example_inventory
    
# label axe_label:
#     $ backpack.sellweapon(axe)
#     "Вы продали секиру. Ваши деньги: [backpack.money]"
#     call screen simple_example_inventory








    # This ends the game.

return
