// Auth Check
const token = localStorage.getItem("token");
if (!token) {
    window.location.href = "index.html";
}

// Button click animation / page transition
document.querySelector(".cta-btn").addEventListener("click", () => {
    console.log("Visualization started");
    window.location.href = "survey.html";
});
const arrow = document.getElementById("arrow");

setInterval(() => {
    arrow.style.transform = "translateX(6px)";
    setTimeout(() => {
        arrow.style.transform = "translateX(0)";
    }, 200);
}, 800);
