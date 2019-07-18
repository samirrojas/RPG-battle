#! /usr/bin/env python3

# FF proyect

import random
import time

class Personaje():

    def show_menu(self):
        x = 1
        action_list = []
        for item in player.menu:        # attributes defined in sub-classes
            print(str(x) + '.', item)
            action_list.append(player.menu[item])
            x += 1
        return action_list

    def choose_special_menu(self, players, enemies):
        x = 1
        action_list = []
        for k in self.special_menu:
            print(str(x) + '.', k)
            action_list.append(self.special_menu[k])
            x += 1
        q = self.action_selection(action_list, players, enemies)
        if q:
            return q

    def action_selection(self, actions, players, enemies):
        selec = ''
        num_str = ''
        for i in range (1, len(actions) + 1):
            num_str += str(i) + ' '
        while selec not in num_str.split():
            print('\n que deseas hacer? (1 - ' + str(len(actions)) + ')')
            selec = input()
            if selec == 'q':
                battle_end = True
                return battle_end

        q = actions[int(selec) - 1](players, enemies)
        if q:
            battle_end = True
            return battle_end

    def turn(self, players, enemies):
        actions = player.show_menu()
        q = player.action_selection(actions, players, enemies)
        if q:
            return 'q'

    def affected_character_math(self, math_value, att_key, type='damage'):
        for k, v in self.stats.items():
            if k == att_key:
                att = v
                att_key = k
        att = int(att)

        if type == 'damage':
            att -= math_value
            print (self.name + "'s", att_key, '-', math_value, ' \n')
            time.sleep(1.5)
            self.stats[att_key] = att
            if att <= 0:
                att = 0
                if att_key == 'hp':
                    self.alive = False

        else:
            att += math_value
            print(self.name + "'s", att_key, '+', math_value)
            time.sleep(1)
            self.stats[att_key] = att
            if self.stats[att_key] == 'hp':
                if self.stats['hp'] > self.max_hp:
                    self.stats['hp'] = self.max_hp
            elif self.stats[att_key] == 'mp':
                if self.stats['mp'] > self.max_mp:
                    self.stats['mp'] = self.max_mp


    def cast_spell(self, players, enemies, spell_name, type='damage', target='', damage=''):

        #Check for enough mp, if not, and if spellcaster is player, show again menu to choose.
        if self.stats['mp'] < self.spell_costs[spell_name]:
            print('Not enough mp!')
            time.sleep(0.7)
            if self in players:
                self.choose_special_menu(players, enemies)

        # if the magic casted is of 'healing' type:
        else:
            if type == 'healing':
                if self in players:
                    target = get_healing_target(players)
                if target == 'q':
                    return target
                print(self.name + ' cura con ' + spell_name + ' a ' + target.name + '\n')
                heal = random.randint(0, 3)
                change_val = self.mpk + heal
                magic_att = 'hp'
                magic_type = 'healing'
                target.affected_character_math(change_val, magic_att, magic_type)
                self.affected_character_math(self.spell_costs[spell_name], 'mp', 'damage')

            elif type == 'damage':
                target = get_enemy_target(enemies)
                if target == 'q':
                    return target
                print(self.name + ' ataca con ' + spell_name + ' a ' + target.name + '\n')
                time.sleep(1)
                print('Hit!!')
                time.sleep(0.5)
                if damage == '':
                    damage = random.randint(0, 3)
                discount = self.mpk + damage - target.stats['mag_dfns']
                if self.name == 'Guerrero' or self.name == 'Caballero':
                    discount = self.atk + damage - target.stats['dfns']
                change_val = discount
                magic_att = 'hp'
                magic_type = 'damage'
                target.affected_character_math(change_val, magic_att, magic_type)
                self.affected_character_math(self.spell_costs[spell_name], 'mp', 'damage')

    def atack(self, players, enemies, preset_target=''):
        '''check who is atacking, player or enemy,
        and get respective target.'''

        if self in players:
            target = get_enemy_target(enemies)
        elif self in enemies:
            if preset_target == '':
                target = get_player_target(players)
            else:
                target = preset_target
        if target == 'q':
            q = True
            return q

        # generate atack
        print(self.name + ' ataca a ' + target.name)
        time.sleep(0.5)

        # miss random chance
        miss = random.randint(0, 20)
        if miss > self.miss_rate:
            print('Hit!!')
            time.sleep(0.7)
            discount = self.atk

            # sepcial random chance
            hit = random.randint(0,20)
            if hit > 14:
                self.atk += 3
                print('Special!!'.upper() + '\n')
                time.sleep(0.9)
                discount = self.atk
                self.atk -= 3

            discount -= target.stats['dfns']
            target.affected_character_math(discount, 'hp', 'damage')
        else:
            print('Miss!!' + '\n')
            time.sleep(1.5)

    def defend(self, players, enemies):
        print(self.name + ' se defiende.')

    def item(self, players, enemies):
        for k, v in self.items.items():
            print(k + ': ', v)
        print('usando un item en ' + target.name)


