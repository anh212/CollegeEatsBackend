const getLocations = (req, res, db) => {
    const {schoolName} = req.body;

    //getting schoolID
    db.select('school_id').from('schools').where({
        school_name: schoolName
    }).then(schoolIDBody => {
        if (schoolIDBody.length) {

            //getting names and location
            db.select('dining_name', 'location_name').from('dining_locations').where({
                school_id: schoolIDBody[0].school_id
            }).then(diningNames => {
                console.log(diningNames);
                if (diningNames.length) {
                    res.json(diningNames);
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
    getLocations: getLocations
} 