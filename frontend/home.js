// Reserved for future interactions
// Button click animation / page transition can be added later

document.querySelector("button").addEventListener("click", () => {
    console.log("Visualization started");
});
const arrow = document.getElementById("arrow");

setInterval(() => {
    arrow.style.transform = "translateX(6px)";
    setTimeout(() => {
        arrow.style.transform = "translateX(0)";
    }, 200);
}, 800);
