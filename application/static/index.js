// Toggles sidebar on click of hamburger button
function toggleSideBar() {
    if ($("#sidebar").css("display") == "none") {
        $("#sidebar").css("display", "table-cell");
    } else {
        $("#sidebar").css("display", "none");
    }
}