class Guerrero(Personaje):
    def __init__(self):
        self.name = 'Guerrero'
        self.hp = 30
        self.max_hp = 30
        self.max_mp = 15
        self.mp = 15
        self.atk = 8
        self.mpk = 7
        self.dfns = 2
        self.mag_dfns = 1
        self.time = 3
        self.miss_rate = 3
        self.alive = True
        self.atk_special1_cost = 4
        self.atk_special2_cost = 6

        self.stats = {'name': self.name, 'hp': self.hp,'hp max': self.max_hp, 'mp': self.mp, 'mp max':self.max_mp,
                      'atk': self.atk, 'mpk': self.mpk, 'dfns': self.dfns, 'mag_dfns':self.mag_dfns, 'time': self.time}

        self.special_menu = {'Atake Especial 1': self.atk_special1, 'Atake Especial 2': self.atk_special2,
                             'Regresar':self.turn}

        self.menu = {'Atacar': self.atack, 'Atake Especial': self.choose_special_menu, 'Defender': self.defend,
                     'Item': self.item}

        self.spell_costs = {'Atake Especial 1': self.atk_special1_cost, 'Atake Especial 2': self.atk_special2_cost}

        self.items = {'Potion': 2, 'Ether': 2}


    def atk_special1(self, players, enemies):
        self.cast_spell(players, enemies, 'Atake Especial 1', 'damage', damage=3)

    def atk_special2(self, players, enemies):
        self.cast_spell(players, enemies, 'Atake Especial 2', 'damage', damage=5)


class Caballero(Personaje):
    def __init__(self):
        self.name = 'Caballero'
        self.hp = 40
        self.mp = 10
        self.max_hp = 40
        self.max_mp = 10
        self.atk = 10
        self.mpk = 7
        self.dfns = 3
        self.mag_dfns = 0
        self.time = 3
        self.miss_rate = 3
        self.alive = True
        self.atk_special1_cost = 6
        self.atk_special2_cost = 8


        self.stats = {'name': self.name, 'hp': self.hp, 'hp max': self.max_hp, 'mp': self.mp, 'mp max': self.max_mp,
                      'atk': self.atk, 'mpk': self.mpk, 'dfns': self.dfns, 'mag_dfns': self.mag_dfns, 'time': self.time}

        self.special_menu = {'Atake Especial 1': self.atk_special1, 'Atake Especial 2': self.atk_special2,
                             'Regresar': self.turn}

        self.menu = {'Atacar': self.atack, 'Especial': self.choose_special_menu, 'Defender': self.defend,
                     'Item': self.item}

        self.spell_costs = {'Atake Especial 1': self.atk_special1_cost, 'Atake Especial 2': self.atk_special2_cost}

        self.items = {'Potion': 2, 'Ether': 2}


    def atk_special1(self, players, enemies):
        self.cast_spell(players, enemies, 'Atake Especial 1', 'damage', damage=5)

    def atk_special2(self, players, enemies):
        self.cast_spell(players, enemies, 'Atake Especial 2', 'damage', damage=7)


