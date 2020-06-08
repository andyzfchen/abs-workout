from gtts import gTTS
import os
import time   # time.sleep() in seconds
import numpy as np
import csv
import argparse
import configparser
import exerciseplayer as ep

parser = argparse.ArgumentParser(description="Process exercise configuration.")
parser.add_argument("-c","--conf",type=str, default="default_abdominal.conf", help="Configuration file name.")
args = parser.parse_args()

player = ep.ExercisePlayer(args.conf)

print("App is starting.")
player.play_mp3("starting %s exercises" % player.eMode)
time.sleep(3)

print("Duration: %.1f mins" % player.tTotal)
player.play_mp3("%.1f minutes" % player.tTotal)
time.sleep(3)

player.gen_all_exercise_mp3()

player.randomizeExercise()

rep = 0
for j in range(player.nInt):
  # breaktime
  if ((j%(player.eRpS+1))==player.eRpS):
    # normal break
    print("break time")
    player.breaktime(player.tBreak)

    # not last interval
    if ((j+1)!=player.nInt):
      print("Next exercise: %s" % player.arrExer[player.eDifficulty[rep%player.eRpS]][rep][0])
      player.ex_next(player.arrExer[player.eDifficulty[rep%player.eRpS]][rep][0])

    player.ex_countdown()

  # exercise
  else:
    print("Current exercise: %s" % player.arrExer[player.eDifficulty[rep%player.eRpS]][rep][0])
    player.ex_start(player.arrExer[player.eDifficulty[rep%player.eRpS]][rep][0],player.tReady)

    # split exercise
    if (int(player.arrExer[player.eDifficulty[rep%player.eRpS]][rep][1])):
      player.splitexercise(player.tRepTimes[rep%player.eRpS])
    # normal exercise
    else:
      player.exercise(player.tRepTimes[rep%player.eRpS])

    # last interval
    if ((j+1)==player.nInt):
      print("almost done!")
      player.play_mp3("almost done")
    # next is break
    elif (((j+1)%(player.eRpS+1))==player.eRpS):
      print("Next exercise: break time")
      player.ex_next("break time")
    # next is exercise
    else:
      print("Next exercise: %s" % player.arrExer[player.eDifficulty[(rep+1)%player.eRpS]][rep+1][0]) 
      player.ex_next(player.arrExer[player.eDifficulty[(rep+1)%player.eRpS]][rep+1][0])

    player.ex_countdown()

    rep += 1

print("Exercise complete.")
player.play_mp3("congratulations abdominal exercises completed")
