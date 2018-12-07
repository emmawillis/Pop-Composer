 
# Download typesurvey and change values appropropriately:
typesurveyredo = read.csv("C:/Users/Carolyn/Downloads/4490Survey1.csv", header=TRUE, stringsAsFactors = FALSE)
typesurveyredo[typesurveyredo=="Computer-generated" | typesurveyredo=="Computer-Generated" | typesurveyredo == "Machine-generated"] = "Machine-Generated"
View(typesurveyredo);

# Create a vector that states what each sequence is ACTUALLY supposed to be.
actualvalues <- c("Random", "Man-made", "Machine-Generated", "Man-made", "Random", "Man-made", "Machine-Generated", "Machine-Generated", "Random")

# Find number of assigned random that are actually random.
typesurveyredo$randgivrand = (ifelse(typesurveyredo$Sequence.1.==actualvalues[1], 1, 0) + ifelse(typesurveyredo$Sequence.5==actualvalues[5], 1, 0) + ifelse(typesurveyredo$Sequence.9==actualvalues[9], 1, 0))/3

# Create a new table to hold values:
conditionalProbabilities <- data.frame("randgivrand" = mean(typesurveyredo[,"randgivrand"]))

# Find number assigned Man-Made or Machine-Generated that are random:
typesurveyredo$mangivrand <- (ifelse(typesurveyredo$Sequence.1.=="Man-made", 1, 0) + ifelse(typesurveyredo$Sequence.5=="Man-made", 1, 0) + ifelse(typesurveyredo$Sequence.9=="Man-made", 1, 0))/3
conditionalProbabilities$mangivrand=mean(typesurveyredo[,"mangivrand"])

typesurveyredo$comgivrand <- (ifelse(typesurveyredo$Sequence.1.=="Machine-Generated", 1, 0) + ifelse(typesurveyredo$Sequence.5=="Machine-Generated", 1, 0) + ifelse(typesurveyredo$Sequence.9=="Machine-Generated", 1, 0))/3
conditionalProbabilities$comgivrand = mean(typesurveyredo[,"comgivrand"]) 

# Find number assigned Man-made given (1) Man-made, (2) Machine-Generated, (3) Random.
typesurveyredo$mangivman <- (ifelse(typesurveyredo$Sequence.2.=="Man-made", 1, 0) + ifelse(typesurveyredo$Sequence.4=="Man-made", 1, 0) + ifelse(typesurveyredo$Sequence.6=="Man-made", 1, 0))/3
conditionalProbabilities$mangivman = mean(typesurveyredo[,"mangivman"])

typesurveyredo$comgivman <- (ifelse(typesurveyredo$Sequence.2.=="Machine-Generated", 1, 0) + ifelse(typesurveyredo$Sequence.4=="Machine-Generated", 1, 0) + ifelse(typesurveyredo$Sequence.6=="Machine-Generated", 1, 0))/3
conditionalProbabilities$comgivman = mean(typesurveyredo[,"comgivman"])

typesurveyredo$randgivman <- (ifelse(typesurveyredo$Sequence.2.=="Random", 1, 0) + ifelse(typesurveyredo$Sequence.4=="Random", 1, 0) + ifelse(typesurveyredo$Sequence.6=="Random", 1, 0))/3
conditionalProbabilities$randgivman = mean(typesurveyredo[,"randgivman"])

# Find number assigned etc. given Machine-Generated:

typesurveyredo$randgivcom <- (ifelse(typesurveyredo$Sequence.3.=="Random", 1, 0) + ifelse(typesurveyredo$Sequence.7=="Random", 1, 0) + ifelse(typesurveyredo$Sequence.8=="Random", 1, 0))/3
conditionalProbabilities$randgivcom=mean(typesurveyredo[,"randgivcom"])

