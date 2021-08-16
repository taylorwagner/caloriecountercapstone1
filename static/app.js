/** processForm: get data from form and make AJAX call to backend API */

function processFoodForm(e) {
    e.preventDefault();

    $.ajax({
        method: "POST",
        url: "/api/get-food-cal",
        contentType: "application/json",
        data: JSON.stringify({
            food: $("#food").val()
        }),
        success: handleResponse
    })
}

/** handleResponse: deal with response from backend food-cal API */

function handleResponse(res) {
    if("errors" in res) {
        for(let field in res.errors) {
            $(`#${field}-error`).text(res.errors[field]);
        }
    }

    else {
        let {food, calories} = res;
        let card = `<div class="card" style="width: 18rem;">
                    <div class="card-header"> ${date} </div>
                    <ul class="list-group list-group-flush>
                    <li class="list-group-item"> ${food}...${calories} <li>
                    </ul>
                    </div>`

        $("#journal-cards").appendChild(card)
    }
}


$("#food_form").JSON("submit", processFoodForm);