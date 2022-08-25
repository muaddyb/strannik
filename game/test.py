import random
class Enemy:
    def __init__(self, name, attack, llist):
        self.name = name
        self.attack = attack
        self.llist = llist
def attack():
    x = random.randint(1, 15)
    print('function executed')
    return(x)
enemy0 = Enemy('Orc', attack(), [])
enemy0.llist.append(['test'])
if ['test'] in enemy0.llist:
    print('Found')
class EnemyList:
    def __init__(self):
        self.bunch = []
enemybunch = EnemyList()
enemybunch.bunch.append(enemy0)
enemybunch.bunch[0].name = 'Changed'
print(enemy0.name)
print(enemybunch.bunch[0].name)
enemy0.name = 'Changed Again'
print(enemy0.name)
print(enemybunch.bunch[0].name)
##
# label green_breeze_peninsula_1:
#     "Тебе повстречались три безмозглых зомби"
#     python:
#         enemy0 = Enemy('Первый Зомби', zombie_attack(), 8, 6, 4, 'normal', 5, ['song', 'death', 'illusion', 'poison', 'trans'], [], 'zombie')
#         enemy1 = Enemy('Второй Зомби', zombie_attack(), 8, 6, 4, 'normal', 5, ['song', 'death', 'illusion', 'poison', 'trans'], [], 'zombie')
#         enemy2 = Enemy('Третий Зомби', zombie_attack(), 8, 6, 4, 'normal', 5, ['song', 'death', 'illusion', 'poison', 'trans'], [], 'zombie')
#         turn_def()
#     if rnd == 0:
#         jump green_breeze_peninsula_1_defend
#     else:
#         jump green_breeze_peninsula_1_fight

# label green_breeze_peninsula_1_fight:
#     if enemy1.hp <= 0 and enemy0.hp <= 0 and enemy2.hp <= 0:
#         jump green_breeze_peninsula_1_win
#     if rnd == 0:
#         jump green_breeze_peninsula_1_defend 
# menu:
#     "[enemy0.name] / [enemy0.hp]" if enemy0.hp > 0:
#         jump green_breeze_peninsula_1_fight_0
#     "[enemy1.name] / [enemy1.hp]" if enemy1.hp > 0:
#         jump green_breeze_peninsula_1_fight_1
#     "[enemy2.name] / [enemy2.hp]" if enemy2.hp > 0:
#         jump green_breeze_peninsula_1_fight_2

# label green_breeze_peninsula_1_fight_0:
# menu:
#     "Атаковать [enemy0.name]":
#         jump green_breeze_peninsula_1_fight_attack_0
# label green_breeze_peninsula_1_fight_attack_0:
#     nvl clear
#     "[name] атакует [enemy0.name]"
#     python:
#         atk = attack()
#     if atk > enemy0.defence:
#         $ enemy0.hp -= damage
#         "[name] успешно атаковал [enemy0.name] и нанёс урон [damage]."
#         if enemy0.hp <= 0:
#             "[enemy0.name] убит!"
#     else:
#         "[enemy0.name] отразил атаку."
#     $ turn()
#     jump green_breeze_peninsula_1_fight

# label green_breeze_peninsula_1_fight_1:
# menu:
#     "Атаковать [enemy1.name]":
#         jump green_breeze_peninsula_1_fight_attack_1
# label green_breeze_peninsula_1_fight_attack_1:
#     nvl clear
#     "[name] атакует [enemy1.name]"
#     python:
#         atk = attack()
#     if atk > enemy1.defence:
#         $ enemy1.hp -= damage
#         "[name] успешно атаковал [enemy1.name] и нанёс урон [damage]."
#         if enemy1.hp <= 0:
#             "[enemy1.name] убит!"
#     else:
#         "[enemy1.name] отразил атаку."
#     $ turn()
#     jump green_breeze_peninsula_1_fight

# label green_breeze_peninsula_1_fight_2:
# menu:
#     "Атаковать [enemy2.name]":
#         jump green_breeze_peninsula_1_fight_attack_2
# label green_breeze_peninsula_1_fight_attack_2:
#     nvl clear
#     "[name] атакует [enemy2.name]"
#     python:
#         atk = attack()
#     if atk > enemy2.defence:
#         $ enemy2.hp -= damage
#         "[name] успешно атаковал [enemy2.name] и нанёс урон [damage]."
#         if enemy2.hp <= 0:
#             "[enemy2.name] убит!"
#     else:
#         "[enemy2.name] отразил атаку."
#     $ turn()
#     jump green_breeze_peninsula_1_fight

# label green_breeze_peninsula_1_defend:
#     if enemy0.hp > 0:
#         "[enemy0.name]] атакует"
#         $ atk = enemy0.attack
#         if atk > defence:
#             $ hp -= enemy0.damage
#             "[enemy0.name] успешно атаковал [name] и нанёс урон [enemy0.damage]."
#             if hp <= 0:
#                 "[name] убит!"
#                 jump game_over
#         else:
#             "[name] отразил атаку."
#     if enemy1.hp > 0:
#         if enemy1.hp > 0:
#             "[enemy1.name] атакует"
#             $ atk = enemy1.attack
#         if atk > defence:
#             $ hp -= enemy1.damage
#             "[enemy1.name] успешно атаковал [name] и нанёс урон [enemy1.damage]."
#             if hp <= 0:
#                 "[name] убит!"
#                 jump game_over
#         else:
#             "[name] отразил атаку."
#     if enemy2.hp > 0:
#         if enemy2.hp > 0:
#             "[enemy2.name] атакует"
#             $ atk = enemy2.attack
#         if atk > defence:
#             $ hp -= enemy2.damage
#             "[enemy2.name] успешно атаковал [name] и нанёс урон [enemy2.damage]."
#             if hp <= 0:
#                 "[name] убит!"
#                 jump game_over
#         else:
#             "[name] отразил атаку."
#     $ turn()
#     jump green_breeze_peninsula_1_fight

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
size_change_spell = Spell('Увеличение Роста', 8, 'trans', 'size_change_spell')
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

