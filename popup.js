let currentClaimIndex = 0;
let claimsData = [];

document.getElementById("verifyBtn").addEventListener("click", async () => {
    const query = document.getElementById("queryInput").value.trim();
    if (!query) return;

    try {
        const url = `http://127.0.0.1:8000/check_fake_news`;
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ article_text: query })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        claimsData = data.results;
        currentClaimIndex = 0;
        updateDisplay();
    } catch (error) {
        console.error("Error fetching data:", error);
    }
});

function updateDisplay() {
    if (claimsData.length === 0) {
        document.getElementById("claimContainer").style.display = "none";
        return;
    }

    document.getElementById("claimContainer").style.display = "flex";
    const currentClaim = claimsData[currentClaimIndex];
    document.getElementById("claimText").textContent = currentClaim.claim;

    displayResults(currentClaim.scores);
    drawChart(currentClaim.scores);
}

document.getElementById("prevClaim").addEventListener("click", () => {
    if (currentClaimIndex > 0) {
        currentClaimIndex--;
        updateDisplay();
    }
});

document.getElementById("nextClaim").addEventListener("click", () => {
    if (currentClaimIndex < claimsData.length - 1) {
        currentClaimIndex++;
        updateDisplay();
    }
});

function displayResults(scores) {
    const container = document.getElementById("resultsContainer");
    container.innerHTML = "";

    scores.forEach((item, index) => {
        const div = document.createElement("div");
        div.classList.add("result-item");
        div.style.background = `linear-gradient(to right, #34A224 ${item.reliability_score}%, transparent ${item.reliability_score}%)`;
        div.innerHTML = `<strong>${index + 1}. <a href="${item.link}" target="_blank">${item.link}</a></strong> (Score: ${item.reliability_score}%)`;
        container.appendChild(div);
    });

    container.style.overflowY = "auto";
    container.style.maxHeight = "300px";
}

function drawChart(scores) {
    const reliabilityScores = scores.map(item => item.reliability_score);
    const avgScore = reliabilityScores.reduce((a, b) => a + b, 0) / reliabilityScores.length;

    const ctx = document.getElementById("credibilityChart").getContext("2d");

    if (window.myChart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: scores.map((_, i) => `Source ${i + 1}`),
            datasets: [{
                data: reliabilityScores,
                backgroundColor: ["red", "blue", "green", "orange", "purple"]
            }]
        }
    });

    const existingAvg = document.getElementById("avgScore");
    if (existingAvg) existingAvg.remove();

    const avgScoreElement = document.createElement("p");
    avgScoreElement.id = "avgScore";
    avgScoreElement.innerHTML = `<strong>Average Score: ${avgScore.toFixed(1)}%</strong>`;
    document.getElementById("credibilityChart").insertAdjacentElement("afterend", avgScoreElement);
}