# ********************************************************
# This is an overview of Wyvern's moves and what they do
# ********************************************************

# Tail Slash (this is an automatic move when selected)
# basic attack move
# multiplies by 1.2 for attack damage
# starts at 90% accuracy
# speed can make the accuracy go up or down by 5%
# lowest accuracy can be 20% and highest can be 95%
# if it hits, it does full damage
# if it misses, it still does 50% damage


#********************************************************************************************************
#Note: bonus attacks can stay active throughout turns where the other attacks happen once you choose them.
# Wyvern's Wrath (a bonus attack that can happen during rounds through acitvation or deactivation)
# gives the wyvern +3 attack
# lasts for 2 dragon turns
# always works
# cannot stack with itself
# if it is already active and used again, nothing happens


# Wing Rush ( a bonus that can happen during rounds through activation or deactivation)
# gives the wyvern +2 speed
# lasts for 2 dragon turns
# always works
# cannot stack with itself
# if it is already active and used again, nothing happens
#*********************************************************************************************************


# Venomous Bite
# - poison move
# - starts at 75% accuracy
# - speed can make the accuracy go up or down by 5%
# - lowest accuracy can be 20% and highest can be 95%
# - if it hits, the enemy gets poisoned
# - poison takes away 2 HP at the end of the enemy's turn
# - poison lasts for 3 enemy turns
# - poison does not stack
# - if it misses, nothing happens



import random


# Base stats for the wyvern
# These are the normal values before temporary buffs are added
base_attack = 10
base_defense = 10
base_speed = 10
current_hp = 50  # changes when damage happens


# temporary stats start out the same as the base stats
# these can change when buffs are active
temporary_attack = base_attack
temporary_speed = base_speed


# Tracks whether Wyvern's Wrath is currently active
wyvern_wrath_active = False

# Tracks how many dragon turns Wyvern's Wrath has left
wyvern_wrath_turns = 0


# Tracks whether Wing Rush is currently active
wing_rush_active = False

# Tracks how many dragon turns Wing Rush has left
wing_rush_turns = 0



# This function prepares the wyvern for the start of a new turn
def start_dragon_turn():

    # global lets this function change variables that were created outside the function
    global wyvern_wrath_active, wing_rush_active, temporary_attack, temporary_speed

    # Reset temporary stats back to the normal base values
    # This prevents old bonuses from accidentally stacking again
    temporary_attack = base_attack
    temporary_speed = base_speed

    # If Wrath has no turns remaining, turn the buff off
    if wyvern_wrath_turns == 0:
        wyvern_wrath_active = False

    # if Wing Rush has no turns remaining, turn the buff off
    if wing_rush_turns == 0:
        wing_rush_active = False

    # If Wrath is still active, add +3 attack for this turn
    if wyvern_wrath_active:
        temporary_attack += 3

    # If Wing Rush is still active, add +2 speed for this turn
    if wing_rush_active:
        temporary_speed += 2



# function that handles what happens at the end of the dragon's turn
# buffs can hit 0 here, but they do not turn off until the start of the next dragon turn
def end_of_dragon_turn():

    # global lets this function change variables that were created outside the function
    global wyvern_wrath_turns, wing_rush_turns

    # if Wrath still has turns left, count it down by 1
    if wyvern_wrath_turns > 0:
        wyvern_wrath_turns -= 1

    # if Wing Rush still has turns left, count it down by 1
    if wing_rush_turns > 0:
        wing_rush_turns -= 1



# function that activates Wyvern's Wrath
def wyvern_wrath_activated():

    # global lets this function change the Wrath variables outside of the function
    global wyvern_wrath_active, wyvern_wrath_turns

    # only activate Wrath if it is not already active
    if wyvern_wrath_active == False:

        # turns Wrath on
        wyvern_wrath_active = True

        # Wrath will stay active for 2 dragon turns
        wyvern_wrath_turns = 2



# function that activates wing rush
def wing_rush_activated():

    # global lets this function change the wing rush variables outside of the function
    global wing_rush_active, wing_rush_turns

    # only activate wing rush if it is not already active
    if wing_rush_active == False:

        # turns wing rush on
        wing_rush_active = True

        # wing rush will stay active for 2 dragon turns
        wing_rush_turns = 2



