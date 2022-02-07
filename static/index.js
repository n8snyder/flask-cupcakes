"use strict";

async function getAllCupcakes() {
  const response = await axios.get("/api/cupcakes");
  return response.data.cupcakes;
}

async function displayCupcakesList() {
  const cupcakes = await getAllCupcakes();

  for (let cupcake of cupcakes) {
    const cupcakeTemplate = `
        <li>
            <img src ="${cupcake.image}" />
            <span>Flavor: ${cupcake.flavor}</span>
            <span>Size: ${cupcake.size}</span>
            <span>Rating: ${cupcake.rating}</span>
        </li>`;
    $("#cupcake-list").append(cupcakeTemplate);
  }
}

$(document).ready(displayCupcakesList);
