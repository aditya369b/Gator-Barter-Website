// Check if item is tradable
function isTradable(tradable) {
    if (tradable != 0) {
        $(".tradable-label").css("background-color", "red");
    } else {
        $(".tradable-label").css("background-color", "blue");
    }
}

// Choose images
function chooseFile() {
    $("#fileInput").click();
}
    // TO display "file uploaded" message in item-posting
function fileUploaded(){
    console.log("in file uploaded")
    document.getElementById("imageUpload").style.visibility = "visible";
}

// To validate a form for item-posting
function validateForm() {
    if (document.forms["item_form"]["item_title"].value == "") {
        alert("Title must be filled out");
        return false;
    }
    if (document.forms["item_form"]["category"].value == "") {
        alert("Category must be filled out");
        return false;
    }
    if (document.forms["item_form"]["item_desc"].value == "") {
        alert("Description must be filled out");
        return false;
    }
    if (document.forms["item_form"]["item_price"].value == "") {
        alert("Price must be filled out. Put 0 if, it is a free give away.");
        return false;
    }

    // if (document.forms["item_form"]["isTradable"].value == 1) {
    //     alert("Select appropriate option for - Would you like to trade this item?");
    //     return false;
    // }

    if (document.forms["item_form"]["fileInput"].value == "") {
        alert("Select a picture of item you wish to sell!");
        return false;
    }

    return true;
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

function goBack(){
  window.history.back();
}

 function goHome(){
   window.location.href='/';
}

function closeWindow(){
  close();
}