# function that activates tail slash
def tail_slash_activated(opponent_speed, opponent_defense, opponent_hp):

    # Tail Slash starts at 90% accuracy
    wyvern_tail_slash_start_accuracy = 90

    # compares the wyvern's speed to the opponent's speed
    wyvern_tail_slash_speed_calc = temporary_speed - opponent_speed

    # each speed point changes the accuracy by 5%
    wyvern_tail_slash_speed_calc_update = wyvern_tail_slash_speed_calc * 5

    # updates the starting accuracy using the speed difference
    wyvern_tail_slash_start_accuracy_update = (
        wyvern_tail_slash_start_accuracy
        + wyvern_tail_slash_speed_calc_update
    )

    # accuracy cannot go above 95%
    if wyvern_tail_slash_start_accuracy_update > 95:
        wyvern_tail_slash_start_accuracy_update = 95

    # accuracy cannot go below 20%
    if wyvern_tail_slash_start_accuracy_update < 20:
        wyvern_tail_slash_start_accuracy_update = 20


    # random roll from 1 to 100 decides if the attack hits or misses
    random_hit_miss = random.randint(1, 100)

    # if the random roll falls inside the final accuracy, Tail Slash hits
    if random_hit_miss <= wyvern_tail_slash_start_accuracy_update:

        # Tail Slash does 1.2 times the Wyvern's attack for this turn
        attack_damage_update = temporary_attack * 1.2

        # opponent defense is taken away from the attack damage
        final_damage = attack_damage_update - opponent_defense

        # damage cannot go below 0
        if final_damage < 0:
            final_damage = 0

        # takes the damage away from the opponent's hp
        opponent_hp -= final_damage

        # keeps the opponent's hp from going below 0
        if opponent_hp < 0:
            opponent_hp = 0

        # sends the updated hp back
        return opponent_hp


    else:

        # Tail Slash misses, so it only does 50% damage
        attack_damage_update = temporary_attack * 1.2

        # cuts the damage in half
        attack_damage_update *= 0.5

        # opponent defense still reduces the damage
        final_damage = attack_damage_update - opponent_defense

        # damage cannot go below 0
        if final_damage < 0:
            final_damage = 0

        # subtracts the reduced damage from the opponent's HP
        opponent_hp -= final_damage

        # keeps the opponent's hp from going below 0
        if opponent_hp < 0:
            opponent_hp = 0

        # sends the updated hp back
        return opponent_hp



# keeps track of whether the opponent is poisoned
opponent_poisoned = False
opponent_poison_turns = 0



# function that handles Venomous Bite
def venomous_bite_activated(opponent_speed):

    # global lets this function change the poison variables outside the function
    global opponent_poisoned, opponent_poison_turns

    # Venomous Bite starts at 75% accuracy
    venomous_bite_start_accuracy = 75

    # compares the Wyvern's current speed to the opponent's speed
    venomous_bite_speed_calc = temporary_speed - opponent_speed

    # each speed point changes accuracy by 5%
    venomous_bite_speed_update = venomous_bite_speed_calc * 5

    # updates the accuracy based on the speed difference
    venomous_bite_accuracy_update = (
        venomous_bite_start_accuracy
        + venomous_bite_speed_update
    )

    # accuracy cannot go above 95%
    if venomous_bite_accuracy_update > 95:
        venomous_bite_accuracy_update = 95

    # accuracy cannot go below 20%
    if venomous_bite_accuracy_update < 20:
        venomous_bite_accuracy_update = 20

    # random roll decides if Venomous Bite hits or misses
    random_hit_miss = random.randint(1, 100)

    # if the roll is inside the accuracy range, the bite hits
    if random_hit_miss <= venomous_bite_accuracy_update:

        # poison does not stack if the opponent is already poisoned
        if opponent_poisoned == False:

            # turns poison on
            opponent_poisoned = True

            # poison lasts for 3 enemy turns
            opponent_poison_turns = 3



# handles poison at the end of the opponent's turn
def opponent_poison_damage(opponent_hp):

    # global lets this function change the poison variables outside the function
    global opponent_poisoned, opponent_poison_turns

    # poison does 2 damage at the end of the opponent's turn
    if opponent_poisoned == True and opponent_poison_turns > 0:

        # takes 2 hp from the opponent
        opponent_hp -= 2

        # counts down one poison turn
        opponent_poison_turns -= 1

        # keeps the opponent's HP from going below 0
        if opponent_hp < 0:
            opponent_hp = 0

    # turns poison off once all 3 turns are finished
    if opponent_poison_turns == 0:
        opponent_poisoned = False

    # sends the updated opponent HP back
    return opponent_hp



#-------------------------------------------------------------------------------------------#


