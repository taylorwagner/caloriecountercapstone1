/** processForm: get data from form and make AJAX call to backend API */

function processForm(e) {
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
        let {food} = res;
        let
    }
}