typesurveyredo$mangivcom <- (ifelse(typesurveyredo$Sequence.3.=="Man-made", 1, 0) + ifelse(typesurveyredo$Sequence.7=="Man-made", 1, 0) + ifelse(typesurveyredo$Sequence.8=="Man-made", 1, 0))/3
conditionalProbabilities$mangivcom=mean(typesurveyredo[,"mangivcom"])

typesurveyredo$comgivcom <- (ifelse(typesurveyredo$Sequence.3.=="Machine-Generated", 1, 0) + ifelse(typesurveyredo$Sequence.7=="Machine-Generated", 1, 0) + ifelse(typesurveyredo$Sequence.8=="Machine-Generated", 1, 0))/3
conditionalProbabilities$comgivcom = mean(typesurveyredo[,"comgivcom"]) 

newConProb <- rbind(conditionalProbabilities, c(sd(typesurveyredo$randgivrand), sd(typesurveyredo$mangivrand), sd(typesurveyredo$comgivrand), sd(typesurveyredo$mangivman), sd(typesurveyredo$comgivman), sd(typesurveyredo$randgivman), sd(typesurveyredo$randgivcom), sd(typesurveyredo$mangivcom), sd(typesurveyredo$comgivcom)))


# Calculate average percentage assignments for people who play/don't play musical instruments:
# Find number assigned random that are actually random for musicians
musicianframe <- subset(typesurveyredo, Do.you.play.a.musical.instrument. == "Yes")
condProbMusic <- data.frame("randgivrand" = mean(musicianframe[,"randgivrand"]))
condProbMusic$mangivrand = mean(musicianframe[,"mangivrand"])
condProbMusic$comgivrand = mean(musicianframe[,"comgivrand"])
condProbMusic$mangivman = mean(musicianframe[,"mangivman"])
condProbMusic$comgivman = mean(musicianframe[,"comgivman"])
condProbMusic$randgivman = mean(musicianframe[,"randgivman"])
condProbMusic$randgivcom = mean(musicianframe[,"randgivcom"])
condProbMusic$mangivcom = mean(musicianframe[,"mangivcom"])
condProbMusic$comgivcom = mean(musicianframe[,"comgivcom"])

# Insert Standard Deviations:
newMusicConProb <- rbind(condProbMusic, c(sd(musicianframe$randgivrand), sd(musicianframe$mangivrand), sd(musicianframe$comgivrand), sd(musicianframe$mangivman), sd(musicianframe$comgivman), sd(musicianframe$randgivman), sd(musicianframe$randgivcom), sd(musicianframe$mangivcom), sd(musicianframe$comgivcom)))

# Deal with nonmusicians:
nomusicianframe <- subset(typesurveyredo, Do.you.play.a.musical.instrument. == "No")
condProbNoMusic <- data.frame("randgivrand" = mean(nomusicianframe[,"randgivrand"]))
condProbNoMusic$mangivrand = mean(nomusicianframe[,"mangivrand"])
condProbNoMusic$comgivrand = mean(nomusicianframe[,"comgivrand"])
condProbNoMusic$mangivman = mean(nomusicianframe[,"mangivman"])
condProbNoMusic$comgivman = mean(nomusicianframe[,"comgivman"])
condProbNoMusic$randgivman = mean(nomusicianframe[,"randgivman"])
condProbNoMusic$randgivcom = mean(nomusicianframe[,"randgivcom"])
condProbNoMusic$mangivcom = mean(nomusicianframe[,"mangivcom"])
condProbNoMusic$comgivcom = mean(nomusicianframe[,"comgivcom"])

newNoMusicConProb <- rbind(condProbNoMusic, c(sd(nomusicianframe$randgivrand), sd(nomusicianframe$mangivrand), sd(nomusicianframe$comgivrand), sd(nomusicianframe$mangivman), sd(nomusicianframe$comgivman), sd(nomusicianframe$randgivman), sd(nomusicianframe$randgivcom), sd(nomusicianframe$mangivcom), sd(nomusicianframe$comgivcom)))

