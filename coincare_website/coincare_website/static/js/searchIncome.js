const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

// Hide the table output initially
tableOutput.style.display = "none";

searchField.addEventListener("keyup", async (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    try {
      paginationContainer.style.display = "none";
      tbody.innerHTML = "";

      const response = await fetch("/income/search-income/", {
        // Added trailing slash
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ searchText: searchValue }),
      });

      if (!response.ok) {
        // Log the response status and text for debugging
        const errorText = await response.text();
        throw new Error(
          `Network response was not ok. Status: ${response.status}. Text: ${errorText}`
        );
      }

      const data = await response.json();

      console.log("data", data);

      appTable.style.display = "none";
      tableOutput.style.display = "block";

      if (data.length === 0) {
        noResults.style.display = "block";
        tableOutput.style.display = "none";
      } else {
        noResults.style.display = "none";
        const fragment = document.createDocumentFragment(); // Create a document fragment

        data.forEach((item) => {
          const row = document.createElement("tr");
          row.innerHTML = `
              <td>${item.amount}</td>
              <td>${item.source}</td>
              <td>${item.description}</td>
              <td>${item.date}</td>
            `;
          fragment.appendChild(row); // Append row to fragment
        });

        tbody.appendChild(fragment); // Append all rows to tbody in one go
      }
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
      // Optionally, display an error message to the user here
    }
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
