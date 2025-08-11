from cmu_graphics import *
import random
import os, pathlib
import copy

def onAppStart(app):
    newGame(app)

def newGame(app):
    app.screen = "start"
    app.screens = ['start','help', 'levels', 'play']
    app.rows = 9
    app.cols = 9
    app.boardLeft = 50
    app.boardTop = 50
    app.boardWidth = 700
    app.boardHeight = 700
    app.cellBorderWidth = 2
    app.difficulty = None
    app.selected = False
    app.selectedRow = None
    app.selectedCol = None
    app.legals = False
    app.hintStatuses = [0,1,2]
    app.hintStatus = 0
    app.cx = 0
    app.cy = 0
    app.redCircle = False
    app.gameOver = False
    app.clicksound = loadSound('sounds/click.mp3')
    #Pixabay https://pixabay.com/sound-effects/search/click/
    app.losesound = loadSound('sounds/lose.mp3')
    #Pixabay https://pixabay.com/sound-effects/search/you%20lose/?manual_search=1&order=None
    app.winsound = loadSound('sounds/win.mp3')
    #Pixabay https://pixabay.com/sound-effects/search/yay/?manual_search=1&order=None


# def loadSound(relativePath):
#     url = pathlib.Path(os.path.abspath(relativePath)).as_uri()
#     return Sound(url)
def loadSound(relativePath):
    abs_path = os.path.abspath(relativePath)  # full path, no URI encoding
    return Sound(abs_path)
#From 112 TA (Shawn), a 112 student, and CS Academy Dev Team, "Sound Demo!" @1129 Piazza
# https://piazza.com/class/lcuom1poo696ei/post/1129

def solveSudoku(board, verbose=None):
    boardcopy = copy.deepcopy(board)
    stateboard = solution(boardcopy)
    stateboard.insertLegals()
    nextRow, nextCol = lookForLeastLegalsNew(stateboard.legals, stateboard.board)
    return solve(stateboard, nextRow, nextCol)

def hasNoZero(grid):
    rows, cols = len(grid), len(grid[0])
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                return False
    return True

def solve(stateboard, row, col):
    if hasNoZero(stateboard.board):
        return stateboard.board
    else:
        for legal in stateboard.legals:
            if legal[0] == (row, col):
                possibleValues = legal[1]
        for num in possibleValues:
            if canPlaceNum(num, row, col, stateboard.board):
                stateboard.set(row, col, num)
                nextPosition = lookForLeastLegalsNew(stateboard.legals, stateboard.board)
                if nextPosition == None:
                    return stateboard.board
                else:
                    nextRow, nextCol = nextPosition
                solution = solve(stateboard, nextRow, nextCol)
                if solution != None:
                    return solution
                stateboard.set(row, col, 0)
        return None
    
