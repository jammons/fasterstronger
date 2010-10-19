def round_to_plate_size(lift_weight, plate_weight):
    ''' Rounds a given lift weight down or up to the nearest weight
    achievable given a specified minimum plate weight 
    
    ex: 
        round_to_plate_size(183.2, 5) returns 185
        round_to_plate_size(183.2, 2.5) returns 182.5
    '''
    diff = lift_weight % plate_weight

    if diff == 0:
        return lift_weight

    if diff >= float(plate_weight)/2:
        #round up
        return lift_weight + plate_weight - diff
    else:
        #round down
        return lift_weight - diff
