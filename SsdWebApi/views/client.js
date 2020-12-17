//Comando: shift+alt+f per allineamento corretto!

function init() {
}

function findAll() {
  console.log("Enter into findAll")
  $.ajax({
    //url: "https://localhost:5001/api/Indici", 
    url: "http://localhost:5000/api/Indici",
    type: "GET",
    contentType: "application/json",
    success: function (result) { //se il risultato ha successo lo passo al log
      console.log(result);
      readResult(JSON.stringify(result)); //passo come parametro il risultato in formato Json
    },
    error: function (xhr, status, p3, p4) { //altrimenti, se la chiamata NON ha avuto successo entro nell'errore he chiama a sua volta un altra funzione facendo parsing
      var err = "Error " + " " + status + " " + p3;
      if (xhr.responseText && xhr.responseText[0] == "{")
        err = JSON.parse(xhr.responseText).message;
      alert(err);
    }
  });
}

function readResult(str) {
  document.getElementById('txtarea').value += str;
  console.log(str);
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
        readResultId(JSON.parse(result));
      },
      error: function (xhr, status, p3, p4) {
        var err = "Error " + " " + status + " " + p3;
        if (xhr.responseText && xhr.responseText[0] == "{")
          err = JSON.parse(xhr.responseText).message;
        alert(err);
      }
    });
}

function readResultId(str) {
  document.getElementById('txtarea').value = "";
  document.getElementById('txtarea').value += str.text;
}