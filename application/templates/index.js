function toggleSideBar() {
    if (document.getElementById("sidebar").style.display === "none") {
        document.getElementById("sidebar").style.display = "table-cell";
    } else {
        document.getElementById("sidebar").style.display = "none";
    }
}