# Python-Snake-Solvers
A Repository of Different Automated Snake Solving Scripts

Issues:
- The A* solver can trap itself, or crash due to iterating too many times (even if there is still a path)
  -  I have not found a solution to this so I have caused the program to exit if these occur
- The Snake AI only trains one snake at a time and the reward system is flawed
  -  To do : Add support for more snakes and a better training system
