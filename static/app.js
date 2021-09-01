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
        let {food, date} = res;
        let card = `The date is ${date}. The food is ${food.food} and the calorie count is ${food.calories}.`;

        $("#journal-demo").text(card);
    }
}


$("#food_form").on("submit", processFoodForm);


// /** handleResponse: deal with response from backend food-cal API */

// function handleFoodResponse(res) {
//     let card = document.createElement('div');
//     card.classList.add('card');

//     let header = document.createElement('div');
//     header.classList.add('card-header');
//     card.appendChild(header);

//     let foodList = document.createElement('ul');
//     foodList.classList.add('list-group');
//     foodList.classList.add('list-group-flush');
//     card.appendChild(foodList);

//     let foodItem = document.createElement('li');
//     foodItem.classList.add('list-group-item');
//     foodList.appendChild(foodItem);

//     if("errors" in res) {
//         for(let field in res.errors) {
//             $(`#${field}-err`).text(res.errors[field]);
//         }
//     }

//     else {
//         let {food, date} = res;
//         header.innerText = `${date}`
//         foodItem.innerText = `${food.food}...${food.calories}`

//         $("#journal-demo").appendChild(card);
//     }
// }