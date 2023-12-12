import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
screenWidth = 800
screenHeight = 600
hexagonRadius = 20
grid = [
    ["x","x","x","x","x","x","x","x","x"  ],
    [  "x","x","x","x","x","x","x","x","x"],
    ["x","x","x","x","x","x","x","x","x"  ],
    [  "x","x","x","x","o","x","x","x","x"],
    ["x","x","x","x","x","x","x","x","x"  ],
    [  " "," "," ","x","x","x"," "," "," "],
    [" "," "," ","x","x","x","x"," "," "  ],
    [  " "," "," ","x","x","x"," "," "," "],
    [" "," "," ","x","x","x","x"," "," "  ],
    [  " "," "," ","x","x","x"," "," "," "],
    [" "," "," ","x","x","x","x"," "," "  ],
    [  " "," "," ","x","x","x"," "," "," "],
    [" "," "," ","x","x","x","x"," "," "  ]
]
doors = [
    {
        "first": {
            "partId": 1,
            "cords": {
                "q": 0,
                "r": 0,
                "s": 0
            }
        },
        "second": {
            "partId": 2,
            "cords": {
                "q": -1,
                "r": 1,
                "s": 0
            }
        }
    }
]

# Calculate the total width and height of the hexagonal grid
gridWidth = len(grid[0]) * 2 * hexagonRadius
gridHeight = len(grid) * 1.5 * hexagonRadius

# Calculate the starting position to center the grid
startX = (screenWidth - gridWidth) // 2
startY = (screenHeight - gridHeight) // 2

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Create a display window
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Grid test showcase")

# Function to calculate the vertices of a hexagon
def calculateHexagonVertices(x, y, radius):
    vertices = []
    for i in range(6):
        angle = math.radians(60 * i)
        vertexX = x + radius * math.cos(angle)
        vertexY = y + radius * math.sin(angle)
        vertices.append((vertexX, vertexY))

    rotationAngle = math.radians(90)
    vertices = [(centerX + (vertex[0] - centerX) * math.cos(rotationAngle) - (vertex[1] - centerY) * math.sin(rotationAngle),
                 centerY + (vertex[0] - centerX) * math.sin(rotationAngle) + (vertex[1] - centerY) * math.cos(rotationAngle))
                for vertex in vertices]

    return vertices

# Get the coordinates of the center point
found = False
xCoord = 0
yCoord = 0

for y, row in enumerate(grid):
    if found:
        break

    for x, cell in enumerate(row):
        if cell == "o":
            xCoord = x
            yCoord = y
            found = True
            break

# Main drawing loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(white)

    # Loop through the grid and draw hexagons for 'x' and 'o'
    for rowIndex, row in enumerate(grid):
        for colIndex, cell in enumerate(row):
            # Cube coordinates
            q = round((colIndex - xCoord) - ((rowIndex - yCoord) - ((rowIndex - yCoord) & 1)) / 2)
            r = round(rowIndex - yCoord)
            s = round(-q - r)

            # Check if the current hexagon is a door
            isDoor = False
            for door in doors:
                if (door["first"]["cords"]["q"] == q and door["first"]["cords"]["r"] == r and door["first"]["cords"]["s"] == s) or \
                   (door["second"]["cords"]["q"] == q and door["second"]["cords"]["r"] == r and door["second"]["cords"]["s"] == s):
                    isDoor = True
                    break

            if cell == 'x' or cell == 'o':
                # Calculate the center position for the hexagon
                centerX = startX + colIndex * 1.9 * hexagonRadius + (rowIndex % 2) * hexagonRadius
                centerY = startY + rowIndex * 1.55 * hexagonRadius

                # Calculate hexagon vertices
                hexagonVertices = calculateHexagonVertices(centerX, centerY, hexagonRadius)

                # Draw the rotated hexagon with a border
                pygame.draw.polygon(screen, black, hexagonVertices)
                pygame.draw.polygon(screen, white, hexagonVertices, 3)

            # Draw the center point
            if cell == 'o':
                pygame.draw.circle(screen, red, (centerX + 1, centerY + 1), hexagonRadius / 2)

            # Draw the door as cross
            if isDoor:
                pygame.draw.line(screen, white,
                                 (centerX - hexagonRadius / 2, centerY - hexagonRadius / 2),
                                 (centerX + hexagonRadius / 2, centerY + hexagonRadius / 2), 3)
                pygame.draw.line(screen, white,
                                 (centerX + hexagonRadius / 2, centerY - hexagonRadius / 2),
                                 (centerX - hexagonRadius / 2, centerY + hexagonRadius / 2), 3)


    # Update the display
    pygame.display.flip()
