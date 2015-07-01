extractdate<-function(data, column){
  # function to extract an element from a given column
  
  as.POSIXct(as.double(substr(data[[column]],7,nchar(data[[column]])-2))/1000,origin="1970-01-01")
}