# Copyright (c) 2012: DJ Swart
#

# TODO: Make it work for single column matrices (vectors)

ApplyZOH <- function(matrix, type='price') {
  # Apply a zero order hold to the data in the matrix to remove NA's - column wise
  # 
  # Args: 
  #   matrix: Data to which the zero order hold should be applied; can be a matrix or timeSeries
  #   
  #   type: Price or returns - defaults to 'price' when returns the NA's are replaced with zeros.
  #
  # Returns:
  #   Cleaned up matrix
  
  # first go
  # Get the NA indices
  idx <- which(is.na(combined.ts), arr.ind=TRUE)

  rows <- idx[,1]
  cols <- idx[,2]
  
  for (i in 1:length(rows)) {
    
    # replace NA with previous observation in same column - if not the first obs. of the column
    if (rows[i]>1) {
      matrix[rows[i], cols[i]] <- matrix[rows[i]-1, cols[i]]
    }
    
  }
  
  idx <- which(is.na(matrix), arr.ind= TRUE)
  na.cols <- as.integer(levels(as.factor(idx[,2])))
  missingdata <- c()
  
  for (k in na.cols) {
    # check if first two observations of each column is NA
    
    if(is.na(matrix[1,k])) {
      
      # if first observation is NA and second is not
      if (!is.na(matrix[2,k])) {
        # apply backward ZOH
        matrix[1,k] <- matrix[2,k]
      }
      else {
        # do something here with the rest of the columns
        missingdata <- c(missingdata, k)
      }
          
    }
  }
  
  retval = list(data=matrix, NACols= missingdata )
  
  return(retval)
  
}