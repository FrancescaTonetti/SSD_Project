//Comando: shift+alt+f per allineamento corretto!

function init() {
}

function start() {
  /*var id = $('#txtId').val();*/
  $.ajax(
    {
      //url: "https://localhost:5001/api/Indici", 
      url: "http://localhost:5000/api/Indici",
      type: "GET",
      contentType: "application/json",
      data: "",
      success: function (result) {
        console.log(result)
        readResultId(result);
      },
      error: function (xhr, status, p3, p4) {
        var err = "Error " + " " + status + " " + p3;
        if (xhr.responseText && xhr.responseText[0] == "{")
          err = JSON.parse(xhr.responseText).message;
        alert(err);
      }
    });
}

function readResult(str) {
  document.getElementById('txtarea').value = "";
  document.getElementById('txtarea').value += str;
}