import hlt
import logging
import random
from collections import OrderedDict

game = hlt.Game("optimus_v5")
logging.info("Starting optimus")

while True:
    game_map = game.update_map()
    command_queue = []

    team_ships = game_map.get_me().all_ships()

    for ship in team_ships:
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key = lambda t: t[0]))

        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]
        # # just enemy ships list
        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]

        entities_very_close = list(entities_by_distance.keys())

        r = random.randint(-1,4)

        if r <2 and r>=0:

            c = 0 

            for i in entities_very_close[:10]:
                if isinstance(entities_by_distance[i][0], hlt.entity.Planet) and not entities_by_distance[i][0].is_owned():
                    target_planet = entities_by_distance[i][0]
                    c+=1

                    if ship.can_dock(target_planet):
                        command_queue.append(ship.dock(target_planet))

                    else:
                        navigate_command = ship.navigate(
                                ship.closest_point_to(target_planet),
                                game_map,
                                speed=int(hlt.constants.MAX_SPEED),
                                ignore_ships=False)

                        if navigate_command:
                            command_queue.append(navigate_command)
                    
                    break        

            if c == 0:
                for i in entities_very_close:
                    if isinstance(entities_by_distance[i][0], hlt.entity.Ship) and entities_by_distance[i][0] not in team_ships:
                        target = entities_by_distance[i][0]
                        break

                    elif isinstance(entities_by_distance[i][0], hlt.entity.Planet):
                        not_own_us = 0
                        if entities_by_distance[i][0].is_owned():
                            for ii in team_ships:
                                if ii.shipid() in entities_by_distance[i][0].all_docked_ships():
                                    not_own_us+=1
                                    break
                            if not_own_us != 0:
                                target = entities_by_distance[i][0]
                                break



                navigate_command = ship.navigate(
                        ship.closest_point_to(target),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

        elif r>=2 and r<=3:
            if len(closest_empty_planets) > 0:
            
                target_planet = closest_empty_planets[0]

                if ship.can_dock(target_planet):
                    command_queue.append(ship.dock(target_planet))

                else:
                    navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)

                    if navigate_command:
                        command_queue.append(navigate_command)

            elif len(closest_enemy_ships) > 0:
                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(
                        ship.closest_point_to(target_ship),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

        else:
            our_planet = list()
            closest_non_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].is_owned()]
            for i in range(len(closest_non_empty_planets)):
                for ii in team_ships:
                    if ii.shipid() in closest_non_empty_planets[i].all_docked_ships():
                        our_planet.append(closest_non_empty_planets[i])

            if len(our_planet) !=0:

                random_our_planet = random.randint(-1,len(our_planet))

                random_our_planet_key = our_planet[random_our_planet]

                target_our_planet = our_planet[random_our_planet_key][0]
                command_queue.append(ship.dock(target_our_planet))

            else:
                target = closest_enemy_ships[0]
                navigate_command = ship.navigate(
                        ship.closest_point_to(target),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)



    game.send_command_queue(command_queue)

    # TURN END
# GAME END