def canPlaceNum(value, row, col, board):
    if board[row][col] != 0:
        return False
    rowIn = [(row, col) for col in range(9)]
    colIn = [(row, col) for row in range(9)]
    blockRow = row//3
    blockCol = col//3
    block = 3*blockRow + blockCol
    rows = [(block//3*3 + row) for row in range(3)]
    cols = [(block%3*3 + col) for col in range(3)]
    blockIn = []
    for row in rows:
        for col in cols:
            blockIn.append((row, col))
    for row, col in rowIn:
        if board[row][col] == value:
            return False
    for row, col in colIn:
        if board[row][col] == value:
            return False
    for row, col in blockIn:
        if board[row][col] == value:
            return False
    return True

def lookForLeastLegalsNew(legals, board):
    leastLegals = 9
    squareLeastLegals = None
    for square in legals:
        (row, col) = square[0]
        if len(square[1]) > 0 and board[row][col] == 0:
            if len(square[1]) < 2:
                return square[0]
            elif len(square[1]) < leastLegals:
                leastLegals = len(square[1])
                squareLeastLegals = square[0]
    return squareLeastLegals

def numSameAnswers(board, solution):
    result = 0
    for row in range(9):
        for col in range(9):
            if board[row][col] == solution[row][col]:
                result += 1
    return result

def redrawAll(app):
    if app.screen == 'start':
        if 950 <= app.cx <= 1200 and 305 <= app.cy <= 385:
                tempMouse = 'play'
        elif 950 <= app.cx <= 1200 and 505 <= app.cy <= 585:
                tempMouse = 'help'
        else:
            tempMouse = None
        drawRect(0, 0, app.width, app.height, fill='orange')
        drawLabel('SUDOKU',720, 80, size=96, fill='red', 
                  bold = True)
        drawRect(950, 305, 250, 80, fill = 'lightYellow' if tempMouse == 'play' else 'lightGray', border = 'black')
        drawLabel("PLAY", 1075, 345, size = 26, bold=True)
        drawRect(950, 505, 250, 80, fill = 'lightYellow' if tempMouse == 'help' else 'lightGray', border = 'black')
        drawLabel("HELP", 1075, 545, size = 26, bold=True)
        drawCircle(400, 440, 200, fill='yellow', border='black')
        drawOval(330,380,65,65)
        drawOval(470,380,65,65)
        drawArc(400, 490, 150, 150, 185, 170, fill = 'orange', border = 'black')
    if app.screen == 'help':
        drawRect(0, 0, app.width, app.height, fill='lightGreen')
        drawLabel('HELP',720, 75, size=72, fill='midnightBlue', bold = True)
        drawLine(550, 110, 890, 110, fill='midnightBlue')
        drawLabel('Welcome to Sudoku! To win, fill out the 9x9 board with its proper values',
                  720, 160, size=24, fill='midnightBlue', bold = True)
        drawLabel('Each row, column, and 3x3 box must contain all the numbers 1-9 exactly once',
                  720, 240, size=24, fill='midnightBlue', bold = True)
        drawLabel('Click on square to select it. Use the numbers on the keyboard or on screen to fill the square',
                  720, 320, size=24, fill='midnightBlue', bold = True)
        drawRect(220, 425, 100, 100, fill='lightGray', border='black')
        drawLabel('H', 270, 475, size=36, bold=True)
        drawLabel('Hint (Singletons)', 270, 575, size=24, fill='black', bold = True)
        drawRect(520, 425, 100, 100, fill='lightGray', border='black')
        drawLabel('J', 570, 475, size=36, bold=True)
        drawLabel('Autoplay Singletons', 570, 575, size=24, fill='black', bold = True)
        drawRect(820, 425, 100, 100, fill='lightGray', border='black')
        drawLabel('L', 870, 475, size=36, bold=True)
        drawLabel('Display Legals', 870, 575, size=24, fill='black', bold = True)
        drawRect(1120, 425, 100, 100, fill='lightGray', border='black')
        drawLabel('R', 1170, 475, size=36, bold=True)
        drawLabel('Show Wrong Numbers', 1170, 575, size=24, fill='black', bold = True)
        drawLabel('Good luck!',720, 650, size=36, fill='midnightBlue', bold = True)
        drawLabel('Press space to return',720, 730, size=36, fill='midnightBlue', bold = True)
    if app.screen == 'levels':
        if 172.5 <= app.cx <= 422.5 and 240 <= app.cy <= 320:
            tempdiff = 'easy'
        elif 595 <= app.cx <= 845 and 240 <= app.cy <= 320:
            tempdiff = 'medium'
        elif 1017.5 <= app.cx <= 1267.5 and 240 <= app.cy <= 320:
            tempdiff = 'hard'
        elif 320 <= app.cx <= 570 and 420 <= app.cy <= 500:
            tempdiff = 'expert'
        elif 870 <= app.cx<= 1120 and 420 <= app.cy <= 500:
            tempdiff = 'evil'
        else:
            tempdiff = None
        drawRect(0, 0, app.width, app.height, fill='orange')
        drawLabel('LEVELS',720, 80, size=72, fill='red', 
                  bold = True)
        drawRect(172.5, 240, 250, 80, fill = 'lightGreen' if tempdiff == 'easy' else 'lightGray', border = 'black')
        drawLabel("EASY", 297.5, 280, size = 26, bold=True)
        drawRect(595, 240, 250, 80, fill = 'lightGreen' if tempdiff == 'medium' else 'lightGray', border = 'black')
        drawLabel("MEDIUM", 720, 280, size = 26, bold=True)
        drawRect(1017.5, 240, 250, 80, fill = 'yellow' if tempdiff == 'hard' else 'lightGray', border = 'black')
        drawLabel("HARD", 1142.5, 280, size = 26, bold=True)
        drawRect(320, 420, 250, 80, fill = 'yellow' if tempdiff == 'expert' else 'lightGray', border = 'black')
        drawLabel("EXPERT", 445, 460, size = 26, bold=True)
        drawRect(870, 420, 250, 80, fill = 'red' if tempdiff == 'evil' else 'lightGray', border = 'black')
        drawLabel("EVIL", 995, 460, size = 26, bold=True)
    if app.screen == 'play':
        drawRect(0, 0, app.width, app.height, fill='pink')
        drawBoard(app)
        drawBoardBorder(app)
        rows, cols = len(app.board), len(app.board[0])
        cellWidth, cellHeight = getCellSize(app)
        for row in range(rows):
            for col in range(cols):
                num = app.board[row][col]
                if app.redCircle:
                    if num != 0 and num != app.solution[row][col]:
                        drawCircle(app.boardLeft + row*cellWidth + 9*cellWidth/10, 
                                   app.boardTop + col*cellHeight + 9*cellHeight/10, 
                                   5, fill='red')
                if num != 0:
                    drawLabel(num, 
                            app.boardLeft + cellWidth/2 + row*cellWidth,
                            app.boardTop + cellHeight/2 + col*cellHeight,
                            size=32, bold=True)
                else:
                    if app.legals:
                        for legals in app.state.legals:
                            if legals[0] == (col,row):
                                if legals[1] != set():
                                    drawLabel(str(sorted(legals[1]))[1:-1], 
                                    app.boardLeft + cellWidth/2 + row*cellWidth,
                                    app.boardTop + cellHeight/8 + col*cellHeight,
                                    size=11)
        drawCircle(1125, 205, 180, fill='yellow', border='black')
        duckStatus = numSameAnswers(app.state.board, app.solution)
        drawCircle(1065 ,145, 25)
        drawCircle(1185 ,145, 25)
        if 0 <= duckStatus <= 35:
            start, sweep = 230, 80
            drawCircle(1065, 185, 15,fill='cyan')
        elif 36 <= duckStatus <= 60:
            start, sweep = 230, 80
        elif 61 <= duckStatus <= 70:
            start, sweep = 210, 120
        elif 71 <= duckStatus <= 81:
            start, sweep = 185, 170
        else:
            start, sweep = 185, 170
        drawArc(1125, 245, 150, 150, start, sweep, fill = 'orange', border = 'black')
        drawRect(900, 425, 75, 75, fill='lightGray', border='black')
        drawLabel('H', 937.5, 462.5, size=24, bold=True)
        drawLabel('Hint (Singletons)', 1050, 462.5, size=16, fill='black', bold = True)
        drawRect(1125, 425, 75, 75, fill='lightGray', border='black')
        drawLabel('J', 1162.5, 462.5, size=24, bold=True)
        drawLabel('Autoplay Singletons', 1300, 462.5, size=16, fill='black', bold = True)
        drawRect(900, 545, 75, 75, fill='lightGray', border='black')
        drawLabel('L', 937.5, 582.5, size=24, bold=True)
        drawLabel('Display Legals', 1050, 582.5, size=16, fill='black', bold = True)
        drawRect(1125, 545, 75, 75, fill='lightGray', border='black')
        drawLabel('R', 1162.5, 582.5, size=24, bold=True)
        drawLabel('Show Wrong Numbers', 1300, 582.5, size=16, fill='black', bold = True)
        if 975 <= app.cx <= 1200 and 680 <= app.cy <= 755:
            color = 'red'
        else:
            color = 'lightGray'
        drawRect(975, 680, 225, 75, fill=color, border='black')
        drawLabel('GIVE UP', 1087.5, 717.5, size=36, bold=True)
        #drawLabel(app.file, 900, 400, size=24)
        if app.gameOver != False:
            drawRect(300, 100, 840, 600, fill = 'lightGreen' if app.gameOver == 'win' else 'orange', border='black')
            drawCircle(720, 390, 120, fill='yellow', border='black')
            if 595 <= app.cx <= 845 and 550 <= app.cy <= 630:
                fill = 'lightYellow'
            else:
                fill = 'lightGray'
            drawRect(595, 550, 250, 80, fill = fill, border = 'black')
            drawLabel('RETURN', 720, 590, size=26, bold=True)
            if app.gameOver == 'win':
                drawLabel('YOU WIN', 720, 200, size=96, bold=True, fill='green')
                drawOval(680,350,40,27.5)
                drawOval(760,350,40,27.5)
                drawArc(720, 415, 100, 100, 185, 170, fill = 'orange', border = 'black')
            elif app.gameOver == 'lose':
                drawLabel('YOU LOSE', 720, 200, size=96, bold=True, fill='red')
                drawOval(680,350,35,35)
                drawOval(760,350,35,35)
                drawCircle(680, 380, 10, fill='cyan')
                drawArc(720, 415, 100, 100, 230, 80, fill = 'orange', border = 'black')

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
#From CS Academy, Animations With 2d Lists, "5.3.2 Drawing a 2d Board".
#https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def drawBoardBorder(app):
    cellWidth, cellHeight = getCellSize(app)
    for i in range(3):
        for j in range(3):
            left = 50 + i*cellWidth*3
            top = 50 + j*cellHeight*3
            drawRect(left, top, cellWidth*3, cellHeight*3,
                    fill=None, border='black',
                    borderWidth=app.cellBorderWidth)
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)
#From CS Academy, Animations With 2d Lists, "5.3.2 Drawing a 2d Board".
#https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    hintRow, hintCol = lookForLeastLegals(app.state.legals, app.state.board)
    if app.state.original[col][row] != 0:
        fill = 'lightGray'
    elif (col, row) == (app.selectedRow, app.selectedCol):
        fill = 'lightBlue'
    elif app.state.board[col][row] != 0:
        fill = 'lightCyan'
    elif app.hintStatus == 1 and (hintRow, hintCol) != (None, None) and (row, col) == (hintRow, hintCol):
        fill = 'yellow'
    else:
        fill = 'white'
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=fill, border='gray',
             borderWidth=app.cellBorderWidth)
