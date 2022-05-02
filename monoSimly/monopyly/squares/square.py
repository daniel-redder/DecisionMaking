import copy


class Square(object):
    '''
    A base class for squares on the Monopoly board.
    '''
    class Name(object):
        '''
        An 'enum' for the squares on the board.
        '''
        GO = "Go"
        OLD_KENT_ROAD = "Old Kent Road"
        COMMUNITY_CHEST = "Community Chest"
        WHITECHAPEL_ROAD = "Whitechapel Road"
        INCOME_TAX = "Income Tax"
        KINGS_CROSS_STATION = "Kings Cross Station"
        THE_ANGEL_ISLINGTON = "The Angel Islington"
        CHANCE = "Chance"
        EUSTON_ROAD = "Euston Road"
        PENTONVILLE_ROAD = "Pentonville Road"
        JAIL = "Jail"
        PALL_MALL = "Pall Mall"
        ELECTRIC_COMPANY = "Electric Company"
        WHITEHALL = "Whitehall"
        NORTHUMBERLAND_AVENUE = "Northumberland Avenue"
        MARYLEBONE_STATION = "Marylebone Station"
        BOW_STREET = "Bow Street"
        MARLBOROUGH_STREET = "Marlborough Street"
        VINE_STREET = "Vine Street"
        FREE_PARKING = "Free Parking"
        STRAND = "Strand"
        FLEET_STREET = "Fleet Street"
        TRAFALGAR_SQUARE = "Trafalgar Square"
        FENCHURCH_STREET_STATION = "Fenchurch Street Station"
        LEICESTER_SQUARE = "Leicester Square"
        COVENTRY_STREET = "Coventry Street"
        WATER_WORKS = "Water Works"
        PICCADILLY = "Piccadilly"
        GO_TO_JAIL = "Go To Jail"
        REGENT_STREET = "Regent Street"
        OXFORD_STREET = "Oxford Street"
        BOND_STREET = "Bond Street"
        LIVERPOOL_STREET_STATION = "Liverpool Street Station"
        PARK_LANE = "Park Lane"
        SUPER_TAX = "Super Tax"
        MAYFAIR = "Mayfair"
        hold_dic = [
            OLD_KENT_ROAD,
            WHITECHAPEL_ROAD,
            KINGS_CROSS_STATION,
            THE_ANGEL_ISLINGTON,
            EUSTON_ROAD,
            PENTONVILLE_ROAD,
            PALL_MALL,
            ELECTRIC_COMPANY,
            WHITEHALL,
            NORTHUMBERLAND_AVENUE,
            MARYLEBONE_STATION,
            BOW_STREET,
            MARLBOROUGH_STREET,
            VINE_STREET,
            STRAND,
            FLEET_STREET,
            TRAFALGAR_SQUARE,
            FENCHURCH_STREET_STATION,
            LEICESTER_SQUARE,
            COVENTRY_STREET,
            WATER_WORKS,
            PICCADILLY,
            REGENT_STREET,
            OXFORD_STREET,
            BOND_STREET,
            LIVERPOOL_STREET_STATION,
            PARK_LANE,
            MAYFAIR
        ]



    def __init__(self, name):
        '''
        The 'constructor'.
        '''
        self.name = name


    async def landed_on(self, game, player):
        '''
        Must be overridden in derived classes.
        '''
        raise Exception("landed_on() not implemented")

    def __str__(self):
        '''
        String representation of the Square, ie its name.
        '''
        return self.__repr__()

    def __repr__(self):
        '''
        String representation of the Square, ie its name.
        '''
        return self.name
