import hlt
import logging
from collections import OrderedDict

game = hlt.Game("optimus_v4")
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

        # closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]
        # # just enemy ships list
        # closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]

        entities_very_close = list(entities_by_distance.keys())

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



    game.send_command_queue(command_queue)

    # TURN END
# GAME END