#From CS Academy, Animations With 2d Lists, "5.3.2 Drawing a 2d Board".
#https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)
#From CS Academy, Animations With 2d Lists, "5.3.2 Drawing a 2d Board".
#https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
#From CS Academy, Animations With 2d Lists, "5.3.2 Drawing a 2d Board".
#https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def readFile(path):
    with open(path, "rt") as f:
        return f.read()
#From CMU 15-112 Spring 2023 (Lecture 3/4) Tp:Sudoku Notes
#https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15112-3-s23/www/notes/term-project.html
    
def loadBoard(app):
    if app.difficulty in ['easy','medium','hard']:
        num = str(random.randint(1, 50))
    elif app.difficulty in ['evil','expert']:
        num = str(random.randint(1, 25))
    if int(num) < 10:
        num = '0' + num
    file = f'{app.difficulty}-{num}.png.txt'
    #file = random.choice(os.listdir('tp-starter-files/boards/')) 
    #from stackoverflow 701402
    contents = readFile('tp-starter-files/boards/'+file)
    app.state = state(contentsToList(contents))
    app.board = app.state.board
    app.file = file
    app.solution = solveSudoku(app.board)

def contentsToList(contents):
    result = []
    for row in contents.splitlines():
        newRow = []
        for c in row.split():
            newRow.append(int(c))
        result.append(newRow)
    return result

