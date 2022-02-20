# Automated Nonogram Solver

This is a scipt that can solve 10x10 nonogram puzzles. It is calibrated on the screen size and resolution of the Google Pixel 4a.

An ADB connection is required to run this scipt. The script will automatically detect the device and connect to it.

To solve the puzzle, a screenshot of the puzzle is taken and analyzed using image recognition in openCV. After all hints are extracted, the correct solution is calculated and entered using simulated tabs. After the puzzle is solved, a new game is started automatically. An adblocker is recommended to prevent the script from getting caught on ads.