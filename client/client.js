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

function findById() {
  var id = $('#txtId').val();
  $.ajax(
    {
      //url: "https://localhost:5001/api/Indici/", 
      url: "http://localhost:5000/api/Indici/" + id,
      type: "GET",
      contentType: "application/json",
      data: "",
      success: function (result) {
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
  /*
    str.split("\n").forEach(element => document.getElementById('txtarea').value += element);
    str.split("\n").forEach(element => console.log(element));
  */
  document.getElementById('txtarea').value = "";
  document.getElementById('txtarea').value += res.text;
  renderImage(str.img);
}

function renderImage(base64imageString) {
	var baseStr64 = base64imageString;
	baseStr64 = baseStr64.substring(0, baseStr64.length-1); // tolgo l'ultimo carattere della stringa che codifica l'immagine ("'")
	baseStr64 = baseStr64.substring(2, baseStr64.length); // tolgo i primi due caratteri della stringa che codifica l'immagine ("b'")
	var image = new Image();
	image.src = 'data:image/png;base64,' + baseStr64; // dico che l'immagine è una png codificata in base64 e fornisco l'immagine codificata vera e propria ("baseStr64")
	document.body.appendChild(image);
}