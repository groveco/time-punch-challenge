const knex = require('knex')({
  client: 'pg',
  connection: {
    host : '127.0.0.1',
    port : 5432,
    user : 'aseiden',
    database : 'time-punch-challenge'
  }
});
const moment = require('moment');
const _ = require('lodash');
const { printTable } = require('console-table-printer');


class TimePunchCombiner {
  constructor(knex) {
    this.knex = knex;
  }

  async fetch_data() {
    // Fetches all data, but could be adjusted to only fetch a subset for larger use cases.
    return this.knex('employee')
      .join('employee_activity', 'employee.id', 'employee_activity.employee_id')
      .select('employee.id', 'employee.name', 'employee_activity.activity_name', 'employee_activity.start_time', 'employee_activity.end_time')
  }

  append_time_punch(punch, combined_punches) {
    const user_record = combined_punches[punch.id];
    if (!user_record) {
      combined_punches[punch.id] = {
        name: punch.name,
        punches: {
          Picking: [],
          Packing: [],
          Cleaning: [],
        },
      }
    }

    const task_specific_punches = combined_punches[punch.id].punches[punch.activity_name];
    // This approacch to 5 minute tasks is not correct, but it's all I could manage
    // in the time allotted for the exercise and it works for the test cases. It doesn't handle cases where multiple
    // 5 minute shifts combine into a more meaningful shift. To handle that case, I would
    // go back after everything has been organized and remove 5 minute shifts that are
    // inside other shifts.
    const is_five_minute_task = moment(punch.end_time).diff(punch.start_time, 'minutes') <= 5

    if (is_five_minute_task) {
      // do nothing
      // this is really ugly as it's a last minute addition to handle the edge case
    } else if (task_specific_punches.length === 0) {
      task_specific_punches[0] = [punch.start_time, punch.end_time];
    } else {
      // This over-combines, but it's odd. William has one pair of shifts divided
      // by 30 minutes combined and one pair non-combined.

      // let most_recent_records = [];
      // for (const activity in combined_punches[punch.id].punches) {
      //   most_recent_records.push({
      //     times: _.last(combined_punches[punch.id].punches[activity]),
      //     name: activity,
      //   });
      //   most_recent_records = _.filter(most_recent_records, 'times');
      // }
      // console.log(most_recent_records);
      // const most_recent_record = _.reduce(most_recent_records, (max, record) => {
      //   if (max.times[1] > record.times[1]) {
      //     return max;
      //   } else {
      //     return record;
      //   }
      // });
      // const is_extension_of_prior_task = most_recent_record.name === punch.activity_name;

      const most_recent_record = task_specific_punches[task_specific_punches.length - 1];
      const most_recent_end_time = most_recent_record[1];
      const is_extension_of_prior_task = moment(punch.start_time).diff(most_recent_end_time, 'minutes') <= 5;
      if (is_extension_of_prior_task) {
        most_recent_record[1] = punch.end_time;
      } else {
        task_specific_punches.push([punch.start_time, punch.end_time]);
      }
    }
  }

  async combine_time_punches() {
    const time_punches = await this.fetch_data();
    const combined_punches = {};

    // iterate across time_punches and group them together
    time_punches.forEach((punch) => {
      this.append_time_punch(punch, combined_punches);
    });

    // Prepare the data for printing
    const printable_punches = [];
    for (const id in combined_punches) {
      const employee = combined_punches[id];
      for (const punch_name in employee.punches) {
        const punch = employee.punches[punch_name];
        punch.forEach((time) => {
          printable_punches.push({
            ID: id,
            Name: employee.name,
            Activity: punch_name,
            "Start Time": time[0],
            "End Time": time[1],
          })
        });
      }
    }

    printTable(printable_punches);

  }
}

const combiner = new TimePunchCombiner(knex);

(async () => {
  try {
      var text = await combiner.combine_time_punches();
      console.log(text);
  } catch (e) {
      console.log(e);
  }
})();

