// Toggles sidebar on click of hamburger button
function toggleSideBar() {
    if ($("#sidebar").css("display") == "none") {
        $("#sidebar").css("display", "table-cell");
    } else {
        $("#sidebar").css("display", "none");
    }
}

// Check if item is tradable
function isTradable(tradable) {
    if (tradable != 0) {
        $(".tradable-label").css("background-color", "red");
    } else {
        $(".tradable-label").css("background-color", "blue");
    }
}