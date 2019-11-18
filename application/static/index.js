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

function showWishlist() {
    var showFields = $("#showDiv").css("display", "block");
    return showFields;
}

function hideWishlist() {
    var hideFields = $("#showDiv").css("display", "none");
    return hideFields;
}

// Choose images
function chooseFile() {
    $("#fileInput").click();
}

function dropHandler(ev) {
    console.log('File(s) dropped');

    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();

    if (ev.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        for (var i = 0; i < ev.dataTransfer.items.length; i++) {
            // If dropped items aren't files, reject them
            if (ev.dataTransfer.items[i].kind === 'file') {
                var file = ev.dataTransfer.items[i].getAsFile();
                console.log('... file[' + i + '].name = ' + file.name);
            }
        }
    } else {
        // Use DataTransfer interface to access the file(s)
        for (var i = 0; i < ev.dataTransfer.files.length; i++) {
            console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
        }
    }
}