class state:
    def __init__(self, board):
        self.board = board
        self.legals = []
        self.original = copy.deepcopy(self.board)
        self.originalLegals = []
    def set(self, row, col, value):
        self.board[row][col] = value
    def ban(self, row, col, value):
        self.originalLegals = copy.deepcopy(self.legals)
        for legals in self.legals:
            if (legals[0] == (row, col)) and value in legals[1]:
                legals[1].remove(value)
    def unban(self, row, col, value):
        for legals in self.legals:
            if (legals[0] == (row, col)):
                legals[1].add(value)
    def getRowRegion(self, row):
        return [(row, col) for col in range(9)]
    def getColRegion(self, col):
        return [(row, col) for row in range(9)]
    def getBlockRegion(self, block):
        rows = [(block//3*3 + row) for row in range(3)]
        cols = [(block%3*3 + col) for col in range(3)]
        result = []
        for row in rows:
            for col in cols:
                result.append((row, col))
        return result
    def getBlock(self, row, col):
        blockRow = row//3
        blockCol = col//3
        return 3*blockRow + blockCol
    def getBlockRegionByCell(self, row, col):
        block = 3*(row//3) + col//3
        rows = [(block//3*3 + row) for row in range(3)]
        cols = [(block%3*3 + col) for col in range(3)]
        result = []
        for row in rows:
            for col in cols:
                result.append((row, col))
        return result
    @staticmethod
    def getCellRegionsStatic(row, col):
        result = []
        rowregion = [(row, col) for col in range(9)]
        colregion = [(row, col) for row in range(9)]
        block = 3*(row//3) + col//3
        rows = [(block//3*3 + row) for row in range(3)]
        cols = [(block%3*3 + col) for col in range(3)]
        blockregion = []
        for row in rows:
            for col in cols:
                blockregion.append((row, col))
        result.append(rowregion)
        result.append(colregion)
        result.append(blockregion)
        return result
    def getCellRegions(self, row, col):
        return state.getCellRegionsStatic(row, col)
    @staticmethod
    def getAllRegionsStatic():
        result = []
        for row in range(9):
            newRow = [(row, col) for col in range(9)]
            result.append(newRow)
        for col in range(9):
            newCol = [(row, col) for row in range(9)]
            result.append(newCol)
        for block in range(9):
            rows = [(block//3*3 + row) for row in range(3)]
            cols = [(block%3*3 + col) for col in range(3)]
            newBlock = []
            for row in rows:
                for col in cols:
                    newBlock.append((row, col))
            result.append(newBlock)
        return result
    def getAllRegions(self):
        return state.getAllRegionsStatic()
    def getAllRegionsThatContainTargets(self, targets):
        result = []
        allRegions = state.getAllRegionsStatic()
        for region in allRegions:
            addRegion = True
            for target in targets:
                if not state.isInRegion(self.board,region,target):
                    addRegion = False
            if addRegion:
                result.append(region)
        return result
    @staticmethod
    def isInRegion(board, region, target):
        for square in region:
            row, col = square[0], square[1]
            if board[col][row] == target:
                return True
        return False
    def insertLegals(self):
        rows, cols = len(self.board), len(self.board[0])
        for row in range(rows):
            for col in range(cols):
                legals = [(col, row), set()]
                if self.board[row][col] == 0:
                    cellRegions = state.getCellRegionsStatic(row, col)
                    for num in range(1,10):
                        numIsLegal = True
                        for region in cellRegions:
                            for cell in region:
                                cellRow, cellCol = cell[0], cell[1]
                                if (cellRow, cellCol != row, col) and self.board[cellRow][cellCol] == num:
                                    numIsLegal = False
                        if numIsLegal:
                            legals[1].add(num)
                self.legals.append(legals)
#Structure from CMU 15-112 Spring 2023 (Lecture 3/4) Tp:Sudoku Hints
#https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15112-3-s23/www/notes/tp-sudoku-hints.html
    
class solution(state):
    def insertLegals(self):
        rows, cols = len(self.board), len(self.board[0])
        for row in range(rows):
            for col in range(cols):
                legals = [(row, col), set()]
                if self.board[row][col] == 0:
                    cellRegions = state.getCellRegionsStatic(row, col)
                    for num in range(1,10):
                        numIsLegal = True
                        for region in cellRegions:
                            for cell in region:
                                cellRow, cellCol = cell[0], cell[1]
                                if (cellRow, cellCol != row, col) and self.board[cellRow][cellCol] == num:
                                    numIsLegal = False
                        if numIsLegal:
                            legals[1].add(num)
                self.legals.append(legals)

def mouseToRowCol(app, mouseX, mouseY):
    row = (mouseX - 50)//(700/9)
    col = (mouseY - 50)//(700/9)
    return int(row), int(col)

def onMousePress(app, mouseX, mouseY):
    if not app.gameOver:
        if app.screen == 'start':
            if 950 <= mouseX <= 1200 and 305 <= mouseY <= 385:
                app.screen = 'levels'
                app.clicksound.play()
            elif 950 <= mouseX <= 1200 and 505 <= mouseY <= 585:
                app.screen = 'help'
                app.clicksound.play()
        elif app.screen == 'levels':
            if 172.5 <= mouseX <= 422.5 and 240 <= mouseY <= 320:
                app.difficulty = 'easy'
                app.clicksound.play()
            elif 595 <= mouseX <= 845 and 240 <= mouseY <= 320:
                app.difficulty = 'medium'
                app.clicksound.play()
            elif 1017.5 <= mouseX <= 1267.5 and 240 <= mouseY <= 320:
                app.difficulty = 'hard'
                app.clicksound.play()
            elif 320 <= mouseX <= 570 and 420 <= mouseY <= 500:
                app.difficulty = 'expert'
                app.clicksound.play()
            elif 870 <= mouseX <= 1120 and 420 <= mouseY <= 500:
                app.difficulty = 'evil'
                app.clicksound.play()
            if app.difficulty != None:
                loadBoard(app)
                app.state.insertLegals()
                app.screen = 'play'
        elif app.screen == 'play':
            mouseRow, mouseCol = mouseToRowCol(app, mouseX, mouseY)
            if (mouseRow, mouseCol) == (app.selectedRow, app.selectedCol):
                app.selected = False
                app.selectedRow, app.selectedCol = None, None
            elif (0 <= mouseRow <= 8 and 0 <= mouseCol <= 8 and
                app.state.original[mouseRow][mouseCol] == 0):
                app.selected = True
                app.selectedRow = mouseRow
                app.selectedCol = mouseCol
            elif 975 <= mouseX <= 1200 and 680 <= mouseY <= 755:
                app.clicksound.play()
                app.gameOver = 'lose'
                app.losesound.play()
    elif app.gameOver:
        if 595 <= mouseX <= 845 and 550 <= mouseY <= 630:
            app.clicksound.play()
            newGame(app)

def onMouseMove(app, mouseX, mouseY):
    app.cx = mouseX
    app.cy = mouseY        

def onKeyPress(app, key):
    if not app.gameOver:
        if app.screen == 'help':
            if key == 'space':
                app.screen = 'start'
        if app.screen == 'play':
            if app.selected:
                if key in '123456789' and app.board[app.selectedRow][app.selectedCol] == 0:
                    app.state.set(app.selectedRow, app.selectedCol, int(key))
                    cellregions = app.state.getCellRegions(app.selectedRow, app.selectedCol)
                    for region in cellregions:
                        for cell in region:
                            cellRow = cell[0]
                            cellCol = cell[1]
                            app.state.ban(cellCol, cellRow, int(key))
                    app.hintStatus = 0
                    app.selected = False
                    app.selectedRow, app.selectedCol = None, None
                elif key == 'backspace' and app.hintStatus == 0:
                    if app.board[app.selectedRow][app.selectedCol] != 0:
                        originalValue = app.board[app.selectedRow][app.selectedCol]
                        app.state.set(app.selectedRow, app.selectedCol, 0)
                        #app.state.unban(app.selectedRow, app.selectedCol, originalValue)
                        cellregions = app.state.getCellRegions(app.selectedRow, app.selectedCol)
                        for region in cellregions:
                            for cell in region:
                                cellRow = cell[0]
                                cellCol = cell[1]
                                if app.state.original[cellRow][cellCol] == 0 and isLegal(app.state.board, cellRow, cellCol, originalValue):
                                    app.state.unban(cellCol, cellRow, originalValue)    
                                #probably buggy
                        app.selected = False
                        app.selectedRow, app.selectedCol = None, None

            if key.lower() == 'l':
                app.legals = not app.legals
            if key == 'h' and not app.selected and correctBoardSoFar(app.board, app.solution):
                app.hintStatus = app.hintStatus+1
                if app.hintStatus == 2:
                    row, col = lookForLeastLegals(app.state.legals, app.state.board)
                    if (row, col) != (None, None):
                        for legal in app.state.legals:
                            if legal[0] == (row, col):
                                value = int(str(legal[1])[1:-1])
                                app.state.set(col, row, value)
                                cellregions = app.state.getCellRegions(row, col)
                                for region in cellregions:
                                    for cell in region:
                                        cellRow = cell[0]
                                        cellCol = cell[1]
                                        app.state.ban(cellRow, cellCol, value)
                    app.hintStatus = 0
            if key == 'r':
                app.redCircle = not app.redCircle
            if key == 'j':
                if app.hintStatus == 0:
                    singletons = []
                    for legal in app.state.legals:
                        row, col = legal[0]
                        if (len(legal[1]) == 1 and app.state.board[col][row] == 0 
                            and correctBoardSoFar(app.state.board, app.solution)):
                            singletons.append(legal)
                    for legal in singletons:
                        row, col = legal[0]
                        value = int(str(legal[1])[1:-1])
                        app.state.set(col, row, value)
                        cellregions = app.state.getCellRegions(row, col)
                        for region in cellregions:
                            for cell in region:
                                cellRow = cell[0]
                                cellCol = cell[1]
                                app.state.ban(cellRow, cellCol, value)
            if app.board == app.solution:
                app.gameOver = 'win'
                app.winsound.play()



def isLegal(board, row, col, value):
    rowIn = [(row, col) for col in range(9)]
    colIn = [(row, col) for row in range(9)]
    blockRow = row//3
    blockCol = col//3
    block = 3*blockRow + blockCol
    rows = [(block//3*3 + row) for row in range(3)]
    cols = [(block%3*3 + col) for col in range(3)]
    blockIn = []
    for row in rows:
        for col in cols:
            blockIn.append((row, col))
    for row, col in rowIn:
        if board[row][col] == value:
            return False
    for row, col in colIn:
        if board[row][col] == value:
            return False
    for row, col in blockIn:
        if board[row][col] == value:
            return False
    return True



def isInAnyRegion(board, regions, target):
    for region in regions:
        for square in region:
                row, col = square[0], square[1]
                if board[col][row] == target:
                    return True
    return False

def hasCommonRegion(regions1, regions2):
    for region1 in regions1:
        for region2 in regions2:
            if region1 == region2:
                return True
    return False

def lookForLeastLegals(legals, board):
    for square in legals:
        row, col = square[0]
        if len(square[1]) == 1 and board[col][row] == 0:
            return square[0]
    return None, None

def correctBoardSoFar(board, solution):
    for row in range(9):
        for col in range(9):
            boardnum = board[row][col]
            if boardnum != 0:
                if boardnum != solution[row][col]:
                    return False
    return True

def main():
    runApp(width = 1440, height = 800)

main()


