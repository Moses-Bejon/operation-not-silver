with open("../../Text analysis/trainingData", "r") as trainingData:
    trainingData = trainingData.readlines()

trainingData = trainingData[:107270]+trainingData[119092:]

with open("../../Text analysis/trainingData", "w") as file:
    file.writelines(trainingData)