# Copyright (c) 2012 DJ Swart
# Helper functions for creating sql queries for the FINANCIALDATA SQL Server database
# 

CreateSqlSelect<-function(fields="*"){
  # Create a Sql select statement by specifying the fields in the table that must be selected
  # 
  # Args: 
  #   fields: A vector of fields in the table that must be selected. 
  #         Defaults to '*' meaning all fields in the table will be selected
  #
  # Returns:
  #   Sql select statement
  
  n <- length(fields)
  
  if (n==1) {
    selectstmt <- paste("SELECT ", fields[1],sep="")
  }
  if (n>1){
    selectstmt <- paste("SELECT ", fields[1],",",sep="")
    if ((n-1)<2) {
      selectstmt <- paste(selectstmt, fields[n],sep="")
    }
    else {
      for (i in 2:(n-1)){
        selectstmt <- paste(selectstmt, fields[i], ",", sep="")
      }
      selectstmt <- paste(selectstmt, fields[n], sep="")
    }
  }
  return(selectstmt)
}

CreateSqlFrom <- function(table) {
  # Create from statment for sql query
  
  fromstmt <- paste("FROM", table)
  
}

CreateSqlWhere <- function(codefilter="", sectorfilter="", exchange="JSE", startdate="", enddate="") {
  # Filter statement for sql query
  
  cn <- length(codefilter)
  cn_1 <- cn-1;
  
  qw <- ""
  
  if (cn<=0) { return(qw) }
  else if (cn>1) {
    for (i in 1:cn_1) {
      qw <- paste(qw, "( Symbol=", "'", codefilter[i], "' AND Exchange='", exchange[i],"'", ") OR ", sep="")
    }
    qw <- paste(qw, "( Symbol=", "'", codefilter[cn], "' AND Exchange='", exchange[cn],"'", ")", sep="")

    qd <- paste("Datestamp >=", "'",startdate,"'", " AND ", "Datestamp <=", "'",enddate,"'" )
  
    qstmt <- paste("WHERE", "(", qw, ")", " AND ", "(", qd ,")") 
    return(qstmt)
  }
  else
  {
    qw <- paste(qw, "Symbol=", "'", codefilter[cn], "'", sep="")
    qd <- paste("Datestamp >=", startdate, " AND ", "Datestamp <=",enddate )
    
    qstmt <- paste("WHERE", "(", qw, ")", " AND ", "(", qd ,")") 
    return(qstmt)
  }
}

# Create Sql Query
CreateSqlQuery <- function(select="*", from, where="") {
  # Create from statment for sql query
  
  query <- CreateSqlSelect(select)
  query <- paste(query, CreateSqlFrom(from))
  query <- paste(query, CreateSqlWhere(codefilter=where$Symbols, exchange=where$exchange,
                                       startdate=where$StartDate, enddate=where$EndDate))
  
  return(query)
}