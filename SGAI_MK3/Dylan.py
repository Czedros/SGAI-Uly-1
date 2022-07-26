import pygame
import ctypes
from Int2 import Int2
import time
import constants
import renderConstants
from Cell import Cells
start = time.process_time()
#######
pygame.init()
display_surface = pygame.display.set_mode((renderConstants.SIZE, renderConstants.SIZE))
ctypes.windll.user32.SetProcessDPIAware()#If you're not using Windows, here's an L -> L :).
pygame.display.set_caption("Sus")
#######
day = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\Backgrounds\\SunBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
noon = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\Backgrounds\\SunDownBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
night = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\Backgrounds\\MoonBackground.png'), (renderConstants.SIZE, renderConstants.SIZE))
dayProgressBarHeight = renderConstants.SIZE * 0.06
dayProgress = pygame.image.load(r'Assets\\UI\\DayProgressBar.png')
dayProgress = pygame.transform.scale(dayProgress, (dayProgress.get_width() / dayProgress.get_height() * dayProgressBarHeight, dayProgressBarHeight))
dayProgressPos = (renderConstants.SIZE * (1 - 0.13) - dayProgress.get_width(), renderConstants.SIZE * (1 - 0.005) - dayProgress.get_height())
dayProgressBorderSize = 0.13
dayProgressBorderSize = (dayProgressBorderSize * dayProgress.get_height() / dayProgress.get_width(), dayProgressBorderSize)
dayProgressRectWidth = 3
dayProgressRectBounds = dayProgressBorderSize[0] * dayProgress.get_width()
dayProgressRectBounds = (dayProgressPos[0] + dayProgressRectBounds + 1, dayProgressPos[0] + dayProgress.get_width() - dayProgressRectBounds - dayProgressRectWidth + 1)
dayProgressRect = pygame.Rect(dayProgressRectBounds[1], dayProgressPos[1] + dayProgress.get_height() * dayProgressBorderSize[1] + 0.5, dayProgressRectWidth, dayProgress.get_height() * (1 - dayProgressBorderSize[1] * 2) + 0.5)
#######
resourceIcon = pygame.transform.scale(pygame.image.load(r'Assets\\UI\\ResourceIcon2.png'), (renderConstants.SIZE * 0.1, renderConstants.SIZE * 0.1))
resourceBarHeight = resourceIcon.get_height() * 0.5
resourceBar = pygame.image.load(r'Assets\\UI\\ResourceBar.png')
resourceBar = pygame.transform.scale(resourceBar, (resourceBarHeight * resourceBar.get_width() / resourceBar.get_height(), resourceBarHeight))
iconDist = renderConstants.SIZE * renderConstants.GRIDDIST - resourceIcon.get_height() * 0.75
iconYOff = renderConstants.SIZE * 0.01
resourceBarPos = (iconDist + resourceIcon.get_width() - renderConstants.SIZE * 0.015, iconDist + resourceIcon.get_height() * 0.75 - resourceBar.get_height() - iconYOff)
resourceBorderSize = 0.23
resourceRectBound = resourceBar.get_width() - resourceBar.get_height() * resourceBorderSize * 2 + 2
resourceBarRect = pygame.Rect(resourceBarPos[0] + resourceBar.get_height() * resourceBorderSize, resourceBarPos[1] + resourceBar.get_height() * resourceBorderSize, resourceRectBound, resourceBar.get_height() * (1 - resourceBorderSize * 2) + 2)
##
resourceFont = pygame.font.Font('freesansbold.ttf', int(renderConstants.SIZE / 40))
resourceText = resourceFont.render('Resources: sus', True, (255, 255, 255))
resourceTextRect = resourceText.get_rect()
resourceTextRect.left = resourceBarPos[0] + renderConstants.SIZE * 0.02
resourceTextRect.top = resourceBarPos[1] - resourceTextRect.height
#######
apImageSize = 0.12
apImage = pygame.image.load(r'Assets\\UI\\APBar.png')
apImage = pygame.transform.scale(apImage, (renderConstants.SIZE * apImageSize * apImage.get_width() / apImage.get_height(), renderConstants.SIZE * apImageSize));
apImagePos = (renderConstants.SIZE * 0.05, renderConstants.SIZE - apImage.get_height())
apBorderSize = (0.35, 0.345)
apBarPos = (apImagePos[0] + apImage.get_width() * apBorderSize[0] - 1, apImagePos[1] + apImage.get_height() * apBorderSize[1] + 1)
apRectBound = apImage.get_width() * (1 - apBorderSize[0] - 0.033)
apBarRect = pygame.Rect(apBarPos[0], apBarPos[1], apRectBound, apImage.get_height() * (1 - apBorderSize[1] * 2) + 2)
apFont = pygame.font.Font('freesansbold.ttf', int(apImage.get_width() / 15))
apText = apFont.render('Action Points: sus', True, (255, 255, 255))
apTextRect = apText.get_rect()
apTextRect.left = apBarRect.left + apImage.get_width() * 0.01
apTextRect.top  = apBarRect.top + (apBarRect.height - apTextRect.height) / 2
#######
resources = 0
ap = 0
turn = 0
mainLoop = True
while mainLoop:
    turn = int((time. process_time() - start))
    ap = int((time. process_time() - start) % (constants.MAX_HUMAN_AP + 1))
    resources = min((time. process_time() - start) * 5, constants.MAX_RESOURCES)
    display_surface.fill((0, 0, 0))
    #######
    for x in range(constants.ROWS):
        cellX = int(renderConstants.GRIDRECT.left + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * x + renderConstants.CELLOFF)
        for y in range(constants.ROWS):
            cellY = int(renderConstants.GRIDRECT.top + constants.LINE_WIDTH + (constants.LINE_WIDTH + renderConstants.CELLSIZE) * y + renderConstants.CELLOFF)
            display_surface.blit(Cells.grass.value.image, (cellX, cellY))
    #######
    if(turn % renderConstants.CYCLELEN < renderConstants.CYCLELEN/2):
        if(turn % renderConstants.CYCLELEN > renderConstants.CYCLELEN/2 - 1 - renderConstants.NOONLENGTH):
            display_surface.blit(noon, (0, 0))
        else:
            display_surface.blit(day, (0, 0))
    else:
        display_surface.blit(night, (0, 0))
    #######
    display_surface.blit(dayProgress, dayProgressPos)
    ratio = (turn % (renderConstants.CYCLELEN)) / (renderConstants.CYCLELEN - 1)
    dayProgressRect.left = dayProgressRectBounds[0] * (1 - ratio) + dayProgressRectBounds[1] * ratio
    pygame.draw.rect(display_surface, (255, 255, 255), dayProgressRect)
    #######
    display_surface.blit(resourceBar, resourceBarPos)
    display_surface.blit(resourceIcon, (iconDist, iconDist - iconYOff))
    resourceBarRect.width = resourceRectBound * resources / constants.MAX_RESOURCES
    pygame.draw.rect(display_surface, (202, 0, 69), resourceBarRect)
    resourceText = resourceFont.render('Resources: ' + str(int(resources)) + "/" + str(constants.MAX_RESOURCES), True, (255, 255, 255))
    display_surface.blit(resourceText, resourceTextRect)
    #######
    display_surface.blit(apImage, apImagePos)
    apBarRect.width = apRectBound * ap / constants.MAX_HUMAN_AP
    pygame.draw.rect(display_surface, (239, 73, 52), apBarRect)
    apText = apFont.render('Action Points: ' + str(ap) + "/" + str(constants.MAX_HUMAN_AP), True, (255, 255, 255))
    display_surface.blit(apText, apTextRect)
    #######
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
    pygame.display.update()