# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
define narrator = nvl_narrator

init python:
    
#Имя по-умолчанию
    name = 'Strannik'
#Базовые характеристики
    strength = 0
    agility = 0
    health = 0
    intellect = 0
#Текущие характеристики в бою
    currentstr = strength
    currentagi = agility
    currenthlt = health
    currentint = intellect
#Основные параметры
    character_class = ''
    character_class_rus = ''
#Производные параметры
    hp = 0
    hp_max = 0
    mana = 0
    mana_max = 0
    defence = 0
    belovedweapon = []
    bannedweapon = []
    status = []
    resistance = []
    armor_spell_count = 0
#Цена за повышение основной харктеристики
    strengthcost = 80
    agilitycost = 90
    healthcost = 90
    intellectcost = 100

#Функции

#Бросок шестигранного кубика
    def dice(n = 1):
        x = 0
        for i in range(n): 
            x += renpy.random.randint(1,6)
        return(x)
#Предметы
    class Item:
        def __init__(self, name, cost, ident):
            self.name = name
            self.cost = cost
            self.ident = ident
    class Weapon:
        def __init__(self, name, cost, damage, dmgtype, ident):
            self.name = name
            self.cost = cost
            self.damage = damage
            self.ident = ident
            self.dmgtype = dmgtype
    dagger = Weapon('кинжал', 3, 3, 'normal', 'dagger')
    sword = Weapon('меч', 5, 4, 'normal', 'sword')
    heavy_sword = Weapon('тяжёлый меч', 10, 5, 'normal', 'heavy_sword')
    axe = Weapon('секира', 15, 6, 'normal', 'axe')
    magic_sword = Weapon('волшебный меч', 20, 6, 'energy', 'magic_sword')
    class Armor:
        def __init__(self, name, cost, defencebonus, ident):
            self.name = name
            self.cost = cost
            self.defencebonus = defencebonus
            self.ident = ident
    knight_armor = Armor('рыцарские доспехи', 30, 3, 'knight_armor')
    class Shield:
        def __init__(self, name, cost, defencebonus, ident):
            self.name = name
            self.cost = cost
            self.defencebonus = defencebonus
            self.ident = ident
    class MagicItem:
        def __init__(self, name, cost, bonus, ident):
            self.name = name
            self.cost = cost
            self.bonus = bonus
            self.ident = ident

    class Inventory:
        def __init__(self, money=6):
            self.money = money
            self.items = []
            self.weaponset = []
            self.armorset = []
            self.magicitems = []
            self.shieldset = []
            self.currentshield = []
            self.currentarmor = []
            self.currentweapon = []

        def buyitem(self, item):
            if self.money >= item.cost:
                self.money -= item.cost
                self.items.append(item)
                return True
            else:
                return False
        def buyweapon(self, weapon):
            if self.money >= weapon.cost:
                self.money -= weapon.cost
                self.weaponset.append(weapon)

        def sellweapon(self, weapon):
            if weapon in self.weaponset:
                self.money += weapon.cost
                self.weaponset.remove(weapon)
        def sellarmor(self, armor):
            if armor in self.armorset:
                self.money += armor.cost
                self.armorset.remove(armor)
        def sellitem(self, item):
            if item in self.items:
                self.money += item.cost
                self.items.remove(item)
        def sellmagicitem(self, magicitem):
            if magicitem in self.magicitems:
                self.money += magicitem.cost
                self.magicitems.remove(magicitem)

        def additem(self, item):
            self.items.append(item)
        def addweapon(self, weapon):
            self.weaponset.append(weapon)
        def addshield(self, shield):
            self.shieldset.append(shield)
        def addarmor(self, armor):
            self.armorset.append(shield)

        def equiparmor(self, armor):
            if len(self.currentarmor):
                self.armorset.append(self.currentarmor[0])
                self.currentarmor.remove[0]
            self.currentarmor.append(armor)
            self.armorset.remove(armor)

        def equipshield(self, shield):
            if len(self.currentshield):
                self.shieldset.append(self.currentshield[0])
                self.currentshield.remove[0]
            self.currentshield.append(shield)
            self.shieldset.remove(shield)

        def equipweapon(self, weapon):
            if len(self.currentweapon):
                self.weaponset.append(self.currentweapon)
                self.currentweapon.remove[0]
            self.currentweapon.append(weapon)
            self.weaponset.remove(weapon)

    backpack = Inventory()

    