class MagoBlanco(Personaje):
    def __init__(self):
        self.name = 'Mago Blanco'
        self.hp = 15
        self.mp = 40
        self.max_hp = 15
        self.max_mp = 40
        self.atk = 6
        self.mpk = 7
        self.dfns = 1
        self.mag_dfns = 2
        self.time = 3
        self.miss_rate = 3
        self.alive = True
        self.cure1_cost = 7
        self.cure2_cost = 12

        self.stats = {'name': self.name, 'hp': self.hp, 'hp max': self.max_hp, 'mp': self.mp, 'mp max': self.max_mp,
                      'atk': self.atk, 'mpk': self.mpk, 'dfns': self.dfns, 'mag_dfns': self.mag_dfns, 'time': self.time}

        self.special_menu = {'Cure 1': self.cure1, 'Cure 2': self.cure2, 'Regresar':self.turn}

        self.menu = {'Atacar': self.atack, 'Magia Blanca': self.choose_special_menu, 'Defender': self.defend,
                     'Item': self.item}

        self.spell_costs = {'Cure 1':self.cure1_cost, 'Cure 2':self.cure2_cost}

        self.items = {'Potion': 2, 'Ether': 2}


    def cure1(self, players, enemies):
        self.cast_spell(players, enemies, 'Cure 1', 'healing')

    def cure2(self, players, enemies):
        self.cast_spell(players, enemies, 'Cure 2', 'healing')


class MagoNegro(Personaje):
    def __init__(self):
        self.name = 'Mago Negro'
        self.hp = 15
        self.mp = 40
        self.max_hp = 15
        self.max_mp = 40
        self.atk = 6
        self.mpk = 10
        self.dfns = 1
        self.mag_dfns = 3
        self.time = 3
        self.miss_rate = 3
        self.alive = True
        self.hielo_cost = 7
        self.fuego_cost = 9

        self.stats = {'name': self.name, 'hp': self.hp, 'hp max': self.max_hp, 'mp': self.mp, 'mp max': self.max_mp,
                      'atk': self.atk, 'mpk': self.mpk, 'dfns': self.dfns, 'mag_dfns': self.mag_dfns, 'time': self.time}

        self.special_menu = {'Hielo': self.hielo, 'Fuego': self.fuego, 'Regresar':self.turn}

        self.menu = {'Atacar': self.atack, 'Magia Negra': self.choose_special_menu, 'Defender': self.defend,
                     'Item': self.item}

        self.spell_costs = {'Hielo': self.hielo_cost, 'Fuego': self.fuego_cost}

        self.items = {'Potion': 2, 'Ether': 2}


    def hielo(self, players, enemies):

        self.cast_spell(players, enemies, 'Hielo', 'damage')

    def fuego(self, players, enemies):

        self.cast_spell(players, enemies, 'Fuego', 'damage')


class Enemigo(Personaje):
    def __init__(self, num):
        self.name = 'Enemigo ' + str(num)
        self.hp = 30
        self.mp = 30
        self.max_hp = 30
        self.max_mp = 30
        self.atk = 5
        self.mpk = 7
        self.dfns = 3
        self.mag_dfns = random.randint(1,3)
        self.time = 3
        self.miss_rate = 3
        self.alive = True
        self.heal_cost = 6
        self.atake_especial_2_cost = 10

        self.stats = {'name': self.name, 'hp': self.hp, 'hp max': self.max_hp, 'mp': self.mp, 'mp max':self.max_mp,
                      'atk': self.atk, 'mpk': self.mpk, 'dfns': self.dfns, 'mag_dfns':self.mag_dfns, 'time': self.time}

        self.special_menu = {'Heal': self.heal, 'atake especial 2': self.atk_special2}

        self.menu = {'Atacar': self.atack, 'Especial': self.choose_special_menu, 'Defender': self.defend, 'Item': self.item}

        self.spell_costs = {'Heal': self.heal_cost, 'Atake Especial 2': self.atake_especial_2_cost}

        self.items = {'Potion': 2, 'Ether': 2}

    def enemy_action_selection(self, players, enemies):
        '''MORE ENEMY AI HERE'''
        target = ''
        for enemy in enemies:
            if enemy.stats['hp'] < 10:
                target = enemy

        if target != '':
            self.heal(players, enemies, target)

        else:
            for player in players:
                if player.stats['hp'] < 10:
                    p_target = player
                else:
                    p_target = ''

            self.atack(players, enemies, preset_target=p_target)

    def heal(self, players, enemies, target):
        self.cast_spell(players, enemies, 'Heal', 'healing', target=target)

    def atk_special2(self):
        print('enemigo especial 2')


