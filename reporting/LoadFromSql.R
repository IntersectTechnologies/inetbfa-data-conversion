# Copyright (c) 2012: DJ Swart
# Load data from the FINANCIALDATA SQL Server database

LoadFromSql<-function(fields="*", table, filter=""){
  # Loads data from local Sql Database
  #
  # Args:
  #   fields: A vector of fields that should be selected from the table
  #   table: The database table from where the data is loaded
  #   filter: a vector of assets that should be selected
  #
  # Returns:
  #   data.frame containing the selected data  
  
  
  library(RODBC)
  source('sql_query_helper_functions.R')
  
  dbhandle <- odbcDriverConnect('driver={SQL Server Native Client 10.0};
                                server=NIEL-PC\\FINANCIALDATA;
                                database=PORTFOLIO_ANALYTICS;
                                trusted_connection=yes')
  
  query <- CreateSqlQuery(fields, table, filter)
  
  ts <- sqlQuery(dbhandle, query,)
  
  # Clean text data
  ts[fields[2]] <- sapply(ts[fields[2]], 
                      function(string) { 
                        sub("\\s.+", "", string) 
                      })
  
  close(dbhandle)
  return(ts)
}