
## Time Punch Challenge Instructions
1. Fork this repo
2. Make changes to the code in the forked repository
3. Once ready, create a PR from the forked repository into this repository

## Environment
This is a Python 3 project. 

## Dependencies
* __Database:__ postgres database
* __Other Packages:__ psycopg2 (refer to requirements.txt)


## Time Punch Challenge details
1. The input database has Employee and Punches. The SQL file has the DDLs to seed data. The SQL is catered to PostgreSQL syntax.
3. The goal is to combine punches. 
4. For the input in the database, below is the expected output
5. Special case: If there is a different activity between 2 of the same for the same employee, combine them to the bigger activity if the `middle` activity duration is <= 5 minutes
   e.g. 
   
   Input 
   
   Lucy        Picking     12:25 PM    1:00 PM
   
   Lucy        Cleaning    1:00 PM     1:05 PM
   
   Lucy        Picking     1:05 PM     2:00 PM
   
   
   Expected output: cleaning rolls up into Picking
   Lucy    Picking     12:25 PM    2:00 PM


****** EXPECTED OUTPUT BELOW ******

 OUTPUT:
 
    ID  Name    Activity    Start Time  End Time
    
    Joe     Picking     2021-01-24 9:05 AM      2021-01-24 10:00 AM
    
    William Packing     2021-01-24 9:15 AM      2021-01-24 10:00 AM
    
    Joe     Packing     2021-01-24 11:00 AM     2021-01-24 11:45 AM
    
    Joe     Picking     2021-01-24 11:50 AM     2021-01-24 12:30 PM
    
    Lucy    Packing     2021-01-24 11:30 AM     2021-01-24 12:20 PM
    
    William Packing     2021-01-24 10:30 AM     2021-01-24 3:00 PM
    
    Lucy    Picking     2021-01-24 12:25 PM     2021-01-24 2:00 PM
    
    William Picking     2021-01-24 3:05 PM      2021-01-24 5:00 PM
    
    Joe     Cleaning    2021-01-24 11:55 PM     2021-01-25 12:35 AM
