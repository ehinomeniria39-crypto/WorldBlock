import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


class BlockWorldAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        #Add your code here! Your solve method should receive
		#as input two arrangements of blocks. The arrangements
		#will be given as lists of lists. The first item in each
		#list will be the bottom block on a stack, proceeding
		#upward. For example, this arrangement:
		#
		#[["A", "B", "C"], ["D", "E"]]
		#
		#...represents two stacks of blocks: one with B on top
		#of A and C on top of B, and one with E on top of D.
		#
		#Your goal is to return a list of moves that will convert
		#the initial arrangement into the goal arrangement.
		#Moves should be represented as 2-tuples where the first
		#item in the 2-tuple is what block to move, and the
		#second item is where to put it: either on top of another
		#block or on the table (represented by the string "Table").
		#
		#For example, these moves would represent moving block B
		#from the first stack to the second stack in the example
		#above:
		#
		#("C", "Table")
		#("B", "E")
		#("C", "A")
        
		#store where each block is and what is on top of it
        block_under = {}
        block_above = {}
 
        blocks = []
        for stack in initial_arrangement:
            for index, block in enumerate(stack):
                blocks.append(block)
                block_above[block] = None
                if index == 0:
                    block_under[block] = "Table"
                else:
                    block_under[block] = stack[index - 1]
                    block_above[stack[index - 1]] = block
 
        #build goal arrangement
        goal_on = {}
        for stack in goal_arrangement:
            for index, block in enumerate(stack):
                if index == 0:
                    goal_on[block] = "Table"
                else:
                    goal_on[block] = stack[index - 1] 
                    
		
        logger.info("Solving Block World problem with %d blocks", len(blocks))
        logger.debug("Initial arrangement: %s", initial_arrangement)
        logger.debug("Goal arrangement: %s", goal_arrangement)
        logger.debug("current: %s", block_under)
        logger.debug("goal: %s", goal_on)			
		
        
        moves = []
 
        def is_clear(x):
            #table always available
            if x == "Table":
                return True
            return block_above[x] is None
 
        def is_correct(block, checked):
            if block in checked:
                return checked[block]
            current = block_under[block]
            target = goal_on[block]
            if current != target:
                checked[block] = False
                return False
            if current == "Table":
                checked[block] = True
                return True
            result = is_correct(current, checked)
            checked[block] = result
            return result
 
        def move_block(block, destination):
            old_position = block_under[block]
            if old_position != "Table":
                block_above[old_position] = None
            block_under[block] = destination
            if destination != "Table":
                block_above[destination] = block
            moves.append((block, destination))
            logger.debug("Move #%d: %s -> %s (was on %s)", len(moves), block, destination, old_position)
            
 
        #keep moving blocks until they match the goal
        iteration = 0
        while True:
            iteration += 1
            checked = {}
            wrong_blocks  = [block for block in blocks if not is_correct(block, checked)]
            if not wrong_blocks:
                break
             
            moved = False
                        
            for block in wrong_blocks:
                #find the top block
                top_block  = block
                while not is_clear(top_block ):
                    top_block  = block_above[top_block]
 
                target = goal_on[top_block]
                logger.debug("Considering block %s (climbed from %s); goal position = %s", top_block, block, target)
 
                if target == "Table":
                    move_block(top_block , "Table")
                    moved = True
                    break
                elif is_clear(target) and is_correct(target, checked):
                    logger.debug("destination %s is clear and correct; placing %s there for good", target, top_block)
                    move_block(top_block, target)
                    moved = True
                    break
                elif block_under[top_block] != "Table":
                    logger.debug("destination %s not ready yet; unstacking %s to the table", target, top_block)
                    move_block(top_block, "Table")
                    moved = True
                    break
 
            if not moved:              
                break
		
        logger.info("Solved in %d moves over %d iterations", len(moves), iteration)
        return moves


