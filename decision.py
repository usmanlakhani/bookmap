import requests
import json
import pandas as pd
import sys
import random

      
def initiate(fileName, dummySignificantLow, significantLowMarker, range):
    
    # Step 0: Assign values to variables
    intPriceSigLow = int(dummySignificantLow)
    lowerBoundary = range.split('-')[0]
    upperBoundary = range.split('-')[1]
    intSignificantLowMarker = int(significantLowMarker)
    conditionOneMet = 0 # 0 - No, 1 - Partly , 2 - Yes
    conditionTwoMet = 0
    currStockPrice = None
    prevStockPrice = None
    
    # Step 1: Load data
    dataFrame = pd.read_csv(fileName)
    
    # Step 2: Declare a dataframe that will display the analysis
    dataFrameResults= pd.DataFrame(columns=['Current Stock Price','Existing Sig Low','Condition # 1 Met','Condition # 2 Met','Recommendation'])
    
    # Step 3: Compare price of stock vs known significant low price    
    for idx, row in dataFrame.iterrows():        
        
        if prevStockPrice is None:
            prevStockPrice = row['price']
            currStockPrice = row['price']
        else:
            prevStockPrice = currStockPrice
            currStockPrice = row['price']

        if currStockPrice < intPriceSigLow:
            intPriceSigLow = currStockPrice
            prevStockPrice = currStockPrice
            new_row = {"Current Stock Price": currStockPrice, 'Existing Sig Low': intPriceSigLow, 'Condition # 1 Met': 'No','Condition # 2 Met': 'No','Recommendation': 'No Action'}
            dataFrameResults.loc[len(dataFrameResults)] = new_row
            continue
        
        if currStockPrice > intPriceSigLow and conditionOneMet == 0:
            
            difference = currStockPrice - intPriceSigLow
            
            if (difference > intSignificantLowMarker or difference < intSignificantLowMarker):
                conditionOneMet = 0
                conditionTwoMet = 0
                prevStockPrice = currStockPrice
                new_row = {"Current Stock Price": currStockPrice, 'Existing Sig Low': intPriceSigLow, 'Condition # 1 Met': 'No','Condition # 2 Met': 'No','Recommendation': 'No Action'}
                dataFrameResults.loc[len(dataFrameResults)] = new_row
                continue
            
            if (difference == intSignificantLowMarker):
                conditionOneMet = 1
                conditionTwoMet = 0
                prevStockPrice = currStockPrice
                new_row = {"Current Stock Price": currStockPrice, 'Existing Sig Low': intPriceSigLow, 'Condition # 1 Met': 'Watch','Condition # 2 Met': 'No','Recommendation': 'No Action'}
                dataFrameResults.loc[len(dataFrameResults)] = new_row
                continue
            
        if currStockPrice > intPriceSigLow and conditionOneMet == 1:
            
            if currStockPrice > prevStockPrice:
                conditionOneMet = 0
                conditionTwoMet = 0
                prevStockPrice = currStockPrice
                new_row = {"Current Stock Price": currStockPrice, 'Existing Sig Low': intPriceSigLow, 'Condition # 1 Met': 'No','Condition # 2 Met': 'No','Recommendation': 'No Action'}
                dataFrameResults.loc[len(dataFrameResults)] = new_row
                continue
            
            if currStockPrice - prevStockPrice >= int(lowerBoundary) + 1 and currStockPrice - prevStockPrice <= int (upperBoundary)-1:
                conditionTwoMet = 2
                prevStockPrice = currStockPrice
                new_row = {"Current Stock Price": currStockPrice, 'Existing Sig Low': intPriceSigLow, 'Condition # 1 Met': 'Yes','Condition # 2 Met': 'Yes','Recommendation': 'Buy'}
                dataFrameResults.loc[len(dataFrameResults)] = new_row
                continue
    
    print(dataFrameResults)
    fileNameToSaveto = str(random.randrange(1,25)) + "output.xlsx"            
    dataFrameResults.to_excel(fileNameToSaveto)
 
if __name__ == "__main__":
    
    # pass in Significant Low, Range to confirm the Significant Low
    # For next enhancement: If SL is not entered, look back either 24 hours or 36 hours
    dummySignificantLow = sys.argv[1]
    significantLowUpperLimit = sys.argv[2]
    confirmationRange = sys.argv[3]
    fileName='test_data.csv'
    initiate(fileName,dummySignificantLow,significantLowUpperLimit,confirmationRange)