document.getElementById("verifyBtn").addEventListener("click", async () => {
    const query = document.getElementById("queryInput").value.trim();
    if (!query) return;

    try {
        const url = `http://54.235.11.31:6969/data?query=${encodeURIComponent(query)}`;
        const response = await fetch(url, { method: "GET" });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        displayResults(data);
        drawChart(data);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
});

function displayResults(data) {
    const container = document.getElementById("resultsContainer");
    container.innerHTML = "";

    data.forEach((item, index) => {
        const div = document.createElement("div");
        div.classList.add("result-item");
        div.style.background = `linear-gradient(to right, green ${item.score}%, transparent ${item.score}%)`;
        div.innerHTML = `<strong>${index + 1}. <a href="${item.link}" target="_blank">${item.link}</a></strong> (Score: ${item.score}%)`;
        container.appendChild(div);
    });

    container.style.overflowY = "auto"; // Enable scrolling if needed
    container.style.maxHeight = "300px"; // Prevents overflow
}

function drawChart(data) {
    const scores = data.map(item => item.score);
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;

    const ctx = document.getElementById("credibilityChart").getContext("2d");

    // Destroy old chart if it exists
    if (window.myChart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: data.map((_, i) => `Source ${i + 1}`),
            datasets: [{
                data: scores,
                backgroundColor: ["red", "blue", "green", "orange", "purple"]
            }]
        }
    });

    // Remove previous average score if exists
    const existingAvg = document.getElementById("avgScore");
    if (existingAvg) existingAvg.remove();

    // Display average score
    const avgScoreElement = document.createElement("p");
    avgScoreElement.id = "avgScore";
    avgScoreElement.innerHTML = `<strong>Average Score: ${avgScore.toFixed(1)}%</strong>`;
    document.getElementById("credibilityChart").insertAdjacentElement("afterend", avgScoreElement);
}
