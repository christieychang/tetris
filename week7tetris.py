#TETRIS Week 7
# Christie Chang + cchang2 + section E



from tkinter import *
import random
import copy
####################################
# customize these functions
####################################

#getCellBounds taken from course site
#link:https://www.cs.cmu.edu/~112/notes/notes-animations-examples.html#gridDemo


def initialPieces(data):
    iPiece = [[True, True, True, True]]
    jPiece = [[True, False, False],
              [True, True, True]]
    lPiece = [[ False, False, True],
              [ True,  True,  True]]
    oPiece = [[True, True],
              [True, True]]
    sPiece =  [[ False, True, True ],
               [ True,  True, False ]]
    tPiece = [[False, True, False],
              [True,  True, True]]
    zPiece = [[ True, True, False ],
              [ False,  True, True]]
    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    return tetrisPieces


def init(data):
    data.timerDelay = 300
    data.margin = 35
    data.cols = 10
    data.rows = 15
    data.emptyColor = "blue"
    data.board = [[data.emptyColor]*data.cols for row in range(data.rows)]
    tetrisPieceColors = [ "light blue", "yellow", "magenta", "pink",
                                                    "cyan", "light green", "turquoise" ]
    data.tetrisPieces = initialPieces(data)
    data.tetrisPieceColors = tetrisPieceColors
    newFallingPiece(data)
    data.fallingPieceCols = len(data.fallingPiece[0])
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols//2-data.fallingPieceCols//2
    data.isGameOver = False
    data.pause = False
    data.fullRows = 0
    data.score = 0


def newFallingPiece(data):
    numOfPieces = 7
    pieceIndex = random.randint(0, 6)
    data.fallingPiece = data.tetrisPieces[pieceIndex]
    data.fallingPieceColor = data.tetrisPieceColors[pieceIndex]
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols//2-len(data.fallingPiece[0])//2


#modified from grid-demo.py
def getCellBounds(row, col, data):
    gridWidth = data.width - data.margin*2
    gridHeight = data.height - data.margin*2
    x0 = data.margin + gridWidth*col / data.cols
    x1 = data.margin + gridWidth*(col+1) / data.cols
    y0 = data.margin + gridHeight*row / data.rows
    y1 = data.margin + gridHeight*(row+1) / data.rows
    return (x0,y0,x1,y1)


def fallingPieceIsLegal(data):
    (rows, cols) = (len(data.fallingPiece), len(data.fallingPiece[0]))
    for row in range(data.fallingPieceRow,data.fallingPieceRow+rows):
        for col in range(data.fallingPieceCol, data.fallingPieceCol+cols):
            if data.fallingPiece[row-data.fallingPieceRow]\
                                            [col-data.fallingPieceCol]==True:
                if (data.fallingPieceRow<0 or data.fallingPieceRow+rows>15
                    or data.fallingPieceCol<0 or data.fallingPieceCol+cols>10):
                    return False
                if (data.board[row][col] != data.emptyColor):
                    return False
    return True


