const postgres = require('./postgre');
const connection = postgres.connection

/* solution Assumptions: 
start time will always be less than end time,
each employee has more than one record in the db
entries are the same day
*/


postgres.connect().then(() => {

    getEmployeeData().then(result => {
        let uniqueArr = [...new Set(result.map(val => val.employee_id))]

        let promises = []
        let curr
        for (let i = 0; i < uniqueArr.length; i++) {
            curr = uniqueArr[i]
            let each
            let eachArr = []
            for (let j = 0; j < result.length; j++) {
                each = result[j]
                if (each.employee_id == curr) {
                    eachArr.push(each)
                    let right, left, innerCurr, mid, midVal

                    for (let k = 0; k < eachArr.length; k++) {
                        innerCurr = eachArr[k]
                        mid = findMidIndex(eachArr)
                        midVal = eachArr[mid]
                        left = k !== 0 ? eachArr[mid - 1] : eachArr[0]
                        right = k !== eachArr.length - 1 ? eachArr[mid + 1] : eachArr[eachArr.length - 1]
                        if (left.activity_name == right.activity_name && calculateTime(mid.start_time, mid.end_time) <= 2700) {
                                console.log({ left, right })

                        } else if (innerCurr.activity_name == right.activity_name) {
                            innerCurr.end_time = right.end_time
                        }
                    }
                }
            }
            promises.push(i)
        }
        Promise.all(promises).then(arr => {
            // console.log('HII: ' + JSON.stringify(result))
        })
    })

}).catch(error => {

    console.log('ERROR:  ' + JSON.stringify(error.message))
})

function findMidIndex(arr) {
    return arr.indexOf(arr[Math.floor(arr.length / 2)])
}

function deleteEmployeeActivity(record) {
    // return new Promise((resolve, reject) => {
    //     connection.db().query(`DELETE FROM employee_activity WHERE id= ${record.id}`, function (err, result) {
    //         if (err) reject(err)
    //         resolve(result)
    //     })
    // })
}

function updateEmployeeActivity(record) {
    // return new Promise((resolve, reject) => {
    //     connection.db().query(`INSERT INTO employee_activity SET ? WHERE id = ?`, [record, record.id], function (error, result) {
    //         if (error) reject(error)
    //         resolve(result)
    //     })
    // })
}


function getEmployeeData() {
    return new Promise((resolve, reject) => {
        connection.db().query('SELECT * FROM employee_activity;', (err, result) => {
            if (err) reject(err)
            resolve(result.rows)
        })

    })

}

function calculateTime(start, end) {
    return ((new Date(end).getTime() - new Date(start).getTime()) / 1000);
}

/* NOTES::
2. start time is greater than end time, this isn't correct. start time should be less than end time

TODO:
update sql records and delete mid value if time <= minutes
*/