#Заклинания
    class Spell:
        def __init__(self, name, manacost, type, ident):
            self.name = name
            self.manacost = manacost
            self.type = type
            self.ident = ident
    class SpellsKnown:
        def __init__(self):
            self.spells = []
        def learnspell(self, spell):
            if learn() == True:
                if spell in self.spells:
                    return(False)
                else:
                    self.spells.append(spell)
                    return(True)
            else:
                return(False)
        def addspell(self, spell):
            self.spells.append(spell)
    
    spellbook = SpellsKnown()
    fire_fingers_spell = Spell('Огненные Пальцы', 5, 'fire', 'fire_fingers_spell')
    size_change_spell = Spell('Изменение Роста', 8, 'trans', 'size_change_spell')
    armor_spell = Spell('Волшебные Доспехи', 3, 'energy', 'armor_spell')
    energy_spell = Spell('Сгусток Энергии', 3, 'energy', 'energy_spell')
    noose_spell = Spell('Удавка', 10, 'energy', 'noose_spell')
    poisoned_spear_spell = Spell('Отравленное Копьё', 5, 'poison', 'poisoned_spear_spell')
    ghost_spell = Spell('Привидение', 15, 'trans', 'ghost_spell')
    fireball_spell = Spell('Огненный Шар', 6, 'fire', 'fireball_spell')
    vampire_spell = Spell('Энергетический Вампиризм', 3, 'energy', 'vampire_spell')
    lightning_spell = Spell('Молния', 6, 'lightning', 'lightning_spell')
    lightning_chain_spell = Spell('Молния-цепочка', 7, 'lightning', 'lightning_chain_spell')
    stone_skin_spell = Spell('Каменная Кожа', 5, 'stone', 'stone_skin_spell')
    ice_storm_spell = Spell('Ледяной Смерч', 8, 'ice', 'ice_storm_spell')
    transmutation_spell = Spell('Превращение', 25, 'trans', 'transmutation_spell')
    fire_skin_spell = Spell('Огненная Кожа', 15, 'fire', 'fire_skin_spell')
    healing_spell = Spell('Врачевание Ран', 3, 'energy', 'healing_spell')
    elementary_resistance_spell = Spell('Защита От Стихийных Сил', 1, 'energy', 'elementary_resistance_spell')
    healing_acceleration_spell = Spell('Ускоренное Заживление Ран', 2, 'energy', 'healing_acceleration_spell')
    false_death_spell = Spell('Ложная Смерть', 25, 'illusion', 'false_death_spell')
    death_spell = Spell('Смерть', 45, 'death', 'death_spell')

    peace_song_spell = Spell('Песня Мира', 5, 'song', 'peace_song_spell')
    lullaby_song_spell = Spell('Песня Сна', 8, 'song', 'lullaby_song_spell')
    dead_fear_song_spell = Spell('Песня Изгнания Мёртвых', 10, 'holy', 'dead_fear_song_spell')
    pain_song_spell = Spell('Песн Боли', 12, 'song', 'pain_song_spell')

    death_ring_spell = Spell('Символ Смерти (Перстень Смерти)', 0, 'death', 'death_ring_spell')

