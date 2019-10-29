/* проверка формата загружаемого изображения */ 
function checkImage() {
    var fileElement = document.getElementById("choice");
    var fileExtension = "";
    if (fileElement.value.lastIndexOf(".") > 0) {
        fileExtension = fileElement.value.substring(fileElement.value.lastIndexOf(".") + 1, fileElement.value.length);
    }

    /* если файл допустимого формата, выполнить функцию openFile()*/
    if ((fileExtension.toLowerCase() == "png") || (fileExtension.toLowerCase() == "jpg")) {
        onchange(openFile(event));
        return true;
    }else {
        fileElement.value = "";
        alert('Неверный формат файла, пожалуйста выберите файл формата: png или jpg');
        return false;
    }
}
/* проверка формата прикрепляемого файла */ 
function ValidateSingleInput(oInput) {
    var _validFileExtensions = [".pdf"]; 
    if (oInput.type == "file") {
        var sFileName = oInput.value;
         if (sFileName.length > 0) {
            var blnValid = false;
            for (var j = 0; j < _validFileExtensions.length; j++) {
                var sCurExtension = _validFileExtensions[j];
                if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                    blnValid = true;
                    break;
                }
            }
             
            if (!blnValid) {
                alert("Формат файла " + "не соотвествует: " + _validFileExtensions.join(",") + " или .epub");
                oInput.value = "";
                return false;
            }
        }
    }
    return true;
}

// Проверка заполнения
function checkform(f) {
    var errMSG = ""; 
    // цикл ниже перебирает все элементы в объекте f, 
    // переданном в качестве параметра
    // функции, в данном случае - наша форма.            
    for (var i = 0; i<f.elements.length; i++) 
      // если текущий элемент имеет атрибут required
      // т.е. обязательный для заполнения
      if (null!=f.elements[i].getAttribute("required")) 
         // проверяем, заполнен ли он в форме
          if (isEmpty(f.elements[i].value)) // пустой
              errMSG += "  " + f.elements[i].name + "\n"; // формируем сообщение
                                                         // об ошибке, перечисляя 
                                                         // незаполненные поля
          // если сообщение об ошибке не пусто,
          // выводим его, и возвращаем false     
          if ("" != errMSG) {
              alert("Не заполнены обязательные поля:\n" + errMSG);
              return false;
        }
}

function isEmpty(str) {
    for (var i = 0; i < str.length; i++)
    if (" " != str.charAt(i))
        return false;
    return true;
} 

// Проверка всей формы перед отправлением на сервер, при нажати на кнопку "Добавить"
function checkAll(f){
    var file = document.getElementById('hider');
    var image = document.getElementById('choice');
    if(image.value == ""){
        alert("Изображение не добавлено");
        return false;
    }
    if(file.value == ""){
        alert("Файл не добавлен");
        return false;
    }
    if(!checkform(f)){
        return false;
    }
}



// Ввод только цифр в поле Дата Издания
function validate(evt) {
    var theEvent = evt || window.event;
    var key = theEvent.keyCode || theEvent.which;
    key = String.fromCharCode( key );
    var regex = /[0-9]|\./;
    if( !regex.test(key) ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
}