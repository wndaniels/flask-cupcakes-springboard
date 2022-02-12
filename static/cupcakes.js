const BASE_URL = "http://127.0.0.1:5000/api";

function generateCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
    <img class="Cupcake-img" src="${cupcake.image}" alt="{no image provided}"
      <ul>
        <li>
            ${cupcake.flavor}
            <button class="delete-button">X</button>
        </li>
        <li>
        ${cupcake.size}
        </li>
        <li>
        ${cupcake.rating}
        </li>
      </ul>
    </div>
    `;
}

async function showInitialCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeInfo of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeInfo));
    $("#cupcakes-list").append(newCupcake);
  }
}

$("#add-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();

  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image,
  });

  let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
});

/** handle clicking delete: delete cupcake */

$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();
  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});

$(showInitialCupcakes);