#Противники
    class Enemy:
        def __init__(self, name, attack, defence, hp, damage, damagetype, bonus, resistance, status, ident):
            self.name = name
            self.attack = attack
            self.defence = defence
            self.hp = hp
            self.damage = damage
            self.damagetype = damagetype
            self.bonus = bonus
            self.resistance = resistance
            self.status = status
            self.ident = ident
    class EnemyGroup:
        def __init__(self):
            self.band = []
        def addenemy(self, enemy):
            self.band.append(enemy)
        def killenemy(self, enemy):
            self.band.remove(enemy)
    enemies = EnemyGroup()
#База противников
    def zombie_attack():
        global defence
        global status
        r = 0
        for i in status:
            if 'ghost' in i:
                r = 1
        if r == 0:
            x = dice(2) + 1
            if x > defence:
                return(True)
            else:
                return(False)
        else:
            return(False)
            
    zombie = Enemy('Зомби', zombie_attack(), 8, 6, 4, 'normal', 5, ['song', 'death', 'illusion', 'poison', 'trans'], [], 'zombie')

    def skeleton_knight_attack():
        global defence
        global status
        r = 0
        for i in status:
            if 'ghost' in i:
                r = 1
        if r == 0:
            x = dice(2) + 1
            if x > defence:
                return(True)
            else:
                return(False)
        else:
            return(False)
    
    skeleton_knight = Enemy('Всадник-скелет', skeleton_knight_attack(), 8, 7, 5, 'normal', 6, ['song', 'death', 'illusion', 'poison', 'trans'], [], 'skeleton_knight')
    
    def ghost_attack():
        global defence
        global status
        r = 0
        for i in status:
            if 'ghost' in i:
                r = 1
        if r == 0:
            x = dice(3) + 1
            if x > defence:
                return(True)
            else:
                return(False)
        else:
            return(False)
    def ghost_damage():
        x = dice()
        return(x)
    
    ghost = Enemy('Привидение', ghost_attack, 12, 14, ghost_damage(), 'death', 15, ['song', 'death', 'illusion', 'poison', 'normal', 'trans'], [], 'ghost')

    def death_knight_attack():
        global defence
        global status
        r = 0
        for i in status:
            if 'ghost' in i:
                r = 1
        if r == 0:
            x = dice(3) + 4
            if x > defence:
                return(True)
            else:
                return(False)
        else:
            return(False)
    
    death_knight = Enemy('Рыцарь Смерти', death_knight_attack(), 15, 26, 6, 'normal', 25, ['song', 'fire', 'death', 'trans', 'holy'], [], 'death_knight')

    def vampire_attack():
        global defence
        global resistance
        global currenthlt
        r = 0
        for i in resistance:
            if 'death' in i:
                r = 1
        if r == 0:
            x = dice(3) + 3
            if x > defence:
                probe = dice()
                if probe == 6 or probe > currenthlt:
                    currenthlt -= 1
                    return(True)
                else:
                    return(False)
            else:
                return(False)
        else:
            return(False)
    
    vampire = Enemy('Вампир', vampire_attack(), 15, 28, 5, 'death', 28, ['normal', 'death'], [], 'vampire')
    enemy0 = Enemy('Вампир', vampire_attack(), 15, 28, 5, 'death', 28, ['normal', 'death'], [], 'vampire')
    enemy1 = Enemy('Вампир', vampire_attack(), 15, 28, 5, 'death', 28, ['normal', 'death'], [], 'vampire')
    enemy2 = Enemy('Вампир', vampire_attack(), 15, 28, 5, 'death', 28, ['normal', 'death'], [], 'vampire')
    currentenemy = Enemy('Вампир', vampire_attack(), 15, 28, 5, 'death', 28, ['normal', 'death'], [], 'vampire')
    def return_fight():
        global enemy0
        global enemy1
        global enemy2
        global currentenemy
        if currentenemy.ident == '0':
            enemy0 = currentenemy
        elif currentenemy.ident == '1':
            enemy1 = currentenemy
        elif currentenemy.ident == '2':
            enemy2 = currentenemy



    def hp_max_def(): #Определение максимального значения жизненных сил
        global hp_max
        global health
        hp_max = ((health * 4) + 4)

    def attack(enemy): #Определение значения атаки в бою
        global character_class
        global currentagi
        global currentstr
        global backpack
        global belovedweapon
        if character_class == 'thief' and currentagi > 9:
            if currentstr == 1:
                i = int(dice(4))
            elif currentstr == 2:
                i = int(dice(4) + 4)
            elif currentstr == 3:
                i = int(dice(4) + 8)
            elif currentstr == 4:
                i = int(dice(6))
            elif currentstr == 5:
                i = int(dice(6) + 4)
            elif currentstr == 6:
                i = int(dice(6) + 8)
            elif currentstr == 7:
                i = int(dice(8))
            elif currentstr == 8:
                i = int(dice(8) + 4)
            elif currentstr == 9:
                i = int(dice(8) + 8)
            elif currentstr == 10:
                i = int(dice(10))
            elif currentstr == 11:
                i = int(dice(10) + 4)
            elif currentstr == 12:
                i = int(dice(10) + 8)
            elif currentstr == 13:
                i = int(dice(11))
            elif currentstr == 14:
                i = int(dice(11) + 4)
            elif currentstr == 15:
                i = int(dice(11) + 8)
            elif currentstr == 16:
                i = int(dice(12))
            elif currentstr == 17:
                i = int(dice(12) + 4)
            elif currentstr == 18:
                i = int(dice(12) + 8)
        elif character_class == 'shaman':
            if currentstr == 1:
                i = int(dice())
            elif currentstr == 2:
                i = int(dice() + 2)
            elif currentstr == 3:
                i = int(dice() + 4)
            elif currentstr == 4:
                i = int(dice(2))
            elif currentstr == 5:
                i = int(dice(2) + 2)
            elif currentstr == 6:
                i = int(dice(2) + 4)
            elif currentstr == 7:
                i = int(dice(3))
            elif currentstr == 8:
                i = int(dice(3) + 2)
            elif currentstr == 9:
                i = int(dice(3) + 4)
            elif currentstr == 10:
                i = int(dice(4))
            elif currentstr == 11:
                i = int(dice(4) + 2)
            elif currentstr == 12:
                i = int(dice(4) + 4)
            elif currentstr == 13:
                i = int(dice(5))
            elif currentstr == 14:
                i = int(dice(5) + 2)
            elif currentstr == 15:
                i = int(dice(5) + 4)
            elif currentstr == 16:
                i = int(dice(6))
            elif currentstr == 17:
                i = int(dice(6) + 2)
            elif currentstr == 18:
                i = int(dice(6) + 4)
        else:
            if currentstr == 1:
                i = int(dice(2))
            elif currentstr == 2:
                i = int(dice(2) + 2)
            elif currentstr == 3:
                i = int(dice(2) + 4)
            elif currentstr == 4:
                i = int(dice(3))
            elif currentstr == 5:
                i = int(dice(3) + 2)
            elif currentstr == 6:
                i = int(dice(3) + 4)
            elif currentstr == 7:
                i = int(dice(4))
            elif currentstr == 8:
                i = int(dice(4) + 2)
            elif currentstr == 9:
                i = int(dice(4) + 4)
            elif currentstr == 10:
                i = int(dice(5))
            elif currentstr == 11:
                i = int(dice(5) + 2)
            elif currentstr == 12:
                i = int(dice(5) + 4)
            elif currentstr == 13:
                i = int(dice(6))
            elif currentstr == 14:
                i = int(dice(6) + 2)
            elif currentstr == 15:
                i = int(dice(6) + 4)
            elif currentstr == 16:
                i = int(dice(7))
            elif currentstr == 17:
                i = int(dice(7) + 2)
            elif currentstr == 18:
                i = int(dice(7) + 4)
        if character_class == 'warrior' and (backpack.currentweapon[0] in belovedweapon):
            i += int(dice())
        if i > enemy.defence:
            renpy.say(narrator, "Атака успешна.")
            if backpack.currentweapon[0].dmgtype in enemy.resistance:
                renpy.say(narrator, backpack.currentweapon[0].name + " не наносит урона. " + enemy.name + " не боится ударов обычного оружия.")
            else:    
                enemy.hp -= backpack.currentweapon[0].damage
                renpy.say(narrator, enemy.name + " теряет " + str(backpack.currentweapon[0].damage) + " ЖС.")
                if enemy.hp <= 0:
                    renpy.say(narrator, enemy.name + " убит!")
                    enemyband.killenemy(enemy)
            
        return(i)
    def defence_calc(): #Определение базового значения защиты
        global defence
        global currentagi
        global backpack
        defence = currentagi + 7
        if len(backpack.currentarmor):
            defence += backpack.currentarmor[0].defencebonus
        if len(backpack.currentshield):
            defence += backpack.currentshield[0].defencebonus
        if character_class == 'warrior' and backpack.currentweapon[0] in belovedweapon:
            defence += 2

    def trick(x): #Определение значения воровского ума при воровстве
        global character_class
        if character_class == 'thief':
            if x == 1:
                i = int(dice())
            elif x == 2:
                i = int(dice() + 2)
            elif x == 3:
                i = int(dice() + 4)
            elif x == 4:
                i = int(dice(2))
            elif x == 5:
                i = int(dice(2) + 2)
            elif x == 6:
                i = int(dice(2) + 4)
            elif x == 7:
                i = int(dice(3))
            elif x == 8:
                i = int(dice(3) + 2)
            elif x == 9:
                i = int(dice(3) + 4)
            elif x == 10:
                i = int(dice(4))
            elif x == 11:
                i = int(dice(4) + 2)
            elif x == 12:
                i = int(dice(4) + 4)
            elif x == 13:
                i = int(dice(5))
            elif x == 14:
                i = int(dice(5) + 2)
            elif x == 15:
                i = int(dice(5) + 4)
            elif x == 16:
                i = int(dice(6))
            elif x == 17:
                i = int(dice(6) + 2)
            elif x == 18:
                i = int(dice(6) + 4)
        elif character_class == 'bard':
            if x == 4:
                i = int(dice())
            elif x == 5:
                i = int(dice() + 2)
            elif x == 6:
                i = int(dice() + 4)
            elif x == 7:
                i = int(dice(2))
            elif x == 8:
                i = int(dice(2) + 2)
            elif x == 9:
                i = int(dice(2) + 4)
            elif x == 10:
                i = int(dice(3))
            elif x == 11:
                i = int(dice(3) + 2)
            elif x == 12:
                i = int(dice(3) + 4)
            elif x == 13:
                i = int(dice(4))
            elif x == 14:
                i = int(dice(4) + 2)
            elif x == 15:
                i = int(dice(4) + 4)
            elif x == 16:
                i = int(dice(5))
            elif x == 17:
                i = int(dice(5) + 2)
            elif x == 18:
                i = int(dice(5) + 4)
        return(i)
    def mana_max_def(): #Определение максимального значения магической энергии
        global intellect
        global mana_max
        global character_class
        if character_class == 'warrior':
            mana_max = intellect
        elif character_class == 'thief':
            if intellect == 1:
                mana_max = 2
            elif intellect == 2:
                mana_max = 3
            elif intellect == 3:
                mana_max = 5
            elif intellect == 4:
                mana_max = 6
            elif intellect == 5:
                mana_max = 8
            elif intellect == 6:
                mana_max = 9
            elif intellect == 7:
                mana_max = 11
            elif intellect == 8:
                mana_max = 12
            elif intellect == 9:
                mana_max = 14
            elif intellect == 10:
                mana_max = 15
            elif intellect == 11:
                mana_max = 17
            elif intellect == 12:
                mana_max = 18
            elif intellect == 13:
                mana_max = 20
            elif intellect == 14:
                mana_max = 21
            elif intellect == 15:
                mana_max = 23
            elif intellect == 16:
                mana_max = 24
            elif intellect == 17:
                mana_max = 26
            elif intellect == 18:
                mana_max = 27
        elif character_class == 'bard':
            mana_max = intellect * 2
        elif character_class == 'shaman':
            if intellect > 2:
                mana_max = (intellect - 2) * 4
            else:
                mana_max = 2

    def learn():
        global character_class
        l = dice()
        if character_class == 'warrior':
            if l > 4:
                return(True)
            else:
                return(False)
        if character_class == 'thief':
            if l > 3:
                return(True)
            else:
                return(False)
        if character_class == 'bard':
            if l > 2:
                return(True)
            else:
                return(False)
        if character_class == 'shaman':
            return(True)
    def cast(spell):
        global mana
        if spell.manacost >= mana:
            return(True)
        else:
            return(False)
    def defaultstats():
        global strength
        global agility
        global health
        global intellect
        global currentstr
        global currentagi
        global currenthlt
        global currentint
        currentstr = strength
        currentagi = agility
        currenthlt = health
        currentint = intellect
    rnd = 0
    def turn_def():
        global rnd
        global character_class
        if character_class == 'thief':
            rnd = 1
        else:
            x = 0
            y = 0
            while x == y:
                x = dice()
                y = dice()
            if x > y:
                if character_class == 'warrior':
                    rnd = 2
                else:
                    rnd = 1
            else:
                rnd = 0
    def turn():
        global rnd
        global character_class
        if rnd == 0:
            if character_class == 'warrior':
                rnd = 2
            else:
                rnd = 1
        else:
            rnd -= 1
    def enoughmana():
        global currentenemy
        global spellbook
        global mana
        for i in spellbook.spells:
            if mana >= i.manacost:
                return(True)
                break
            else:
                return(False)
    def fight_defend():
        global enemyband
        global name
        global defence
        global armor_spell_count
        global hp
        global narrator
        for i in enemyband.band:
            if ['noose'] in i.status:
                i.hp -= 1
                renpy.say(narrator, "Невидимая удавка на шее врага причиняет урон. " + i.name + " теряет 1 ЖС.")
                if i.hp <= 0:
                    renpy.say(narrator, i.name + " убит!")
            if i.hp > 0:
                renpy.say(narrator, i.name + " атакует")
                atk = i.attack
                if atk > defence:
                    hp -= i.damage
                    renpy.say(narrator, i.name + " успешно атаковал " + name + " и нанёс урон " + str(enemydamage) + ".")
                    if hp <= 0:
                        renpy.say(narrator, name + " убит!")
                        renpy.jump(game_over)
                    elif armor_spell_count > 0:
                        armor_spell_count -= 1
                        defence -= 1
                        if armor_spell_count > 0:
                            renpy.say(narrator, "Силовое поле пробито. Защита снижена до " + str(defence) + ". Осталось уровней — " + str(armor_spell_count))
                        elif armor_spell_count == 0:
                            renpy.say(narrator, "Силовое поле уничтожено. Защита снижена до " + str(defence) + ".")
                else:
                    renpy.say(narrator, "[name] отразил атаку.")
            