# keeps track of the dragon's current battle stats
dragon_state = {
    "hp": current_hp,
    "speed": temporary_speed,
    "defense": base_defense
}


# keeps track of the enemy's current battle stats
enemy_state = {
    "hp": 30,
    "speed": 8,
    "defense": 4
}



########################## ROUND ROBIN ###################################


# every action can use up to 3 seconds before moving to the back of the queue
time_quantum = 3


# this list holds all of the actions waiting to be completed
action_queue = []



########################## ADD ACTIONS TO QUEUE ###################################


# this function creates a new action and adds it to the queue
def add_action_to_queue(owner, action, execution_time):

    # makes a new dictionary every time an action is chosen
    new_action = {
        "owner": owner,
        "action": action,
        "original_time": execution_time,
        "remaining_time": execution_time
    }

    # adds the new action to the back of the queue
    action_queue.append(new_action)



########################## FINISHED ACTIONS ###################################


# this function checks which action finished and runs that action
def execute_finished_action(current_action):

    # checks if the finished action belongs to the dragon
    if current_action["owner"] == "dragon":

        # checks if the finished action is Tail Slash
        if current_action["action"] == "Tail Slash":

            # runs Tail Slash and updates the enemy hp
            enemy_state["hp"] = tail_slash_activated(
                enemy_state["speed"],
                enemy_state["defense"],
                enemy_state["hp"]
            )


        # checks if the finished action is Wyvern's Wrath
        elif current_action["action"] == "Wyvern's Wrath":

            # turns Wyvern's Wrath on
            wyvern_wrath_activated()


        # checks if the finished action is Wing Rush
        elif current_action["action"] == "Wing Rush":

            # turns Wing Rush on
            wing_rush_activated()


        # checks if the finished action is Venomous Bite
        elif current_action["action"] == "Venomous Bite":

            # runs Venomous Bite using the enemy's current speed
            venomous_bite_activated(
                enemy_state["speed"]
            )


    # checks if the finished action belongs to the enemy
    elif current_action["owner"] == "enemy":

        # this is where enemy attacks can be connected later
        if current_action["action"] == "Claw Attack":

            # enemy Claw Attack will be added here once we have the enemy attack
            pass



########################## ROUND ROBIN SCHEDULER ###################################


# handles one action at a time using Round Robin scheduling
def round_robin_scheduler():

    # if there is nothing in the queue, there is nothing to run
    if len(action_queue) == 0:
        return

    # takes the first action out of the queue
    current_action = action_queue.pop(0)

    # if the action can finish during this time quantum
    if current_action["remaining_time"] <= time_quantum:

        # the action is finished
        current_action["remaining_time"] = 0

        # runs the action now that it is finished
        execute_finished_action(current_action)

        # since it finished, it does not go back into the queue


    else:

        # subtracts one full quantum from the remaining time
        current_action["remaining_time"] -= time_quantum

        # puts the unfinished action at the back of the queue
        action_queue.append(current_action)



########################## PLAYER CHOICES ###################################


# these functions will eventually connect to the pygame buttons or player choices


# adds Tail Slash to the queue when the player chooses it
def choose_tail_slash():

    # Tail Slash takes 7 seconds to completely finish
    add_action_to_queue(
        "dragon",
        "Tail Slash",
        7
    )


# adds Wyvern's Wrath to the queue when the player chooses it
def choose_wyverns_wrath(execution_time):

    # adds Wyvern's Wrath to the queue
    add_action_to_queue(
        "dragon",
        "Wyvern's Wrath",
        execution_time
    )


# adds Wing Rush to the queue when the player chooses it
def choose_wing_rush(execution_time):

    # adds Wing Rush to the queue
    add_action_to_queue(
        "dragon",
        "Wing Rush",
        execution_time
    )


# adds Venomous Bite to the queue when the player chooses it
def choose_venomous_bite(execution_time):

    # adds Venomous Bite to the queue
    add_action_to_queue(
        "dragon",
        "Venomous Bite",
        execution_time
    )



########################## ENEMY CHOICES ###################################


# adds an enemy Claw Attack to the queue
def choose_enemy_claw(execution_time):

    # adds the enemy Claw Attack to the queue
    add_action_to_queue(
        "enemy",
        "Claw Attack",
        execution_time
    )



########################## END OF ENEMY TURN ###################################


# handles anything that needs to happen after the enemy finishes a turn
def finish_enemy_turn():

    # poison damage happens at the end of the enemy's turn
    enemy_state["hp"] = opponent_poison_damage(
        enemy_state["hp"]
    )