# global game functions
def create_enemies(num=''):
    '''Returns a list with random generated number of enemies (between 1 - 3).
    passes an optional number of enemies to create, bypassing random generated number'''

    enemies = []
    if num != '':
        my_range = int(num + 1)
    else:
        my_range = random.randint(2,4)
    for n in range(1, my_range):
        enemies.append(Enemigo(n))
        enemies[n - 1].stats['hp'] = random.randint(30, 45)
        enemies[n - 1].stats['hp max'] = enemies[n - 1].stats['hp']
        enemies[n - 1].stats['atk'] = random.randint(5, 8)
        enemies[n - 1].stats['dfns'] = random.randint(3, 5)
        enemies[n - 1].stats['time'] = random.randint(3, 5)

    return enemies

def create_players(num=''):
    '''Regresa una lista con el numero y tipo de personajes seleccionados.
    si no se pasa un num, se crean los 4 personajes standard.'''

    all_players = [Guerrero, Caballero, MagoBlanco, MagoNegro]
    actual_players = []
    if num != '':
        '''Mostrar menu de personajes a escojer'''
        print('personajes'.upper().center(20, '*'))
        x  = 0
        for p in all_players:
            x +=1
            print(str(x) + '. ' + str(p.__name__))

        '''escojer un rol por cada personaje de acuerdo al num de jugadores elegido'''
        list_of_names = []
        x = 1
        for i in range (0, num):
            selected_num = ''

            while selected_num not in '1 2 3 4'.split():
                print('\nescoje un rol por jugador ingresando un solo numero del menu: ')
                selected_num = input()
                actual_players.append(all_players[int(selected_num) - 1]())
                if actual_players[i].name not in list_of_names:
                    list_of_names.append(actual_players[i].name)
                else:
                    actual_players[i].name += str(x + 1)
                    x += 1
                print('Escogiste: ' + actual_players[i].name + '\n')
    else:
        for p in all_players:
            actual_players.append(p())


    return actual_players

def show_board(players, enemies):
    '''Show a tables with enemies' names and hp,
    and a 2nd table with player's names, hp and mp'''

    # Show Enemies.
    print('enemies'.upper().center(21, '*'))
    print('hp'.rjust(17))
    for enemy in enemies:
        if enemy.alive:
            print(enemy.name.ljust(12), (str(enemy.stats['hp']) + '/' + str(enemy.stats['hp max'])).rjust(5))
        else:
            print(enemy.name.ljust(12), 'DEAD')

    # Show Players.
    print()
    print('players'.upper().center(21, '*'))
    print('hp'.rjust(17), 'mp'.rjust(5))
    for player in players:
        if player.alive:
            print(player.name.ljust(12), (str(player.stats['hp']) + '/' +
                                          str(player.max_hp)).rjust(5), (str(player.stats['mp']) +
                                                                '/' + str(player.max_mp)).rjust(5))
        else:
            print(player.name.ljust(12), 'DEAD')

def get_player_target(players):
    '''ENEMY AI HERE
    Given enemy AI, return enemy's player target'''

    while True:
        p_index = random.randint(0,len(players) - 1)
        if players[p_index].alive:
            target_player = players[p_index]
            break

    return target_player