# The game starts here.
# screen simple_example_inventory:
#     frame xalign 1 ypos 0.01:
#         vbox:
#             text "Строка вот такая длинная"
#             text "Cnhjrf djn nfrfz lkbyyfz"
label start:
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
    "Твои характеристики: Сила — [strength], Ловкость — [agility], Здоровье — [health], Интеллект — [intellect]."
    "Твоя жизненная энергия: [hp] / [hp_max]. Твоя магическая энергя: [mana] / [mana_max]. Защита: [defence]"
    "Количество монет в кармане — [backpack.money]"
    "В руке у тебя [backpack.currentweapon[0].name] с уроном [backpack.currentweapon[0].damage]."
    "Настало время приключений!"
    nvl clear
    call choose_path
# screen grid_test:
#     grid 2 3:
#         text "[name]"
#         text "[inventory.money]]"

#         text "Сила: [strength]\nЛовкость: [agility]\nЗдоровье: [health]\nИнтеллект: [intellect]"
#         text "ЖС: [hp] / [hp_max]"

#         text ""
#         text "Нижний правый"
label choose_path:
    nvl clear
    call screen worldmap()
screen worldmap():
    tag worldmap
    use navigation
    imagemap:
        ground "images/ground.jpg"
        hover "images/hover.jpg"
        hotspot (71, 324, 60, 40) action Jump('goto_south_castle')

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
        enemy0 = Enemy('Первый Зомби', zombie_attack(), 8, 6, 4, 'normal', 5, ['song', 'death', 'illusion', 'poison', 'trans'], [], '0')
        enemy1 = Enemy('Второй Зомби', zombie_attack(), 8, 6, 4, 'normal', 5, ['song', 'death', 'illusion', 'poison', 'trans'], [], '1')
        enemy2 = Enemy('Третий Зомби', zombie_attack(), 8, 6, 4, 'normal', 5, ['song', 'death', 'illusion', 'poison', 'trans'], [], '2')
        enemyband = EnemyGroup()
        enemyband.addenemy(enemy0)
        enemyband.addenemy(enemy1)
        enemyband.addenemy(enemy2)
        turn_def()
    if rnd == 0:
        $fight_defend
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
    "Твоя магическая энергия [mana]"
