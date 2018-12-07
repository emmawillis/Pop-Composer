# Read file 
creativity = read.csv("C:/Users/Carolyn/Downloads/20181207030754-SurveyExport.csv", header=TRUE, stringsAsFactors = FALSE)

# Find average Creativity for each type of sequence:
creativity$phaseIII = (creativity$Sequence.1 + creativity$Sequence.3 + creativity$Sequence.7)/3
creativity$phaseIV = (creativity$Sequence.4 + creativity$Sequence.6 + creativity$Sequence.10 + creativity$Sequence.11)/4
creativity$phaseV = (creativity$Sequence.2 + creativity$Sequence.5 + creativity$Sequence.1.1 + creativity$Sequence.9 + creativity$Sequence.12)/5

# Find mean values
 meanValues <- data.frame("phaseIII" = mean(creativity$phaseIII), "phaseIV" = mean(creativity$phaseIV), "phaseV" = mean(creativity$phaseV))
 summary <- rbind(meanValues, c(sd(creativity$phaseIII), sd(creativity$phaseIV), sd(creativity$phaseV)))