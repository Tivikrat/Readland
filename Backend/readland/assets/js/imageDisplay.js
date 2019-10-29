/* отображение изображения */
var openFile = function(event) {
    var input = event.target;

    var reader = new FileReader();
    reader.onload = function(){
      var dataURL = reader.result;
      var output = document.getElementById('output'); /* возвращает ссылку на элемент который имеет атрибут id с указанным значением*/
      output.src = dataURL;
    };
    reader.readAsDataURL(input.files[0]);
    }