menu:
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



label fire_fingers_cast:
    "[name] применяет заклинание [fire_fingers_spell.name]"
    $ mana -= fire_fingers_spell.manacost
    if 'fire' in currentenemy.resistance:
        "Заклинание не подействовало. [currentenemy.name] не боится огня."
        return
    else:
        "[currentenemy.name] теряет 5 ЖС от урона огнём"
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
        "[name] увеличил свой рост. Сила выросла, а ловкость снизилась в 2 раза."
        return
    "Уменьшить свой рост":
        $ mana -= size_change_spell.manacost
        $ currentstr = currentstr // 2
        $ currentagi = currentagi * 2
        $ defence_calc()
        "[name] уменьшил свой рост. Ловкость увелиилась, а сила снизилась в 2 раза."
        return

label armor_spell_cast:
    nvl clear
    "У тебя [mana] МЭ. Сколько создать уровней силового поля?"
    python:
        armor_spell_amount_max = mana // 3
        armor_spell_amount = renpy.input("Введи число не более [armor_spell_amount_max]")
        chck = True
        try:
            armor_spell_amount = int(armor_spell_amount)
        except ValueError:
            chck = False
    if chck == True and armor_spell_amount <= armor_spell_amount_max and armor_spell_amount_max > 0:
        $ mana -= armor_spell.manacost * armor_spell_amount
        $ defence += armor_spell_amount
        $ armor_spell_count = armor_spell_amount
        "[name] создал вокруг себя силовое поле [armor_spell_count] уровня"
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
        "Каждый встрел тратит [energy_spell.manacost] МЭ. У тебя [mana] МЭ.\nВ кого направить сгусток энергии?"
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
            "Сгусток энергии поразил врага. [enemy0.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy1.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy2.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy3.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy4.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy5.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy6.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy7.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy8.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy9.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy10.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy11.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy12.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy13.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy14.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy15.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy16.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy17.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy18.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy19.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy20.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy21.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy22.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy23.name] теряет 3 ЖС."
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
            "Сгусток энергии поразил врага. [enemy24.name] теряет 3 ЖС."
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
        "[currentenemy.name] ощущает на своей шее невидимую удавку, которая душит его, причиняя в каждм кругу ущерб в 1 ЖС, и мешает применять магиню."
        return    

label poisoned_spear_spell_cast:
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
