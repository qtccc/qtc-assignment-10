// document.getElementById("search-form").addEventListener("submit", async function(event) {
//     event.preventDefault();

//     const keyword = document.getElementById("keyword").value.trim();
//     const filter = document.getElementById("filter").value.trim();

//     if (!keyword) {
//         alert("Please enter a valid keyword.");
//         return;
//     }

//     try {
//         const response = await fetch("/search", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({ keyword: keyword, filter: filter })
//         });

//         const data = await response.json();

//         const resultsDiv = document.getElementById("results");
//         const resultsContainer = document.getElementById("results-container");

//         resultsContainer.innerHTML = ""; // Clear previous results

//         if (data.results && data.results.length > 0) {
//             data.results.forEach(result => {
//                 const p = document.createElement("p");
//                 p.textContent = result;
//                 resultsContainer.appendChild(p);
//             });
//         } else {
//             resultsContainer.textContent = "No results found.";
//         }

//         resultsDiv.style.display = "block";
//     } catch (error) {
//         console.error("Error:", error);
//         alert("An error occurred while fetching results.");
//     }
// });
document.getElementById("search-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById("search-form"));

    try {
        const response = await fetch("/search", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        const resultsDiv = document.getElementById("results");
        const resultsContainer = document.getElementById("results-container");

        resultsContainer.innerHTML = ""; // Clear previous results

        if (data.results && data.results.length > 0) {
            data.results.forEach(result => {
                const item = document.createElement("div");
                item.classList.add("result-item");

                const img = document.createElement("img");
                img.src = result.image;
                item.appendChild(img);

                const similarity = document.createElement("p");
                similarity.textContent = `Similarity: ${result.similarity}`;
                item.appendChild(similarity);

                resultsContainer.appendChild(item);
            });
        } else {
            resultsContainer.textContent = "No results found.";
        }

        resultsDiv.style.display = "block";
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while fetching results.");
    }
});