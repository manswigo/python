# AAplayground - Autonomous Agents Playground

AAplayground bundles several turn-based drone scenarios powered by pygame.  
Users can pilot the drone manually or plug in autonomous agents of their own design, switching between farming, planting, and navigation challenges.

## Quick start

1. Ensure Python 3.10+ is available.
2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # On Windows: .venv\Scripts\activate
   ```

   or let VSCode handle it for you.

3. Install dependencies from the project root:

   ```bash
   pip install -r requirements.txt
   ```

4. Launch the planting playground with keyboard control (default):

   ```bash
   python run_planting.py
   ```

   Controls: arrow keys move, `.` wait, `Esc` quit. **Seeds are planted automatically** as you move!

5. Follow the [Tutorial 1](./TUTORIAL_01.md) to implement your first autonomous agent!


## Simulation concepts

In each simulation step (the drone's turn), the agent receives an observation of the environment and must decide on an action to perform. 

**In the planting challenge**, seeds are planted automatically at every position the drone visits. The available actions are moving in four directions or waiting. Your goal is to cover all farmable tiles efficiently!


## Package Structure

- `aa_playground/core.py` – shared enums and action dataclasses.
- `aa_playground/agents.py` – base agent class, keyboard controller, and BFS reference agent.
- `aa_playground/environment.py` – grid world engine plus farming, planting, and navigation variants.
- `aa_playground/game.py` – pygame session responsible for rendering and input.
- `run_planting.py` – planting marathon launcher (keyboard play or custom agents).

## Field Cell States (Planting Challenge)

- **Empty soil** – ready for planting (just move here and a seed is automatically planted!)
- **Seed** (newly planted) – transforms into a growing crop after configured turns (default: 2)
- **Growing crop** – becomes fully grown after additional turns (default: 3)
- **Fully grown crop** – persists indefinitely once matured (goal: maximize these!)
- **Tree/Obstacle** – impassable obstacle tiles that block movement

**Note**: In the planting challenge, drones have infinite seeds and battery, so the focus is entirely on efficient coverage and obstacle navigation!

## Writing Your Own Agent

Create a file `my_sweep_agent.py` in the `sample_agents/` directory:

```python
from aa_playground import BaseAgent, Action, ActionType, Direction, Observation


class SweepAgent(BaseAgent):
    """Example agent that sweeps the field from left to right."""

    def decide(self, observation: Observation) -> Action:
        x, y = observation.position
        if x == observation.width - 1:
            return Action(ActionType.MOVE, direction=Direction.DOWN)
        return Action(ActionType.MOVE, direction=Direction.RIGHT)
```

Then run it with:
```bash
python run_planting.py --controller sample_agents.my_sweep_agent:SweepAgent
```
