/** processForm: get data from food form and make AJAX call to backend API */

function processFoodForm(e) {
    e.preventDefault();

    $.ajax({
        method: "POST",
        url: "/api/get-food-cal",
        contentType: "application/json",
        data: JSON.stringify({
            food: $("#foodItem").val(),
            date: $("#foodDate").val()
        }),
        success: handleFoodResponse
    })
}

/** handleResponse: deal with response from backend food-cal API */

function handleFoodResponse(res) {
    if("errors" in res) {
        for(let field in res.errors) {
            $(`#${field}-err`).text(res.errors[field]);
        }
    }

    else {
        let {food} = res;
        let card = `The date is ${date}. The food is ${food.food} and the calorie count is ${food.calories}.`;

        $("#journal-cards").text(card);
    }
}


$("#food_form").on("submit", processFoodForm);


/** processForm: get data from exercise form and make AJAX call to backend API */

function processExerciseForm(e) {
    e.preventDefault();

    $.ajax({
        method: "POST",
        url: "/api/get-exercise-cal",
        contentType: "application/json",
        data: JSON.stringify({
            exercise: $("#exerciseType").val(),
            date: $("#exerciseDate").val()
        }),
        success: handleExerciseResponse
    })
}

/** handleResponse: deal with response from backend exercise-cal API */

function handleExerciseResponse(res) {
    if("errors" in res) {
        for(let field in res.errors) {
            $(`#${field}-err`).text(res.errors[field]);
        }
    }

    else {
        let {exercise, date} = res;
        let card = `<div class="card" style="width: 18rem;">
                    <div class="card-header"> ${date} </div>
                    <ul class="list-group list-group-flush>
                    <li class="list-group-item"> ${exercise.exercise}...${exercise.calories} <li>
                    </ul>
                    </div>`

        $("#journal-cards").appendChild(card);
    }
}


$("#exercise_form").on("submit", processExerciseForm);