def get_enemy_target(enemies):
    '''If there is more than 1 enemy, let the player choose the enemy target.
    Returns player's enemy target'''

    if len(enemies) > 1:
        for x in range(len(enemies)):
            if enemies[x].alive:
                print(enemies[x].name.ljust(12), (str(enemies[x].stats['hp']) + '/' +
                                                  str(enemies[x].stats['hp max'])).rjust(5))
            else:
                print(str(x + 1) + '.', players[x].name, 'DEAD')

        enemy = ''
        enemy_str = ''
        for i in (range(1, (len(enemies) + 1))):
            enemy_str += (str(i) + ' ')

        while enemy == '':
            answer = ''
            while answer not in enemy_str.split():
                print('A quien deseas atacar? (1 - ' + str(len(enemies)) + ')')
                answer = input()
                if answer == 'q':
                    return answer
            enemy = enemies[int(answer) - 1]
            if not enemy.alive:
                print('Ese enemigo ya ha muerto.')
                enemy = ''
    else:
        enemy = enemies[0]

    return enemy

def get_healing_target(players, type='heal'):
    '''let the player select a 'healing' or 'ether' ally target.
    returns player's ally target.'''

    if type == 'heal':
        type_att = 'hp'
        max_type_att = 'hp max'
    elif type == 'ether':
        type_att = 'mp'
        max_type_att = 'mp max'
    for x in range(len(players)):
        if players[x].alive:
            print(players[x].name.ljust(12), (str(players[x].stats[type_att]) + '/' +
                                              str(players[x].stats[max_type_att])).rjust(5))
        else:
            print(str(x + 1) + '.', players[x].name, 'DEAD')
    player = ''
    while player == '':
        answer = ''
        answer_string = ''
        for i in range(1,len(players) + 1):
            answer_string += (str(i) + ' ')
        while answer not in answer_string.split():
            print('A quien deseas curar? (1 - ' + str(len(players)) + ')')
            answer = input()
            if answer == 'q':
                return answer
        player = players[int(answer) - 1]
        if not player.alive:
            print('Ese personaje ya ha muerto.')
            player = ''

    return player

def get_enemy_healing_target(enemies):
    '''ENEMY AI HERE
        Given enemy AI, return enemy's healing target ally'''
    for enemy in enemies:
        if enemy.stats['hp'] < 10:
            target_ally = enemy

    return target_ally

def play_again():
    '''Asks the user if wants to play a new battle'''

    print('\nPlay Again? (n/s)')
    again = input()
    if again == '' or again.lower().startswith('s'):
        return True
    return False

def start_conditions():
    '''sets up the starting conditions necesary to beggining a new game.
    Returns 6 variables.'''

    enemies = create_enemies() # random number (1-3) if not passed arguments
    players = create_players() # 4 characters if not passed arguments
    y = len(enemies)
    w = 0
    game_end = False
    battle_end = False
    return enemies, players, y, w, game_end, battle_end

# GAME START

enemies, players, y, w, game_end, battle_end = start_conditions()

# MAIN GAME LOOP

while not game_end:
    while not battle_end:
        x = 0
        print('\n' + ('Ronda ' + str(w + 1) + '\n').center(20))
        time.sleep(1)
        w += 1

        for player in players:
            if player.alive:
                show_board(players, enemies)
                time.sleep(1)

                # check if player has won
                if all ([enemy.alive == False for enemy in enemies]):
                    print()
                    print('You Win!!'.upper().center(30, '+'))
                    battle_end = True
                    break

                # Player's Turn
                print('\n turno del ' + player.name + '\n')
                time.sleep(1.5)
                end = player.turn(players, enemies)
                if end == 'q':
                    battle_end = True
                    break

                # check if Player has lost
                if all([player.alive == False for player in players]):
                    print()
                    print('You Loose!!'.upper().center(30, '-'))
                    battle_end = True
                    break

            # Enemy Turn
            if x < y:
                if enemies[x].alive:
                    print('\n turno de ' + enemies[x].name + '\n')
                    time.sleep(2)
                    enemies[x].enemy_action_selection(players, enemies)
                x += 1


    if play_again():
        enemies, players, y, w, game_end, battle_end = start_conditions()
    else:
        print('Gracias por jugar a "FF Proyect".')
        game_end = True