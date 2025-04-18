const resultsDiv = document.getElementById("results");

document.getElementById("search-button").addEventListener("click", () => {
    resultsDiv.innerHTML = ""; // Clear previous results
    const query = document.getElementById("search-input").value;
    window.api.searchGames(query);
});
window.api.onResults((results) => {
    results.forEach(result => {
        console.log(result);

        const titleDiv = document.createElement("div");
        titleDiv.className = "result-item";

        const link = document.createElement("a");
        link.href = result.href;
        link.target = "_blank"; // ouvre dans un nouvel onglet

        const titleText = document.createElement("h1");
        titleText.textContent = result.title;

        // Ajoute le <h1> dans le <a>, puis le <a> dans la div
        link.appendChild(titleText);
        titleDiv.appendChild(link);

        // Enfin ajoute à la div globale
        resultsDiv.appendChild(titleDiv);



    });
});