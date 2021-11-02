## Assumptions
* I grab all employees and all employee_activities; in the real world, this would not be reasonable.
* Thankfully, I could safely assume that there was an employee record for every employee_activity, given the foreign key constraint.
* I'm assuming that no employee has an employee_activity record contained, even partially, within another. Ensuring the data integrity in that fashion is a bit less straight-forward.
* I'm assuming just printing the final result is a reasonable solution

## Modifications
* I'm unaware of a (reasonable) way to get Python to format a datetime exactly as shown in the example output (namely, not padding hours with zeroes)
* One of the inserted rows was "bad data"; we should never end up with an end_time that is before a start_time, and records should be validated before insert to ensure this. I filtered the record out rather than modifying the SQL.
* The results in the README did not follow any order I could recognize; my results are returned in order of start_time
* I failed to think up a reasonable rule for why some of the records were combined and others weren't (excluding the "special case"), so I came up with my own -- if it was half an hour or less of dead time between similar employee activities, I combined them. This meant all of William's time rolled up together.

## Running It
You can start the postgres container by running `docker-compose up postgres` from the working directory.
Then you can run `docker-compose run app` however many times you want to get the output.
Feel free to make modifications to the seed data in the data_load file between runs to see how the app handles it.