def round_to_plate_size(lift_weight, plate_weight):
    ''' Rounds a given lift weight down or up to the nearest weight
    achievable given a specified minimum plate weight. Don't forget
    that the smallest weight is actually your plate size * 2.
    
    ex: 
        round_to_plate_size(183.2, 5) returns 180
        round_to_plate_size(183.2, 2.5) returns 185
    '''
    two_plates = plate_weight * 2
    diff = lift_weight % two_plates

    if diff == 0:
        return lift_weight

    if diff >= float(two_plates)/2:
        #round up
        return lift_weight + two_plates - diff
    else:
        #round down
        return lift_weight - diff
