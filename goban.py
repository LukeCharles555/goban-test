import enum

block = []
liberties = []

class Status(enum.Enum):
    """
    Enum representing the Status of a position on a goban
    """

    WHITE = 1
    BLACK = 2
    EMPTY = 3
    OUT = 4


class Goban(object):
    def __init__(self, goban):
        self.goban = goban

    def get_status(self, x, y):
        """
        Get the status of a given position

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            a Status
        """
        if (
            not self.goban
            or x < 0
            or y < 0
            or y >= len(self.goban)
            or x >= len(self.goban[0])
        ):
            return Status.OUT
        elif self.goban[y][x] == ".":
            return Status.EMPTY
        elif self.goban[y][x] == "o":
            return Status.WHITE
        elif self.goban[y][x] == "#":
            return Status.BLACK

    '''
    Check if captured by recursively going round the board and checking neighbours
    This will add to two arrays (block, and liberties). Idea of if there are no liberties/freedoms, stone will be captured

    Args:
        - x: x coordinate
        - y: y coordinate

    Returns: A boolean
    '''
    def check_if_captured(self, x, y):
        ix = 1
        iy = 1

        initStoneStatus = self.get_status(x, y)

        # Go round the Goban board
        while (ix < len(self.goban[0]) and iy < len(self.goban)):
            # If there is a liberty, append array
            if (self.get_status(x, y+iy) == Status.EMPTY):
                liberties.append([x, y+iy])
                break
            elif (self.get_status(x+ix, y) == Status.EMPTY):
                liberties.append([x+ix, y])
                break
            elif (self.get_status(x-ix, y) == Status.EMPTY):
                liberties.append([x-ix, y])
                break
            elif (self.get_status(x, y-iy) == Status.EMPTY):
                liberties.append([x, y-iy])
                break
            # If this is a block of coloured stones, append to the group array
            elif (self.get_status(x, y-iy) == initStoneStatus and [x, y-iy] not in block):
                block.append([x, y-iy])
                iy -= 1
                continue
            elif (self.get_status(x+ix, y) == initStoneStatus and [x+ix, y] not in block):
                block.append([x+ix, y])
                ix += 1
                continue
            elif (self.get_status(x-ix, y) == initStoneStatus and [x-ix, y] not in block):
                block.append([x-ix, y])
                ix -= 1
                continue
            elif (self.get_status(x, y+iy) == initStoneStatus and [x, y+iy] not in block):
                block.append([x, y+iy])
                iy += 1
                continue
            else:
                block.append([x, y])
                liberties.clear()
                break
        
        # This just means that block/stone is surrounded
        if (len(liberties) == 0):
            return True
        # Return not captured by default scenario
        else:
            return False




    def is_taken(self, x, y):
        """
        Runs the Goban and position played through the scenarios

        Args:
            x: The x coordinate of the stone
            y: The y coordinate of the stone

        Returns:
            A boolean of True or False
        """
        return self.check_if_captured(x, y)
