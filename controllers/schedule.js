const getSchedule = (req, res, db) => {
    const {schoolName, diningName} = req.body;

    //getting schoolID
    db.select('school_id').from('schools').where({
        school_name: schoolName
    }).then(schoolIDBody => {
        if (schoolIDBody.length) {

            //getting diningID
            db.select('dining_id').from('dining_locations').where({
                dining_name: diningName
            }).then(diningIDBody => {
                if (diningIDBody.length) {

                    //Getting schedule
                    db.select('*').from('hours').where({
                        school_id: schoolIDBody[0].school_id,
                        dining_id: diningIDBody[0].dining_id
                    }).then(hoursBody => {
                        if (hoursBody.length) {
                            res.json(hoursBody);
                        } else {
                            res.status(400).json('no schedule')
                        }
                    })
                    .catch(err => res.status(400).json('error getting hours'))
                } else {
                    res.status(400).json('Dining location not found');
                }
            })
            .catch(err => res.status(400).json('error getting diningID'))
        } else {
            res.status(400).json('School not found');
        }
    })
    .catch(err => res.status(400).json('error getting schoolID'))
}

module.exports = {
    getSchedule: getSchedule
} 