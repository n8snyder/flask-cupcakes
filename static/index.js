"use strict";

const $cupcakeList = $("#cupcake-list");

/** getAllCupcakes: Query API for list of cupcakes */

async function getAllCupcakes() {
  console.log("getAllCupcakes");
  const response = await axios.get("/api/cupcakes");
  return response.data.cupcakes;
}

/** displayCupcakesList: Empty and rebuild the cupcake list */

function displayCupcakesList(cupcakes) {
  console.log("displayCupcakesList");
  $cupcakeList.empty();
  for (let cupcake of cupcakes) {
    addCupcakeToList(cupcake);
  }
}

/** addCupcakeToList: Adds a cupcake to the cupcake list */

function addCupcakeToList(cupcake) {
  const cupcakeTemplate = `
        <li>
            <img src ="${cupcake.image}" />
            <span>Flavor: ${cupcake.flavor}</span>
            <span>Size: ${cupcake.size}</span>
            <span>Rating: ${cupcake.rating}</span>
        </li>`;
  $cupcakeList.prepend(cupcakeTemplate);
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

  const resp = await axios.post("/api/cupcakes", newCupcake);
  addCupcakeToList(resp.data.cupcake);
  $("#new-cupcake-form").trigger("reset");
}


async function handleCupcakeSearch(evt) {
  evt.preventDefault();
  const searchString = $("#input-find-flavor").val();
  const response = await axios.get("/api/cupcakes/search", {
    params: {
      searchString: searchString
    }
  });
  displayCupcakesList(response.data.cupcakes);
  $("#find-cupcakes-by-flavor").trigger("reset");
}

$("#new-cupcake-form").submit(handleCreateCupcake);
$("#find-cupcakes-by-flavor").submit(handleCupcakeSearch);