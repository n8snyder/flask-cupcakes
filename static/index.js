"use strict";

// const $cupcakeList = $("#cupcake-list");

/** getAllCupcakes: Query API for list of cupcakes */

async function getAllCupcakes() {
  console.log("getAllCupcakes");
  const response = await axios.get("/api/cupcakes");
  return response.data.cupcakes;
}

/** displayCupcakesList: Empty and rebuild the cupcake list */

function displayCupcakesList(cupcakes) {
  console.log("displayCupcakesList");
  $("#cupcake-list").empty();
  for (let cupcake of cupcakes) {
    const cupcakeTemplate = `
        <li>
            <img src ="${cupcake.image}" />
            <span>Flavor: ${cupcake.flavor}</span>
            <span>Size: ${cupcake.size}</span>
            <span>Rating: ${cupcake.rating}</span>
        </li>`;
    $("#cupcake-list").prepend(cupcakeTemplate);
  }
}

/** generateCupcakesList:
 * Controller function for getting cupcakes and displaying them on page */

async function generateCupcakesList() {
  console.log("generateCupcakesList");
  const cupcakes = await getAllCupcakes();
  displayCupcakesList(cupcakes);
}

$(document).ready(generateCupcakesList);

/** handleCreateCupcake: Performs POST to server to create cupcake */

async function handleCreateCupcake(evt) {
  console.log("handleCreateCupcake");
  evt.preventDefault();
  const newCupcake = {
    flavor: $("#flavor-input").val(),
    size: $("#size-input").val(),
    rating: $("#rating-input").val(),
    image: $("#image-input").val()
  };

  response = await axios.post("/api/cupcakes", newCupcake);

  generateCupcakesList();
}

$("#new-cupcake-form").submit(handleCreateCupcake);