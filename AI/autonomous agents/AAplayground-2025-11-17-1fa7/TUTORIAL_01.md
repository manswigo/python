# Tutorial 1: Autonomous Drone for Planting

Welcome! In this challenge, you'll program an autonomous drone to plant seeds across a field. The drone automatically plants seeds at every position it visits, so your task is to write an agent that efficiently covers the entire field.

## Goal

**Cover all farmable tiles in the field to maximize grown crops!**

Your drone automatically plants seeds wherever it moves, and crops grow over time. The more ground you cover, the more crops will grow to full maturity.

---

## Step 1: Installation

See the [AAplayground README](./README.md) for installation instructions. Make sure you have Python 3.10+ and the required dependencies installed.

## Step 2: Play Manually (Keyboard Control)

Before writing an agent, try controlling the drone yourself to understand the game.

### Run the Game
```bash
python run_planting.py
```

### Controls
- **Arrow keys** - Move the drone (UP, DOWN, LEFT, RIGHT)
- **. (period)** - Wait/stay in place
- **Esc** - Quit the game

### Automatic Planting
Notice that **seeds are planted automatically** at every position you visit. You don't need to press any planting button - just move around and explore!


## Step 3: Run the Random Agent

Let's see how an autonomous agent works by running the sample random agent.

```bash
python run_planting.py --controller sample_agents.random_agent:RandomAgent
```

**What happens:**
- The agent moves in random directions
- Seeds are automatically planted at each position
- Crops grow over time
- At the end, you'll see stats like total grown plots


## Step 4: Write Your Own Agent

Now it's time to create your own agent! Your goal is to write an agent that covers all farmable tiles efficiently.

### Create Your Agent File

Create a new file `my_agent.py` in the `sample_agents/` directory:

```python
"""
my_agent.py

Author: Your Name <your.email@example.com>
Description: My first autonomous drone agent for field coverage.
"""

from aa_playground import BaseAgent, Action, ActionType, Direction, Observation


class MyDroneAgent(BaseAgent):
    """Agent that explores the field systematically."""
    
    def __init__(self, name: str = "MyDrone") -> None:
        super().__init__(name=name)
        # Initialize any state your agent needs here
        # For example, you might want to track visited positions
        self.visited = set()
    
    def decide(self, observation: Observation):
        """
        Decide the next action based on the observation.
        
        Args:
            observation: Contains information about the current state:
                - observation.position: Current (x, y) position
                - observation.tiles: Dict of nearby tiles
                - observation.turn: Current turn number
                - observation.width: Field width
                - observation.height: Field height
        
        Returns:
            An Action with movement direction
        """
        # Mark current position as visited
        self.visited.add(observation.position)
        
        # Get current position
        x, y = observation.position
        
        # Check which neighbors are available
        # observation.tiles contains only nearby tiles (current + 4 neighbors)
        # Each tile is a dict like: {"terrain": "empty"} or {"terrain": "obstacle"}
        
        # Try to move right if possible
        right_pos = (x + 1, y)
        if right_pos in observation.tiles:
            terrain = observation.tiles[right_pos].get("terrain", "")
            if terrain not in ("obstacle", "base") and right_pos not in self.visited:
                return Action(ActionType.MOVE, direction=Direction.RIGHT)
        
        # Try other directions...
        # DOWN
        down_pos = (x, y + 1)
        if down_pos in observation.tiles:
            terrain = observation.tiles[down_pos].get("terrain", "")
            if terrain not in ("obstacle", "base") and down_pos not in self.visited:
                return Action(ActionType.MOVE, direction=Direction.DOWN)
        
        # LEFT
        left_pos = (x - 1, y)
        if left_pos in observation.tiles:
            terrain = observation.tiles[left_pos].get("terrain", "")
            if terrain not in ("obstacle", "base") and left_pos not in self.visited:
                return Action(ActionType.MOVE, direction=Direction.LEFT)
        
        # UP
        up_pos = (x, y - 1)
        if up_pos in observation.tiles:
            terrain = observation.tiles[up_pos].get("terrain", "")
            if terrain not in ("obstacle", "base") and up_pos not in self.visited:
                return Action(ActionType.MOVE, direction=Direction.UP)
        
        # If all nearby unvisited tiles are blocked, try any valid move
        for direction in [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]:
            dx, dy = direction.delta()
            next_pos = (x + dx, y + dy)
            if next_pos in observation.tiles:
                terrain = observation.tiles[next_pos].get("terrain", "")
                if terrain not in ("obstacle", "base"):
                    return Action(ActionType.MOVE, direction=direction)
        
        # Can't move anywhere, wait
        return Action(ActionType.WAIT)
```

### Understanding the Observation

Your agent receives an `Observation` object with:

- **`position`**: Current (x, y) coordinates
- **`tiles`**: Dictionary of nearby tiles (current position + 4 neighbors)
  - Each tile is a dict: `{"terrain": "terrain_type"}`
- **`turn`**: Current turn number
- **`width`, `height`**: Field dimensions (useful for planning)
- **`inventory`**: Your items (seeds are infinite)

### Terrain Types

The `terrain` value in each tile can be:
- `"empty"` - Farmable soil (safe to move)
- `"seed"` - Recently planted
- `"growing"` - Crop growing
- `"ready"` - Fully grown crop
- `"obstacle"` - Tree/obstacle (cannot move here)
- `"base"` - Launch pad

### Test Your Agent

Run your agent in the game:

```bash
python run_planting.py --controller sample_agents.my_agent:MyDroneAgent 
```

---

## Step 5: Improve Your Strategy

### Challenge: Cover ALL Farmable Tiles

Your goal is to visit every farmable position in the field. Think about:

1. **Systematic Coverage**: Can you move in a pattern (like a lawnmower)?
2. **Avoid Obstacles**: Navigate around trees efficiently
3. **Don't Get Stuck**: Have a strategy when blocked
4. **Track Progress**: Remember where you've been

### Tips

- **Use the field dimensions**: `observation.width` and `observation.height`
- **Track visited positions**: Use a set to remember where you've been
- **Plan ahead**: Think about coverage patterns
- **Local vision**: Remember you can only see adjacent tiles

### Experiment with Different Field Sizes

```bash
# Small field (easier)
python run_planting.py --controller sample_agents.my_agent:MyDroneAgent --width 6 --height 4 

# Medium field
python run_planting.py --controller sample_agents.my_agent:MyDroneAgent --width 10 --height 8

# Large field (harder)
python run_planting.py --controller sample_agents.my_agent:MyDroneAgent --width 15 --height 10
```

---

## Success Criteria

A good agent should:
- ✅ Visit all farmable tiles (or as many as possible)
- ✅ Navigate around obstacles efficiently  
- ✅ Not get stuck in loops
- ✅ Maximize the `grown_plots` count

**Challenge yourself:** Can you cover the entire field? Can you do it in the fewest turns?

---

## Next Steps

Once you have a working agent:
1. Try different field sizes and obstacle configurations
2. Optimize for speed (minimum turns to full coverage)
3. Compare strategies with classmates
4. Think about: What's the optimal coverage pattern?

Good luck! 🚁🌱
