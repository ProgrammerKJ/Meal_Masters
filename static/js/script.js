function addItem() {
  const itemText = document.getElementById("itemInput").value;
  if (itemText.trim() !== "") {
    const listItem = document.createElement("li");
    listItem.className =
      "list-group-item d-flex justify-content-between align-items-center";

    const itemCheckbox = document.createElement("input");
    itemCheckbox.type = "checkbox";
    itemCheckbox.className = "form-check-input";
    itemCheckbox.addEventListener("change", toggleItem);

    const itemTextSpan = document.createElement("span");
    itemTextSpan.textContent = itemText;

    const removeButton = document.createElement("button");
    removeButton.textContent = "Remove";
    removeButton.className = "btn btn-danger btn-sm";
    removeButton.addEventListener("click", removeItem);

    listItem.appendChild(itemCheckbox);
    listItem.appendChild(itemTextSpan);
    listItem.appendChild(removeButton);

    document.getElementById("itemList").appendChild(listItem);

    document.getElementById("itemInput").value = "";

    saveShoppingList();
  }
}

function toggleItem(event) {
  const listItem = event.target.parentElement;
  if (event.target.checked) {
    listItem.style.textDecoration = "line-through";
  } else {
    listItem.style.textDecoration = "none";
  }

  saveShoppingList();
}

function removeItem(event) {
  const listItem = event.target.parentElement;
  listItem.remove();

  saveShoppingList();
}

document
  .getElementById("clearListButton")
  .addEventListener("click", function () {
    document.getElementById("itemList").innerHTML = "";

    saveShoppingList();
  });

document.addEventListener("DOMContentLoaded", function () {
  const savedItems = localStorage.getItem("shoppingList");
  if (savedItems) {
    document.getElementById("itemList").innerHTML = savedItems;
  }
});

function saveShoppingList() {
  const itemList = document.getElementById("itemList").innerHTML;
  localStorage.setItem("shoppingList", itemList);
}

document.getElementById("addItemButton").addEventListener("click", addItem);

document
  .getElementById("itemInput")
  .addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      addItem();
    }
  });