def moveFallingPiece(data,drow,dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if not fallingPieceIsLegal(data):
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True


def placeFallingPiece(data):
    (rows, cols) = (len(data.fallingPiece), len(data.fallingPiece[0]))
    currentRow = data.fallingPieceRow
    currentCol = data.fallingPieceCol
    for row in range(rows):
        for col in range(cols):
            if data.fallingPiece[row][col]==True:
                data.board[currentRow][currentCol] = data.fallingPieceColor
            currentCol+=1
        currentRow +=1
        currentCol = data.fallingPieceCol
    currentRow=0


def isFullRow(row, data):
    (rows,cols) = (data.rows,data.cols)
    for col in range(cols):
        if row[col] == data.emptyColor:
            return False
    return True


def removeFullRows(data):
    rows = data.rows
    newRow = data.rows-1
    for oldRow in range(rows-1,-1,-1):
        if not isFullRow(data.board[oldRow], data):
            data.board[newRow] = copy.copy(data.board[oldRow])
            newRow -= 1
        else:
            data.fullRows += 1
    data.score += data.fullRows**2
    data.fullRows = 0
    
                
def rotateFallingPiece(data):
    origPiece = data.fallingPiece
    (origRows, origCols) = (len(origPiece), len(origPiece[0]))
    (newRows, newCols) = (origCols, origRows)
    origStartingRow = data.fallingPieceRow
    origStartingCol = data.fallingPieceCol
    origCenterRow = origStartingRow + (origRows//2)
    origCenterCol = origStartingCol + (origCols//2)
    (newCenterRow, newCenterCol) = (origCenterRow, origCenterCol)
    newRow = newCenterRow - (newRows//2)
    newCol = newCenterCol - (newCols//2)
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol
    rotatedPiece = [[0]*newCols for row in range(newRows)]
    for row in range(newRows):
        for col in range(newCols):
            rotatedPiece[row][col] = origPiece[col][origCols-1-row]
    data.fallingPiece = rotatedPiece
    if not fallingPieceIsLegal(data):
        data.fallingPiece = origPiece
        data.fallingPieceRow = origStartingRow
        data.fallingPieceCol = origStartingCol


def mousePressed(event, data):
    pass


def keyPressed(event, data):
    if event.keysym == "Left":
        moveFallingPiece(data,0,-1)
    if event.keysym == "Right":
        moveFallingPiece(data,0,+1)
    if event.keysym == "Down":
        moveFallingPiece(data,+1,0)
    if event.keysym == "Up":
        rotateFallingPiece(data)
    if event.keysym == "r": #restarts the game
        data.pause = False
        init(data)
    if event.keysym == "p":
        data.pause = True
    if event.keysym == "g": #unpauses the game
        data.pause = False


def timerFired(data):
    if not data.pause:
        if not moveFallingPiece(data,+1,0):
            placeFallingPiece(data)
            newFallingPiece(data)
            removeFullRows(data)
            if not moveFallingPiece(data,0,0):
            #immediately checks if new falling piece is illegal
                data.isGameOver = True
                data.pause = True


def drawFallingPiece(canvas, data):
    (rows, cols) = (len(data.fallingPiece), len(data.fallingPiece[0]))
    currentRow = data.fallingPieceRow
    currentCol = data.fallingPieceCol
    for row in range(rows):
        for col in range(cols):
            if data.fallingPiece[row][col]==True:
                drawCell(canvas, currentRow, currentCol,
                            data.fallingPieceColor, data)
            currentCol+=1
        currentRow +=1
        currentCol = data.fallingPieceCol


def drawCell(canvas, row, col, color, data):
    (x0,y0,x1,y1) = getCellBounds(row, col, data)
    m = 1 #outline around smaller square
    canvas.create_rectangle(x0,y0,x1,y1,fill="black", width=0)
    canvas.create_rectangle(x0+m,y0+m,x1-m,y1-m,fill=color, width=0)

def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, row, col, data.board[row][col], data)
    drawFallingPiece(canvas,data)

def drawGame(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="black",width=0)
    drawBoard(canvas, data)


def drawScore(canvas, data):
    canvas.create_text(data.width/2,data.margin/2,
        text="Your score: %d" % data.score, fill="white", font="Times 20 bold")


def redrawAll(canvas, data):
    drawGame(canvas, data)
    drawScore(canvas, data)
    if (data.isGameOver == True):
        canvas.create_rectangle(data.margin, data.height/3,
            data.width-data.margin,2*(data.height/3),fill="black")
        canvas.create_text(data.width/2, data.height/2-30,text="Game Over!",
            fill="red", font="Times 40 bold")
        canvas.create_text(data.width/2, data.height/2,
            text="Your Final Score: %d" % data.score,
            fill="white", font="Times 20 bold")
        canvas.create_text(data.width/2,data.height/2+30,
            text='Press the "R" Key\nto restart the game!',
            fill="light blue", font="Times 15 bold")


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(450,675)
